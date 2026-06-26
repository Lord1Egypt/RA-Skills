## Description: <br>
Generates images from text prompts using user-configured MiniMax, OpenAI DALL-E, or Stability AI API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoliang1319-cloud](https://clawhub.ai/user/xiaoliang1319-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill in OpenClaw to generate images from natural-language prompts through their configured image-provider API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may be sent to external image-generation providers and could expose confidential or sensitive details. <br>
Mitigation: Avoid secrets or confidential information in prompts and configure only the provider API keys intended for use. <br>
Risk: Provider API usage can create billing or quota exposure. <br>
Mitigation: Monitor provider usage and billing for the configured API keys. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoliang1319-cloud/xiaoxia-image-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions, Shell commands, API calls] <br>
**Output Format:** [Markdown with inline bash code blocks and prompt text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes image generation to MiniMax, OpenAI DALL-E, or Stability AI based on configured API keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
