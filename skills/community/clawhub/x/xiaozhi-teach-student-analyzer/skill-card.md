## Description: <br>
Helps teachers analyze student performance data, identify class-level and individual weak points, and turn those findings into differentiated teaching suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qizhitang](https://clawhub.ai/user/qizhitang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers use this skill to convert externally supplied grades, exam item data, and classroom observations into class profiles, weak-point analysis, individual diagnostics, and teaching adjustments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive student performance and classroom-observation data. <br>
Mitigation: Prefer student IDs or aliases over names, use aggregate data for public reports, and avoid sending individual student details unless the teacher explicitly requests an internal workflow. <br>
Risk: Analysis results can be written to other teaching skills without a clear per-use consent step. <br>
Mitigation: Confirm what fields will be shared before cross-skill writeback and limit shared data to the minimum needed, such as weak knowledge points or class-level grouping strategy. <br>
Risk: Sparse or single-event data can lead to overconfident student diagnoses. <br>
Mitigation: Require external evidence for analyses, mark conclusions as insufficiently supported when samples are small, and avoid stable individual trend claims without at least three relevant observations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qizhitang/xiaozhi-teach-student-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/qizhitang) <br>
- [Analysis framework and templates](references/analysis-framework.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown reports, diagnostic summaries, heatmaps, teaching recommendations, and structured data-sharing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires teacher-supplied or linked assessment and observation data; should use aliases or student IDs when individual details are unnecessary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
