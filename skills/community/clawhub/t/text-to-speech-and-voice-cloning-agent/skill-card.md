## Description:

Turn your AI assistant into a TTS and voice cloning powerhouse using the Verbatik API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[verbatik](https://clawhub.ai/user/verbatik)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate speech from text, clone voices from audio samples, manage cloned voices, browse Verbatik voices, and check prepaid account balance through the Verbatik API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends text and voice-sample URLs to Verbatik using a user-provided API key.

Mitigation: Install only when the user accepts Verbatik processing, protect the VERBATIK_API_KEY value, and avoid sending sensitive text or voice samples without approval.

Risk: Voice cloning can be misused when the speaker has not consented.

Mitigation: Require explicit consent from the voice owner before cloning or generating speech with a cloned voice.

Risk: The skill can trigger paid operations for text-to-speech and voice cloning.

Mitigation: Estimate costs, check prepaid balance, and ask for confirmation before bulk or paid operations.

Risk: The skill can delete cloned voices.

Mitigation: Require a separate confirmation before deleting any cloned voice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/verbatik/skills/text-to-speech-and-voice-cloning-agent)
- [Verbatik API](https://api.verbatik.com)
- [Verbatik MCP Endpoint](https://api.verbatik.com/api/mcp/mcp)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration, JSON]

**Output Format:** [Markdown instructions with HTTP request examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated Verbatik operations may return hosted audio URLs, binary audio streams, response headers, costs, and account-balance metadata.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
