## Description: <br>
A meta-skill that helps an agent turn GitHub repositories into standardized Trae skills by cloning or scanning repositories, generating scaffold files, and assembling a context bundle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guangliang2233](https://clawhub.ai/user/guangliang2233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when they want to package a GitHub repository as a reusable Trae skill, including generated scaffolding, a context bundle, and usage guidance. It is intended for repository-to-skill conversion workflows, especially when a user provides a GitHub URL and asks the agent to install or integrate the tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or overwrite persistent agent skill files from GitHub repository content. <br>
Mitigation: Use trusted public repositories, review generated SKILL.md and context files before use, and run generated or cloned code in a sandbox. <br>
Risk: The skill uses local execution and secret-handling patterns, including loading environment variables and optionally using GitHub tokens. <br>
Mitigation: Avoid running it from directories containing sensitive .env files and do not use it with private or internal repositories unless mirrors are disabled and verified. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/guangliang2233/yuhang) <br>
- [GitHub CLI documentation](https://cli.github.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, generated skill scaffolding, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent skill directories and context_bundle.md files; may clone or scan GitHub repositories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
