## Description: <br>
Translates or dubs user-provided video files or video URLs through an online service and returns a preview URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[papawaigo](https://clawhub.ai/user/papawaigo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit a video file or public video URL for translation or dubbing, optionally request subtitles, poll completion, and return the translated video's preview URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The selected video file or URL is sent to audiox-api-global.luoji.cn for processing. <br>
Mitigation: Use this skill only for media that may be shared with the provider, and avoid confidential, regulated, or copyrighted content unless the provider's privacy and retention practices are acceptable. <br>
Risk: The skill requires a service API key for authenticated requests. <br>
Mitigation: Provide the key through VIDEO_TRANSLATE_SERVICE_API_KEY, avoid exposing it in prompts or logs, and rotate it if disclosure is suspected. <br>


## Reference(s): <br>
- [API Contract](references/api-contract.md) <br>
- [Video translation service](https://audiox-api-global.luoji.cn) <br>
- [Publisher profile](https://clawhub.ai/user/papawaigo) <br>
- [Skill page](https://clawhub.ai/papawaigo/video-translator) <br>
- [Service support and privacy information](https://luoji.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Text containing job status, errors, or a preview URL; helper usage may include shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns preview_url on successful translation; requires VIDEO_TRANSLATE_SERVICE_API_KEY and sends selected video input to the external service.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
