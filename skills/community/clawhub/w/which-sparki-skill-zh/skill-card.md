## Description:

This Chinese Sparki navigation skill helps users choose the right Sparki video-editing skill and guides Sparki CLI setup, upload, editing, status, and download workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to select a Sparki video-editing workflow, then operate the Sparki CLI for local or Telegram Mini App uploads, style-guided or prompt-driven edits, project status checks, and result downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video files, filenames, editing prompts, and project metadata may be sent to Sparki for remote processing.

Mitigation: Confirm user consent before upload, avoid private or business-sensitive videos unless the user accepts the exposure, and disclose that remote processing is part of the workflow.

Risk: Credential and endpoint handling can expose a Sparki API key or direct traffic to an untrusted endpoint.

Mitigation: Prefer SPARKI_API_KEY from the environment over saved local credentials, and use --base-url only when the endpoint is fully trusted.

Risk: The skill can write configuration and downloaded video output under the user's OpenClaw directories.

Mitigation: Review the configured output path before download and protect result URLs or files that may contain private edited content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fischerlam/skills/which-sparki-skill-zh)
- [Sparki homepage](https://sparki.io)
- [Sparki Telegram bot](https://t.me/Sparki_AI_bot)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce downloaded video files and short-lived result URLs when Sparki jobs complete.]

## Skill Version(s):

1.0.0 (source: frontmatter, pyproject.toml, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
