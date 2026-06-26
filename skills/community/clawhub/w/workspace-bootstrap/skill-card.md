## Description: <br>
Workspace Bootstrap creates OpenClaw workspace directory structures, core markdown templates, scenario examples, and validation checks for new or migrated agent workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack-long-2022](https://clawhub.ai/user/jack-long-2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to initialize or migrate an agent workspace, choose a starter scenario, generate core files, and check common setup pitfalls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workspace may contain persistent personal data or credentials in markdown files and generated directories. <br>
Mitigation: Create the workspace in a new empty directory, avoid storing raw API keys or SSH secrets, and review or redact USER.md, SOUL.md, memory, reports, shared, and user-data before sharing. <br>
Risk: Whole-workspace sharing can expose private user or agent data. <br>
Mitigation: Treat generated workspace content as private until reviewed, and add a .gitignore before using Git. <br>
Risk: Bootstrap or wizard scripts may affect files in an existing workspace. <br>
Mitigation: Review existing files before running bootstrap or wizard scripts, especially outside a clean workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jack-long-2022/workspace-bootstrap) <br>
- [README](README.md) <br>
- [Quickstart](docs/QUICKSTART.md) <br>
- [Usage Guide](docs/USAGE.md) <br>
- [Workspace Template](templates/WORKSPACE-TEMPLATE.md) <br>
- [Test Report](tests/test-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands and generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates workspace directories and core markdown templates, with optional scenario examples and pitfall checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
