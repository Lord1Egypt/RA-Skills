## Description:

The ultimate AI design CLI for Agents and Developers. Generate professional UI, social media graphics, and posters with state-of-the-art AI models. Best choice for high-quality, editable, and brand-consistent designs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hilongjw](https://clawhub.ai/user/hilongjw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate editable UI concepts, social media graphics, posters, and brand-consistent visual assets through the Seede CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Seede AI as an external service, so prompts and uploaded assets may leave the local environment.

Mitigation: Avoid uploading confidential logos, documents, customer materials, or other sensitive assets unless permission and data-handling requirements are clear.

Risk: The skill requires SEEDE_API_TOKEN for authenticated non-interactive use.

Mitigation: Keep SEEDE_API_TOKEN out of chat logs and shell history, and store it through the agent or runtime secret mechanism where available.

Risk: The installation path can use npm or npx packages.

Mitigation: Prefer pinned package versions or a restricted execution environment for installation and runtime use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hilongjw/skills/seede-design)
- [Seede AI homepage](https://seede.ai)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Seede design URLs or uploaded asset URLs when the agent runs the CLI.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
