## Description: <br>
AI video generator for text-to-video, image-to-video, and reference-to-video generation through the Veevid API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meigesir](https://clawhub.ai/user/meigesir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to generate videos from prompts or images, compare available Veevid video models, check credit balance, and get quoted costs before generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local Veevid API key and sends selected prompts or images to Veevid. <br>
Mitigation: Protect ~/.config/veevid/api_key, rotate the key if exposed, and only install the skill if sending selected content to Veevid is acceptable. <br>
Risk: Video generation can spend Veevid credits. <br>
Mitigation: Use the quote step to show the exact cost and current balance, then wait for user confirmation before generating. <br>
Risk: In Discord or group chats, the skill may inspect recent messages to find image attachments. <br>
Mitigation: Filter attachments by the requesting sender and quote the selected image back for confirmation before upload or generation. <br>


## Reference(s): <br>
- [Veevid API Reference](references/api-reference.md) <br>
- [Veevid AI](https://veevid.ai) <br>
- [API Key Management](https://veevid.ai/settings/api-keys) <br>
- [Pricing and Credits](https://veevid.ai/pricing) <br>
- [ClawHub Skill Page](https://clawhub.ai/meigesir/veevid) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands, API request examples, JSON response summaries, and generated video URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Veevid API key file at ~/.config/veevid/api_key and requires user confirmation before spending credits.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
