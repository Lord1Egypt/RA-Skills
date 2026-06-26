## Description: <br>
CLI tool for generating tests, scanning contracts, managing story-based tests, and setting up MCP integration in web projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ianderrington](https://clawhub.ai/user/ianderrington) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to apply the Supernal Interface CLI in web projects for contract scanning, generated tests, story-based test workflows, validation, and MCP or Claude Code setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can install software, rewrite project files, change IDE or MCP configuration, and install other agent components. <br>
Mitigation: Review the @supernal/interface package and publisher before installation, then run commands first in a disposable project or clean git branch. <br>
Risk: Automated setup and commit flags can apply changes before a developer has reviewed the resulting diffs. <br>
Mitigation: Prefer --dry-run and --manual modes, avoid --force and --git-commit until diffs are reviewed, and require explicit approval before setup-mcp or setup-claude runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ianderrington/si) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with bash command examples and generated project artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to run CLI commands that generate tests, contracts, route/name files, MCP configuration, IDE configuration, and Claude Code integration files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
