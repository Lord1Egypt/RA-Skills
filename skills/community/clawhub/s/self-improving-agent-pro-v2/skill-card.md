## Description: <br>
A self-improving AI agent framework for self-correction, persistent memory, decision verification, continuous learning, and autonomous upgrade workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mark-heartflow](https://clawhub.ai/user/mark-heartflow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent builders use this skill to add self-correction, memory routing, verification loops, and upgrade-oriented learning behavior to AI agents. It is most relevant when an agent needs to evaluate decisions, retain lessons, and package improvements across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence flags under-disclosed autonomous code modification and source-write behavior. <br>
Mitigation: Install in a sandboxed or experimental environment and require human review before enabling automatic upgrades or repository write access. <br>
Risk: The security evidence flags persistent memory logging and psychological profiling behavior. <br>
Mitigation: Review and disable persistent memory logging and profiling paths unless they are necessary, disclosed, and governed by the deployment's data policies. <br>
Risk: The security evidence flags external-code ingestion paths. <br>
Mitigation: Do not grant broad network, shell, or repository access unless each external-code path can be audited and approved. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [GitHub Sources](references/GITHUB_SOURCES.md) <br>
- [RL Closed Loop](references/rl-closed-loop.md) <br>
- [Verification Methodology](references/verification-methodology.md) <br>
- [Reflexion](https://arxiv.org/abs/2308.07915) <br>
- [Self-Verification](https://arxiv.org/abs/2312.09210) <br>
- [CRITIC](https://arxiv.org/abs/2312.04445) <br>
- [Constitutional AI](https://arxiv.org/abs/2212.08073) <br>
- [Generative Agents](https://arxiv.org/abs/2304.03442) <br>
- [Self-Reward](https://arxiv.org/abs/2403.00564) <br>
- [Plan-and-Solve](https://arxiv.org/abs/2305.04091) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and source files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve local state, persistent memory, and upgrade-related file changes when installed and executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release, artifact frontmatter, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
