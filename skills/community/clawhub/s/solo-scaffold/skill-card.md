## Description: <br>
Generates complete projects from a PRD and stack template, including directory structure, configuration files, AI project docs, Git setup, and optional GitHub push. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fortunto2](https://clawhub.ai/user/fortunto2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to bootstrap new applications from a PRD and chosen stack. It helps produce project files, documentation, command interfaces, Git setup, and next-step guidance for common application stacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or modify local project files and store persistent defaults under the user's home directory. <br>
Mitigation: Confirm the target path, project name, organization defaults, and local-only expectations before allowing file creation. <br>
Risk: The skill can use local GitHub credentials to create and push a private repository. <br>
Mitigation: Confirm the GitHub account or organization, repository visibility, and whether a push should occur before running repository commands. <br>
Risk: Generated setup, install, and build commands can affect the selected project environment. <br>
Mitigation: Review the proposed stack, generated commands, and working directory before running install or build checks. <br>


## Reference(s): <br>
- [Stack-specific file structures](references/stack-structures.md) <br>
- [ClawHub release page](https://clawhub.ai/fortunto2/solo-scaffold) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance plus generated project files and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local files, persistent defaults, a Git repository, and a private GitHub repository after confirmation.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
