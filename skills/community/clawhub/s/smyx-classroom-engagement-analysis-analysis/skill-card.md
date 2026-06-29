## Description: <br>
Analyzes fixed-camera classroom video or image inputs to produce class-level engagement scores, emotion distributions, anonymous low-engagement seat coordinates, heatmap links, and teacher-facing suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators, school operators, and smart-classroom developers use this skill to analyze classroom camera footage for aggregate engagement trends and real-time teaching support. Use requires appropriate consent and data-processing controls for student video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Student classroom video and derived engagement reports are sensitive, especially when minors are involved. <br>
Mitigation: Use only where the school or organization has explicit consent and a data-processing agreement covering cloud upload, retention, deletion, access controls, and permitted uses. <br>
Risk: The release is framed as anonymous and real-time, while security evidence reports persistent identity state, token storage, and cloud history retrieval. <br>
Mitigation: Confirm identity linkage, token storage, report retention, deletion behavior, and access controls with the publisher before deployment. <br>
Risk: Emotion and engagement outputs could be misused as individual student evaluation or profiling. <br>
Mitigation: Restrict outputs to aggregate teaching support and anonymous seat-level prompts; do not use them for student performance evaluation, parent communication, public ranking, or psychological diagnosis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-classroom-engagement-analysis-analysis) <br>
- [API documentation](references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown reports and tables, JSON API responses, report links, heatmap image URLs, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include cloud-hosted report links and heatmap image URLs returned by the analysis API.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
