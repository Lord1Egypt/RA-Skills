## Description: <br>
L4 evaluation layer for automated six-dimension skill assessment, report generation, and improvement recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pagoda111king](https://clawhub.ai/user/pagoda111king) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to evaluate single skills or batches across six dimensions, compare versions, and receive improvement recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests evaluator-style access to read skill projects and may run tests or inspect project data. <br>
Mitigation: Install only where that access is acceptable, review requested actions before execution, and run evaluations in a controlled workspace. <br>
Risk: Scores may be approximate because the security evidence notes placeholder scoring and under-scoped retention behavior. <br>
Mitigation: Treat scores as decision support, require human review for important assessments, and confirm any data retention behavior before use. <br>
Risk: Future API calls, log analysis, or database storage could expose project or usage data if enabled without clear controls. <br>
Mitigation: Require explicit opt-in before enabling external calls or persistence, and avoid providing sensitive logs or proprietary project data unless necessary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pagoda111king/six-dim-evaluator) <br>
- [Six Dim Evaluator documentation](https://docs.cloud-shrimp.com/six-dim-evaluator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown and JSON evaluation reports with scores, comparisons, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include six-dimension scores, trend analysis, version comparisons, and suggested improvement actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
