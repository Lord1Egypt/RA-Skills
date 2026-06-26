## Description: <br>
Tracks patient-side postoperative rehabilitation progress by summarizing completion, pain, function, phase progress, and attention items for display. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Patients and care teams can use this skill to turn rehabilitation task records, pain scores, and functional self-assessments into structured progress data and readable summaries. It is intended for progress tracking and visualization, not diagnosis, treatment decisions, or rehabilitation prescription changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rehabilitation progress information is sent to a named external medical-model API using an app key. <br>
Mitigation: Use only when that external API is acceptable for the data involved, protect the app key, and avoid direct patient identifiers where possible. <br>
Risk: Document and image inputs increase parsing surface through optional local parsers, converters, or OCR tools. <br>
Mitigation: Prefer JSON input for routine use and process only trusted documents or images when expanded input support is needed. <br>
Risk: Generated summaries could be mistaken for medical advice. <br>
Mitigation: Treat summaries as informational progress tracking and have qualified clinicians review conclusions before making care decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-rehab-progress-tracking) <br>
- [Referenced rehabilitation analyzer skill](https://agent-skills.md/skills/huifer/WellAlly-health/rehabilitation-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [UTF-8 JSON with structured progress fields and Markdown or natural-language summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local completion and trend fields; model-generated text is informational and should be reviewed before clinical use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
