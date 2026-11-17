## Description:

Automates local Windows PC WeChat workflows for reading recent chats with OCR, generating short Chinese replies, sending text or media, capturing recent image previews, and optionally reusing a local daemon for faster repeated replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pddsa](https://clawhub.ai/user/pddsa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation-capable agents use this skill to operate a logged-in Windows PC WeChat client: locate a contact, read the latest visible conversation, draft a natural Chinese reply, and send text or files on the user's behalf.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read private WeChat conversations, capture chat screenshots, and manipulate the clipboard.

Mitigation: Use it only on accounts and chats where the user has consent and a clear task; limit reads to the latest needed messages and avoid exposing screenshots or transcripts beyond the task.

Risk: The skill can send messages and files as the logged-in WeChat user, including through daemon-assisted repeated operations.

Mitigation: Confirm the recipient, message text, and file paths before sending; reserve daemon use for explicitly authorized sessions and stop the daemon when finished.

Risk: Smart-reply mode may upload visible chat transcript text to the configured LLM endpoint.

Mitigation: Use a dedicated limited API key, verify the endpoint and model configuration, and avoid smart-reply mode for sensitive personal, medical, legal, financial, or confidential conversations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pddsa/skills/wechat-reply-ai)
- [Runtime requirements](artifact/references/runtime-requirements.md)
- [Fast reply workflow](artifact/references/fast-reply-workflow.md)
- [OCR and window rules](artifact/references/ocr-and-window-rules.md)
- [Reply style guide](artifact/references/reply-style-guide.md)
- [Persona](artifact/persona.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Plain text, JSON status messages, saved image files, and Markdown guidance with PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a logged-in Windows PC WeChat session; smart-reply mode may send chat transcript text to the configured LLM endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
