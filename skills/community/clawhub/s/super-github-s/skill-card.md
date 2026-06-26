## Description: <br>
Helps an agent use the GitHub CLI for issues, pull requests, workflow runs, CI checks, and GitHub API queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to have an agent inspect GitHub issues, pull requests, CI workflow runs, and API responses through the local gh CLI. It is useful when repository-scoped GitHub commands and structured JSON or jq output help with development and review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides an agent to use the local GitHub CLI, including gh api, which can run write-capable operations when credentials allow it. <br>
Mitigation: Install only when local GitHub CLI use is intended, keep commands scoped with --repo or explicit URLs, and review write-capable gh or gh api commands before execution. <br>
Risk: The skill description includes unrelated words, which may indicate sloppy scoping. <br>
Mitigation: Review the skill text before deployment and ask the publisher to remove unrelated description text. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/subaru0573/super-github-s) <br>
- [Publisher profile](https://clawhub.ai/user/subaru0573) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should keep GitHub CLI commands scoped with --repo or explicit URLs when not inside a git directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
