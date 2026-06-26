## Description: <br>
Generates 9:16 Tibetan cinematic videos with Google Veo from a user image and exactly three Chinese theme words, saving the resulting MP4 under ~/.openclaw/workspace/tibetanProc/. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j3ffyang](https://clawhub.ai/user/j3ffyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to turn a Tibetan source image and three Chinese theme words into a short vertical cinematic video while preserving the skill's cultural style guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The selected image is uploaded to the configured Google Veo service for video generation. <br>
Mitigation: Use only images appropriate for remote processing and confirm the endpoint's retention and privacy handling before use. <br>
Risk: Generated MP4 files are written locally under ~/.openclaw/workspace/tibetanProc/. <br>
Mitigation: Review the generated file location, manage cleanup as needed, and avoid sensitive, confidential, or copyrighted images unless their use is permitted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/j3ffyang/tibetan-cinematic-video) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Files] <br>
**Output Format:** [Google Veo prompt text and a generated MP4 video file saved as ~/.openclaw/workspace/tibetanProc/yymmddHHMM_{title}.mp4] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires one input image and exactly three comma-separated Chinese theme words; the skill is designed for a single portrait clip per call.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
