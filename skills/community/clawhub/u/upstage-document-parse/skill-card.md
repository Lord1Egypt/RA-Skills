## Description: <br>
Parse documents into layout-aware markdown or HTML with tables, figures, headings, and bounding boxes using the Upstage Document Parse API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upstage-deployment](https://clawhub.ai/user/upstage-deployment) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing agents use this skill to convert PDFs, images, and office documents into structured markdown or HTML while preserving layout elements such as tables, figures, headings, equations, and coordinates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents submitted for parsing leave the local machine and are processed by Upstage's remote API. <br>
Mitigation: Use the skill only for documents your organization permits sending to Upstage, and confirm Upstage terms, retention, and handling requirements before processing confidential, regulated, or highly sensitive content. <br>
Risk: The skill requires a sensitive Upstage API key. <br>
Mitigation: Provide UPSTAGE_API_KEY through the runtime environment and avoid hardcoding, logging, or committing the credential. <br>


## Reference(s): <br>
- [Upstage Document Parse Console](https://console.upstage.ai/api/document-digitization/document-parsing) <br>
- [ClawHub Skill Page](https://clawhub.ai/upstage-deployment/upstage-document-parse) <br>
- [Document Parse Async API Workflow](references/async-workflow.md) <br>
- [Document Parse Sync API Detail](references/sync-options.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance, Files] <br>
**Output Format:** [Markdown guidance with Python and curl examples; parsed document output may be Markdown, HTML, text, or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses UPSTAGE_API_KEY from the environment, sends selected documents to the Upstage API, writes parsed output files when requested, and prints the resolved absolute output path.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
