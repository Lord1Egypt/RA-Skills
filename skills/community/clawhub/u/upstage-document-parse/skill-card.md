## Description:

Parse documents such as PDFs, images, DOCX, PPTX, XLSX, and HWP files into layout-aware Markdown or HTML with tables, figures, headings, and bounding boxes using the Upstage Document Parse API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upstage-deployment](https://clawhub.ai/user/upstage-deployment)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users use this skill to convert selected documents into structured Markdown or HTML while preserving layout elements such as tables, charts, figures, headings, and coordinates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents are sent to Upstage for processing, which can expose confidential, regulated, or highly sensitive content to a remote service.

Mitigation: Use only documents approved for Upstage processing and confirm organizational policies and remote retention behavior before uploading sensitive content.

Risk: Async processing stores results for 30 days and uses temporary download URLs that expire after 15 minutes.

Mitigation: Plan async workflows around approved retention expectations and re-fetch status when a download URL expires.

Risk: The skill requires an Upstage API key for API calls.

Mitigation: Provide the key through the UPSTAGE_API_KEY environment variable and avoid placing credentials in prompts, files, or command history.

## Reference(s):

- [Upstage Document Parsing](https://console.upstage.ai/api/document-digitization/document-parsing)
- [Document Parse - Sync API Detail](references/sync-options.md)
- [Document Parse - Async API Workflow](references/async-workflow.md)
- [ClawHub skill release](https://clawhub.ai/upstage-deployment/skills/upstage-document-parse)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and curl examples, plus parsed Markdown or HTML files generated from user-selected documents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses UPSTAGE_API_KEY, supports sync and async Upstage API workflows, and prints the resolved absolute output path when writing parsed files.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
