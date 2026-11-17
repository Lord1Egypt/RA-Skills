## Description:

WiseDiag-Report interprets medical report images or PDFs provided as local files or image URLs using WiseDiag OCR and analysis, then highlights detected values, abnormal indicators, and health advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wisediag](https://clawhub.ai/user/wisediag)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit medical report images or PDFs to WiseDiag for OCR-based interpretation, abnormal indicator detection, and generated explanatory guidance. It is intended as reference material only and not as a substitute for professional medical diagnosis or treatment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical reports and image URLs are sent to WiseDiag cloud services for processing.

Mitigation: Use the skill only when the user trusts WiseDiag with the report contents and understands that the output is reference guidance, not medical diagnosis.

Risk: The API key is required for requests and could be exposed if handled casually in shell history or shared environments.

Mitigation: Use a temporary environment variable or a dedicated secret manager for WISEDIAG_API_KEY, and avoid printing or committing the key.

Risk: Custom output directories and filenames affect where Markdown results are written locally.

Mitigation: Choose a trusted output directory and avoid custom output names containing path separators or '..' until filename handling is fixed.

Risk: Private or signed image URLs can disclose access to sensitive reports when submitted for remote processing.

Mitigation: Prefer local file upload when appropriate and avoid private or signed URLs unless the user has explicitly accepted that exposure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wisediag/skills/wisediag-report)
- [WiseDiag API key console](https://console.wisediag.com/apiKeyManage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report saved to a local .md file with streamed terminal text during processing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WISEDIAG_API_KEY; accepts up to 5 local image/PDF files or image URLs per request; supports optional question, output directory, and output filename.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
