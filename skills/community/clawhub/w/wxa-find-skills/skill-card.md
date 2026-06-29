## Description: <br>
Find MP Skills helps an agent search, review, and install community mini-program AI Skills into an existing mini-program project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binggg](https://clawhub.ai/user/binggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers maintaining existing mini-program projects use this skill to discover suitable community AI Skills, compare search results, install the selected skill, and run the required setup steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing community mini-program skills can add dependencies and project files to an existing application. <br>
Mitigation: Confirm the target project path, review the community skill and dependencies before installation, and use version control or a backup before applying changes. <br>
Risk: Cloud setup steps may affect billing, environment configuration, or existing data. <br>
Mitigation: Run setup against a test cloud environment first when billing or existing data could be affected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binggg/wxa-find-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands and installation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in an installed Skill directory and app.json registration entry in the target mini-program project.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
