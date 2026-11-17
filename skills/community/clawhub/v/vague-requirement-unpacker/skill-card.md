## Description:

Cold-start unpacker for product managers who need to turn vague boss or business requirements into confirmation questions, scenario narrowing, scope skeletons, readiness scoring, risk flags, and stakeholder reply scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris1wang3](https://clawhub.ai/user/chris1wang3)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers use this skill when a stakeholder provides only a vague direction, oral task, chat screenshot, or one-line meeting note and they need a fast alignment pack before writing a PRD. It helps external or internal teams clarify intent, identify key questions, narrow scenarios, define scope boundaries, score readiness, and prepare reply language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional HTML reports can expose users to active web content if untrusted or externally supplied requirement text is inserted naively.

Mitigation: Prefer Markdown for lower-risk sharing, or escape and sanitize user-provided and model-derived text before opening, sharing, or hosting HTML reports.

Risk: A vague requirement unpacking report could be mistaken for a final PRD or engineering-ready commitment.

Mitigation: Keep assumptions and missing facts clearly marked as pending confirmation, and use the output as an alignment pack rather than a delivery commitment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chris1wang3/skills/vague-requirement-unpacker)
- [Unpacking Playbook](references/unpacking-playbook.md)
- [Deterministic Scoring Engine](references/scoring-engine-deterministic.md)
- [User Input Templates](references/user_templates.md)
- [HTML Report Template](references/report-template-pro.html)
- [Intake Form UI](assets/intake-form.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output level is selected as L1, L2, or L3; HTML output uses the bundled report template.]

## Skill Version(s):

1.0.3 (source: server release evidence and artifact/claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
