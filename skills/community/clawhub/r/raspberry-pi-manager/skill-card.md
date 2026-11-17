## Description:

A local bash command-line journal for recording Raspberry Pi-related operational notes, searching saved entries, viewing recent activity, and exporting logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators can use this skill as a local operations journal for Raspberry Pi fleet notes, automation records, status observations, searches, and exports. It should not be treated as a device management or monitoring interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is advertised as Raspberry Pi management, but evidence shows it records local notes and exports logs rather than controlling GPIO, services, sensors, or devices.

Mitigation: Use it only as an operations journal and verify any real device-management needs with separate trusted tooling.

Risk: Operational entries are stored in plaintext under ~/.local/share/raspberry-pi-manager and can be searched or exported.

Mitigation: Do not enter credentials, tokens, private host details, or other sensitive information into logged entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/skills/raspberry-pi-manager)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Files, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and local text, JSON, CSV, or TXT export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores entries in plaintext under ~/.local/share/raspberry-pi-manager.]

## Skill Version(s):

2.0.1 (source: ClawHub release evidence; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
