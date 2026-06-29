## Description: <br>
紫微斗数识人管人报告生成。输入命盘输出八层管理策略（驱动力/软肋/沟通方式/成长路径/合盘适配） <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yifanli94](https://clawhub.ai/user/yifanli94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Managers and team operators use this skill to turn Zi Wei Dou Shu chart data plus workplace context into structured people-management reports for onboarding, promotion review, management-style fit, and team-relationship diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect sensitive birth details, gender, workplace role, reporting relationships, and incident history to generate employee profiles. <br>
Mitigation: Require explicit consent from the subject before use and limit input collection to information approved for the specific management purpose. <br>
Risk: Generated reports may be saved or shared without clear retention or access controls. <br>
Mitigation: Define who may read saved reports, where they may be stored, and when they must be deleted before enabling the report-saving workflow. <br>
Risk: The workflow references third-party charting sites for Zi Wei Dou Shu chart generation. <br>
Mitigation: Do not enter personal data into third-party charting sites unless the organization has approved that site and its data handling terms. <br>
Risk: Default MEMORY.md updates or forwarding could preserve sensitive employee profile data beyond the intended report. <br>
Mitigation: Disable automatic MEMORY.md updates and forwarding unless they are explicitly approved for this use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yifanli94/ziwei-people-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/yifanli94) <br>
- [Online Zi Wei charting tool referenced by the skill](https://ziwei.xiang.com/) <br>
- [Report template](templates/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Long-form Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save reports under team-insights/{name}.md and update MEMORY.md according to the artifact workflow.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
