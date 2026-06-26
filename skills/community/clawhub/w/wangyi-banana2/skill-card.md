## Description: <br>
Generate images and videos via WangYi Banana API (nano-banana, SORA2). Supports text-to-image, image-to-image, text-to-video, image-to-video, and character creation for short video production. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxq790909-maker](https://clawhub.ai/user/zxq790909-maker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to generate and edit images and videos through the WangYi/T8 API for short video production, including character creation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be exposed if users paste paid credentials into chat. <br>
Mitigation: Use an environment variable or local OpenClaw config file for WANGYI_API_KEY, and rotate any key already shared in a conversation. <br>
Risk: Prompts and selected media are sent to an external WangYi/T8 service. <br>
Mitigation: Avoid submitting sensitive personal, business, or private media unless that external sharing is acceptable for the use case. <br>
Risk: Generation can consume paid API credits and video tasks may run for several minutes. <br>
Mitigation: Confirm task, model, and parameters before generation, notify users before long video jobs, and report cost when the API returns it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zxq790909-maker/wangyi-banana2) <br>
- [WangYi/T8 API service](https://ai.t8star.cn) <br>
- [API Key Setup Guide](references/api-key-setup.md) <br>
- [Image Generation Guide](references/image-generation.md) <br>
- [Video Generation Guide](references/video-generation.md) <br>
- [Output Delivery Guide](references/output-delivery.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance, shell commands, JSON status or error text, and generated image, video, or JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media is written under /tmp/openclaw/wangyi-output and should be delivered with the message tool; costs may be reported when returned by the API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
