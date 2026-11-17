## Description:

WhatsLink queries public download, magnet, and torrent links through WhatsLink to summarize metadata and, when present, screenshot URLs without downloading or opening the content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[violin321](https://clawhub.ai/user/violin321)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect public, non-sensitive URLs before opening or downloading them. It reports metadata such as content type, name, size, file count, and screenshot URLs when WhatsLink returns them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitting a URL to WhatsLink discloses that link to an external lookup service.

Mitigation: Use only public, non-sensitive URLs and do not submit signed links, internal resources, document-sharing URLs, tokens, API keys, sessions, or credentials.

Risk: Returned screenshot URLs may expose sensitive information from the target content.

Mitigation: List screenshot URLs only when appropriate, and do not download, open, or forward screenshots unless the user explicitly requests it and the URL is safe to handle.

Risk: WhatsLink may return unknown, incomplete, or empty metadata.

Mitigation: Report unknown results as unavailable metadata and avoid inferring file contents beyond the API response.

## Reference(s):

- [WhatsLink](https://whatslink.info/)
- [WhatsLink API endpoint](https://whatslink.info/api/v1/link)
- [ClawHub skill page](https://clawhub.ai/violin321/skills/whatslink)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable metadata summary or raw JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May list screenshot URLs by default; does not download, open, or forward target content.]

## Skill Version(s):

0.1.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
