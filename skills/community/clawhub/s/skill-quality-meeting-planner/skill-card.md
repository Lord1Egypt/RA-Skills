## Description:

Plans Chinese quality weekly meetings by parsing user-provided quality data, checking required meeting details, confirming an outline, and generating a DOCX meeting plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and quality teams use this skill to turn quality metrics, defects, risks, and improvement items into a structured weekly quality meeting plan. It helps collect missing meeting details, confirm the agenda outline, and produce a final Word document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quality metrics, meeting links, or internal issue details may be exposed if intermediate JSON or generated DOCX files are stored in shared folders.

Mitigation: Use the skill in a private workspace, avoid shared output locations for sensitive meeting material, and delete the intermediate meeting_data.json after the DOCX is created.

Risk: The meeting plan may be incomplete or misleading if required meeting time, attendees, location, or core agenda items are missing.

Mitigation: Require the user to supply missing required information and confirm the generated outline before creating the final document.

## Reference(s):

- [Meeting schema](artifact/references/meeting-schema.md)
- [Server-resolved source repository](https://github.com/duding-engicool/skill-quality-meeting-planner)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-quality-meeting-planner)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown outline, structured JSON meeting data, shell command, and DOCX file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires required meeting details and user outline confirmation before DOCX generation.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
