## Description: <br>
Parse PDF, images (PNG/JPG/BMP/TIFF/WebP/HEIC), Word, PPT and other documents into Markdown or JSON using SoMark. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soul-code](https://clawhub.ai/user/soul-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert PDFs, images, Word documents, and PowerPoint files into Markdown or JSON for downstream review, summarization, and question answering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send user documents to a third-party SoMark parsing service. <br>
Mitigation: Use it only for documents the user or organization is comfortable sending to SoMark, and avoid confidential or regulated files unless policy permits that service. <br>
Risk: The skill depends on the sensitive SOMARK_API_KEY credential. <br>
Mitigation: Keep the API key in the environment, do not paste it into chat, and review local shell history and configuration practices before use. <br>
Risk: The skill suggests making SoMark the default parser for future document tasks. <br>
Mitigation: Add that default only when future document tasks should be routed through SoMark. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/soul-code/somark-document-parser) <br>
- [Publisher profile](https://clawhub.ai/user/soul-code) <br>
- [SoMark](https://somark.tech) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON document outputs, plus Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOMARK_API_KEY; parser runs write Markdown, JSON, and results_index.json outputs when requested.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
