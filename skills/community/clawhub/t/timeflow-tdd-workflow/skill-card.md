## Description: <br>
Test-Driven Development workflow principles. RED-GREEN-REFACTOR cycle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soponcd](https://clawhub.ai/user/soponcd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to guide agents through TDD: write failing tests, implement minimal passing code, and refactor while keeping tests green. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide code edits and shell commands in a repository. <br>
Mitigation: Use it on a branch, review generated tests and implementation changes, and approve shell commands or commits deliberately. <br>
Risk: TDD guidance can encode an incorrect requirement if the initial failing test is wrong. <br>
Mitigation: Review each test against the intended behavior before relying on implementation or refactoring steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/soponcd/timeflow-tdd-workflow) <br>
- [Skill homepage](https://github.com/soponcd/timeflow-skills/tree/main/teams/skills/tdd-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown guidance with optional code, test, and shell-command proposals.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review generated tests, code changes, and shell commands before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
