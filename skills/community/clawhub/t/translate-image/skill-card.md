## Description:

Translate text in images, extract text via OCR, and remove text using TranslateImage AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cottom](https://clawhub.ai/user/cottom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call TranslateImage's REST API for image translation, OCR, text removal, and image-to-text translation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images and extracted text are sent to translateimage.io.

Mitigation: Use the skill only for images that can be shared with that service, and avoid confidential, medical, financial, identity, or private-location content unless explicit consent exists.

Risk: URL-based image downloads could reach local, private-network, metadata-service, or redirected resources.

Mitigation: Allow only known local image files or ordinary public HTTPS image URLs explicitly provided by the user, and block file://, localhost, private-network, metadata-service, and redirected URLs.

Risk: Text removal can alter watermarks, provenance marks, safety labels, or other protected image content.

Mitigation: Use remove-text only on images the user has rights to edit, and avoid removing watermarks, provenance, or safety labels without authorization.

Risk: API keys can grant endpoint-specific capabilities.

Mitigation: Configure only the scopes required for the intended endpoint and keep TRANSLATEIMAGE_API_KEY out of logs and shared outputs.

## Reference(s):

- [TranslateImage](https://translateimage.io)
- [TranslateImage Dashboard](https://translateimage.io/dashboard)
- [ClawHub Translate Image Skill](https://clawhub.ai/cottom/skills/translate-image)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell command examples, JSON response examples, and generated image file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses TRANSLATEIMAGE_API_KEY and curl/python3 to send image files to TranslateImage API endpoints.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
