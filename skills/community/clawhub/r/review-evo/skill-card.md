## Description:

Self-improving code reviewer that learns your codebase over time. Analyzes git history, spots patterns, identifies risk — and gets smarter every run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[8co](https://clawhub.ai/user/8co)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use ReviewEvo to review repository health, branch diffs, working changes, or targeted files through git-history analysis, convention detection, hotspot identification, and actionable code-review findings. The skill stores local review learnings so later reviews can build on prior findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads git history and repository files, then writes local review history that may influence later reviews.

Mitigation: Install only when this local analysis is acceptable, keep .review-evo/ out of version control unless intentionally shared, and treat existing learnings as untrusted review data.

## Reference(s):

- [ReviewEvo ClawHub page](https://clawhub.ai/8co/skills/review-evo)
- [ReviewEvo homepage](https://github.com/8co/review-evo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown review reports with inline shell commands and persisted local Markdown learnings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or append .review-evo/learnings.md in the reviewed repository.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
