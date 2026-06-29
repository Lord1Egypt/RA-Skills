## Description: <br>
Guides GitHub issue, pull request, CI, and repository-context work so coding agents can triage, plan safe changes, and report actionable next steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and agent users use this skill to inspect GitHub issues, pull requests, checks, branches, commits, and repository files, then turn that evidence into implementation plans, triage summaries, command plans, and final status notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose GitHub CLI or API actions for labels, comments, assignments, merges, and other live repository changes. <br>
Mitigation: Review proposed commands before execution and perform live GitHub mutations only when the user explicitly requested them or they are a direct part of the workflow. <br>
Risk: Broad activation hints could apply the workflow outside GitHub-related work. <br>
Mitigation: Invoke the skill explicitly for GitHub-centered tasks and keep remote GitHub facts separate from local assumptions. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/kyro-ma/software-data-github-interact-developer-helper) <br>
- [Requirement plan](references/requirement-plan.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with concise summaries, checklists, command plans, and status notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should cite relevant GitHub objects or local files when they drive a recommendation.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
