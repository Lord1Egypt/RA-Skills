## Description:

Israel Red Alert API for real-time and historical rocket and missile alert data, with city and time-range queries plus shelter-time statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dannyshmueli](https://clawhub.ai/user/dannyshmueli)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to query recent Israeli alert history, monitor real-time alert channels, check provider status, and summarize shelter-time impact for selected cities or nationwide data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The real-time listener and daemon can run persistently and append alert data to local JSONL files without built-in retention controls.

Mitigation: Run listener modes with storage and process limits, and configure log rotation or retention for /data/clawd/tmp/redalert-*.jsonl.

Risk: The real-time mode depends on a vulnerable network-facing Socket.IO dependency tree according to the authoritative security evidence.

Mitigation: Update the Socket.IO dependency tree before using real-time listener modes in unattended or production contexts.

Risk: The current real-time mode is under-scoped for unattended use.

Mitigation: Review the listener behavior before installation and supervise persistent deployments with operational monitoring.

## Reference(s):

- [ClawHub Red Alert Skill](https://clawhub.ai/dannyshmueli/skills/red-alert)
- [Endpoint Inventory](references/ENDPOINTS.md)
- [RedAlert API](https://redalert.orielhaim.com/)
- [Tzeva Adom Alert History API](https://api.tzevaadom.co.il/alerts-history)
- [RedAlert Status API](https://redalert.orielhaim.com/api/status)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON examples, JSON lines, and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Real-time listener modes may emit newline-delimited JSON and write JSONL files under /data/clawd/tmp.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
