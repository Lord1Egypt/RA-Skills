## Description: <br>
Guides agents through a structured root-cause debugging workflow before proposing or implementing fixes for broken behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kkenny0](https://clawhub.ai/user/kkenny0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill when a bug, crash, failed check, regression, or unexpected behavior needs systematic investigation. It helps reproduce the issue, gather evidence, identify the root cause, test hypotheses, and verify a focused fix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Debug reports, web searches, or persistent learning notes may expose sensitive logs, secrets, customer data, hostnames, IP addresses, or file paths. <br>
Mitigation: Sanitize sensitive values before sharing, searching, or storing investigation evidence. <br>
Risk: The evidence-first workflow can slow urgent bug fixes because it requires reproduction and root-cause investigation before implementation. <br>
Mitigation: Use the skill's timebox guidance to pause and present findings when investigation exceeds the stated budget without convergence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kkenny0/taku-debug) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown debug report with optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only workflow; produces investigation notes, hypotheses, verification evidence, and fix status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
