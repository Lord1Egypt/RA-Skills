## Description: <br>
Create new skills, modify existing skills, and validate skill quality for the FlagOS skills repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wbavon](https://clawhub.ai/user/wbavon) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to scaffold new agent skills, improve existing skill instructions, validate skill structure, and prepare evaluation cases for the FlagOS skills repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or modified skill instructions can contain incorrect, overly broad, or misleading guidance. <br>
Mitigation: Review proposed edits before accepting them and run the skill validation workflow before release. <br>
Risk: Broad trigger guidance can cause the skill to activate in sensitive or unrelated workflows. <br>
Mitigation: Keep generated trigger descriptions specific to the intended workflow and narrow them during review. <br>
Risk: The skill can scaffold files and suggest shell commands as part of skill creation. <br>
Mitigation: Inspect file diffs and commands before execution, especially in shared or production repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wbavon/skill-creator-flagos) <br>
- [README.md](artifact/README.md) <br>
- [Skill Writing Guide](artifact/references/writing-guide.md) <br>
- [JSON Schemas](artifact/references/schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated files, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify skill files and supporting resources when the agent applies the workflow.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata; artifact metadata: 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
