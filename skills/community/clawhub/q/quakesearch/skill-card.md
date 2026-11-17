## Description:

Helps an agent use a local Quake CLI binary to run asset searches, page through results, and export CSV or raw output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biglizi775](https://clawhub.ai/user/biglizi775)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security practitioners use this skill to prepare Quake CLI commands for asset discovery, domain, host, info, and honeypot lookups, with automated pagination and CSV or raw exports. It is intended for users who already have authorized Quake API access and provide their own trusted Quake binary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passing the Quake API key with --key can expose the credential through process listings, shell history, logs, or error output.

Mitigation: Initialize the Quake credential outside the wrapper when possible, prefer environment-based secret handling, avoid --key on shared machines or CI, and rotate the key if exposure is suspected.

Risk: The skill runs a local Quake binary supplied by the user.

Mitigation: Use only an official, trusted Quake binary appropriate for the operating system, or specify a reviewed binary path with --quake-bin.

Risk: CSV and raw exports may contain sensitive asset discovery results.

Mitigation: Choose output paths deliberately, limit file access, and handle exported CSV and raw text according to the sensitivity of the queried assets.

## Reference(s):

- [Quake Search v1.0 on ClawHub](https://clawhub.ai/biglizi775/skills/quakesearch)
- [Publisher profile: biglizi775](https://clawhub.ai/user/biglizi775)
- [Artifact script README](artifact/scripts/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to create CSV and raw text export files through the bundled wrapper script.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
