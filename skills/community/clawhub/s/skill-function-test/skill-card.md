## Description: <br>
skill-function-test is a scenario-driven testing suite for backing up target skills, scanning their structure, running scenario, function, and execution-fidelity tests, optionally repairing findings, bumping versions, and writing test reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldxs001](https://clawhub.ai/user/ldxs001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and skill maintainers use this skill to audit, regression-test, and optionally repair agent skills before publishing updates or validating releases. It is intended for structured skill quality checks, including scenario coverage, function-level checks, execution-fidelity testing, and report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute and modify target skills. <br>
Mitigation: Install and run it only in disposable or sandboxed workspaces and only against targets you are willing to execute and modify. <br>
Risk: Reports may be misleading if hook-bypass or fabricated-report behavior is present. <br>
Mitigation: Treat reports as non-authoritative until real execution logs are reviewed and the bypass or fabricated-report behavior is removed or ignored. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/skill-function-test) <br>
- [Usage guide](references/guide.md) <br>
- [Examples](references/examples.md) <br>
- [Permissions and risk notes](references/permissions.md) <br>
- [Scenario test plan schema](references/s-test-plan-schema.md) <br>
- [S4 execution-fidelity testing](references/s4-noise-testing.md) <br>
- [Changelog](references/changelog.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, HTML, JSON test artifacts, shell commands, and modified skill files when repair mode is enabled] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create backups, test plans, execution traces, reports, configuration files, version updates, and repaired skill files.] <br>

## Skill Version(s): <br>
1.16.1 (source: server release metadata, SKILL.md frontmatter, _meta.json, changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
