## Description: <br>
Execute JavaScript code in a secure sandbox for data processing, computation, and quick expression evaluation without network or filesystem access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulgnz](https://clawhub.ai/user/paulgnz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run small JavaScript calculations, data transformations, and expression checks in a constrained sandbox without network or filesystem access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally executes user-provided JavaScript, which can produce incorrect results, long-running computations, or misleading logs. <br>
Mitigation: Run only snippets intended for computation, review returned results before relying on them, and use the disclosed timeout and output limits for bounded execution. <br>
Risk: Users may overestimate the sandbox's access to external systems or local resources. <br>
Mitigation: Treat the execution environment as pure computation only; the reviewed evidence states it has no network, filesystem, credential, import, or persistence behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paulgnz/xpr-code-sandbox) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, analysis] <br>
**Output Format:** [JSON object with result, logs, duration, type, or error fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default 5 second timeout, maximum 30 seconds, and 10MB output limit.] <br>

## Skill Version(s): <br>
0.2.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
