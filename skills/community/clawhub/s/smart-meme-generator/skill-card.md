## Description: <br>
Generates context-aware meme images by selecting suitable templates and helping craft concise captions for a topic, situation, reaction image, joke, or social media post. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olisim02](https://clawhub.ai/user/olisim02) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, creators, and developers use this skill to turn a topic or situation into a shareable meme image URL. The agent selects an appropriate meme template, writes short captions, and can return either human-readable output or JSON for automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meme captions and topics may be sent to Imgflip, a third-party service. <br>
Mitigation: Avoid sensitive or private text in prompts and disclose that generated captions may leave the local environment. <br>
Risk: The skill uses a shared hardcoded Imgflip account by default, creating privacy and reliability tradeoffs. <br>
Mitigation: Configure a personal Imgflip account with IMGFLIP_USER and IMGFLIP_PASS before routine use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/olisim02/smart-meme-generator) <br>
- [Imgflip Signup](https://imgflip.com/signup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON] <br>
**Output Format:** [Markdown or JSON containing selected template details, captions, and generated meme image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Imgflip to produce a hosted image URL; no local image file is produced by default.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
