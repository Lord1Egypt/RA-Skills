## Description:

Full sales system: scripts, objection handling, follow-up, BANT and MEDDIC qualification, pipeline management and commercial offers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raaipro](https://clawhub.ai/user/raaipro)

### License/Terms of Use:

MIT-0

## Use Case:

Sales leaders, business owners, and commercial teams use Sales Pro to generate sales scripts, objection handling, follow-up sequences, lead qualification, pipeline reports, win/loss analysis, unit economics, and ROI-backed commercial offers for repeatable B2B sales processes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer lead and deal details may be stored in agent memory and synchronized through Supabase without enough scoping or consent detail.

Mitigation: Use the skill with real customer data only after explicit opt-in storage is configured, the Supabase tenant and access rules are defined, shared fields are minimized, and deletion or sync-disable procedures are confirmed.

Risk: Pipeline forecasts, qualification scores, ROI calculations, and win/loss analysis can mislead sales decisions when the configured business data or deal records are incomplete or stale.

Mitigation: Require accurate config.yaml inputs, keep pipeline data current, and review generated sales analysis before using it for management decisions or customer-facing commitments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/raaipro/skills/raai-sales-pro)
- [README](artifact/README.md)
- [Onboarding Guide](artifact/docs/onboarding.md)
- [Anti-Fail Guidance](artifact/docs/anti-fail.md)
- [ROI Guide](artifact/docs/roi.md)
- [Quick Start Examples](artifact/examples/quick-start.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown and plain text with optional configuration files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces sales workflow artifacts such as scripts, message sequences, qualification scoring, pipeline summaries, win/loss analysis, ROI calculations, and implementation guidance.]

## Skill Version(s):

3.5.4 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
