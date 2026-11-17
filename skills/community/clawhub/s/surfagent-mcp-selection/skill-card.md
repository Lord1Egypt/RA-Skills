## Description:

Selection guide for SurfAgent automation layers, showing when to use perception, platform adapters, MCPs, and raw browser control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[surfagentapp](https://clawhub.ai/user/surfagentapp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to choose the lightest SurfAgent browser automation layer that can complete a task with visible proof.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Related browser, Gmail, adapter, or MCP skills may perform real account actions when used with this routing guide.

Mitigation: Review the separate action-capable skills and require post-action verification before using them in account workflows.

Risk: Incorrect layer selection could produce weak proof or unnecessary broad browser inspection.

Mitigation: Follow the skill's sequence of inspecting state, choosing the narrowest capable layer, acting once, and verifying on the smallest reliable surface.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/surfagentapp/skills/surfagent-mcp-selection)
- [SurfAgent Homepage](https://surfagent.app)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown guidance for agent routing decisions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance-only skill; no executable code, persistence, or unrelated data access is reported by security evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
