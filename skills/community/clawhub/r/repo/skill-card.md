## Description: <br>
Project initialization toolkit. contributing - auto-generate CONTRIBUTING.md from project structure [contributing.md]. "init", "project init", "initialize project", "contributing guide", "CONTRIBUTING.md", "contributing generate" triggers <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and maintainers use this skill to inspect a repository's project structure, configuration files, package scripts, and conventions, then draft a project-specific CONTRIBUTING.md guide. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated CONTRIBUTING.md content may be incorrect or misleading if repository conventions are ambiguous or incomplete. <br>
Mitigation: Review the generated guide against the repository's actual setup before accepting it. <br>
Risk: Broad trigger phrases such as "init" may invoke the skill unintentionally. <br>
Mitigation: Use explicit prompts for contributing-guide generation and review activation before allowing file writes. <br>
Risk: The skill can propose overwriting an existing CONTRIBUTING.md file. <br>
Mitigation: Confirm before overwrite and keep the existing file available for comparison. <br>


## Reference(s): <br>
- [Contributing Generator](contributing.md) <br>
- [Repo skill page](https://clawhub.ai/drumrobot/repo) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a CONTRIBUTING.md draft from repository configuration and directory structure; review before accepting or overwriting files.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and CHANGELOG, released 2026-06-03) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
