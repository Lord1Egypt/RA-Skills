## Description:

Safe Execution is intended to help agents avoid repeated failing tool calls by using three-strike loop detection, cost estimation, and exception-channel safeguards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laolong507](https://clawhub.ai/user/laolong507)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to reduce runaway tool-call loops and protect user balances during normal agent operation. Reviewers should note that the released runtime SKILL.md is empty, so the artifact may not provide the described behavior until completed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package's main SKILL.md file is empty, so agents may receive little or no executable runtime guidance.

Mitigation: Review the installed package before use and require a completed SKILL.md before relying on the loop-prevention behavior.

Risk: The artifact documentation describes cost-control behavior that is not present in the empty runtime skill file.

Mitigation: Validate behavior in a controlled session with repeated failing tool calls before deployment.

Risk: The license signal differs between server evidence and artifact documentation.

Mitigation: Confirm the authoritative license terms before public release or downstream redistribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laolong507/skills/safe-execution)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The current artifact has an empty SKILL.md, so actual runtime output may be absent.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
