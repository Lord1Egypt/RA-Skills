## Description: <br>
Turns workshop goals, participants, timing, and constraints into reviewable agendas, facilitation runbooks, materials checklists, risk notes, and follow-up plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, facilitators, and team leads use this skill to turn meeting goals, participants, available time, and known constraints into a structured workshop agenda and facilitation plan. It is intended for draft generation, review, and follow-up planning rather than calendar changes, room booking, or external-system actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated workshop plans may include incorrect assumptions or sensitive meeting details if the input is incomplete or unredacted. <br>
Mitigation: Review outputs before sharing or acting on them, and avoid providing unredacted sensitive notes unless the package and workspace are trusted. <br>
Risk: The bundled Python helper runs locally and can write an output file when explicitly invoked. <br>
Mitigation: Run the helper only on explicit meeting-planning inputs and inspect generated files before distributing or using them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/workshop-agenda-designer) <br>
- [README.md](artifact/README.md) <br>
- [resources/spec.json](artifact/resources/spec.json) <br>
- [resources/template.md](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown by default, with optional JSON from the local helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include reviewable drafts, explicit missing-information prompts, and next-step guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
