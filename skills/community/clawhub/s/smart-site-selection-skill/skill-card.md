## Description:

AI-assisted site-selection skill for physical retail businesses that collects customer and strategy inputs, uses AMap location data, and generates ranked location insights with an interactive report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hzhyjr2021-beep](https://clawhub.ai/user/hzhyjr2021-beep)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators use this skill to evaluate candidate retail locations after providing target customer and operating strategy details. The agent asks for missing strategic inputs, gathers top candidate coordinates, prepares market commentary, and hands data to supporting scripts that produce the final site-selection report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AMap API keys may be exposed through generated reports or shared artifacts.

Mitigation: Use a restricted AMap key and remove or replace keys before sharing generated reports.

Risk: Generated HTML report content may be unsafe until escaping and sanitization are verified.

Mitigation: Treat generated HTML as untrusted, review it before opening or sharing, and add escaping for user- and API-derived content.

Risk: Broad triggers, silent dependency installation, and uncontrolled file writes can create unexpected execution or workspace changes.

Mitigation: Install in an isolated environment, review requested actions before execution, pin dependencies, and constrain output locations.

Risk: Location rankings and recommendations can be misleading if source data, scoring assumptions, or user strategy inputs are incomplete.

Mitigation: Review the generated report against independent business data before making real site-selection decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hzhyjr2021-beep/skills/smart-site-selection-skill)
- [AMap Open Platform](https://console.amap.com)
- [AMap Place Around API endpoint](https://restapi.amap.com/v3/place/around)
- [AMap Static Map API endpoint](https://restapi.amap.com/v3/staticmap)
- [ECharts CDN dependency](https://cdn.staticfile.net/echarts/5.5.0/echarts.min.js)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Text guidance and status messages plus a generated single-file HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AMAP_WEBSERVICE_KEY and may write generated report files to the current working directory.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
