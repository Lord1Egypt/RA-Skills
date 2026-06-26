## Description: <br>
Create videos using ShortVideo API, including product-to-video, image-to-ad-video, and replicate-video workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheCur](https://clawhub.ai/user/TheCur) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to generate marketing videos from product images, create advertisement videos from image sets, replicate video styles with new media, and poll for generated video status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected media, URLs, and prompts are sent to the ShortVideo service. <br>
Mitigation: Only provide files, URLs, and prompts that are approved for the service, especially when media is non-public or regulated. <br>
Risk: The integration uses a ShortVideo API key and can consume account credits. <br>
Mitigation: Keep SHORTVIDEO_API_KEY private, verify SHORTVIDEO_BASE_URL points to the intended ShortVideo API host, and install only when the provider and publisher are trusted. <br>


## Reference(s): <br>
- [Product to Video](references/product-to-video.md) <br>
- [Image to Ad Video v2](references/image-to-ad-video-v2.md) <br>
- [Replicate Video](references/replicate-video.md) <br>
- [ShortVideo](https://shortvideo.ai) <br>
- [Shortvideo ClawHub Release](https://clawhub.ai/TheCur/shortvideo-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces ShortVideo task requests, polling guidance, and returned task or video status data through command-line scripts.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
