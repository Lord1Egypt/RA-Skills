## Description: <br>
Autonomous engine that systematically evaluates and ranks agent skills across models using rubric grading, error taxonomy, and improvement feedback loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jensen-srp](https://clawhub.ai/user/jensen-srp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to evaluate agent skills against baselines, compare behavior across execution models, generate evaluation reports, maintain leaderboards, and produce improvement drafts for low-scoring skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated skill improvements or knowledge-base updates could introduce incorrect or misleading behavior if installed without review. <br>
Mitigation: Review generated SKILL-improved.md files and knowledge-base changes before adopting them in production agent behavior. <br>
Risk: Evaluation runs may expose private skill content to configured external model providers. <br>
Mitigation: Use an isolated workspace and avoid evaluating private skills with external providers unless that data sharing is acceptable. <br>


## Reference(s): <br>
- [Skill-Eval on ClawHub](https://clawhub.ai/jensen-srp/skill-eval) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON evaluation data, HTML leaderboard output, and draft skill-improvement files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce per-model score tables, grading summaries, benchmark metadata, leaderboard entries, and SKILL-improved.md drafts.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
