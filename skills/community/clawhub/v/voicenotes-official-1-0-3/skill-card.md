## Description:

This Voicenotes skill lets OpenClaw search notes semantically, retrieve full transcripts, filter by tags or date range, and create text notes through the Voicenotes API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kscoggins](https://clawhub.ai/user/kscoggins)

### License/Terms of Use:

MIT-0

## Use Case:

External users with Voicenotes accounts use this skill to search, retrieve, and create their own Voicenotes content from OpenClaw conversations. It is useful for agents that need note lookup, transcript retrieval, tag/date filtering, or text-note creation through authenticated API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Voicenotes API key grants access to the user's Voicenotes data.

Mitigation: Store VOICENOTES_API_KEY as a secret, treat it like a password, and only install the skill when the user trusts Voicenotes with the requested note operations.

Risk: Created notes and submitted queries may contain sensitive information intended for Voicenotes storage or search.

Mitigation: Avoid sending sensitive note text unless the user intends that information to be stored or processed in Voicenotes.

Risk: Unsafe request construction could allow malformed search queries, recording IDs, or JSON bodies.

Mitigation: URL-encode search queries, validate recording IDs against the documented alphanumeric 8-character pattern, and JSON-encode body fields instead of concatenating raw user input.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kscoggins/skills/voicenotes-official-1-0-3)
- [ClawHub Publisher Profile](https://clawhub.ai/user/kscoggins)
- [Voicenotes](https://voicenotes.com)
- [Voicenotes OpenClaw Integration Settings](https://voicenotes.com/app?open-claw=true#settings)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl examples, JSON response examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VOICENOTES_API_KEY and curl; API requests are limited to the user's authenticated Voicenotes data.]

## Skill Version(s):

1.0.3 (source: artifact/_meta.json); ClawHub release version 1.0.0 (source: evidence.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
