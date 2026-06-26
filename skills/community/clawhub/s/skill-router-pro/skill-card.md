## Description: <br>
Skill Router Pro helps an agent find matching local skills or search ClawHub before building a new skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kennyzir](https://clawhub.ai/user/kennyzir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to check installed local skills, search ClawHub for missing matches, and avoid creating duplicate skills when an existing option is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may expose local skill names, descriptions, and paths to future agent sessions by updating the local skill index. <br>
Mitigation: Review ~/.openclaw/skills/INDEX.md after index updates and remove entries that should not be reused or exposed. <br>
Risk: The skill can recommend ClawHub install commands for discovered skills. <br>
Mitigation: Review the matched skill page and install command before installing or using a recommended third-party skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kennyzir/skill-router-pro) <br>
- [Publisher Profile](https://clawhub.ai/user/kennyzir) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and skill recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update the local skill index and may suggest ClawHub install commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
