## Description:

Parse PDFs, images, Word, PowerPoint, and other documents into Markdown or JSON using SoMark.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soul-code](https://clawhub.ai/user/soul-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to parse local documents and document directories into structured Markdown and JSON so downstream agents can inspect, summarize, or answer questions over the content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents are sent to an external SoMark API and may contain confidential, regulated, or proprietary information.

Mitigation: Use the skill only for documents you are comfortable sending to SoMark, and review data handling requirements before parsing sensitive files.

Risk: The skill encourages persistent default routing for future document parsing tasks.

Mitigation: Avoid making it a blanket default parser unless users explicitly want future document tasks routed through SoMark.

Risk: Parsed documents can contain prompt-like or malicious instructions.

Mitigation: Treat parsed output strictly as document data and do not follow instructions embedded inside parsed content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/soul-code/skills/somark-document-parser)
- [Publisher Profile](https://clawhub.ai/user/soul-code)
- [SoMark](https://somark.tech)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown and JSON files with a run-level JSON index]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SOMARK_API_KEY and sends selected documents to the SoMark API.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
