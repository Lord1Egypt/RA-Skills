## Description: <br>
Resilient PDF recovers PDF extraction and summarization workflows when native PDF handling fails by using local or remote PDF extraction, optional chunking, and first-pass summary artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cdmichaelb](https://clawhub.ai/user/cdmichaelb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill as a fallback when native PDF tooling fails, times out, rejects large files, or cannot process remote PDFs directly. It helps extract markdown or text, produce chunks, and create a first-pass summary artifact for grounded downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote PDF download can fetch untrusted or unexpected content. <br>
Mitigation: Use trusted PDF URLs, keep downloads inside the workspace, and inspect extraction output before relying on it. <br>
Risk: The helper invokes local uvx and markitdown tooling against PDFs selected by the operator. <br>
Mitigation: Do not silently install dependencies; run the extraction only when the operator accepts the local toolchain and source document. <br>
Risk: Generated first-pass summaries may omit or distort important details from the extracted text. <br>
Mitigation: Treat summary artifacts as navigation aids and verify quoted, numeric, or high-impact claims against the extracted markdown or chunks. <br>
Risk: Sensitive PDFs may be written to local output files, chunks, or summaries. <br>
Mitigation: Process sensitive documents only in an appropriate workspace and review output paths before sharing or persisting artifacts. <br>


## Reference(s): <br>
- [Resilient PDF patterns](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell command examples, markdown/text files, and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write downloaded PDF files, extracted markdown, chunk files, and first-pass summary artifacts inside the workspace.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
