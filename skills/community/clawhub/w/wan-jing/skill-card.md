## Description: <br>
Wan Jing is a roleplay-style storyboard assistant that designs cinematic shot plans and prompt text, then can use a video-generation model to create storyboard clips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wavegeometry](https://clawhub.ai/user/wavegeometry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and storytellers use this skill to explore visual concepts, build structured shot lists, and draft video-generation prompts for storyboard clips. It is best suited to creative preproduction workflows where a human reviews prompts and media-generation choices before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can activate on broad filming terms and encourage external video generation. <br>
Mitigation: Invoke it explicitly and require user confirmation before any external model call or file creation. <br>
Risk: Storyboard or video prompts may involve identifiable people or private scenes. <br>
Mitigation: Avoid generating media of identifiable people without consent and review prompts for privacy-sensitive content before use. <br>
Risk: The skill describes persistent media storage and non-deletion behavior. <br>
Mitigation: Do not use private or sensitive material, and do not rely on the skill's archive behavior for retention or deletion guarantees. <br>


## Reference(s): <br>
- [Wan Jing on ClawHub](https://clawhub.ai/wavegeometry/skills/wan-jing) <br>
- [Publisher profile](https://clawhub.ai/user/wavegeometry) <br>
- [Wan Jing dialogue examples](artifact/references/wan-jing_dialogue.md) <br>
- [Wan Jing requirements](artifact/references/wan-jing_requirements.md) <br>
- [Wan Jing data](artifact/references/wan-jing_data.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown narrative with structured storyboard prompt blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include video-generation prompts and confirmation guidance before external media generation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
