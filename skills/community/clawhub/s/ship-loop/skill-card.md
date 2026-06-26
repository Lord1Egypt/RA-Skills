## Description: <br>
Ship Loop runs chained build, preflight, deploy, verification, repair, and reflection loops for multi-segment feature work handled by coding agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fernando-fernandez3](https://clawhub.ai/user/fernando-fernandez3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent operators use Ship Loop to run multi-segment feature implementation through build, test, deploy, verification, repair, and reflection loops while preserving progress across restarts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured agent, preflight, deploy, notify, and custom script commands can run with the user's privileges and without sandboxing. <br>
Mitigation: Install only in trusted repositories, review SHIPLOOP.yml as executable code, start with dry-run, and run in an isolated branch or worktree. <br>
Risk: The tool can autonomously modify files, commit, push, deploy, and clean repository state. <br>
Mitigation: Use well-controlled deployment targets, constrain or disable meta and optimization loops when human review is required, and inspect changes before allowing production deployment. <br>
Risk: Run context and operational details may be persisted in the local SQLite state backend. <br>
Mitigation: Avoid custom scripts and notification commands in environments with sensitive variables, and review stored state before sharing a workspace. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fernando-fernandez3/ship-loop) <br>
- [README](README.md) <br>
- [Configuration Reference](docs/src/content/docs/reference/configuration.md) <br>
- [CLI Reference](docs/src/content/docs/reference/cli.md) <br>
- [PyPI Package](https://pypi.org/project/shiploop/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with inline shell commands and YAML configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run configured commands and produce repository changes, commits, deployment checks, status reports, learnings, and budget summaries.] <br>

## Skill Version(s): <br>
5.0.0 (source: evidence release metadata, SKILL.md metadata.openclaw.version, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
