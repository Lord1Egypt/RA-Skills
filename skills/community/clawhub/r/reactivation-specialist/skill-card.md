## Description:

Designs a closed-loop email reactivation program for lapsed cohorts, including cohort definition, staged win-back offer ladder, re-consent capture, sunset-confirm suppression rule, and handoff facts for related email lifecycle skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, lifecycle, and email operations teams use this skill to plan win-back and re-permission programs for inactive subscribers before suppressing unrecovered contacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose suppression or re-consent rules based on subscriber engagement and consent-related data.

Mitigation: Review the proposed cohort, consent capture, and suppression rules before applying them in an email platform.

Risk: Lapsed-subscriber exports and pasted engagement data may contain untrusted or sensitive content.

Mitigation: Treat exported data as untrusted input and use it only as evidence for planning, not as instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/reactivation-specialist)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown guidance with structured campaign sections and a handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces planning guidance and proposed rules; it does not automatically change subscriber records or execute email platform actions.]

## Skill Version(s):

19.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
