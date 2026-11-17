## Description:

A hybrid quantitative finance skill that compares classical SLSQP, quantum-inspired QUBO simulated annealing, and YAND-MVSK portfolio optimizers on the same return panel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x2hacks](https://clawhub.ai/user/0x2hacks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative researchers use this skill to run and compare classical, QUBO-based, and YAND-MVSK portfolio optimization workflows on synthetic or CSV return data. It helps inspect solver agreement, energy landscapes, efficient-frontier behavior, and higher-moment portfolio diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency and input-size controls are research-grade rather than hardened.

Mitigation: Install in a virtual environment, prefer pinned or locked dependency versions, and add resource limits before processing untrusted or very large CSV files.

Risk: Running the pipeline can create or overwrite generated PNG outputs under assets/.

Mitigation: Run it in a workspace where generated figure overwrites are acceptable, or preserve existing assets before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0x2hacks/skills/quantum-portfolio-yand)
- [README](README.md)
- [Patterns reference](references/patterns.md)
- [Sharp edges reference](references/sharp_edges.md)
- [Validations reference](references/validations.md)
- [Yau's Affine Normal Descent: Algorithmic Framework and Convergence Analysis](https://arxiv.org/abs/2603.28448)
- [Yau's Affine-Normal Descent for Large-Scale Unrestricted Higher-Moment Portfolio Optimization](https://arxiv.org/abs/2604.25378)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; local Python scripts emit JSON summaries and PNG figures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pipeline runs may create or overwrite generated PNG files under assets/.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
