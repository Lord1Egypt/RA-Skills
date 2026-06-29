## Description: <br>
Build reliable GitHub issue, pull request, review, and automation workflows with safe API usage, clear repository context, and reproducible local checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, release engineers, and agent builders use this skill to inspect or act on GitHub issues, pull requests, reviews, CI checks, branches, and repository files while preserving review context. It helps produce triage summaries, scoped patch plans, safe command or API suggestions, concise GitHub comments, and verification checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested GitHub comments, API calls, gh commands, or repository actions could change the wrong issue, pull request, branch, or repository if context is incomplete. <br>
Mitigation: Confirm the target repository, PR or issue number, branch, permissions, and whether the operation is mutating before running or posting anything. <br>
Risk: Automation guidance could introduce incorrect or misleading repository workflow advice if proposed actions are not reviewed. <br>
Mitigation: Review proposed commands, API calls, comments, and patch plans before execution, then verify results with metadata fetches, git diffs, tests, or CI output. <br>


## Reference(s): <br>
- [Requirement Plan](references/requirement-plan.md) <br>
- [GitHub Interaction Developer Helper on ClawHub](https://clawhub.ai/kyro-ma/skills/software-data-github-interact-developer-helper-040526) <br>
- [Popular ClawHub skill demand: Github](https://clawhub.ai/skills/github) <br>
- [GitHub CI community discussion](https://news.ycombinator.com/item?id=48624574) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with concise prose, lists, inline code, and command or API examples when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include assumptions, repository state summaries, verification notes, and remaining blockers.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
