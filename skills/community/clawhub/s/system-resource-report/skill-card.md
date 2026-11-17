## Description:

Check current Linux system resource usage and report load, memory, swap, disk, and top CPU/memory processes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[karryklein](https://clawhub.ai/user/karryklein)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and administrators use this skill to collect a quick Linux host health summary covering load, memory, swap, root disk usage, and top CPU or memory consumers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: System health output and top process command lines may expose sensitive local operational details or command arguments.

Mitigation: Run the skill only in contexts where sharing local resource metrics and process command lines with the agent is acceptable; redact sensitive output before redistributing summaries.

Risk: Reported values depend on standard Linux tools being available and reflecting the host accurately.

Mitigation: Confirm unusual findings directly on the host before making operational decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary with command output interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports local Linux system metrics and may include process command lines.]

## Skill Version(s):

1.0.0 (source: server release metadata and publishing notes)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
