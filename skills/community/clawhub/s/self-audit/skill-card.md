## Description:

Self Audit describes a workflow for logging, analyzing, scoring, and improving an agent's tool-call usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuge897](https://clawhub.ai/user/jiuge897)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Self Audit to review tool-call logs, distinguish necessary calls from reflexive calls, and identify efficiency improvements. The release advertises CLI-style usage, but server security evidence notes the advertised executable is not bundled, so users should verify functionality before operational use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A working implementation would record tool names, inputs, reasons, and context in local audit logs, which could include secrets, credentials, private customer data, or sensitive business details.

Mitigation: Avoid logging sensitive data unless retention, deletion, and access controls are defined before use.

Risk: The package appears to be missing the advertised self-audit CLI script.

Mitigation: Verify the executable or implementation path before depending on the advertised CLI commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiuge897/skills/self-audit)
- [Publisher Profile](https://clawhub.ai/user/jiuge897)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with example shell commands and text audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or rely on local audit logs in a working implementation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
