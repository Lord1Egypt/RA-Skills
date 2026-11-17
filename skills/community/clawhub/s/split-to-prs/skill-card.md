## Description:

Split current work into small reviewable PRs. Use when the user asks to split a chat, set of changes, branch, or PR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to split mixed repository work, branches, chats, or pull requests into smaller reviewer-aligned PRs while preserving user work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to create branches, commits, pushes, and pull requests after approval, affecting repository state and review flow.

Mitigation: Require user approval of the split plan, create a recoverable backup snapshot before moving work, stage only named files or hunks, and avoid destructive git actions without explicit approval.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with PR titles, URLs, optional Mermaid diagrams, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proposes repository actions first; branch, commit, push, and pull request execution requires user approval.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
