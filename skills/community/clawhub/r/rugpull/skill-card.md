## Description:

Analyze rugpull operations. Use when you need to understand rugpull mechanisms, evaluate protocol security, or reference on-chain concepts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to run the bundled command-line helper for status, note entry management, search, export, stats, and configuration related to rugpull investigation notes. Security evidence says the inspected artifact behaves as a local note/config tool rather than a true rugpull-analysis implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised rugpull-analysis purpose does not match the inspected behavior, so users may expect analysis the artifact does not perform.

Mitigation: Review behavior before installation and treat the artifact as a local note/config manager until the implementation and documentation are aligned.

Risk: The script writes persistent local data, can delete stored entries, and can export copies into the working directory.

Mitigation: Use a dedicated non-sensitive RUGPULL_DIR and review remove/export commands before running them.

Risk: The config command is flagged as unsafe when used with untrusted input.

Mitigation: Do not pass untrusted values to config, and inspect configuration changes before reuse.

## Reference(s):

- [Rugpull ClawHub skill page](https://clawhub.ai/xueyetianya/skills/rugpull)
- [Publisher profile](https://clawhub.ai/user/xueyetianya)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses RUGPULL_DIR for local data storage and can export JSONL or CSV files into the working directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
