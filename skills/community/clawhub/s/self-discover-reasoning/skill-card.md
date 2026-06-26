## Description: <br>
Automatically detects runtime capabilities and composes task-specific reasoning structures for complex, multi-step agent problem solving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomaszhou22](https://clawhub.ai/user/thomaszhou22) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to improve answers for debugging, planning, architecture decisions, math, logic, and analytical tasks by selecting and applying fit-for-purpose reasoning modules before producing a response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad automatic activation can affect ordinary high-importance prompts. <br>
Mitigation: Review activation criteria before installation and disable or narrow automatic activation for tasks where an added reasoning layer is not desired. <br>
Risk: Persistent memory behavior may store derived reasoning structures related to sensitive goals, confidential projects, or private user context. <br>
Mitigation: Review or disable memory-writing behavior for sensitive workflows and prefer in-conversation memory when persistence is not required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thomaszhou22/self-discover-reasoning) <br>
- [Publisher profile](https://clawhub.ai/user/thomaszhou22) <br>
- [SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures](https://arxiv.org/abs/2402.03660) <br>
- [Academic sources](references/sources.md) <br>
- [Discovery prompt templates](references/discovery-templates.md) <br>
- [Benchmark report](BENCHMARK.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown responses with optional inline code blocks and structured recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May add internal reasoning-structure overhead of up to about 40% for high-complexity tasks; raw reasoning structures are intended to remain internal.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and CHANGELOG.md, released 2026-05-20) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
