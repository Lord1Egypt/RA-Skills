## Description: <br>
Translate documents and text between multiple languages with support for glossaries, translation memory, and common office document formats through the Xdoc Translation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangsongbai1](https://clawhub.ai/user/yangsongbai1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, localization teams, and document-heavy workflows can use this skill to submit files or short text for translation, monitor translation status, and retrieve translated results. It also supports glossary and translation memory operations for consistent terminology. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents and text submitted for translation are sent to Xdoc's external service for processing. <br>
Mitigation: Install only if you trust Xdoc with the content being translated, and avoid submitting confidential or regulated material without authorization. <br>
Risk: The skill requires an Xdoc API key that could expose account access or quota if mishandled. <br>
Mitigation: Store XDOC_API_KEY in a secure environment variable or secret store and avoid logging or sharing it. <br>
Risk: Glossary, translation memory, and file delete or edit operations can modify account data. <br>
Mitigation: Review requested delete and edit operations before applying them to important files, glossaries, or translation memories. <br>


## Reference(s): <br>
- [Xdoc Translation Service](https://translation.x-doc.ai/) <br>
- [Xdoc Website](https://x-doc.ai) <br>
- [Xdoc Privacy Policy](https://x-doc.ai/privacy) <br>
- [ClawHub Skill Page](https://clawhub.ai/yangsongbai1/xdoc-translationx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown guidance with API request details, status summaries, translated text, and download links when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XDOC_API_KEY and may upload user-provided documents to Xdoc for processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
