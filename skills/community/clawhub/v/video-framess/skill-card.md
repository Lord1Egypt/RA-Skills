## Description:

Documents video frame or clip extraction and SkillBoss API access for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martinpollitt](https://clawhub.ai/user/martinpollitt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover and call SkillBoss/HeyBoss models for multimodal generation, transcription, search, document processing, email, and SMS workflows. The server security evidence flags it as a broad remote AI/API integration, so users should confirm intended data sharing before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is labeled as a video-frame tool but documents broad remote AI/API access.

Mitigation: Review the full documented behavior before installation and deploy it only when broad SkillBoss/HeyBoss API access is intended.

Risk: Prompts, files or file URLs, audio, search queries, email addresses, and phone numbers may be sent to heybossai.com-backed services.

Mitigation: Avoid sending confidential or regulated data unless the user's policy and provider terms allow it.

Risk: The skill documents email and SMS actions.

Mitigation: Require explicit user confirmation before any email, SMS, OTP, or notification request is executed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/martinpollitt/skills/video-framess)
- [SkillBoss](https://www.skillboss.co)
- [HeyBoss API Base URL](https://api.heybossai.com/v1)
- [Video Models](video-models.md)
- [Chat Models](chat-models.md)
- [Image Models](image-models.md)
- [Audio Models](audio-models.md)
- [Search and Scraping Models](search-models.md)
- [Tool Models](tools-models.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Code]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for documented API calls.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
