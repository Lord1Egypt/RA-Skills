## Description:

Shiyi helps exam-prep users capture wrong-question screenshots or quick text entries, organize them with reusable tags, schedule review prompts, and export filtered Excel mistake notebooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kagurananaga](https://clawhub.ai/user/kagurananaga)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and exam-prep users use this skill to track mistakes across exams, convert screenshots or short text notes into structured study records, receive review reminders, and export filtered mistake notebooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain exam text, annotations, and screenshots that may contain personal or sensitive study material.

Mitigation: Avoid sending screenshots with personal or account details, and review local saved data before using the skill on shared machines.

Risk: Screenshot recognition uses the configured vision model, which may process image contents outside the local data directory.

Mitigation: Use the skill only with a trusted model configuration and avoid images containing confidential or regulated information.

Risk: Excel exports may include raw question text, annotations, and embedded screenshots.

Mitigation: Review generated spreadsheets before sharing them, and use the no-image export path when screenshots are unnecessary.

Risk: The security guidance flags export sanitization, tag validation, temporary-file handling, dependency pinning, and broad trigger phrases as issues to review.

Mitigation: Address those items before broader deployment, especially on shared devices or with sensitive study materials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kagurananaga/skills/shiyi-study-tracker)
- [ClawHub publisher profile](https://clawhub.ai/user/kagurananaga)
- [OpenClaw](https://openclaw.ai)
- [Node.js](https://nodejs.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown-style agent messages, structured JSON study records, and generated XLSX export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores study data locally under the user's OpenClaw skill data directory and can attach exported Excel workbooks.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
