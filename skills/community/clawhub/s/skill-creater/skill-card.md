## Description: <br>
Generate complete AgentSkills from user requirements, including SKILL.md, scripts, references, asset folders, and ready-to-upload ClawHub packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timyljob2011-sudo](https://clawhub.ai/user/timyljob2011-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to clarify requirements, generate AgentSkill files and helper scripts, and package the result for ClawHub distribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates local files and zip archives as part of normal packaging behavior. <br>
Mitigation: Use it in a dedicated clean folder, then inspect generated files and archive contents before uploading or sharing them. <br>
Risk: The included build script has a name/path mismatch noted by the security guidance. <br>
Mitigation: Review and fix the build script before running it, or package the skill with the Python packager directly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/timyljob2011-sudo/skill-creater) <br>
- [Publisher profile](https://clawhub.ai/user/timyljob2011-sudo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with generated skill files, scripts, JSON configuration, and zip packaging output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local files and zip archives when its helper scripts are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
