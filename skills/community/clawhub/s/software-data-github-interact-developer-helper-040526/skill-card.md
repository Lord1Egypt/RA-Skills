## Description:

Build reliable GitHub issue, pull request, review, and automation workflows with safe API usage, clear repository context, and reproducible local checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, release engineers, and agent builders use this skill to inspect and act on GitHub issues, pull requests, checks, comments, branches, and repository files while preserving contributor intent and verifying repository state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad GitHub-related requests and can propose mutating repository actions such as posting comments, rerunning checks, or changing repository state.

Mitigation: Confirm the repository, pull request or issue number, branch, permission scope, and intended mutation before approving any state-changing action.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/software-data-github-interact-developer-helper-040526)
- [Popular ClawHub Skill Demand: Github](https://clawhub.ai/skills/github)
- [GitHub Banned All CI for Our OSS Org Because of Bad Drive-By Contributors](https://news.ycombinator.com/item?id=48624574)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise summaries, command examples, API call suggestions, scoped patch plans, and verification checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GitHub triage summaries, review comments ready to post, repository-state assumptions, and remaining blockers.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
