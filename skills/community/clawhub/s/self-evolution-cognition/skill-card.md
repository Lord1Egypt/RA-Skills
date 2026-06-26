## Description: <br>
Self-Evolution Cognition is a SOUL-based cognition framework that helps an agent separate knowns and unknowns, persist reasoning state, incorporate human feedback, and return confidence-scored analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingofzhao](https://clawhub.ai/user/kingofzhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add structured metacognition, persistent memory files, four-perspective reasoning, human-feedback injection, and confidence gating to agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reasoning, feedback, and intermediate state may be persisted in local files without clear retention or deletion controls. <br>
Mitigation: Use the skill only in workspaces where persistent local memory is acceptable, and define deletion or rotation practices before installation. <br>
Risk: Sensitive data could be captured in persisted memory files if users provide secrets, credentials, customer data, or incident details. <br>
Mitigation: Do not provide sensitive inputs unless the storage paths and cleanup process have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingofzhao/self-evolution-cognition) <br>
- [Project homepage](https://github.com/KingOfZhao/AGI_PROJECT) <br>
- [A Survey of Self-Evolving Agents](https://arxiv.org/abs/2507.21046) <br>
- [SAGE: Multi-Agent Self-Evolution for LLM Reasoning](https://arxiv.org/abs/2603.15255) <br>
- [Group-Evolving Agents](https://arxiv.org/abs/2602.04837) <br>
- [Self-evolving Embodied AI](https://arxiv.org/abs/2602.04411) <br>
- [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564) <br>
- [Beyond RAG for Agent Memory](https://arxiv.org/abs/2602.02007) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Text or Markdown responses with confidence values, collision logs, and memory file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists reasoning and feedback state in local workspace files when used as described.] <br>

## Skill Version(s): <br>
1.1.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
