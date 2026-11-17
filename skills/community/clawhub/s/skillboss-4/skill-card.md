## Description:

Skillboss is a Swiss-knife for AI agents, offering 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS with smart routing for cost saving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Skillboss to route model requests across chat, image, video, audio, search, scraping, document processing, email, SMS, embeddings, and presentation services through a Node-based command interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, files, audio, and generated content may be routed to external model or processing providers.

Mitigation: Review data sensitivity before use, avoid private or regulated inputs unless approved, and document which provider routes are acceptable.

Risk: Email, SMS, OTP, and batch messaging actions can contact external recipients.

Mitigation: Require explicit user approval for recipient lists, message content, and any email, SMS, OTP, or batch messaging invocation.

Risk: The skill depends on SKILLBOSS_API_KEY for remote API access.

Mitigation: Store the key in an approved secret store or environment variable, restrict access to trusted agents, and avoid exposing the key in logs or shared transcripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marjoriebroad/skills/skillboss-4)
- [SkillBoss Website](https://www.skillboss.co)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Console text, JSON, generated media URLs, Markdown, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and SKILLBOSS_API_KEY; media results are returned as URLs for optional download.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
