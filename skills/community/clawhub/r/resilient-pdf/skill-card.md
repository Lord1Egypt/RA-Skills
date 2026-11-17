## Description:

Recover PDF extraction and summarization workflows for local or remote PDFs when native PDF handling fails, hangs, times out, rejects large files, or exceeds provider limits, using URL download, local extraction via `uvx` and `markitdown[pdf]`, optional chunking, and first-pass summary artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cdmichaelb](https://clawhub.ai/user/cdmichaelb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to recover analysis of local or remote PDFs when built-in PDF handling fails, then extract markdown, chunk large documents, and create first-pass summary artifacts for follow-up summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can download arbitrary remote PDF URLs from the agent's network context.

Mitigation: Use trusted PDF URLs, keep outputs workspace-local, and apply network controls or sandboxing for sensitive environments.

Risk: The helper invokes a runtime-resolved third-party PDF conversion package.

Mitigation: Use a sandbox or pinned converter environment before processing sensitive documents or untrusted files.

Risk: Extracted markdown and generated first-pass summaries can be noisy, incomplete, or misleading.

Mitigation: Inspect the extracted text or relevant chunks before relying on summaries, quotes, or numeric claims.

## Reference(s):

- [Resilient PDF patterns](references/patterns.md)
- [Resilient PDF ClawHub page](https://clawhub.ai/cdmichaelb/skills/resilient-pdf)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown instructions, extracted markdown files, optional chunk files, optional first-pass summary markdown, and optional JSON run results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports local PDF paths or remote PDF URLs, optional chunking, and optional first-pass summary artifact generation.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
