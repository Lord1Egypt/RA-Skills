## Description:

Analyzes skin tone and facial attributes from a selfie using YouCam (Perfect Corp) AI, returning color references, feature shapes, and approximate facial proportions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youcam-api](https://clawhub.ai/user/youcam-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users can request a color reference from a selfie, facial feature labels, or approximate facial proportions. The skill returns a readable analysis and explains that results are for reference only.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The chosen selfie is sent to YouCam/Perfect Corp, and provider-side data handling was not verified.

Mitigation: Review the provider's privacy and retention terms and submit only an image you are comfortable sharing.

Risk: Each selected analysis can consume paid credits.

Mitigation: Check and state the current cost for each analysis, then run only the analyses the user chooses.

Risk: The skill requires a YouCam API key, which could be exposed if handled carelessly.

Mitigation: Keep the key private and provide it through the documented environment variable or local credentials file.

Risk: Installed dependency versions were not verified.

Mitigation: Use current patched dependencies in a local virtual environment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/youcam-api/skills/youcam-facial-consultant)
- [Facial Consultant interpretation guide](references/guide.md)
- [YouCam skin tone analysis API reference](https://docs.perfectcorp.com/reference/ai_skin_tone_analysis.md)
- [YouCam facial analyzer API reference](https://docs.perfectcorp.com/reference/ai_face_analyzer.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Readable Markdown report with color names, feature labels, and approximate proportion summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports only returned color values; omits missing attributes; labels proportions as approximate; includes a reference-only disclaimer.]

## Skill Version(s):

1.1.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
