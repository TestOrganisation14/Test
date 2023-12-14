import sys
import re
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
            'doc': match.group('doc').replace('\n', ' ').strip()
        }
        ops_config.append(entry)

    return ops_config

def extract_doc_info(doc_string):
    info = {
        "description_table": "",
        "example": "",
        "default_value": ""
    }

    # not working with keys : "CPLiveMaxLiveInputs"	"CPLiveGRPCEndPoint"
    description_match = re.search(r'Description\s*[\s:]+(?:\n+)?(.*?)(?=\s+(?:Format|Supported values|Notes|Example)\b)', doc_string, re.DOTALL)
    if description_match:
        description = description_match.group(1).replace('\n', ' ').strip()
        info['description_table'] = description

    example_match = re.search(r'Example\s*.*?=\s*(.*?)(?=\s{3,}\S|$)', doc_string, re.DOTALL)
    if example_match:
        info['example'] = example_match.group(1).strip()

    return info
def generate_markdown_table(entries):
    markdown_table = "Key | Description | Type | Default Value | Sample Value\n"
    markdown_table += "---|---|---|---|---\n"

    for entry in entries:
        info = extract_doc_info(entry['doc'])
        row = f"{entry['key']} | {info['description_table']} | string | {info['default_value']} | {info['example']}\n"
        markdown_table += row
    return markdown_table

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python configTableGenerator.py <file_path>")
        sys.exit(1)
    new_file_path = sys.argv[1]
    new_config = read_ops_config(new_file_path)
    markdown_content = generate_markdown_table(new_config)
    with open('configChangelog.md', 'w') as file:
        file.write(markdown_content)
