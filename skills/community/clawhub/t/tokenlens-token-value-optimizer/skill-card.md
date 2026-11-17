## Description:

TokenLens Token Value Optimizer helps OpenClaw users review token usage, estimate efficiency, and generate recommendations for context loading, model routing, and session practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuellai118](https://clawhub.ai/user/samuellai118)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to inspect local token-use estimates, record historical usage, and receive practical recommendations for reducing unnecessary context and choosing model tiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token and cost values may be mock or historical estimates rather than live billing data.

Mitigation: Use the output as directional guidance and verify important budget or routing decisions against authoritative provider or OpenClaw usage records.

Risk: The skill stores token usage history and configuration locally under the OpenClaw workspace.

Mitigation: Review the local data directory before use and only enable scheduled checks if ongoing local history collection is acceptable.

Risk: Some recommendations describe commands or configuration changes that are not automatically applied by the skill.

Mitigation: Review proposed commands manually and apply only the changes that match the user's workspace policy.

## Reference(s):

- [TokenLens homepage](https://tokenlens.ai)
- [ClawHub skill page](https://clawhub.ai/samuellai118/skills/tokenlens-token-value-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Terminal text and Markdown guidance, with optional JSON from supported script commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local token usage and configuration data under ~/.openclaw/workspace/memory/tokenlens/; reported token and cost values may be mock or historical estimates.]

## Skill Version(s):

1.0.3 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
