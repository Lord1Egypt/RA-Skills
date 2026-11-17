## Description:

u2-downloader helps agents download YouTube videos by URL in selected resolutions or audio-only mode through the u2foru.site API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xjouska](https://clawhub.ai/user/xjouska)

### License/Terms of Use:


## Use Case:

Developers and agent users can use this skill to request YouTube video downloads, choose a supported resolution, check account status, and receive a downloadable media URL from a third-party API service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and requested YouTube URLs are sent to the third-party u2foru.site service.

Mitigation: Use a dedicated API key when possible and review the service's terms and privacy practices before installation.

Risk: Downloaded videos may be subject to platform rules, copyright, or other legal restrictions.

Mitigation: Confirm that each requested download complies with applicable platform rules and law before using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xjouska/skills/u2-downloader)
- [u2foru.site API key portal](https://u2foru.site/?page=apikeys)
- [u2foru.site service](https://u2foru.site)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON, curl, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Download requests require a bearer API key and a YouTube URL; supported resolution values are 360, 480, 720, 1080, best, and audio.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
