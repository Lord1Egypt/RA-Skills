## Description:

Trio Stream Vision lets agents analyze live video streams with natural-language checks, continuous event monitoring, and periodic summaries through the Trio API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drandrewlaw](https://clawhub.ai/user/drandrewlaw)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operators use this skill to inspect authorized live streams, check visual conditions, start monitored event alerts, and request periodic summaries without building a video pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stream URLs and captured frames or clips may be sent to Trio for processing.

Mitigation: Use only streams the user owns or is authorized to analyze, avoid privacy-sensitive feeds unless approved, and avoid camera URLs with embedded credentials.

Risk: Live monitoring, digests, and webhooks can create ongoing processing, notification, cost, and privacy exposure.

Mitigation: Require explicit confirmation before starting monitoring, digest, or webhook delivery; set bounded durations and explain how to check status or cancel jobs.

Risk: Shell examples that incorporate user-provided stream URLs or conditions can be unsafe if values are inserted without escaping.

Mitigation: Construct JSON payloads with a trusted serializer or carefully escape user-provided text before passing it to curl.

Risk: The Trio API key could be exposed through logs, chat output, shell history, or pasted commands.

Mitigation: Store TRIO_API_KEY in a secret store or environment variable, never display its value, and review command output before sharing it.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/drandrewlaw/skills/trio-stream-vision)
- [Trio API Reference](https://docs.machinefi.com/api-reference/)
- [Trio Console](https://console.machinefi.com)
- [Trio API Base URL](https://trio.machinefi.com/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash curl commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TRIO_API_KEY; may return job IDs, explanations, boolean trigger results, stream digests, and remediation messages.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
