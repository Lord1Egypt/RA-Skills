## Description: <br>
Launch automated multi-skill pipeline that chains skills into a loop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fortunto2](https://clawhub.ai/user/fortunto2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to coordinate research or development workflows that chain multiple skills after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can coordinate multiple downstream skills and continue work through pipeline state. <br>
Mitigation: Review the confirmation prompt before starting and inspect or delete the documented .solo pipeline state file if a pipeline resumes unexpectedly. <br>
Risk: Optional launcher scripts are external to this skill and depend on a separately installed Claude Code plugin. <br>
Mitigation: Use direct skill invocation as the primary path and run launcher scripts only after separately trusting the plugin that provides them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fortunto2/solo-pipeline) <br>
- [Publisher profile](https://clawhub.ai/user/fortunto2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline command examples and direct skill invocation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before starting a pipeline; optional launcher scripts depend on a separately trusted Claude Code plugin.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
