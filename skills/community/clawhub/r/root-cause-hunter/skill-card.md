## Description:

Root Cause Hunter guides agents through a strict five-phase root-cause investigation workflow before implementing fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengpengliu1212-art](https://clawhub.ai/user/pengpengliu1212-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to keep debugging work evidence-driven: reproduce the issue, inspect recent changes and environment differences, validate one hypothesis at a time, implement the narrow fix, and capture lessons afterward.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rollback validation could lead to unintended code reverts if treated as permission to change files without review.

Mitigation: Keep user control over any actual revert and use rollback checks only as deliberate diagnostic steps.

Risk: Local debug logs or lesson notes may capture sensitive error output, configuration, or environment details.

Mitigation: Review diagnostic notes before storing them and avoid writing secrets, credentials, or unnecessary private data.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown text with diagnostic steps, hypotheses, commands, and proposed code changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend local diagnostic logs and lesson notes when useful.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
