## Description: <br>
Standardizes a pull request submission workflow by scanning changed files for sensitive information, confirming the file scope, generating a conventional commit message, pushing the current branch, and creating a GitHub PR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mykelio1001](https://clawhub.ai/user/mykelio1001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare and submit a pull request from a local Git repository with explicit checks for changed-file scope, commit wording, and sensitive information before pushing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can stage files, create a commit, push the current branch, and open a GitHub PR using the local Git and GitHub CLI sessions. <br>
Mitigation: Review the changed-file list, generated commit message, and PR body before approving the workflow. <br>
Risk: Submitting unrelated or sensitive files could expose unintended repository changes. <br>
Mitigation: Use the built-in sensitive-information scan and file-scope confirmation, and stop the workflow if any file or line looks unrelated or secret-bearing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mykelio1001/submit-pr) <br>
- [Publisher profile](https://clawhub.ai/user/mykelio1001) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with Git and GitHub CLI command execution steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow uses the provided PR title argument and requires user confirmation before staging confirmed files and committing.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
