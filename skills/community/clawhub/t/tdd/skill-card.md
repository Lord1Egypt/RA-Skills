## Description: <br>
Tdd guides agents through test-driven development for coding and bug fixing, including Red-Green-Refactor workflow, test execution, and test design techniques. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering agents use this skill to define expected behavior as tests before implementation, run the relevant test scope, and report results during coding and bug-fixing work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases such as "verify" or "doesn't work" may invoke the skill during ordinary debugging. <br>
Mitigation: Use the skill when an assertive test-first workflow is desired, and review whether its trigger behavior fits the agent's normal debugging process. <br>
Risk: The workflow strongly prioritizes Red test authoring before diagnosis or implementation, which can slow tasks where test-first work is not appropriate. <br>
Mitigation: Apply the skill to coding and bug-fixing tasks where regression evidence is valuable, and avoid using it for non-code analysis or tasks that cannot support test authoring. <br>


## Reference(s): <br>
- [TDD skill overview](SKILL.md) <br>
- [TDD Cycle](cycle.md) <br>
- [Test Run](run.md) <br>
- [Test Strategies](test-strategies.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow guidance and test-related agent actions; it does not declare API calls, MCP tools, or credential requirements.] <br>

## Skill Version(s): <br>
0.3.1 (source: release metadata and changelog, released 2026-06-19; frontmatter metadata says 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
