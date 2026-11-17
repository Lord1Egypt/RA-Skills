## Description:

Automatically generates detailed Standard Operating Procedures (SOPs) for recurring digital tasks used in agency operations or internal AI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[balkanblbn](https://clawhub.ai/user/balkanblbn)

### License/Terms of Use:


## Use Case:

External users and operations teams use this skill to turn recurring digital tasks into repeatable SOP markdown files with numbered workflow steps and success criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled SOP generation script can overwrite Markdown files outside the intended SOPs folder when given a crafted task name.

Mitigation: Reject task names containing slashes, backslashes, .. path components, or existing destination paths before running the script.

Risk: The release security verdict is suspicious for broad use with untrusted task names.

Mitigation: Review and constrain inputs before installation or execution in shared or automated environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/balkanblbn/skills/sop-architect)
- [Publisher profile](https://clawhub.ai/user/balkanblbn)

## Skill Output:

**Output Type(s):** [markdown, shell commands, files, guidance]

**Output Format:** [Markdown SOP files with numbered steps and success criteria]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated SOP filenames are derived from the task name.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
