## Description: <br>
Interact with GitHub using the gh CLI for PR checks, workflow run details, logs, API queries, and JSON output filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yequanzheng](https://clawhub.ai/user/yequanzheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to ask an agent for GitHub CLI commands that check PR status, inspect workflow runs and logs, query GitHub APIs, and format JSON results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub CLI commands can access repositories available to the user's local gh login, including private repository data. <br>
Mitigation: Review repository targets, command flags, and any gh api request before execution, especially for private repositories. <br>
Risk: State-changing GitHub API methods could modify repository resources if an agent or user adapts the examples. <br>
Mitigation: Confirm the HTTP method and endpoint before running gh api commands, and avoid write-capable requests unless the intended change is explicit. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API queries] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may read GitHub repository data using the user's local gh authentication.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
