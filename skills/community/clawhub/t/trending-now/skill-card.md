## Description: <br>
Monitor internet and social media trends with heartbeat topic watchlists, freshness scoring, and concise alerts on what changed and why it matters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and teams use this skill to monitor chosen topics across public internet and social sources, validate trend signals, and receive concise alerts only when meaningful changes occur. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring public web lookups can expose monitored topic keywords to external services. <br>
Mitigation: Use explicit-only mode when proactive monitoring is not wanted, keep watchlists narrow, and avoid secrets, private credentials, or highly sensitive topics in ~/trending-now. <br>
Risk: Single-source spikes or stale public posts can produce misleading trend alerts. <br>
Mitigation: Require timestamped evidence from at least two independent source families and record uncertainty before sending an alert. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/trending-now) <br>
- [Setup](setup.md) <br>
- [Heartbeat Template](HEARTBEAT.md) <br>
- [Research Protocol](research-protocol.md) <br>
- [Source Map](source-map.md) <br>
- [Message Format](message-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and concise text alerts with optional inline shell commands for local setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return HEARTBEAT_OK when no actionable trend change is detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
