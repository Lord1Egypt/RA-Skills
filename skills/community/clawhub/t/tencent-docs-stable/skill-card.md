## Description:

Provides a structured recovery path for Tencent Docs writes when the MCP connector fails, with credential checks, a single retry, JSON-RPC fallback, chunking, and read-back verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to complete Tencent Docs uploads and edits when the connector fails or truncates long content. It guides safe recovery and confirms the resulting document content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial because one local reference could not be resolved.

Mitigation: Review the unresolved reference and decide whether it affects your use before installing.

Risk: Fallback API calls can make changes to a Tencent Docs document.

Mitigation: After writing, read back the title and boundary paragraphs and confirm the chunk count; do not delete and recreate the document as a recovery step.

## Reference(s):

- [Tencent Docs Stable Channel on ClawHub](https://clawhub.ai/haiyangchenbj/skills/tencent-docs-stable)

## Skill Output:

**Output Type(s):** [Text, Guidance, API calls]

**Output Format:** [Markdown status report and Tencent Docs document updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chunks long content at paragraph boundaries and verifies the resulting document by reading it back; never exposes credential values.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
