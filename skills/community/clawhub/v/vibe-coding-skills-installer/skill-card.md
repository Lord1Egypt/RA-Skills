## Description: <br>
Install vibe coding skill sets, including OpenSpec, gstack, and Superpowers, for supported agent platforms while prompting for target platform, install scope, and configuration options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fdingiit](https://clawhub.ai/user/fdingiit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and configure OpenSpec, gstack, and Superpowers across supported coding-agent platforms. It helps choose global or project-level installation scope, run prerequisite checks, execute installation commands, and verify installed components. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent global or project-level changes to local skill directories and configuration. <br>
Mitigation: Review the selected platform, scope, and destination path before approving each install command. <br>
Risk: The helper can fetch or run setup code from upstream OpenSpec, gstack, and Superpowers sources. <br>
Mitigation: Install only when those upstream repositories are trusted, and review their setup behavior before use in sensitive environments. <br>
Risk: Project-scope installs may add files to the current repository. <br>
Mitigation: Run git status after installation and review added or modified files before committing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fdingiit/vibe-coding-skills-installer) <br>
- [Platform reference](platforms.md) <br>
- [OpenSpec workflow skills](https://github.com/samotage/cursor-openspec-workflows) <br>
- [gstack](https://github.com/garrytan/gstack) <br>
- [Superpowers](https://github.com/obra/superpowers) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with prompts, summary tables, and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a bundled shell helper that reports status, dependency checks, install actions, and verification results.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
