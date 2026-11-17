## Description:

Modify or debug revert.wtf normalization, revert-data extraction, trace extraction, ABI decoding, catalog matching, selector lookup, or ERC-4337 decoding behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrtdlgc](https://clawhub.ai/user/mrtdlgc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to modify or debug revert.wtf parser and decoder packages for normalization, revert-data extraction, ABI decoding, selector lookup, catalog matching, and ERC-4337 behavior while keeping changes reproducible and tested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent guidance could change parser or decoder behavior in ways that alter results across website, CLI, MCP, and package consumers.

Mitigation: Keep behavioral changes narrow, preserve evidence-based ranking, add fixtures for new provider shapes or revert payloads, and run the TypeScript checks and targeted package tests listed by the skill.

Risk: Live lookups or website-only explanation logic could make parser results non-reproducible or inconsistent across consumers.

Mitigation: Keep parser paths based on package data and caller-provided input, and keep website, CLI, MCP, and packages consuming the same parser and catalog results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrtdlgc/skills/revertwtf-parser-decoder)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, markdown]

**Output Format:** [Markdown guidance with code-oriented recommendations and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scoped to revert.wtf parser, selectors, account abstraction, and shared result types; the artifact contains guidance only and no executable code.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
