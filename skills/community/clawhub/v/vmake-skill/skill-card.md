## Description:

VMake helps agents process images and videos with Vmake AI for watermark removal and quality restoration through catalog-selected, quota-consuming API tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wemayiiii](https://clawhub.ai/user/wemayiiii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route user-provided image or video media through Vmake AI for watermark removal, restoration, upscaling, and quality enhancement. It is intended for environments where Vmake credentials are configured and account quota use is authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied URLs can influence what the skill fetches and uploads.

Mitigation: Use the skill only with intended media inputs, prefer direct uploads or resolved local files for uncertain sources, and keep timeout and size limits enabled.

Risk: Remote service notices and links may be forwarded to users.

Mitigation: Treat service-provided text and links as untrusted; summarize or validate them before presenting them as guidance.

Risk: Media uploads, task history, and result URLs may expose sensitive content.

Mitigation: Run tasks only after explicit upload and quota authorization, and clear local task history when result URLs should not persist.

Risk: Runtime dependency installation can introduce supply-chain exposure.

Mitigation: Pin or preinstall dependencies from a trusted source before deploying the skill.

## Reference(s):

- [VMake ClawHub Release](https://clawhub.ai/wemayiiii/skills/vmake-skill)
- [README](README.md)
- [Agent Instructions](SKILL.md)
- [Errors and Polling](docs/errors-and-polling.md)
- [IM Attachments](docs/im-attachments.md)
- [Multi-Platform Delivery](docs/multi-platform.md)
- [Vmake Developers API Key](https://vmake.ai/developers#api-key)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON task status from CLI operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Vmake result URLs or platform delivery instructions after authorized media processing.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
