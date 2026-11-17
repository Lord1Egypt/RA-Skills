## Description:

Systematic Debugging guides agents through a four-phase root cause debugging process that gathers evidence, narrows scope, forms a hypothesis, and verifies the fix.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aptratcn](https://clawhub.ai/user/aptratcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide software debugging work through evidence gathering, scope isolation, hypothesis formation, and verification before declaring a fix complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may activate the skill for general support requests that mention common debugging terms.

Mitigation: Confirm the user wants a structured debugging workflow before applying the full checklist, or narrow activation triggers during packaging.

Risk: Debugging guidance can lead to code or command proposals that are incorrect for the user's environment.

Mitigation: Require reproduction details, review proposed changes before execution, and verify with the original failing case and regression checks.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with checklists and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces procedural debugging guidance and verification prompts rather than executing commands automatically.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
