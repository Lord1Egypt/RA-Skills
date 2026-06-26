## Description: <br>
Social Publisher formats Markdown content for WeChat, Xiaohongshu, Zhihu, and Douyin, with preview and simulated publishing behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, social media operators, and developers use this skill to convert one Markdown draft into platform-specific text or Markdown previews for Chinese social platforms. Treat real publishing and image upload claims cautiously unless the publisher confirms the implemented integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may assume the skill performs real social publishing or image upload even though the server security evidence characterizes it as a formatter or simulator. <br>
Mitigation: Use preview, dry-run, or simulator workflows until the publisher clarifies which platform integrations are actually implemented. <br>
Risk: The skill asks users to configure social-platform credentials, creating exposure risk if real credentials are provided before integrations and secret handling are clarified. <br>
Mitigation: Do not provide real platform credentials for this version unless the publisher documents the implemented integrations and secret-protection behavior; use test credentials with minimal permissions when validation is necessary. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/utopiabenben/social-publisher) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [Publisher profile](https://clawhub.ai/user/utopiabenben) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell command and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces platform-specific formatted previews and simulated publishing status; real social-platform integrations are not established by the security evidence.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
