## Description: <br>
Use when starting feature work that needs isolation from the current workspace by creating isolated git branches with setup and safety verification for OpenClaw environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill at the start of feature work to choose a workspace location, create a feature branch, run project setup, and verify a clean baseline before implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may overstate workspace isolation because it uses branch-based workflow steps and can direct persistent repository changes and setup commands in the current working tree. <br>
Mitigation: Confirm the working directory before use, review any .gitignore diff before committing, and pause before running package-manager setup commands in repositories that are not fully trusted. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose git branch creation, .gitignore updates, dependency installation, and baseline test commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
