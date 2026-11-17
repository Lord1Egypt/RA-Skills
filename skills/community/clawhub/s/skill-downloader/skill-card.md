## Description:

Skill Downloader helps agents discover, compare, review, install, or update OpenClaw skills from trusted sources using a review-first workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyang100](https://clawhub.ai/user/yyang100)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to find or compare skills, inspect ClawHub-hosted candidates, and install or update skills after review and explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installed skills can influence future agent behavior.

Mitigation: Confirm the source registry and destination directory, then review candidate skill material before approving installation or updates.

Risk: Incomplete registry metadata can lead to overconfident recommendations.

Mitigation: Label results as Full, Partial, or Minimal and avoid firm recommendations unless the available information is complete.

## Reference(s):

- [Advanced Workflows](references/advanced-workflows.md)
- [ClawHub Skill Page](https://clawhub.ai/yyang100/skills/skill-downloader)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with source labels, completeness notes, and optional shell commands or file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installation and update writes require explicit user approval.]

## Skill Version(s):

0.1.20 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
