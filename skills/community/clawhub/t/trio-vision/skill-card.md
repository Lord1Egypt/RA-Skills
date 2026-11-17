## Description:

Turn any live camera into a smart camera by letting an agent check live streams, monitor for natural-language conditions, and produce periodic summaries through Trio by MachineFi.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drandrewlaw](https://clawhub.ai/user/drandrewlaw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask questions about live camera or stream content, set up event monitoring with natural-language conditions, and request live digests without building their own video AI pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live camera streams, selected frames, summaries, and webhook notifications may be sent to Trio/MachineFi and configured webhook destinations.

Mitigation: Use only streams you are authorized to monitor, avoid sensitive or regulated environments without consent, and review webhook destinations before enabling notifications.

Risk: The skill requires a Trio API key and includes shell examples that could expose secrets if copied into persistent shell history or logs.

Mitigation: Store TRIO_API_KEY in a secret manager or ephemeral environment, avoid printing it, and redact it from shared logs or transcripts.

Risk: Curl templates accept user-provided stream URLs, conditions, job IDs, and webhook URLs.

Mitigation: Prefer a structured HTTP client or JSON-safe command construction, validate untrusted values, and avoid pasting untrusted input directly into shell commands.

Risk: Continuous monitoring and live digest jobs can create ongoing per-minute charges.

Mitigation: Disclose the expected cost and duration before starting jobs, set bounded monitor durations where possible, and return job IDs so users can inspect or cancel jobs.

## Reference(s):

- [Trio API Docs](https://docs.machinefi.com)
- [MachineFi](https://machinefi.com)
- [Trio Console](https://console.machinefi.com)
- [ClawHub Skill Listing](https://clawhub.ai/drandrewlaw/skills/trio-vision)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands, JSON request examples, job identifiers, status summaries, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Trio API response fields such as triggered, explanation, latency_ms, job_id, status, and remediation; API key values should not be exposed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
