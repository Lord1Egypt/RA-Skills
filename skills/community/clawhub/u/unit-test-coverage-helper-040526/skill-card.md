## Description: <br>
Add meaningful unit tests to existing codebases by finding uncovered behavior, selecting high-value cases, and validating coverage without brittle test inflation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, software maintainers, QA engineers, open-source contributors, and product teams use this skill to plan, add, and validate unit or regression tests for existing codebases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording may cause the skill to activate for general quality-related development requests. <br>
Mitigation: Invoke the skill explicitly when testing help is desired, and confirm the task is about unit tests, coverage, or regression confidence before applying its workflow. <br>
Risk: Generated tests can encode incorrect assumptions, brittle implementation details, or incomplete coverage claims. <br>
Mitigation: Review proposed tests against intended behavior, run focused and broader test commands when feasible, and report remaining uncovered risks honestly. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/unit-test-coverage-helper-040526) <br>
- [Requirement Plan](artifact/references/requirement-plan.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code patches, test plans, verification commands, and concise coverage notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include focused and broader test commands plus remaining coverage gaps.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
