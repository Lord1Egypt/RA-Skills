## Description:

Supports Chinese–Tibetan translation, Tibetan-language questions and writing, document translation, and image OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youteacher](https://clawhub.ai/user/youteacher)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users translate Chinese and Tibetan text, ask or write in Tibetan, translate DOCX and PDF content, and recognize or translate text in images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text, images, DOCX files, and PDFs submitted for processing leave the user's environment for the AI Skills service and its model/OCR backend.

Mitigation: Upload only what the user authorizes; avoid highly sensitive material unless the organization accepts the service's processing and retention posture.

Risk: An exposed API key can allow unauthorized service use.

Mitigation: Keep the API key in the configured environment variable; never paste it into chat or include it in logs or shared files.

Risk: Incomplete extraction or an invalid service response can leave a translation or OCR task unfinished.

Mitigation: Check each actual response and report missing, failed, or unprocessed content instead of presenting it as complete.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/youteacher/skills/tibetan-ai)
- [AI Skills platform](https://ai-skills.open-idea.net)
- [API key configuration](https://ai-skills.open-idea.net/skill-docs/tibetan-ai/API-KEY.md)
- [Interface routing](https://ai-skills.open-idea.net/skill-docs/tibetan-ai/INTERFACE-ROUTING.md)
- [Document translation](https://ai-skills.open-idea.net/skill-docs/tibetan-ai/DOCUMENT-TRANSLATION.md)
- [Image OCR translation](https://ai-skills.open-idea.net/skill-docs/tibetan-ai/IMAGE-OCR.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Plain text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Document translation returns extracted translated text, not a layout-preserving DOCX or PDF.]

## Skill Version(s):

1.9.0 (source: ClawHub release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
