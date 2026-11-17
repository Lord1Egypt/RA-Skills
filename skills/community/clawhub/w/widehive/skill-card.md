## Description:

WideHive orchestrates wide research by fanning out context-isolated sub-agents over large target lists, merging their structured results with code, and synthesizing scenario-shaped reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxdwind](https://clawhub.ai/user/yxdwind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use WideHive to run large batch research tasks across papers, companies, repositories, products, or other target lists, then merge per-object results into verifiable tables, reports, dashboards, or watch-mode change reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Large research runs require web access, sub-agent spawning, and workspace file read/write privileges.

Mitigation: Run the skill only in contained workspaces and review the planned target list, object count, fields, and cost scale before fan-out.

Risk: Untrusted or malformed target slugs could cause unintended local file access when result paths are constructed.

Mitigation: Accept target lists only from trusted sources and enforce a conservative slug pattern using letters, digits, underscores, and hyphens.

Risk: Generated CSV files may expose spreadsheet users to formula-like cell behavior when opened in Excel or similar tools.

Mitigation: Neutralize formula-like cells before opening or sharing spreadsheet exports from untrusted inputs.

## Reference(s):

- [WideHive ClawHub release](https://clawhub.ai/yxdwind/skills/widehive)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with JSON run files, CSV/JSON merge outputs, optional self-contained HTML dashboards, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates per-object result JSON files, merged.csv, merged.json, reports, optional watch reports, and optional corpus or dashboard files.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
