## Description: <br>
Analyzes videos to detect requested motion sequences, such as martial arts moves, dance moves, or posture changes, and reports the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hena1985](https://clawhub.ai/user/hena1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, video analysts, and automation agents use this skill to inspect user-provided videos, extract frames, identify requested motion order or repetition, and summarize whether the requested action criteria were met. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download or analyze videos from URLs or local files, which may include content the user is not authorized to process. <br>
Mitigation: Use it only with videos the user is allowed to download or analyze. <br>
Risk: The skill sends detection results through Feishu, which could expose sensitive video details or reach the wrong recipient. <br>
Mitigation: Verify the Feishu recipient and message contents before sending, and avoid including sensitive video details unless necessary. <br>
Risk: Motion detection can be unreliable when lighting, occlusion, sampling rate, or limited frame review affects visual analysis. <br>
Mitigation: Review enough frames across the full video, use an appropriate extraction rate for the action speed, and state uncertainty when visual evidence is limited. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with bash and JSON code blocks plus a structured detection summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include video metadata, detection conditions, timestamps, pass/fail conclusions, and Feishu notification content.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
