## Description:

Locally hosted tool for evolving an OpenClaw agent profile through a five-dimensional personality matrix, physical-anchor identity setup, local memory files, and optional Markdown instruction export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create and inspect a local personality and memory profile for an OpenClaw agent, including SUNS/S2-DID identity setup, interaction-log processing, profile reporting, and optional instruction-file export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw interaction text and agent profile data are retained locally in s2_consciousness_data.

Mitigation: Avoid entering secrets or sensitive personal information, inspect generated local files, and delete s2_consciousness_data when it is no longer needed.

Risk: The Sour.md export creates persistent agent-behavior instructions that could affect later agent sessions if automatically loaded.

Mitigation: Keep Sour.md isolated, review it before use, and do not load it automatically into an agent context unless its instructions are intended.

Risk: The skill processes raw user text through an unauthenticated localhost LLM endpoint when that service is available.

Mitigation: Run only trusted local model services, review the configured endpoint before execution, and avoid routing sensitive inputs through the parser.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/spacesq/skills/s2-silicon-soul-os)
- [Publisher Profile](https://clawhub.ai/user/spacesq)
- [Space2 Homepage](https://space2.world)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Interactive terminal text, local JSON state files, and an optional generated Markdown instruction file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local s2_consciousness_data files, can export Sour.md, and may send raw interaction text to a localhost OpenAI-compatible LLM endpoint.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
