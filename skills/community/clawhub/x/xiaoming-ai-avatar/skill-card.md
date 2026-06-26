## Description: <br>
Generates personalized AI avatars and mobile wallpapers across multiple visual styles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prompt a CLI-based image workflow for avatars, mobile wallpapers, batch generation, and style selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt files or image-generation inputs may contain sensitive personal data, secrets, or private image details. <br>
Mitigation: Review prompts before use and avoid including secrets, private images, or sensitive personal data. <br>
Risk: The artifact metadata reports version 1.0.0 while the server release evidence reports version 1.2.0. <br>
Mitigation: Use the server release version for this card and confirm the package metadata before operational rollout. <br>
Risk: The artifact lists curl as required without explaining the expected network behavior. <br>
Mitigation: Confirm the CLI's network calls and data handling with the publisher before production use. <br>
Risk: The artifact describes paid tiers and daily limits that may affect commercial workflows. <br>
Mitigation: Confirm current pricing, limits, watermark behavior, and subscription terms before relying on generated assets. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kaising-openclaw1/xiaoming-ai-avatar) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Artifact documentation describes 512x512 PNG avatar output and 1080x1920 PNG wallpaper output.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence; artifact _meta.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
