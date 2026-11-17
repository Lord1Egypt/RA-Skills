## Description:

Semantically optimizes context history and large text blocks via the Trunkate AI API, with proactive context pruning hooks for automated token management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engineering-trunkate-ai](https://clawhub.ai/user/engineering-trunkate-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to compress long session histories, logs, and large text inputs while preserving task-critical context. OpenClaw users can enable hooks that prune history automatically when token usage crosses a configured threshold.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated hooks can send redacted conversation history to Trunkate's external service.

Mitigation: Enable the hooks only in workspaces where external processing of redacted history is acceptable, and use explicit [PRIVATE] blocks for sensitive content.

Risk: The hook can replace session history with the returned optimized summary.

Mitigation: Review hook behavior before enabling it and keep important source-of-truth project requirements outside replaceable session history.

Risk: TRUNKATE_API_URL can redirect optimization requests away from the default service.

Mitigation: Leave TRUNKATE_API_URL unset except in controlled development environments.

Risk: A relative-path execution issue is present in the hook flow.

Mitigation: Do not enable the hook in untrusted workspaces until the relative-path execution issue is fixed.

Risk: TRUNKATE_API_KEY is required for API access.

Mitigation: Store and scope TRUNKATE_API_KEY carefully and avoid exposing it in shared logs or workspace files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engineering-trunkate-ai/skills/trunkate)
- [Trunkate Homepage](https://trunkate.ai)
- [Optimization Examples and Benchmarks](references/examples.md)
- [Python Proactive Hooks Integration Guide](references/hooks-setup.md)
- [OpenClaw and Trunkate API Integration Spec](references/openclaw-integration.md)
- [Proactive Context Hook](hooks/openclaw/HOOK.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples; runtime tools return optimized text or OpenClaw history update directives.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, requests, TRUNKATE_API_KEY, and OpenClaw history/token environment variables for automated hook operation.]

## Skill Version(s):

0.31.0 (source: ClawHub release evidence, CHANGELOG, version.txt)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
