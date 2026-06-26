## Description: <br>
Before starting an AI task, this skill profiles the task, matches it against supported models, and estimates cost across value, quality, balanced, and local modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minirr890112-byte](https://clawhub.ai/user/minirr890112-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill before AI work to choose a cost-effective model and estimate per-run and daily costs for coding, writing, research, and simple Q&A tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps local aggregate usage history in ~/.hermes/task-cost-history.json. <br>
Mitigation: Use --reset-bonus on shared machines or when the local aggregate history should be cleared. <br>
Risk: The documented install command uses a GitHub branch-style package URL rather than a pinned commit. <br>
Mitigation: Install from a pinned commit or reviewed release when reproducibility or supply-chain review is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/minirr890112-byte/task-cost-estimator) <br>
- [Publisher profile](https://clawhub.ai/user/minirr890112-byte) <br>
- [HermesMade homepage](https://github.com/minirr890112-byte/HermesMade) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Console text with ranked model recommendations, task profile signals, and cost estimates; quiet mode emits a single-line recommendation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains aggregate lifetime savings history in ~/.hermes/task-cost-history.json unless reset by the user.] <br>

## Skill Version(s): <br>
1.1.0 (source: release metadata and SKILL.md frontmatter; pyproject.toml reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
