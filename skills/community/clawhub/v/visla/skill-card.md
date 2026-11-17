## Description:

Creates AI-generated videos from text scripts, URLs, PPT/PDF documents, or AI-generated visuals (AIGC) using Visla.

This skill is ready for commercial/non-commercial use.

## Publisher:

[visla-admin](https://clawhub.ai/user/visla-admin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create Visla videos from scripts, webpages, documents, visual media, speech, ideas, or AIGC storyboard and motion-video workflows, and to check Visla account, avatar, voice, and style options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Visla credentials and may read saved credentials from the default Visla credentials file.

Mitigation: Prefer VISLA_API_KEY and VISLA_API_SECRET environment variables, require explicit user consent before reading saved credentials, and never echo keys or secrets in agent responses.

Risk: Video creation can upload selected files, URLs, or media to Visla/S3 and consume Visla credits.

Mitigation: Use only user-provided content, avoid confidential files and internal URLs, and tell users when an action may spend credits or take several minutes.

Risk: The URL command is review-worthy on networks with private services because URL validation is unrestricted.

Mitigation: Avoid private, localhost, or internal network URLs until URL validation is restricted or explicitly reviewed for the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/visla-admin/skills/visla)
- [ClawHub publisher profile](https://clawhub.ai/user/visla-admin)
- [Visla API credentials page](https://www.visla.us/visla-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration examples, status summaries, and generated project or download links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VISLA_API_KEY and VISLA_API_SECRET; may consume Visla credits and upload selected user content to Visla/S3.]

## Skill Version(s):

2.0.0 (source: server release metadata); CLI version 260811-1640 (source: SKILL.md and scripts/visla_cli.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
