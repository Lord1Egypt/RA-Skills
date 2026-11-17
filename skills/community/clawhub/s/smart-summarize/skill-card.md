## Description:

Summarize URLs or files with the summarize CLI for web pages, PDFs, images, audio, and YouTube, and provide guidance for using SkillBoss models across chat, image, video, audio, search, document, email, and SMS tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to summarize URLs or files and to choose SkillBoss model calls for multimodal generation, search, document processing, email, and SMS workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, file URLs, audio data, document URLs, search queries, and generated content may be sent to the SkillBoss or HeyBoss API.

Mitigation: Use the skill only when an external model gateway is intended, and avoid sending sensitive data unless the use case and data handling requirements allow it.

Risk: Email and SMS examples can initiate outbound communications.

Mitigation: Require explicit user confirmation before running email or SMS actions, including recipient addresses, phone numbers, subjects, and message bodies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quincygunter/skills/smart-summarize)
- [SkillBoss](https://www.skillboss.co)
- [HeyBoss API base](https://api.heybossai.com/v1)
- [Chat Models](artifact/chat-models.md)
- [Image Models](artifact/image-models.md)
- [Video Models](artifact/video-models.md)
- [Audio Models](artifact/audio-models.md)
- [Search & Scraping Models](artifact/search-models.md)
- [Tool Models](artifact/tools-models.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, API request examples, configuration notes, and model guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for live SkillBoss or HeyBoss API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
