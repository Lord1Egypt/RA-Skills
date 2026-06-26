## Description: <br>
Spark Image lets agents generate one to four PNG images from text prompts with optional style guidance through a paid image-generation service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanweiphone](https://clawhub.ai/user/yuanweiphone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create AI-generated images from natural-language prompts, optional style descriptions, and supported 2K-or-larger image sizes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts are sent to image.open-idea.net. <br>
Mitigation: Do not submit sensitive, confidential, or regulated content in prompts. <br>
Risk: The skill requires IMAGE_GATEWAY_API_KEY, a sensitive credential. <br>
Mitigation: Store the key in the environment only and keep it out of chat logs, screenshots, shell history, and version control. <br>
Risk: Image generation is paid and can deduct balance. <br>
Mitigation: Confirm the estimated cost before generation and show the actual charged amount and remaining balance after a successful request. <br>
Risk: Successful responses can include long base64 image payloads. <br>
Mitigation: Render images or provide download links instead of exposing raw base64 or full internal JSON to users. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yuanweiphone/spark-image) <br>
- [Spark Image Service Homepage](https://image.open-idea.net) <br>
- [API Key Configuration](references/API-KEY.md) <br>
- [Behavior Rules](references/BEHAVIOR-RULES.md) <br>
- [HTTP Request Reference](references/HTTP-REQUESTS.md) <br>
- [Image Generation Details](references/IMAGE-GENERATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [Images, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown with rendered PNG images or download links and a billing line] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return one to four base64-encoded PNG images rendered for the user; raw base64 and internal JSON should not be exposed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
