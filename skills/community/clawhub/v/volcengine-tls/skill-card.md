## Description:

Guides agents and CI operators through contract-first Volcengine TLS log administration using the volclog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to discover and execute Volcengine TLS log operations, resolve resources, inspect results, and recover from errors without guessing command contracts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A wrong runtime selector can change the wrong cloud resources or expose log data.

Mitigation: Confirm the profile, secrets file, or environment credentials and review the selected resource before running commands.

Risk: Raw API calls, ingestion, export, and create or update operations can affect resources or disclose sensitive logs.

Mitigation: Review operation contracts and destinations, use dry-run where supported, and require approval before consequential writes or exports.

Risk: Local profiles, secrets files, and output directories may expose credentials or exported data.

Mitigation: Never print or persist credentials in prompts; use protected files and writable output locations with appropriate access controls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/volc-sdk-team/skills/volcengine-tls)
- [CLI project homepage (release metadata)](https://github.com/volcengine-tls/ve-tls-cli)
- [Routing guide](references/routing.md)
- [Operational procedures](references/sops.md)
- [Runtime and recovery guidance](references/best-practices.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands and JSON input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes guidance for interpreting CLI result envelopes and file-based output.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
