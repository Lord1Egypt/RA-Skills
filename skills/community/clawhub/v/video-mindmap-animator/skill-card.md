## Description: <br>
Guides an agent through converting long-form Chinese articles or notes into 9:16 science-explainer videos with mind-map animation, long-form narration, BGM, and multiple duration variants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[golikegod](https://clawhub.ai/user/golikegod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and developers use this skill to turn public-account articles, notes, or long-form knowledge content into structured vertical explainer videos. It provides planning guidance, narration style rules, ffmpeg workflows, and reusable Python templates for rendering frames and mixing audio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included Python templates require local ffmpeg, font, and project paths and can create many frame, audio, and video files. <br>
Mitigation: Review and edit paths before use, run the templates only inside a chosen project folder, and confirm there is enough storage for generated media. <br>
Risk: The workflow may invoke external tools such as ffmpeg, edge_tts, and mmx music. <br>
Mitigation: Install and review those tools separately, run commands in a controlled environment, and avoid adding credentials because the skill does not require them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/golikegod/video-mindmap-animator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs reusable workflow instructions and project-local templates; generated media depends on user-edited paths and available external tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
