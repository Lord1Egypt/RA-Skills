## Description:

Digital construction foreman for crew management, work acceptance, work logs, hidden works acts, safety, schedules, and executive documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raaipro](https://clawhub.ai/user/raaipro)

### License/Terms of Use:

MIT-0

## Use Case:

Construction foremen, site managers, contractors, technical customers, and construction business owners use this skill to structure daily site planning, acceptance checks, safety routines, procurement coordination, work logs, hidden-work acts, schedules, and management reports. It is intended as an operational drafting and control aid, not a replacement for physical inspection, professional judgment, legal review, or safety accountability.

### Deployment Geography for Use:

Global, with artifact content tailored to Russian-language construction workflows and Russian standards.

## Known Risks and Mitigations:

Risk: Packaged installer, build, or smoke-test scripts may be broken or unsafe to run as-is.

Mitigation: Review scripts before execution, repair failing installation/test paths, and do not run build.sh with untrusted version input.

Risk: Construction, safety, legal, and standards outputs may be incomplete, outdated, or wrong for a specific site.

Mitigation: Use outputs as drafts only and require review by qualified construction, safety, legal, or standards professionals before operational use.

Risk: The skill may prompt users to enter client, site-security, personal, or confidential project data.

Mitigation: Minimize sensitive inputs, redact unnecessary confidential details, and apply the user's data-handling controls before sharing project information with an agent.

Risk: The skill cannot perform physical site inspection or enforce safety behavior.

Mitigation: Keep an accountable foreman or qualified person physically present for measurements, acceptance decisions, incident response, and safety enforcement.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/raaipro/skills/raai-foreman-pro)
- [Publisher Profile](https://clawhub.ai/user/raaipro)
- [Quick Start](artifact/examples/quick-start.md)
- [Onboarding Guide](artifact/docs/onboarding.md)
- [Anti-Fail and Limits Guide](artifact/docs/anti-fail.md)
- [ROI Guide](artifact/docs/roi.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tables, checklists, document templates, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primarily Russian-language construction-management outputs that depend on accurate site facts, current standards, and professional verification.]

## Skill Version(s):

3.5.4 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
