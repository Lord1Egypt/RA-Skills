## Description:

S2 Official Smart Space Engine parses 62 spatial types into a 6-element smart-space hardware matrix and includes a local MCP server plus S2-SWM causality data harvester.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, smart-space designers, and sales engineers use this skill to generate brand-agnostic smart-home or commercial-space hardware blueprints across light, air, sound, electromagnetic, energy, and vision dimensions. Agents can call the parser through CLI or MCP to return configuration matrices and scenario recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes a local MCP server and includes a physical-action tool that claims actuation behavior.

Mitigation: Install only in an isolated test environment until the MCP server is reviewed and real actuator authorization, safety checks, and verified device readback are added.

Risk: The Chronos data harvester writes causal-event records to a persistent local JSONL file.

Mitigation: Decide explicitly whether persistent training logs are acceptable, and restrict, rotate, or disable logging when sensitive space or occupancy data may be captured.

Risk: The included Next.js deployment example uses a command-execution route pattern.

Mitigation: Do not copy the documented route as written; replace it with a hardened interface that validates inputs, avoids shell interpolation, and limits executable paths.

## Reference(s):

- [S2-UHSP Whitepaper V1.0](artifact/S2-UHSP-Whitepaper-V1.0.md)
- [S2 Space Architect Manual](artifact/S2_SPACE_ARCHITECT_MANUAL.md)
- [Space2.world](https://space2.world)
- [ClawHub Skill Page](https://clawhub.ai/spacesq/skills/s2-universal-space-parser)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON parser results and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Parser output includes a six-element hardware matrix, recommended scenarios, and agent pruning guidance; the MCP action tool can append causal-event records to a local JSONL file.]

## Skill Version(s):

2.0.1 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
