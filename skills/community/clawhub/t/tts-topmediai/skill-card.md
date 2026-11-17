## Description:

TopMediai text-to-speech skill that supports API key entitlement checks, official and cloned voice listing, and text-to-speech generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[topmediai](https://clawhub.ai/user/topmediai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check TopMediai API key entitlement, inspect available voices, and generate speech from text with a selected voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the configured API key and submitted text to the configured API host.

Mitigation: Install only from a trusted publisher, keep TOPMEDIAI_BASE_URL set to https://api.topmediai.com unless a trusted test endpoint is intentionally used, and avoid submitting sensitive text unless approved for TopMediai processing.

Risk: Dependencies are specified with minimum versions rather than pinned versions.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/topmediai/skills/tts-topmediai)
- [TopMediai publisher profile](https://clawhub.ai/user/topmediai)
- [TopMediai API base URL](https://api.topmediai.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON text returned by command execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOPMEDIAI_API_KEY; TTS responses depend on the configured TopMediai API endpoint.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
