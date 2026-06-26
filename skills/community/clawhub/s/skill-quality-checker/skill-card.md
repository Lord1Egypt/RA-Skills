## Description: <br>
Skill Quality Checker evaluates installed skills across five quality dimensions and produces scoring reports with improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaozhengmao](https://clawhub.ai/user/shaozhengmao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to review installed skills, score them across intent fit, completeness, robustness, description accuracy, and token efficiency, and identify practical improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may include local skill names, paths, or review details that should not be shared broadly. <br>
Mitigation: Run the checker only against skill directories intended for review, choose report output paths deliberately, and review reports before sharing them. <br>
Risk: The quality scores are heuristic static-analysis results and may miss issues or overstate confidence. <br>
Mitigation: Use the report as review support and keep human review as the final decision point before deployment or publication. <br>


## Reference(s): <br>
- [Scoring Criteria](references/scoring-criteria.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/shaozhengmao/skill-quality-checker) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown or JSON quality report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print results to the terminal or write a report to a user-selected output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
