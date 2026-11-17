## Description:

Use beeline, the WireCat CLI for Beeline Cloud PBX call recordings, from an agent — find a command, run it with the owner's profile, read JSON answers. Use when a task needs the company's recorded calls, their transcripts or the people on them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wirecat](https://clawhub.ai/user/wirecat)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and support staff use this skill to find and run Beeline CLI commands for syncing recorded calls, transcribing and searching conversations, and linking callers to Bitrix24 contacts. It guides the agent to use the owner's profile and interpret JSON results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports no scanner findings, but one local reference could not be resolved and review confidence is medium.

Mitigation: Review the unresolved reference and consider the incomplete review when deciding whether to install.

Risk: Call recordings, transcripts, phone numbers, and linked contact records may contain personal or confidential information; commands may also make changes within the selected profile's permissions.

Mitigation: Use the owner's intended profile, follow applicable data-handling rules, and use --dry-run to preview a write when available.

## Reference(s):

- [Beeline Cli on ClawHub](https://clawhub.ai/wirecat/skills/wirecat-beeline)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Text guidance, shell command examples, and JSON service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Service-provided text is treated as data; writes follow the selected profile's permissions.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
