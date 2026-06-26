## Description: <br>
Provides professional code review and Git commit workflow management for Git submission workflows, including pre-commit checks, build verification, and commit guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to review code changes and manage Git commit and push workflows with approval checkpoints, build checks, commit-message guidance, and sensitive-data checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe auto-commit behavior may stage and commit all current changes before user approval. <br>
Mitigation: Require explicit approval before every git add, git commit, git pull, and git push; review git status and the staged diff; scan for secrets; and confirm the remote, branch, and account before pushing. <br>


## Reference(s): <br>
- [Reference Documentation for Code Review](references/api_reference.md) <br>
- [ClawHub release page](https://clawhub.ai/yinwuzhe/tosr-test-pub-update-1774335120) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Git commands and commit messages; Git actions should require explicit user approval.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
