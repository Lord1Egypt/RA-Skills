## Description:

Execute JavaScript code in a sandboxed VM for data processing and computation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulgnz](https://clawhub.ai/user/paulgnz)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run JavaScript snippets for calculations, data processing, expression evaluation, and algorithm checks inside a constrained execution environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the JavaScript sandbox boundary is flawed and may expose the host process despite claims of no process, filesystem, or network access.

Mitigation: Review carefully before installing; run only JavaScript that is fully trusted or strengthen the isolation before treating the tool as a safe sandbox for arbitrary code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paulgnz/skills/xpr-code-sandbox)

## Skill Output:

**Output Type(s):** [text, code]

**Output Format:** [JSON object containing a result, logs, duration, type information, warnings, or an error message.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default timeout is 5 seconds, maximum timeout is 30 seconds, and serialized output is limited to 10MB.]

## Skill Version(s):

0.2.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
