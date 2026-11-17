## Description:

Suno.cn AI Music Assistant helps agents create songs, lyrics, instrumentals, BGM, covers, continuations, stems, MIDI, sheet music, and other audio-processing outputs through the Suno.cn service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adcgg](https://clawhub.ai/user/adcgg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn natural-language music requests into Suno.cn generation and audio-processing tasks, then retrieve generated song, audio, MIDI, WAV, PDF, library, task, account, and credit information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated traffic can be redirected if SUNO_CN_MCP_URL is set.

Mitigation: Use the default Suno.cn endpoint in normal use and review the environment before running the helper.

Risk: Upload commands can send local files selected by path.

Mitigation: Review each file path before upload and avoid sending files that contain private or sensitive content.

Risk: Some operations consume account credits and retries may create additional service requests.

Mitigation: Check account and purchase status first, then retry credit-consuming operations only after explicit user confirmation.

Risk: Local authorization credentials remain active until expiry or logout.

Mitigation: Use the helper's auth logout command when access is no longer needed and never print or copy credential files.

## Reference(s):

- [Suno.cn MCP REST API](references/api.md)
- [Suno.cn Homepage](https://www.suno.cn)
- [ClawHub Skill Page](https://clawhub.ai/adcgg/skills/suno-cn-music)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network requests are routed through the bundled helper; generated media and document artifacts are returned as service links when available.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter/helper version 2.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
