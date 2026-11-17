## Description:

System Watchdog monitors Linux and macOS resource signals, detects actionable anomalies such as worsening memory pressure, runaway processes, sustained CPU burn, and disk pressure, and stays quiet when no issue needs attention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brennerspear](https://clawhub.ai/user/brennerspear)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a local watchdog check, parse JSON system health results, and receive a concise report only when resource anomalies need attention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The watchdog records full process command lines in its local state file, which can expose secrets passed as command arguments.

Mitigation: Run without elevated privileges, store SYSTEM_WATCHDOG_STATE in a protected location, and redact or remove command fields before regular use on systems where command arguments may contain credentials.

## Reference(s):

- [System Watchdog Skill Page](https://clawhub.ai/brennerspear/skills/system-watchdog)
- [Artifact Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON from the watchdog script, followed by concise Markdown or text reports when anomalies are detected]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script persists local state between runs so the agent can detect resource deltas instead of reporting only point-in-time usage.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
