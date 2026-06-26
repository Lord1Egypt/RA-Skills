## Description: <br>
Generates images with MiniMax image-01 and related models, including text-to-image and basic image editing, when a user configures MINIMAX_API_KEY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoliang1319-cloud](https://clawhub.ai/user/xiaoliang1319-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to guide an agent through MiniMax image generation workflows, including prompt setup, aspect ratio selection, response format selection, and API-key configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts or source images sent to MiniMax may contain confidential or sensitive content. <br>
Mitigation: Avoid confidential prompt content and review provider handling terms before using the API. <br>
Risk: MiniMax API usage requires an API key and may consume quota or incur billing. <br>
Mitigation: Store the key in an environment variable, monitor provider quota and billing, and rotate the key if exposure is suspected. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, API calls, configuration] <br>
**Output Format:** [Markdown guidance with JavaScript API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY; API responses can include base64 image data when used with MiniMax.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
