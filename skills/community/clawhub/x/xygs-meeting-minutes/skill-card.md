## Description: <br>
会议纪要融合生成器 v2.0 extracts content from DingTalk and/or 得到 GetNote meeting-minutes PDFs, corrects common ASR transcription errors, and fuses source strengths into a polished 10-section meeting-minutes HTML and PDF output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caizi333333](https://clawhub.ai/user/caizi333333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external collaborators use this skill to convert one or two meeting-minutes PDFs into structured Chinese meeting records with overview, decisions, quotes, action items, timeline, insights, and review sections. It is suited to business meetings, team discussions, and partnership conversations where users need a polished HTML/PDF deliverable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting transcripts may contain confidential business, partnership, or personal information. <br>
Mitigation: Confirm the source PDFs before processing and review the generated HTML/PDF before distributing it. <br>
Risk: Generated minutes may include incorrect ASR corrections, inferred priorities, or incomplete fusion of the source notes. <br>
Mitigation: Review terminology, decisions, action owners, and deadlines against the original meeting materials before treating the output as authoritative. <br>
Risk: Output files could be written with confusing or unintended filenames. <br>
Mitigation: Choose explicit output names and locations for the generated HTML and PDF files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caizi333333/xygs-meeting-minutes) <br>
- [Publisher profile](https://clawhub.ai/user/caizi333333) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Chinese meeting-minutes HTML and PDF files with concise agent guidance and optional shell commands for PDF export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local HTML template, term-correction JSON, and optional Playwright or WeasyPrint PDF export; generated content should be reviewed before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
