## Description: <br>
视频基础质量审核技能，对视频进行批量或单条的基础问题检测，包括画面质量、构图、音频、黑边、分辨率等，输出审核报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sgw2285265753-design](https://clawhub.ai/user/sgw2285265753-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operations teams, video editors, and reviewing agents use this skill for first-pass short-video checks before publication. It helps inspect technical quality, sampled frames, transcribed audio, prohibited words, and timestamped issues that need human review or editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may process extracted video frames and audio transcription from uploaded or local videos. <br>
Mitigation: Use it only on videos approved for that processing path, and avoid confidential footage unless the OpenClaw image analysis and transcription tools are acceptable for the data. <br>
Risk: Automated visual and transcript findings can be incomplete or false positive. <br>
Mitigation: Treat the report as a first-pass review and keep a human reviewer responsible for final publication and editing decisions. <br>
Risk: The short description does not fully disclose content-safety screening and possible speech transcription. <br>
Mitigation: Present the card description and use case with explicit mention of frame review, prohibited word checks, and transcription-sensitive media handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sgw2285265753-design/video-review) <br>
- [Publisher profile](https://clawhub.ai/user/sgw2285265753-design) <br>
- [Prohibited word reference](refs/banned_words.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown-style audit report with inline shell commands and optional JSON jump-frame details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include pass/fail status, issue counts, timestamps, severity labels, and editing recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
