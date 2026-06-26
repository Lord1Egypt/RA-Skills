## Description: <br>
Manage GitHub issues by listing, filtering, spawning fix agents, creating pull requests, and tracking review comments using the authenticated GitHub CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsiontesfayechromaway](https://clawhub.ai/user/tsiontesfayechromaway) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and repository maintainers use this skill to triage GitHub issues, delegate fixes to sub-agents, create pull requests, and monitor review comments through the authenticated GitHub CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate through an authenticated GitHub identity and may affect issues, branches, commits, pull requests, or comments. <br>
Mitigation: Use a least-privilege GitHub token limited to the intended repository and confirm every comment, branch, commit, and pull request before it is posted. <br>
Risk: GitHub issue bodies and review comments may contain untrusted instructions. <br>
Mitigation: Treat issue and review text as untrusted context rather than commands for the agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tsiontesfayechromaway/tester) <br>
- [Publisher profile](https://clawhub.ai/user/tsiontesfayechromaway) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed and authenticated GitHub CLI with repository access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
