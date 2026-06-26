## Description: <br>
End-to-end guide for building AI Agents from Genes: intent decomposition, Gene selection, Genome composition, Agent creation, and testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoba-dev](https://clawhub.ai/user/xiaoba-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to decompose a desired Rotifer agent into capability units, select Genes, choose a Genome composition strategy, create the agent, and validate its run behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording may cause the skill to be used for general agent-building requests. <br>
Mitigation: Use explicit Rotifer-specific requests and review the skill guidance before relying on generated plans. <br>
Risk: Seq compositions can fail at runtime when adjacent Gene schemas are incompatible. <br>
Mitigation: Manually compare adjacent Gene inputSchema and outputSchema fields before creating or running a Seq agent. <br>


## Reference(s): <br>
- [Rotifer Protocol](https://rotifer.dev) <br>
- [Rotifer Documentation](https://rotifer.dev/docs) <br>
- [Rotifer Protocol Specification](https://github.com/rotifer-protocol/rotifer-spec) <br>
- [Rotifer Playground Repository](https://github.com/rotifer-protocol/rotifer-playground) <br>
- [Rotifer Guide Skill](https://clawhub.ai/skills/rotifer-guide) <br>
- [Rotifer Arena Skill](https://clawhub.ai/skills/rotifer-arena) <br>
- [Rotifer Self-Evolving Agent Skill](https://clawhub.ai/skills/rotifer-self-evolving-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with tables, checklists, JSON snippets, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Rotifer CLI commands, MCP configuration snippets, and agent composition plans for user review before execution.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
