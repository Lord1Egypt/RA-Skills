## Description: <br>
Selection guide for SurfAgent automation layers, showing when to use perception, platform adapters, MCPs, and raw browser control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[surfagentapp](https://clawhub.ai/user/surfagentapp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to choose the lightest SurfAgent automation layer that can complete browser or platform tasks with reliable proof. It helps route work across state inspection, platform adapters, MCPs, and raw browser control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recommended downstream browser, Gmail, platform adapter, or MCP tools may access accounts or perform user-visible actions. <br>
Mitigation: Review and authorize the separate tools before use, prefer the narrowest capable layer, and verify resulting browser or platform state after actions. <br>
Risk: Using a heavier automation layer without proof can create unreliable or misleading outcomes. <br>
Mitigation: Follow the skill's ladder: inspect state first, act once with the lightest sufficient layer, and confirm success on the smallest reliable surface. <br>


## Reference(s): <br>
- [SurfAgent homepage](https://surfagent.app) <br>
- [ClawHub skill page](https://clawhub.ai/surfagentapp/surfagent-mcp-selection) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only routing guidance; no code, install hooks, credential handling, persistence, or hidden behavior are included.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
