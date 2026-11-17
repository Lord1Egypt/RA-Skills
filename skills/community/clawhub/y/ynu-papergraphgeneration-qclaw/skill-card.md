## Description:

Generates academic diagrams from PDF or plain-text papers, including paper scans, architecture and flowchart figures, captions, Mermaid topology, Matplotlib charts, and PDF-to-text extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljk00000](https://clawhub.ai/user/ljk00000)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to turn paper PDFs or text excerpts into academic figures, topology descriptions, and captions, and to extract PDF text for downstream diagram generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manuscript text can be sent to configurable external LLM and image services.

Mitigation: Use only papers the user is allowed to share externally, require explicit upload consent, and verify configured endpoints before use.

Risk: Generated chart code can be executed during the Matplotlib results-chart path.

Mitigation: Avoid that path unless execution is sandboxed, or replace executable generated code with structured plotting data.

Risk: Downloaded image outputs and configurable endpoints can expand network and file-handling exposure.

Mitigation: Validate endpoint allowlists and apply bounded image downloads before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ljk00000/skills/ynu-papergraphgeneration-qclaw)
- [Default image API endpoint](https://api.acedata.cloud/nano-banana/images)
- [Default chat API endpoint](https://api.acedata.cloud/nano-banana/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON scan results, Mermaid topology, captions, Python/Matplotlib code, and generated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and configured external LLM/image API credentials; manuscript content may be sent to configured services.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
