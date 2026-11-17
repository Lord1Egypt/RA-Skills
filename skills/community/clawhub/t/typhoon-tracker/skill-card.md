## Description:

Typhoon Tracker helps agents assess Western North Pacific typhoon tracks, landfall risk, wind and rain impacts, transportation disruption, activity feasibility, residual vortices, and nearshore tropical systems using multi-source weather evidence and case-based protocols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[firefljay](https://clawhub.ai/user/firefljay)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to have an agent produce typhoon impact assessments, travel and transportation risk judgments, emergency preparation guidance, and optional reports for China coastal and broader Western North Pacific scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad auto-activation rules may cause the skill to influence travel or weather answers even when the user did not explicitly ask for typhoon analysis.

Mitigation: Review trigger scope before deployment and require explicit user confirmation before high-impact travel, event, or emergency decisions.

Risk: The skill may perform live web searches and write persistent weather or case records.

Mitigation: Run it in an isolated environment, confirm long-term file writes with the user, and keep timestamps and source labels visible in generated reports.

Risk: The documented installer and PDF conversion flow can introduce supply-chain or document-rendering risk.

Mitigation: Avoid curl-to-bash installation, pin dependencies, and convert only trusted Markdown with network loading and active HTML disabled.

## Reference(s):

- [Project homepage](https://github.com/FireflJay/typhoon-tracker)
- [ClawHub skill page](https://clawhub.ai/firefljay/skills/typhoon-tracker)
- [Typhoon Bavi (2609) Case Data](references/bavi_2609_case_data.md)
- [Typhoon Dolphin (2613) Case Data](references/dolphin_2613_case_data.md)
- [Typhoon Nangka (2617) Case Data](references/nangka_2617_case_data.md)
- [Typhoon Saudel (2618) Case Data](references/saudel_2618_case_data.md)
- [Typhoon Gaenari (2620) Case Data](references/gaenari_2620_case_data.md)
- [Nearshore Tropical System Protocol](references/nearsea_system_protocol.md)
- [Empty-Window Convection Protocol](references/empty_window_convection_protocol.md)
- [Deployment and Fallback Guide](references/deployment_guide.md)
- [Mobile Channel Guide](references/mobile_channel_guide.md)
- [Report Template Guide](references/report_template_guide.md)
- [PDF Conversion Guide](references/pdf_conversion_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with structured tables, optional Markdown report files, shell commands, configuration guidance, and optional PDF artifacts when explicitly requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform live web searches, write persistent weather or case records, and convert Markdown reports to PDF when configured.]

## Skill Version(s):

1.2.0 (source: frontmatter, release evidence, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
