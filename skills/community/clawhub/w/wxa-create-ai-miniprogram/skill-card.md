## Description: <br>
Helps developers create a new AI-enabled WeChat Mini Program project from scratch using mp-skills, then configure cloud development, database, login, payment, and starter skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binggg](https://clawhub.ai/user/binggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to plan and scaffold a new AI-enabled WeChat Mini Program, install initial skills, and follow configuration guidance for appid, cloud environment setup, and WeChat developer tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill proposes npx and setup commands that may create files, initialize git, install third-party code, or modify a project directory. <br>
Mitigation: Review the package or skill source before installation and run setup commands only inside a project directory intended for modification. <br>
Risk: The workflow depends on user-provided appid and cloud environment IDs. <br>
Mitigation: Keep those identifiers user-managed and verify them in the WeChat and cloud development consoles before running setup. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may guide project creation and setup commands that create or modify files in the target project.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
