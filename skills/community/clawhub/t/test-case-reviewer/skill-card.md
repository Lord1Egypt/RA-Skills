## Description: <br>
Reviews existing test cases, acceptance checklists, QA test points, regression lists, and test report drafts for quality, coverage, executability, missing scenarios, and release risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runkecheng](https://clawhub.ai/user/runkecheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, product teams, and developers use this skill to review already-written test cases or QA checklists against product context, then identify priority-ranked gaps, unclear expectations, executability problems, and release risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect local paths supplied by the user while reviewing test material. <br>
Mitigation: Provide only relevant test cases and product context, and avoid pointing it at unrelated or sensitive files. <br>
Risk: Coverage conclusions can be overstated when product context is missing. <br>
Mitigation: When context is incomplete, the skill limits its conclusion to expression quality, steps, expectations, and executability instead of claiming full business coverage. <br>
Risk: A user may ask the reviewer to skip the rubric and approve weak test cases. <br>
Mitigation: The skill is instructed to keep using the scoring rubric and identify risks rather than bypassing the quality review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runkecheng/test-case-reviewer) <br>
- [测试用例评审评分表](artifact/references/review-rubric.md) <br>
- [云助手测试用例专项风险图谱](artifact/references/cloud-assistant-risk-map.md) <br>
- [测试用例评审器压测样本](artifact/references/pressure-tests.md) <br>
- [测试用例评审报告模板](artifact/assets/review-report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown review report with scoring tables, P0/P1/P2 findings, impacts, recommendations, coverage gaps, and conclusion guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not execute tests, modify code, or generate a full new test suite; it may inspect user-referenced local files with grep/find when paths are provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
