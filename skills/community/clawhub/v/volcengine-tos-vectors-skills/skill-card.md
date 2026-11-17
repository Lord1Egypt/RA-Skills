## Description:

Manage vector storage and similarity search using TOS Vectors service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jneless](https://clawhub.ai/user/jneless)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to configure TOS Vectors, manage vector buckets and indexes, insert and retrieve vectors, and build semantic search, RAG, recommendation, or image-similarity workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-backed cloud operations can delete vector data, change bucket policies, or affect live TOS resources.

Mitigation: Use least-privileged TOS credentials and require explicit confirmation before delete operations or policy changes.

Risk: The artifact recommends installing the TOS SDK without a consistently pinned package command while noting that TOS Vectors uses a beta SDK version.

Mitigation: Install in an isolated environment and pin and verify the intended TOS SDK version before use.

Risk: Retrieved vector metadata may contain private, third-party, or otherwise untrusted content that could be passed into an LLM workflow.

Mitigation: Review, filter, or redact retrieved metadata before including it in prompts or downstream outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jneless/skills/volcengine-tos-vectors-skills)
- [TOS Vectors API Reference](REFERENCE.md)
- [TOS Vectors Workflows](WORKFLOWS.md)
- [TOS Vectors external endpoint](https://tosvectors-cn-beijing.volces.com)
- [TOS Vectors internal endpoint](https://tosvectors-cn-beijing.ivolces.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include TOS SDK calls and environment variable configuration.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
