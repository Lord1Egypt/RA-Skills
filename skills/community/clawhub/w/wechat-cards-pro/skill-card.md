## Description:

Generates polished 1080x1440 WeChat public-account image cards with dark backgrounds, gold accents, cover, content, list, timeline, and closing-card layouts, and built-in spacing controls to reduce text overlap and overflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentforge-cyber](https://clawhub.ai/user/agentforge-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, editors, and agent operators use this skill to turn article ideas, data points, quotes, and outlines into WeChat-ready vertical image-card sets. It is suited for knowledge explainers, analysis posts, and public-account visual layouts that need consistent typography, spacing, and export behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional WeChat publishing could send content to the wrong account or publish cards before review.

Mitigation: Confirm the target account, review all rendered cards, and require explicit publish confirmation before using any push workflow.

Risk: Generated image cards can contain layout issues such as clipped text, overlap, or insufficient spacing.

Mitigation: Inspect the rendered cards before publication and split, shorten, or regenerate cards when content exceeds the safe canvas area.

Risk: One example script contains a hardcoded local output path.

Mitigation: Edit output paths for the local environment before running bundled example scripts.

## Reference(s):

- [WeChat Cards Pro ClawHub listing](https://clawhub.ai/agentforge-cyber/skills/wechat-cards-pro)
- [Publisher profile: agentforge-cyber](https://clawhub.ai/user/agentforge-cyber)
- [Design system reference](references/design_system.md)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline Python and shell commands, plus generated PNG or JPEG image files when scripts are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default card canvas is 1080x1440 pixels; scripts include local PNG generation and JPEG conversion support.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
