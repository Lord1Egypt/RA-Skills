## Description: <br>
Translate text in images, extract text via OCR, and remove text using TranslateImage AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cottom](https://clawhub.ai/user/cottom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to process images through the TranslateImage API: translate visible text while preserving layout, extract OCR text, remove text, or extract and translate text in one call. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chosen images are uploaded to the third-party TranslateImage API and may contain sensitive or regulated content. <br>
Mitigation: Avoid sensitive screenshots, documents, IDs, secrets, personal photos, or regulated data unless the provider's privacy and retention practices are acceptable. <br>
Risk: Text removal can alter watermarks, attribution, subtitles, or evidentiary annotations. <br>
Mitigation: Use text removal only for images the user owns or has permission to modify, and preserve originals when provenance or auditability matters. <br>
Risk: The skill requires a TranslateImage API key for authenticated API calls. <br>
Mitigation: Store the key in TRANSLATEIMAGE_API_KEY and avoid exposing it in prompts, command history, shared logs, or generated output. <br>


## Reference(s): <br>
- [TranslateImage](https://translateimage.io) <br>
- [TranslateImage Dashboard](https://translateimage.io/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash commands, JSON examples, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TRANSLATEIMAGE_API_KEY for TranslateImage API calls; image outputs may be returned as base64 data URLs or saved files.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
