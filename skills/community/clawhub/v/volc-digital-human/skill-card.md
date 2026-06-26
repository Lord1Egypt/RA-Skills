## Description: <br>
Generates Volcengine digital-human talking-head videos from a user image and dialogue text by creating an avatar, generating speech, synthesizing video, and returning video and thumbnail files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoxiaole2025](https://clawhub.ai/user/xiaoxiaole2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn a supplied face image and dialogue text into a short digital-human spoken video through Volcengine, with optional gender and voice selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes Volcengine credentials and requires cloud API access. <br>
Mitigation: Remove and rotate the bundled credentials before use, then configure scoped VOLC_AK and VOLC_SK values through environment variables or a private config file. <br>
Risk: Face images, generated speech, and generated video may be sent to Volcengine and public file hosts during processing. <br>
Mitigation: Use only images, scripts, and voice content that are acceptable for third-party processing and public temporary hosting. <br>
Risk: The default latest-image behavior can select an unintended local image in private or shared environments. <br>
Mitigation: Prefer explicit image selection and confirm the chosen file before running the workflow. <br>


## Reference(s): <br>
- [Volcengine digital-human API reference](references/volc_api.md) <br>
- [ClawHub release page](https://clawhub.ai/xiaoxiaole2025/volc-digital-human) <br>


## Skill Output: <br>
**Output Type(s):** [Files, API Calls, Shell commands, Configuration instructions] <br>
**Output Format:** [MP4 video file, JPEG thumbnail, generated media URLs, and JSON-like status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Volcengine AK/SK credentials; uploads image and generated audio to public file hosts; downloads the synthesized Volcengine preview video before delivery.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
