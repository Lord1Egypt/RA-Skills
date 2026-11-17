## Description: <br>
Provides bidirectional Chinese-English translation for plain text, code comments, basic terminology, and Markdown-formatted content while preserving structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and cross-language collaborators use this skill to translate Chinese and English text, code comments, Markdown documents, and common technical or business terminology. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests command-execution permission even though normal translation should not require it. <br>
Mitigation: Install only if command execution is acceptable for the intended environment; prefer a version that removes exec for ordinary translation workflows. <br>
Risk: Translation tasks can expose confidential code, credentials, regulated data, or private documents to an LLM-backed workflow. <br>
Mitigation: Review and redact sensitive content before translation, and avoid submitting regulated or secret material unless the deployment is approved for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/translate-hub-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown or plain text translation output, with code structure preserved when translating comments.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports small batches up to five text segments or one file according to the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
