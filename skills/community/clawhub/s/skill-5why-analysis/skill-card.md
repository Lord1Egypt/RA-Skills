## Description:

A Chinese-language 5 Whys root-cause-analysis facilitator that guides users through questioning, answer validation, root-cause decisions, corrective actions, and final conversation summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Operators, quality teams, process engineers, and other external users use this skill to facilitate structured Chinese-language 5 Whys analysis for equipment failures, production abnormalities, quality defects, and similar repeatable problems. It helps keep each round focused on one cause, validate answers, decide whether a corrective action addresses the root cause, and preserve the final analysis record.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enforce a rigid 5 Whys format and may take over broad root-cause-analysis requests where another method would be more suitable.

Mitigation: Use it when a structured 5 Whys facilitation flow is desired, and allow the user or reviewer to switch methods when the problem is exploratory, one-off, or systemically complex.

Risk: Root-cause conclusions and corrective actions may be treated as authoritative in safety-critical, engineering, quality, or business decisions.

Mitigation: Have qualified domain experts review the final cause chain and proposed measures before implementation.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-5why-analysis)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-5why-analysis)
- [5WHY analysis theory reference](references/theory.md)
- [Conversation tracking template](references/tracking-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, analysis]

**Output Format:** [Chinese Markdown-style structured conversation with fixed labels, validation results, corrective actions, root-cause decisions, and a final analysis summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, external access, persistence, or credential handling; outputs should be reviewed before operational use]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
