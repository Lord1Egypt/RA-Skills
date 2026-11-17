## Description:

Search session logs and call SkillBoss-hosted models for chat, media generation, transcription, search, scraping, document processing, email, and SMS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to query session logs and invoke SkillBoss API capabilities from agent-generated shell commands. It covers model discovery and calls for chat, image, video, audio, search, scraping, document processing, email, SMS, embeddings, and presentations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad external API gateway behavior is packaged under a session-log name, which can make its scope easy to underestimate.

Mitigation: Review the full model and action list before installation and enable the skill only when broad SkillBoss API access is intended.

Risk: The skill uses SKILLBOSS_API_KEY for external model calls and can send data to third-party providers, email, SMS, scraping, and document-processing services.

Mitigation: Limit the key's permissions where possible, keep it out of prompts and logs, and avoid sending secrets, private logs, or personal data unless data handling and recipients have been checked.

Risk: Email, SMS, scraping, and document actions can affect external users or third-party systems.

Mitigation: Require human review for recipient lists, message content, scraped targets, and documents before running those actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/session-logss)
- [SkillBoss website](https://www.skillboss.co)
- [SkillBoss API base URL](https://api.heybossai.com/v1)
- [Skill definition](artifact/SKILL.md)
- [Audio Models](artifact/audio-models.md)
- [Chat Models](artifact/chat-models.md)
- [Image Models](artifact/image-models.md)
- [Search & Scraping Models](artifact/search-models.md)
- [Tool Models](artifact/tools-models.md)
- [Video Models](artifact/video-models.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with Bash curl commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; outputs may include generated media URLs, parsed text, search results, sent email or SMS actions, and saved files depending on the command.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
