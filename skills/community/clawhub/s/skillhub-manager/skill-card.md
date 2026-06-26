## Description: <br>
Manage and publish agent skills on SkillHub and ClawHub. Best for developers and operators who need a repeatable workflow to search skills, inspect packages, authenticate securely, and publish local skill folders to a registry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeblackhole1024](https://clawhub.ai/user/codeblackhole1024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to search, inspect, authenticate to, and publish local skill folders to SkillHub-compatible registries while confirming the intended registry before live actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Registry actions could target the wrong SkillHub or ClawHub instance. <br>
Mitigation: Ask for the registry address, repeat it back, and use CLAWHUB_REGISTRY for custom registries before login, search, inspect, explore, or publish. <br>
Risk: Publishing can expose secrets or private files from the selected local skill folder. <br>
Mitigation: Inspect the folder contents before publishing and confirm the registry account with whoami before upload. <br>
Risk: API tokens can be exposed through shared terminals, command history, or logs. <br>
Mitigation: Prefer scoped or short-lived tokens, avoid pasting tokens into shared contexts, and use safer interactive or environment-based login methods when supported. <br>


## Reference(s): <br>
- [SkillHub Manager Workflows](references/workflows.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/codeblackhole1024/skillhub-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts for a target registry before registry actions and may include environment-variable command prefixes for custom registries.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
