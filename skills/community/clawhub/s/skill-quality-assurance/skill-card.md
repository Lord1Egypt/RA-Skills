## Description: <br>
Skill Quality Assurance evaluates agent skills with a six-dimension quality model covering technical depth, cognitive support, orchestration, evolution, market validation, and user experience. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pagoda111king](https://clawhub.ai/user/pagoda111king) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to score, review, and improve agent skills before release, version upgrades, listing checks, or periodic health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The evaluator reads local skill folders and writes Markdown reports, so broad input paths or shared output locations can expose files or replace an existing report. <br>
Mitigation: Run it only on specific skill folders you intend to assess and choose a dedicated output directory where report replacement is acceptable. <br>


## Reference(s): <br>
- [Six Dimensions Criteria](artifact/references/six-dimensions-criteria.md) <br>
- [Evaluation Report Template](artifact/assets/evaluation-template.md) <br>
- [Skill Quality Assurance Evaluation Report](artifact/skill-quality-assurance-evaluation-report.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/pagoda111king/skill-quality-assurance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports with scored tables, summaries, and prioritized improvement guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write a local evaluation report for a specified skill path and optional output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
