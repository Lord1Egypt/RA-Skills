## Description: <br>
Generates a daily Zen Buddhist koan lecture with historical background, interpretation, modern insight, optional Chinese ink wash image prompting, and TTS narration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yumyumtum](https://clawhub.ai/user/yumyumtum) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to produce daily Zen koan content, including bilingual lecture text, image-generation prompts or commands, and spoken narration for contemplative or spiritual-content workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The image workflow can hand off to a separate external image-generation command and service whose data flow is not fully scoped in the skill documentation. <br>
Mitigation: Review the generated image command and the referenced image-generation script before execution, and avoid sending sensitive personal reflections or private context into image prompts. <br>
Risk: Personalized koan lectures, web lookup, image generation, and TTS can expose user-provided text to external services. <br>
Mitigation: Use explicit /koan commands for routine use and avoid including personal, confidential, or sensitive information in personalized prompts or narration text. <br>


## Reference(s): <br>
- [Zen Koan Daily ClawHub Page](https://clawhub.ai/yumyumtum/zen-koan-daily) <br>
- [README](README.md) <br>
- [Koan Reference Examples](references/koans.json) <br>
- [Progress Tracking Reference](references/progress.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown lecture text with optional JSON koan metadata, shell commands, PNG image output paths, and MP3 audio output paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external image and TTS services when the user runs the generated commands; outputs can be persisted under the user's OpenClaw media directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
