## Description: <br>
Analyzes video shot cuts and camera movement, then generates English AI video prompts and detailed motion data for each detected shot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[winme99998](https://clawhub.ai/user/winme99998) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, video editors, and agents use this skill to analyze uploaded video files, identify shot boundaries and camera movement, and turn each shot into an English AI video generation prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analyzed videos and generated thumbnails may contain private or unauthorized visual content. <br>
Mitigation: Use the skill only with videos the user is authorized to analyze, and review generated JSON and thumbnails before sharing or storing them. <br>
Risk: Shot boundaries, movement classifications, and prompt text are heuristic and may be inaccurate. <br>
Mitigation: Treat the analysis as a draft and have a human review the reported cuts, motion labels, and prompts before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/winme99998/toolfolio) <br>
- [Publisher profile](https://clawhub.ai/user/winme99998) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands] <br>
**Output Format:** [Terminal report plus output/<video>/analysis.json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes per-shot timestamps, camera movement labels, confidence values, English AI prompts, base64 JPEG thumbnail data, and motion metrics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
