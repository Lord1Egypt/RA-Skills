## Description: <br>
Provides command examples for controlling Sonos speakers and using the SkillBoss API gateway for AI model, search, document, email, and SMS tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AlvisDunlop](https://clawhub.ai/user/AlvisDunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to discover API usage patterns, prepare shell commands, and configure access for Sonos control and SkillBoss model gateway tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide use of a broad external API gateway, including scraping, email, SMS, OTP verification, and paid model calls. <br>
Mitigation: Use a dedicated limited API key, monitor usage and billing, avoid sending sensitive data unless the provider and downstream routing are trusted, and require explicit human approval before email, SMS, batch messaging, scraping, or OTP verification actions. <br>
Risk: The release is presented as Sonos control while the artifact primarily documents broad SkillBoss API gateway behavior. <br>
Mitigation: Review the actual scope before deployment and restrict agent permissions to the intended Sonos or SkillBoss workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AlvisDunlop/sonosclis) <br>
- [SkillBoss](https://www.skillboss.co) <br>
- [SkillBoss API base URL](https://api.heybossai.com/v1) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Search & Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>
- [Video Models](artifact/video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with curl command examples and parameter tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
