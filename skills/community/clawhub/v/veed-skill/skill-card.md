## Description: <br>
Generates lip-synced talking head MP4 videos from a photo plus either audio or a text script using VEED Fabric 1.0 via fal.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mattdotroberts](https://clawhub.ai/user/mattdotroberts) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create short talking-head videos for product demos, LinkedIn content, investor updates, and similar communication from a supplied headshot plus voice audio or script text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal images, audio, scripts, and generated videos can be sent to fal.ai or VEED infrastructure and may be exposed through public CDN URLs. <br>
Mitigation: Use only media and scripts that are appropriate for third-party processing; avoid confidential, client, biometric face, or voice data unless the workflow adds explicit upload confirmation and output-location controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mattdotroberts/veed-skill) <br>
- [VEED Fabric 1.0 fal.ai model](https://fal.ai/models/veed/fabric-1.0) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline bash commands and saved MP4 video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated videos are downloaded to ./output/ and the hosted fal.ai media URL is reported when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
