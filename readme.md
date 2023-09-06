
# Workflow & Usage Documentation

## **Mandatory Build check for RC merge by** PR Validation for `rc_*` branch

### 1. Introduction

This guide is designed to provide a comprehensive understanding of the automated workflow for validating Pull Requests (PRs) aimed at merging into `rc_*` branches. The goal is to maintain code quality by ensuring that each code change successfully passes the build and test stages in AWS CodeBuild.

---

### 2. Workflow Overview

The validation workflow is automatically activated whenever a PR targeting an `rc_*` branch is opened or updated. The workflow uses AWS CodeBuild for code compilation and testing, and the PR is either marked as ready for merging or flagged for revision based on the build results and keyword in the commit message.

---

### 3. Step-by-Step Workflow

### 3.1 PR Submission and Initial Checks

1. **Developer Action**: A developer submits a PR targeting an `rc_*` branch.
2. **Automated Trigger**: GitHub Actions detects the PR and initializes the validation process.
3. **Commit Message Review**: The head git commit message is examined for the specific keyword "CodeBuild." This serves as a preliminary quality control measure to decide whether to proceed to the AWS CodeBuild phase.

### 3.2 Role & Permission Checks

1. **GitHub Action**: Checks its permissions, which are granted via the AWS IAM role named `CodeBuildFromGitHub`.
2. **Validation**: The IAM role is validated to ensure it has the necessary permissions to initiate and monitor AWS CodeBuild projects.

### 3.3 Code Validation and Testing

1. **AWS CodeBuild Initialization**: The GitHub Action sends a request to AWS CodeBuild to initiate the build process.
2. **Build Status and Phases**: GitHub Actions enters a loop, continuously fetching the build status and current phase from AWS CodeBuild.
3. **Status Monitoring**: The workflow examines whether the build has "SUCCEEDED," "FAILED," or "STOPPED," based on real-time data from AWS CodeBuild.

### 3.4 PR Approval or Rejection

1. **Automated Status Check**: GitHub Actions reviews the received build status.
2. **Decision Point**:
    - If AWS CodeBuild reports a 'Succeeded' status and the commit message contains "CodeBuild," the PR is marked as valid and a reviewer is notified for manual review and merging.
    - If either the build fails or the commit message lacks "CodeBuild," the PR is flagged for revision and blocked from merging.

---

### 4. Usage Scenarios and Considerations

- **Feature Integration**: When new features are ready, this workflow ensures they integrate seamlessly into `rc_*` branches.
- **Bug Fixing**: It confirms that hot fixes resolve issues without introducing new ones.
- **Release Preparations**: As `rc_*` branches are release candidates, this validation process serves as a final quality gate before production deployment.

---

### 5. Best Practices and Compliance

- **Review IAM Permissions**: IAM roles and permissions should be reviewed quarterly to ensure they adhere to the least-privilege principle.
- **Documentation**: Always document any changes made to the GitHub Actions or AWS CodeBuild configurations for audit and compliance purposes

---