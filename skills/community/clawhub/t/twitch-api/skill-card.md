## Description:

Pull a Twitch channel's profile and live status, list its VODs / highlights / uploads, read its stream schedule, and resolve a clip to downloadable MP4 qualities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve structured Twitch profile, VOD, schedule, and clip data through Scavio for creator research, live-status checks, and clip archival workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Twitch channel names, clip identifiers, and the Scavio API key are sent to Scavio, and successful calls consume credits.

Mitigation: Use the skill only when Scavio is an acceptable third-party provider, keep SCAVIO_API_KEY out of source control, and monitor credit usage.

Risk: API responses may indicate invalid input, missing credentials, missing Twitch resources, pagination limits, rate limits, or temporary upstream failures.

Mitigation: Handle documented 400, 401, 404, 422, 429, and 502 responses and return only values supplied by the API.

## Reference(s):

- [Scavio API Documentation](https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=twitch-api)
- [Scavio Rate Limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=twitch-api)
- [ClawHub Skill Listing](https://clawhub.ai/scavio-ai/skills/twitch-api)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON API responses and inline Python or shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; each successful Twitch endpoint call consumes 1 Scavio credit.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
