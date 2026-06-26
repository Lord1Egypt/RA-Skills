## Description: <br>
A universal self-improving AI agent framework for self-correction, persistent memory, decision verification, reflection, and autonomous upgrade workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mark-heartflow](https://clawhub.ai/user/mark-heartflow) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill as a capability layer for agents that need decision checking, persistent memory, reflection, self-healing, and controlled upgrade loops. It is suited for agent engineering workflows where behavior changes and local persistence are reviewed before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory, behavioral steering, local file writes, and optional self-upgrade workflows can change agent behavior or retain sensitive information. <br>
Mitigation: Review setup and sync scripts before installation, run in an isolated environment, gate self-modification and automation, and avoid providing API keys or sensitive conversations unless local persistence and possible external API use are acceptable. <br>
Risk: The server security verdict is suspicious because the framework includes broad self-improving behavior, auto-upgrade or self-modification mechanisms, and hidden always-on profiling that need manual review. <br>
Mitigation: Perform a manual security review before deployment and keep high-risk automation permissioned, monitored, and disabled by default. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Installation Guide](INSTALL_FOR_AI.md) <br>
- [Verification Methodology](references/verification-methodology.md) <br>
- [Memory System Comparison](references/memory-system-comparison.md) <br>
- [RL Closed Loop](references/rl-closed-loop.md) <br>
- [Reflexion](https://arxiv.org/abs/2308.07915) <br>
- [Self-Verification](https://arxiv.org/abs/2312.09210) <br>
- [CRITIC](https://arxiv.org/abs/2312.04445) <br>
- [Constitutional AI](https://arxiv.org/abs/2212.08073) <br>
- [Generative Agents](https://arxiv.org/abs/2304.03442) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JavaScript examples, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local files, persistent memory artifacts, or upgrade proposals when enabled by the consuming agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, artifact metadata, and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
