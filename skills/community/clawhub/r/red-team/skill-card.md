## Description: <br>
Adversarial multi-agent debate engine for stress-testing decisions, ideas, and strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[retrodigio](https://clawhub.ai/user/retrodigio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to stress-test important decisions, investment analyses, product strategies, go/no-go calls, and pre-mortems through structured adversarial debate among AI personas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Questions and selected context files are sent to the chosen AI CLI backend for analysis. <br>
Mitigation: Choose context files deliberately and avoid sensitive or regulated data unless the selected provider is appropriate for that data. <br>
Risk: Custom personas can change the debate behavior and outputs. <br>
Mitigation: Review custom persona definitions before running them. <br>
Risk: Ambiguous user wording could trigger an unintended red-team run. <br>
Mitigation: Ask the agent to confirm before running the skill when the request is ambiguous. <br>


## Reference(s): <br>
- [Red Team Persona Library](references/personas.md) <br>
- [Conclave adversarial idea markets](https://conclave.sh) <br>
- [ClawHub skill page](https://clawhub.ai/retrodigio/red-team) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown decision brief with debate sections, risk matrix, conviction scores, recommendation, and next steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write the report to a user-selected output file or print it to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
