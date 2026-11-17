## Description:

Create new skills, modify and improve existing skills, and measure skill performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pupuking723](https://clawhub.ai/user/pupuking723)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and skill authors use this skill to create, revise, evaluate, benchmark, and package agent skills through guided drafting and iteration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run local Python helpers, invoke the Claude CLI, create files, package skills, write eval workspaces, and start a localhost review server.

Mitigation: Install only when those local side effects are acceptable, run without elevated privileges, and review generated files and package contents before deployment.

Risk: Security evidence flags unsafe local side effects and viewer vulnerabilities, including HTML embedding, arbitrary port-kill behavior, and a symlink packaging issue.

Mitigation: Use trusted skill directories and eval outputs, prefer static review output when appropriate, avoid untrusted inputs until these issues are fixed, and clean up viewer processes after review.

## Reference(s):

- [Skill Creator JSON Schemas](references/schemas.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON snippets, shell commands, generated skill files, evaluation reports, and package artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify skill directories, eval workspaces, benchmark reports, static review HTML, and skill packages.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
