## Description: <br>
Generates high-fidelity 1080p videos with synced audio using Google Veo 3.1. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kghamilton89](https://clawhub.ai/user/kghamilton89) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creative users use this skill to generate short cinematic video clips from text prompts, with the agent installing Node dependencies, invoking the generator, and returning the generated MP4 filename. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video prompts are sent to Google through the Gemini API and may disclose sensitive private information if included by the user. <br>
Mitigation: Avoid sensitive private information in prompts and use an API key with appropriate quota or billing limits. <br>
Risk: Passing user prompt text through shell interpolation could enable shell injection. <br>
Mitigation: Invoke generate.js with an argument array or execFile-style call so the prompt is passed as a discrete argument. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kghamilton89/veo-video-generator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kghamilton89) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Text status messages and an MP4 video file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm, and GEMINI_API_KEY; default generation is 1080p, 9:16 video with audio.] <br>

## Skill Version(s): <br>
1.2.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
