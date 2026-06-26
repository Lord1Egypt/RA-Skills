## Description: <br>
Translates Claude Code skills into Chinese versions by generating a marked target skill directory and guiding the agent to complete the remaining translation work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouchang1988](https://clawhub.ai/user/zhouchang1988) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to localize existing Claude Code skills into Chinese, including SKILL.md content, README content, comments, prompts, and generated output-language guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The translation script can delete an existing output directory, including a custom output path outside the default skills folder. <br>
Mitigation: Use only reviewed output paths, back up any existing target directory first, and inspect the generated files before enabling the translated skill. <br>
Risk: Generated files can contain unfinished translation markers if the agent does not complete the model-stage translation. <br>
Mitigation: Verify that no [待翻译] markers remain and review the generated SKILL.md, scripts, and README before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouchang1988/skill-to-cn) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance plus generated or modified skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a Chinese target skill directory and leaves marked content for the agent to finish translating.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
