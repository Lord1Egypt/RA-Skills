## Description: <br>
Report to Article restructures completed Chinese research reports into reader-facing articles without adding, deleting, or changing source facts, data, judgments, or links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wujiaming88](https://clawhub.ai/user/wujiaming88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, analysts, and agents use this skill to reorganize completed research reports into clearer articles with objective titles, concise subheadings, and a stronger reading path. It is intended for transformations where every original object, fact, data point, judgment, and link must be preserved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long report transformations can omit source objects, facts, data points, judgments, or links if the input or output is truncated. <br>
Mitigation: Build a complete information checklist before restructuring, process long reports in blocks, append each block to the output, and verify final coverage against the checklist. <br>
Risk: The workflow may create or append to an output file and run simple local text-count checks. <br>
Mitigation: Review the target output path and final article, and confirm that the original report's facts and links were preserved before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wujiaming88/report2article) <br>
- [Information checklist template](artifact/references/info-checklist-template.md) <br>
- [Logic skeleton template](artifact/references/logic-skeleton.md) <br>
- [Long report protocol](artifact/references/long-report-protocol.md) <br>
- [Title rules](artifact/references/title-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance, Shell commands] <br>
**Output Format:** [Markdown article text with checklist-style validation notes and optional local verification commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [For long reports, the skill directs agents to write or append output in blocks and verify coverage against an information checklist.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
