## Description: <br>
Use when anything misbehaves - a failing test, production bug, build break, flaky or unexpected behavior - before proposing or attempting any fix, especially under pressure or after a previous fix did not hold. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[escoffier-labs](https://clawhub.ai/user/escoffier-labs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to investigate failures by reading errors, reproducing issues, checking recent changes and contracts, tracing causes, and comparing working siblings before making a fix. It is intended to keep debugging focused on a stated root-cause hypothesis, a failing test where applicable, and one minimal change. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent toward high-impact debugging or fix actions in sensitive repositories. <br>
Mitigation: Use it in an appropriate maintainer or staff context, and review commands, file edits, migrations, PR comments, and any credential-sensitive workflow before approving writes. <br>
Risk: Skipping the workflow can produce symptom-masking fixes that leave the underlying failure unresolved. <br>
Mitigation: Require reproduction, a specific root-cause hypothesis, a failing test where applicable, one minimal change, and verification of the original symptom. <br>


## Reference(s): <br>
- [Skillet Refire ClawHub release page](https://clawhub.ai/escoffier-labs/skillet-refire) <br>
- [escoffier-labs publisher profile](https://clawhub.ai/user/escoffier-labs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown guidance with diagnostic steps, root-cause hypotheses, failing-test plans, and minimal code or shell command proposals when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Root-cause-first workflow; fixes are expected only after reproduction, a stated hypothesis, and verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
