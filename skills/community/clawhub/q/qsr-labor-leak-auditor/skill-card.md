## Description:

QSR Labor Leak Auditor provides real-time labor decision support for restaurant and franchise operators, with concise daily labor reads, week-to-date goal tracking, and recovery planning for payroll-week decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcphersonai](https://clawhub.ai/user/mcphersonai)

### License/Terms of Use:

Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)

## Use Case:

Restaurant and franchise operators use this skill to interpret sales and labor inputs, track week-to-date labor against targets, and produce concise recovery actions before payroll closes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Store-level sales, labor cost, weekly goal, and audit context may be persisted by the configured store memory engine.

Mitigation: Review the memory engine retention, deletion, authentication, authorization, and access-control settings before deployment.

Risk: Labor recommendations can affect staffing decisions if treated as automatic instructions.

Mitigation: Use the output as decision support, keep operator review and override context, and confirm operational constraints before changing schedules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mcphersonai/skills/qsr-labor-leak-auditor)
- [McPherson AI](https://mcphersonai.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown and structured text records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [In-chat summaries with optional detailed math; persistent records depend on the configured store memory engine.]

## Skill Version(s):

3.1.4 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
