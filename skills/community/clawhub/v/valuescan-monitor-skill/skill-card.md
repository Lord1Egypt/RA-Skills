## Description:

Monitors ValueScan market-analysis and token-signal streams and persists incoming events to local files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[valuescan-io](https://clawhub.ai/user/valuescan-io)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ValueScan users use this skill to configure and run background monitors for market analysis and token signals, including selected token symbols, and to save streamed updates to local files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ValueScan API credentials are stored in plaintext in ~/.vs-monitor/config.json.

Mitigation: Restrict permissions on ~/.vs-monitor, use a dedicated account or container, and avoid sharing the configuration file.

Risk: The skill runs long-lived background monitor processes and manages them through PID files.

Mitigation: Review monitor status before start and stop actions, and run the skill in an isolated account when possible.

Risk: Streamed data is continuously written to a user-selected output directory, with signal filenames derived from incoming stream content.

Mitigation: Use a dedicated output directory and review or patch filename validation before using untrusted streams.

Risk: All-token monitoring may collect more stream data than needed.

Mitigation: Prefer token-scoped monitoring unless broad monitoring is required.

## Reference(s):

- [ValueScan homepage](https://www.valuescan.ai)
- [ValueScan Monitor Skill on ClawHub](https://clawhub.ai/valuescan-io/skills/valuescan-monitor-skill)
- [ValueScan Stream API reference](artifact/references/stream-api.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local configuration, PID/log files, and streamed text files under the user-configured output directory.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
