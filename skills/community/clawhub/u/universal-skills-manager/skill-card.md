## Description: <br>
The master coordinator for AI skills that discovers skills from SkillsMP, SkillHub, and ClawHub, then manages installation and synchronization across Claude Code, Gemini CLI, Google Anti-Gravity, OpenCode, and other AI tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacob-bd](https://clawhub.ai/user/jacob-bd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to find, install, package, and synchronize agent skills across supported local and cloud AI tool environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change skill directories loaded by multiple AI agents. <br>
Mitigation: Prefer project-level installs, inspect proposed changes and downloaded skills before use, and keep the built-in security scan enabled. <br>
Risk: Cloud ZIP packaging can include a SkillsMP API key that may be exposed if the archive is shared. <br>
Mitigation: Avoid embedding API keys in shared archives, keep private ZIPs controlled, and rotate any key that may have been exposed. <br>
Risk: Force installs, skipped scans, or unreviewed remote install scripts can bypass useful safety checks. <br>
Mitigation: Review remote sources first and avoid --force or --skip-scan unless there is a specific, understood reason. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jacob-bd/universal-skills-manager) <br>
- [Project homepage](https://github.com/jacob-bd/universal-skills-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code] <br>
**Output Format:** [Markdown guidance with shell commands, configuration details, and generated or modified skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or package skill files when the user authorizes installation, synchronization, or cloud upload workflows.] <br>

## Skill Version(s): <br>
1.7.0 (source: server release metadata and artifact SKILL.md version comment) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
