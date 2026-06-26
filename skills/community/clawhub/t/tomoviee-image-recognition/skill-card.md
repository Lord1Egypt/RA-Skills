## Description: <br>
Auto-generates masks for objects or regions in images through Tomoviee image_recognition operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and image-workflow builders use this skill to call Tomoviee/Wondershare image recognition APIs that create segmentation masks for objects or regions in submitted images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image URLs, prompts, task metadata, and Tomoviee/Wondershare API credentials are sent to the provider. <br>
Mitigation: Use a dedicated API key, avoid private or regulated images unless third-party processing is allowed, and do not paste secrets into shared terminals or logs. <br>
Risk: Bundled reference documents describe broader Tomoviee APIs beyond the image-mask workflow. <br>
Mitigation: Keep use scoped to image-mask generation unless the additional APIs are separately reviewed for the intended workflow. <br>


## Reference(s): <br>
- [Tomoviee Developer Portal](https://www.tomoviee.ai/developers.html) <br>
- [Tomoviee API Documentation](https://www.tomoviee.ai/doc/) <br>
- [Tomoviee Image Generation APIs](references/image_apis.md) <br>
- [Tomoviee Prompt Engineering Guide](references/prompt_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on asynchronous API calls that return task IDs and mask result URLs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
