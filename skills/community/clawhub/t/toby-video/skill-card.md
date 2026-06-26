## Description: <br>
Generate video using SkillBoss API Hub with video generation auto-routed via /v1/pilot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate MP4 video clips from text prompts, with optional image-to-video inputs, duration, aspect ratio, and model-hint controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and input images are sent to SkillBoss API Hub. <br>
Mitigation: Do not use sensitive, private, or confidential prompts or media unless that third-party processing is acceptable. <br>
Risk: Generated videos are saved to a user-provided local path. <br>
Mitigation: Choose output paths carefully to avoid overwriting important local files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/toby-video) <br>
- [SkillBoss API Hub API base](https://api.skillbossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated MP4 file when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and SKILLBOSS_API_KEY; prints a MEDIA line for supported chat providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
