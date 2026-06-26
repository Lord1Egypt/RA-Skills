## Description: <br>
Skill Registry Manager helps Claude Code users list, subscribe to, and install skills from local and remote registries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gavinyao](https://clawhub.ai/user/gavinyao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to manage a reusable skill registry, review available skills, subscribe to shared registries, and install selected skills into global or project-level skill directories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch remote registries and guide installation of skills from npx, git, or local sources. <br>
Mitigation: Use only trusted registries and repositories, inspect the resolved skill source, and confirm each remote fetch and install command before execution. <br>
Risk: Subscription paths and install commands may include user-controlled strings or shell-sensitive characters. <br>
Mitigation: Avoid subscription paths containing shell metacharacters and review expanded paths and commands before running them. <br>
Risk: Installed skills may broaden an agent's behavior after installation. <br>
Mitigation: Keep installed skills inspectable, pinned when possible, and removable; review security scan results before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gavinyao/skills-registry-manager) <br>
- [Publisher Profile](https://clawhub.ai/user/gavinyao) <br>
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code) <br>
- [Default Registry Subscription](https://raw.githubusercontent.com/gavinyao/awesome-skills/main/registry.yaml) <br>
- [registry.example.yaml](registry.example.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and prose with inline shell commands and YAML configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose remote fetches, local file reads, and skill installation commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
