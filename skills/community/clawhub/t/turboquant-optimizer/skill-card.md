## Description:

Optimizes OpenClaw token usage with context compression, semantic deduplication, and adaptive token budgeting to reduce API cost and memory footprint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akanji-creator](https://clawhub.ai/user/akanji-creator)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to analyze, compress, and optimize OpenClaw conversation context through automatic hooks, CLI commands, and a JavaScript API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic context compression can rewrite conversation history and place compressed user content into a system-role message.

Mitigation: Review carefully before installing; use manual optimization or conservative settings for sensitive workflows until system-message promotion is fixed.

Risk: Checkpointing and tool-result caching can retain optimized context or tool summaries in memory.

Mitigation: Disable checkpointing or clear optimizer state where retained conversation context is not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/akanji-creator/skills/turboquant-optimizer)
- [Google Research TurboQuant article](https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets, JavaScript examples, shell commands, and optional JSON statistics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return optimized message arrays and token-savings metadata from the programmatic API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
