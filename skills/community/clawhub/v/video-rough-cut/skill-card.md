## Description: <br>
Video Rough Cut helps agents run a local B-Roll Studio rough-cut pipeline to clean a single talking-head or voiceover video by removing pauses, breaths, and head/tail clutter and optionally applying brightness correction, stabilization, centering, and light beauty. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tiepige8](https://clawhub.ai/user/tiepige8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill through an agent to create a cleaned first-pass rough cut from one local talking-head or voiceover video before manual review or final editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The selected video and its audio or transcript content may be sent to the configured rough-cut API endpoint. <br>
Mitigation: Keep the base URL on localhost unless the user deliberately trusts another endpoint. <br>
Risk: The pipeline writes a rough-cut output file back to disk and may not provide final editorial polish. <br>
Mitigation: Review the generated draft and cut-decision data before using it as a final edit. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tiepige8/video-rough-cut) <br>
- [Rough Cut API](api.md) <br>
- [Current Rough-Cut Pipeline](pipeline.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, a downloaded video file, and optional JSON cut-decision data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one cleaned draft video; optional cut-decision review data may be inspected after completion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
