## Description:

Semantically optimizes agent conversation history and large text blocks through the Trunkate AI API, with optional OpenClaw hooks for proactive context compression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[titus-choi](https://clawhub.ai/user/titus-choi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Trunkate AI to compress long conversations, logs, documents, and handoff context so an agent can continue work within token limits while preserving key task facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic hook behavior can send conversation history, logs, and project content to Trunkate and replace session history without enough user-visible control.

Mitigation: Review before installing, use only where sending that content to Trunkate is acceptable, and avoid enabling the PreRequest hook until explicit opt-in, threshold checks, destination allowlisting, stronger redaction, and confirmation are in place.

Risk: Sensitive context may be included in text selected for optimization.

Mitigation: Use protected rules and KEEP blocks for content that must not be compressed, keep secrets out of compressible context, and verify redaction behavior before enabling automatic operation.

Risk: Compressed history can omit or alter details that matter for later agent decisions.

Mitigation: Preserve critical instructions and project facts explicitly, review optimization logs or outputs at important milestones, and fall back to original context when fidelity is uncertain.

Risk: API failures, missing API keys, or rate limits can leave context unoptimized.

Mitigation: Treat optimization as a best-effort helper, monitor error output, and do not assume compression occurred unless the optimized output or history update is visible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/titus-choi/skills/trunkate-ai)
- [Optimization Examples and Benchmarks](references/examples.md)
- [Python Proactive Hooks Integration Guide](references/hooks-setup.md)
- [OpenClaw and Trunkate API Integration Spec](references/openclaw-integration.md)
- [Proactive Context Hook](hooks/openclaw/HOOK.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Plain text and Markdown with inline shell and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TRUNKATE_API_KEY; optimization returns compressed text or leaves the original text unchanged when the API key is missing or the API call fails.]

## Skill Version(s):

0.20.0 (source: server release metadata, CHANGELOG.md, version.txt; SKILL.md frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
