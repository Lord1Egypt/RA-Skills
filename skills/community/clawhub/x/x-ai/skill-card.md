## Description:

Chat with Grok models via xAI API. Supports Grok-3, Grok-3-mini, vision, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blueberrywoodsym](https://clawhub.ai/user/blueberrywoodsym)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to send prompts, optional image inputs, and X search requests to xAI's Grok models from Clawdbot workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected images are sent to xAI.

Mitigation: Avoid secrets, regulated data, and other sensitive content in prompts or image inputs.

Risk: Image uploads can transmit unintended local files when a path points to a symlink, renamed non-image, or file the user did not personally select.

Mitigation: Use the image option only with personally selected image files and avoid symlinks or files whose contents are uncertain.

Risk: One documented install path is not pinned to an audited version.

Mitigation: Install from the reviewed ClawHub package or a pinned commit.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blueberrywoodsym/skills/x-ai)
- [xAI Documentation](https://docs.x.ai)
- [xAI API Documentation](https://docs.x.ai/api)
- [xAI Console](https://console.x.ai)
- [Installation and Use Instructions](https://claude.ai/public/artifacts/5bb1d4ca-68ef-4d74-900c-d14fefa5c094)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON from Node.js command-line scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XAI_API_KEY; optional image paths are read and sent to xAI for vision requests.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
