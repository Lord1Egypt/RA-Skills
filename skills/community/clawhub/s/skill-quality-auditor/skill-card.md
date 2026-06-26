## Description: <br>
Evaluate and score AgentSkills on design, content, security, and usability, producing a detailed numeric scorecard with improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ann0501](https://clawhub.ai/user/ann0501) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to audit AgentSkills before release or revision. It produces a rubric-based pass or revise report with dimension scores, cited findings, and improvement suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reviewing an overly broad path may expose unrelated local files to the agent during the audit. <br>
Mitigation: Provide the exact skill folder as the review target, not a repository root or home directory. <br>
Risk: Rubric-based findings may miss context or produce incorrect revision guidance for a specific release policy. <br>
Mitigation: Have a maintainer review the scorecard and confirm cited issues before changing or rejecting a skill. <br>


## Reference(s): <br>
- [Skill release page](https://clawhub.ai/ann0501/skill-quality-auditor) <br>
- [Weight Adjustment by Skill Type](references/weight-adjustment.md) <br>
- [D1: Design Quality](references/design-quality.md) <br>
- [D2: Content Quality](references/content-quality.md) <br>
- [D3: Security](references/security.md) <br>
- [D4: Usability](references/usability.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown scorecard with numeric ratings and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes pass or revise verdict, weighted dimension scores, cited findings, highlights, and improvement criteria.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
