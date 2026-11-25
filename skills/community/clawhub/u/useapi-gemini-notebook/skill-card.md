## Description:

Creates Gemini Notebook Audio Overviews, Video Overviews, and slide decks from web pages, YouTube videos, pasted text, or local files through the paid useapi.net API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[useapi](https://clawhub.ai/user/useapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can turn selected web pages, YouTube videos, notes, and local documents into audio podcasts, explainer videos, or slide decks in a connected Google account. Use requires a paid useapi.net account and a Google account connected through that service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected files are sent to the useapi.net service for processing.

Mitigation: Review the selected files before submitting and send only material you are comfortable sharing with useapi.net.

Risk: The skill can generate additional artifact types beyond those listed in its short description.

Mitigation: Check the requested artifact type and options before starting a generation.

Risk: The security scan had incomplete coverage: one referenced helper was unavailable and tool-misuse analysis reached a parser limit.

Mitigation: Review the shipped scripts before use, bearing in mind that the scan does not cover every helper or analysis path.

## Reference(s):

- [Gemini Notebook API documentation](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-gemini-notebook)
- [Supported Notebook artifacts](https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-artifacts)
- [Example code and integrations](https://github.com/useapi/notebooklm-api)

## Skill Output:

**Output Type(s):** [Audio files, Video files, PDF and PowerPoint files]

**Output Format:** [M4A audio, MP4 video, PDF and PPTX slide decks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files are downloaded to the chosen output folder.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
