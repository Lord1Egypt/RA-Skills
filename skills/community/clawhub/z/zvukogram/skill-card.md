## Description:

Text-to-Speech via Zvukogram API with SSML support for generating speech, podcasts, voice notifications, and audio workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erview](https://clawhub.ai/user/erview)

### License/Terms of Use:

MIT

## Use Case:

Developers and content automation users can use this skill to generate speech from text with Zvukogram voices, SSML pronunciation controls, long-text handling guidance, account balance checks, and audio fragment merging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends TTS text, account email, and API token to the Zvukogram service.

Mitigation: Use it only for content appropriate to send to Zvukogram, avoid secrets or regulated data, and store credentials in protected environment variables or configuration files.

Risk: The audio downloader and merge helper use broad network and local-file behavior.

Mitigation: Review or harden download URLs and local file paths before using the helpers in automated or shared environments.

Risk: Credentials placed in GET URLs or logs can be exposed.

Mitigation: Prefer POST requests and avoid putting API tokens or account email in command history, logs, or shared URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erview/skills/zvukogram)
- [Zvukogram API documentation](https://zvukogram.com/node/api/)
- [Zvukogram SSML documentation](https://zvukogram.com/node/ssml/)
- [Zvukogram voice rating](https://zvukogram.com/rating/)
- [API.md](references/API.md)
- [SSML.md](references/SSML.md)
- [VOICES.md](references/VOICES.md)
- [chunking-and-method-choice.md](references/chunking-and-method-choice.md)
- [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, Python examples, and TTS-ready text or SSML guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that call Zvukogram APIs, save audio files, check account balance, or merge local audio fragments.]

## Skill Version(s):

1.1.6 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
