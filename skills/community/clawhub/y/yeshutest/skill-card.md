## Description: <br>
Interact with GitHub using the gh CLI to check PR CI status, view workflow runs and logs, and perform advanced API queries with JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xdlrt](https://clawhub.ai/user/xdlrt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect GitHub pull requests, workflow runs, failed logs, issues, and API responses through the GitHub CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub CLI commands may operate against the wrong account, repository, or scope if the local gh authentication context is unexpected. <br>
Mitigation: Confirm the active gh account before use and specify repositories explicitly with --repo owner/repo or direct URLs. <br>
Risk: Advanced gh api commands can expose or modify data when run against private or important repositories. <br>
Mitigation: Review each gh api command before execution and use the minimum required GitHub token scopes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xdlrt/yeshutest) <br>
- [Publisher profile](https://clawhub.ai/user/xdlrt) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include GitHub CLI commands with JSON output and jq filters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
