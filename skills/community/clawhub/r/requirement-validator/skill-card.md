## Description: <br>
需求真实性验证器 - 用数据验证需求的真实性，避免伪需求浪费资源。多维度验证用户一致性、需求频次、影响面、竞品覆盖、替代方案、ROI等。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijinhongucl-pixel](https://clawhub.ai/user/lijinhongucl-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, founders, and product teams use this skill to evaluate whether proposed requirements are worth implementing. It analyzes feedback, optional behavior data, competitor coverage, alternatives, and ROI signals to produce a data-driven requirement validation report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requirement validation may involve specific requirements, feedback, or behavior datasets that contain sensitive internal information. <br>
Mitigation: Use the skill only for intended requirement validation tasks and avoid providing sensitive internal datasets unless they are meant to be processed. <br>
Risk: Validation results depend on the quality and relevance of supplied feedback, behavior, competitor, and keyword data. <br>
Mitigation: Review input files and treat the generated score as decision support rather than an automatic implementation decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lijinhongucl-pixel/requirement-validator) <br>
- [README](artifact/README.md) <br>
- [Validation rules configuration](artifact/config/validation_rules.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with command examples and data-driven scoring summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read CSV feedback data, optional CSV behavior data, JSON competitor data, and YAML validation rules.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
