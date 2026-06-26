## Description: <br>
Provides document and text translation through the Xdoc Translation API, including supported file formats, glossaries, and translation memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangsongbai1](https://clawhub.ai/user/yangsongbai1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to translate documents or text with Xdoc, manage glossaries and translation memory, and guide API-based upload, polling, and download workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents or text are sent to Xdoc for translation. <br>
Mitigation: Use the skill only when Xdoc's terms meet the user's requirements, and avoid confidential or regulated material unless approved. <br>
Risk: An Xdoc API key is required and could be exposed through sharing or logs. <br>
Mitigation: Use a revocable API key, provide it through XDOC_API_KEY or the x-api-key header, and avoid storing it in public files or logs. <br>
Risk: Glossary and translation-memory operations can create, edit, or delete Xdoc resources. <br>
Mitigation: Review requested resource changes before performing create, edit, or delete operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangsongbai1/xdoc-translation) <br>
- [Xdoc](https://x-doc.ai) <br>
- [Xdoc translation console](https://translation.x-doc.ai/) <br>
- [Xdoc privacy policy](https://x-doc.ai/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Text, Configuration] <br>
**Output Format:** [Markdown guidance with HTTP and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XDOC_API_KEY; may return translated text, translation status, or download URLs from Xdoc.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
