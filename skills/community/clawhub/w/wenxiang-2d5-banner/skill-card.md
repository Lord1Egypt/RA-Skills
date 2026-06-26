## Description: <br>
Generates 2.5D isometric banner illustrations for an agent workflow and saves the resulting image output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icesumer-lgtm](https://clawhub.ai/user/icesumer-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent prepare and run image-generation commands for 2.5D banner artwork, including prompt iteration and saved image outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The published package appears to include unrelated personal workspace files, nested skills, hooks, logs, memory, project data, and possible secrets. <br>
Mitigation: Republish only the skill definition, required image-generation script, and non-secret metadata; rotate any exposed API keys, Feishu secrets, or tenant tokens before use. <br>
Risk: The server release identity describes a Tongyi Wanxiang 2.5D banner skill, while the packaged root skill and script describe a Gemini/Nano Banana image generator. <br>
Mitigation: Verify the intended image provider and align the skill name, documentation, dependencies, and script behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/icesumer-lgtm/wenxiang-2d5-banner) <br>
- [Packaged skill definition](artifact/SKILL.md) <br>
- [Packaged image generation script](artifact/scripts/generate_image.py) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated PNG image files when the script is executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an image-generation API key and local command execution; the published artifact should be minimized before deployment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
