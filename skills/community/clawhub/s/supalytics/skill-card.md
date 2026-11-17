## Description:

Query web analytics data using the Supalytics CLI. Use when the user wants to check pageviews, visitors, top pages, traffic sources, referrers, countries, revenue metrics, conversions, funnels, events, or realtime visitors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yogesharc](https://clawhub.ai/user/yogesharc)

### License/Terms of Use:


## Use Case:

Developers, operators, and site owners use this skill to query Supalytics web analytics from an agent through the Supalytics CLI, including traffic, revenue, conversion, funnel, event, and realtime visitor metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance includes piping a remote Bun install script into a shell.

Mitigation: Review the install path first and prefer a pinned, verified Bun and Supalytics CLI installation.

Risk: Troubleshooting guidance includes sudo symlinks into /usr/local/bin, which can affect the whole system.

Mitigation: Avoid creating system-wide symlinks unless the user explicitly approves and understands the impact.

Risk: Site add, update, and remove commands are administrative actions on Supalytics resources.

Mitigation: Require explicit user approval before running site management commands.

## Reference(s):

- [Supalytics](https://supalytics.co)
- [Bun Runtime](https://bun.sh)
- [ClawHub Skill Page](https://clawhub.ai/yogesharc/skills/supalytics)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Supalytics CLI and an authenticated Supalytics account; analytics commands can return human-readable tables or raw JSON when --json is used.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
