## Description: <br>
Generate images via Google Cloud Vertex AI generateContent using Application Default Credentials (ADC). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neogeosnk](https://clawhub.ai/user/neogeosnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation builders use this skill to generate image files through Google Cloud Vertex AI with ADC or user-token authentication while controlling project, region, and model settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The URL fallback can forward a Google OAuth token to an untrusted URL if a response URI is selected. <br>
Mitigation: Fix or remove the fallback so OAuth tokens are only sent to trusted Google Vertex AI endpoints, and review the skill before installation. <br>
Risk: The script appears broken as shipped because the request URL is undefined. <br>
Mitigation: Confirm request URL construction and run a controlled test before relying on the skill. <br>
Risk: Prompt data and API responses may briefly reside in local temporary files. <br>
Mitigation: Avoid sensitive prompts unless local temporary storage handling is acceptable, and clear debug artifacts according to environment policy. <br>


## Reference(s): <br>
- [Google Cloud Vertex AI](https://cloud.google.com/vertex-ai) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Configuration instructions] <br>
**Output Format:** [Image file plus JSON status, with Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Google Cloud SDK, curl, Google Cloud project configuration, and local prompt/output paths.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
