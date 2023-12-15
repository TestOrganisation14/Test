import re
import yaml
import os
import sys
from datetime import datetime

def extract_doc_info(doc_string):
    info = {
        "description": "",
        "example": "",
        "default_value": ""
    }
    # not working with keys : "CPLiveMaxLiveInputs"	"CPLiveGRPCEndPoint"
    description_match = re.search(r'Description\s*[\s:]+(?:\n+)?(.*?)(?=\s+(?:Format|Supported values|Notes|Example)\b)', doc_string, re.DOTALL)
    if description_match:
        description = description_match.group(1).replace('\n', ' ').strip()
        description = re.sub(r'\s{3,}', '\n', description)
        info['description'] = description

    example_match = re.search(r'Example\s*.*?=\s*(.*?)(?=\s{3,}\S|$)', doc_string, re.DOTALL)
    if example_match:
        info['example'] = example_match.group(1).strip()

    return info

def read_ops_config(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    pattern = r'\{\s*"key"\s*:\s*"(?P<key>[^"]+)"\s*,\s*"scope"\s*:\s*\[(?P<scope>[^\]]+)\]\s*,\s*"doc"\s*:\s*F\("""(?P<doc>.*?)"""\)\s*\}'
    matches = re.finditer(pattern, content, re.DOTALL)

    ops_config = []
    for match in matches:
        entry = {
            'key': match.group('key'),
            'scope': [scope.strip().strip('"') for scope in match.group('scope').split(',')],
            'doc': match.group('doc').strip()
        }
        ops_config.append(entry)
    return ops_config

def generate_changelog(changes,tag,author):
    current_date = datetime.now().strftime("%d/%m/%Y") 
    changelog = [
        f"BuildNotes:",
        f"    \"Tag\": {tag}",
        f"    \"Date\": {current_date}",
        f"    \"Author\": {author}",
        f"    \"Config Changes\":"
    ]

    for change_type in ['New', 'Changed', 'Removed']:
        if changes[change_type]:
            changelog.append(f"      \"{change_type}\":")
            changelog.append(f"        - component : mimas")
            changelog.append(f"          files:")
            
            # Iterate through scopes in the change type
            for scope, keys in changes[change_type].items():
                changelog.append(f"            - file: {scope}Opsconfig")
                changelog.append(f"              \"changes\":")
                
                for key, doc in keys.items():
                    doc_info = extract_doc_info(doc)
                    changelog.append(f"                - key: {key}")
                    doc_info['description'] = doc_info['description'].replace('\n', '\n                                ')
                    changelog.append(f"                  description: \"{doc_info['description']}\"")
                    changelog.append(f"                  type: \"string\"")
                    changelog.append(f"                  \"sample-value\": \"{doc_info['example']}\"")
        else:
            changelog.append(f"      \"{change_type}\": []")
    return '\n'.join(changelog)

def compare_configs(old_file_path,new_file_path):
    old_opsConfigFieldsDocMap = read_ops_config(old_file_path)  
    new_opsConfigFieldsDocMap = read_ops_config(new_file_path)  
    old_data_map = {}
    new_data_map = {}

    for entry in old_opsConfigFieldsDocMap:
        key = entry['key']
        scope = entry['scope']
        doc = entry['doc']

        if key not in old_data_map:
            old_data_map[key] = {}

        for sc in scope:
            if sc not in old_data_map[key]:
                old_data_map[key][sc] = doc

    for entry in new_opsConfigFieldsDocMap:
        key = entry['key']
        scope = entry['scope']
        doc = entry['doc']

        if key not in new_data_map:
            new_data_map[key] = {}

        for sc in scope:
            if sc not in new_data_map[key]:
                new_data_map[key][sc] = doc

    # Identifying New, Changed, and Removed entries
    changes = {'New': {}, 'Changed': {}, 'Removed': {}}

    for key, scopes in new_data_map.items():
        for scope, doc in scopes.items():
            if key not in old_data_map or scope not in old_data_map[key]:
                changes['New'].setdefault(scope, {})[key] = doc
            else:
                old_doc = old_data_map[key].get(scope)
                if old_doc != doc:
                    changes['Changed'].setdefault(scope, {})[key] = doc

    # Checking for removed entries
    for key, scopes in old_data_map.items():
        for scope, doc in scopes.items():
            if key not in new_data_map or scope not in new_data_map[key]:
                changes['Removed'].setdefault(scope, {})[key] = doc

    return changes
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <old_file_path> <new_file_path> <tag> <author>")
        sys.exit(1)
    
    old_file_path, new_file_path = sys.argv[1], sys.argv[2]
    tag = sys.argv[3]
    author = sys.argv[4]
    changes = compare_configs(old_file_path, new_file_path)
    changelog_content = generate_changelog(changes,tag,author)
    # Define the directory where you want to save changelog.yml
    output_directory = 'docs/'
    
    # Combine the directory and filename to create the full path
    output_file_path = os.path.join(output_directory, 'changelog.yml')
    
    # Write content to the specified directory and file
    with open(output_file_path, 'w') as file:
        print(output_file_path)
        file.write(changelog_content)
