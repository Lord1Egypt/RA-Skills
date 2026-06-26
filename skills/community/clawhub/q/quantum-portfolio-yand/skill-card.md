## Description: <br>
A hybrid quantitative finance skill that compares classical SLSQP, quantum-inspired QUBO simulated annealing, and YAND-MVSK portfolio optimizers on the same return panel and visualizes solver disagreement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x2hacks](https://clawhub.ai/user/0x2hacks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative researchers use this skill to load synthetic or user-supplied return data, run three portfolio optimization approaches side by side, and inspect generated diagnostics before relying on any result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio outputs may be mistaken for financial advice. <br>
Mitigation: Treat outputs as research aids and have a qualified reviewer evaluate assumptions, data quality, and suitability before any investment decision. <br>
Risk: User CSV files may contain data the user did not intend to analyze with this local workflow. <br>
Mitigation: Only provide CSV files intended for local analysis and review the input columns and date rows before running the pipeline. <br>
Risk: Optimization and simulated annealing results may be difficult to reproduce across dependency versions or stochastic runs. <br>
Mitigation: Pin dependencies and record run parameters when reproducible research or auditability matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0x2hacks/quantum-portfolio-yand) <br>
- [README](README.md) <br>
- [Portfolio optimization patterns](references/patterns.md) <br>
- [Sharp edges and failure modes](references/sharp_edges.md) <br>
- [Validation rules](references/validations.md) <br>
- [Synthetic demo guide](examples/demo_synthetic.md) <br>
- [Yau's Affine Normal Descent](https://arxiv.org/abs/2603.28448) <br>
- [YAND-MVSK portfolio optimization](https://arxiv.org/abs/2604.25378) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, plus local script outputs such as JSON summaries and PNG figures.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with synthetic data or a user-provided CSV of daily returns; generated figures are written under assets/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
