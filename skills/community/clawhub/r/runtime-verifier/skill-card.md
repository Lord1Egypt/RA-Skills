## Description: <br>
Use when a code change must be verified by actually running the app, endpoint, or CLI flow instead of relying only on unit tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn a code-change request into a concrete live-runtime verification plan, execute the relevant app, endpoint, or CLI flow, and report pass/fail evidence with cleanup status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runtime verification can run commands, endpoints, or application flows that mutate data or affect a live service if the target is underspecified. <br>
Mitigation: Specify the exact target, expected behavior, and commands or endpoints that must not mutate data; prefer local, test, or staging environments over production. <br>
Risk: Started apps, servers, or CLI sessions can remain running after verification and consume resources or ports. <br>
Mitigation: Require a cleanup summary and stop any processes or sessions started during verification. <br>


## Reference(s): <br>
- [Runtime Verifier release page](https://clawhub.ai/wimi321/runtime-verifier) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown with verification steps, pass/fail evidence, and cleanup summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands or endpoints to run when needed for live verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
