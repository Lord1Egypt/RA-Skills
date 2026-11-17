## Description:

Captures learnings, errors, and corrections to enable continuous improvement, and provides access to 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to route agent tasks through SkillBoss for chat, media generation, transcription, search, document processing, email, SMS, embeddings, and presentation generation. It is also positioned as a way to capture learnings, errors, and corrections for continuous improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send prompts, files, emails, and SMS through a third-party SkillBoss API key.

Mitigation: Use it only when that API access is intended, and require separate controls for confidential data, private documents, internal URLs, recipients, approvals, billing, and retention.

Risk: The artifact includes run.mjs examples that depend on a local executable not defined by the artifact.

Mitigation: Do not run those examples unless the executable is trusted and understood; prefer the explicit curl examples when reviewing behavior.

Risk: Smart routing can auto-select models and providers for a task.

Mitigation: Review task type, inputs, provider choice, and expected cost or data handling before allowing unattended use.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/quincygunter/skills/self-improve-agent)
- [SkillBoss API base URL](https://api.heybossai.com/v1)
- [SkillBoss models endpoint](https://api.heybossai.com/v1/models)
- [SkillBoss website](https://www.skillboss.co)
- [Chat Models](artifact/chat-models.md)
- [Image Models](artifact/image-models.md)
- [Audio Models](artifact/audio-models.md)
- [Search & Scraping Models](artifact/search-models.md)
- [Tool Models](artifact/tools-models.md)
- [Video Models](artifact/video-models.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; generated API calls may return text, JSON, file URLs, audio, images, video, email, or SMS-related results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
