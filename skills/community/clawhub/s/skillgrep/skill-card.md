## Description:

Use when a user is trying to discover an installable or reusable skill or workflow, especially when they ask for a skill for a task, want to compare nearby skill categories, or need help narrowing discovery results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[littledinoc](https://clawhub.ai/user/littledinoc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Skill Grep to discover, compare, and narrow installable or reusable skills for a task. The skill guides an agent through structured search, at most one clarification, final recommendations, and feedback submission after the user's verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill-search prompts, clarification details, and recommendation feedback are sent to skills.megatechai.com.

Mitigation: Use only when users are comfortable with remote processing; avoid sensitive prompts and confirm data-sharing requirements before use.

Risk: Suggested install commands may reference repositories or package versions that are not pinned.

Mitigation: Inspect the target repository before installing and prefer pinned package versions or immutable commits.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/littledinoc/skills/skillgrep)
- [Skill Search API Base URL](https://skills.megatechai.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown recommendation summaries with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns 1-3 recommendations and sends feedback after the user's verdict.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
