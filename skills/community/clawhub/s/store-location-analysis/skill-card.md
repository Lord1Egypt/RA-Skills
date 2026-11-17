## Description:

Analyzes store-location suitability using Amap geocoding, POI, traffic, and competitor data, then generates an interactive HTML report with scoring, charts, comparisons, and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators use this skill to evaluate whether a candidate address is suitable for a planned store type. The agent gathers required inputs, runs Amap-backed analysis, and produces a structured JSON result plus an interactive HTML location-analysis report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analyzed addresses and store types are sent to Amap during geocoding, POI, and traffic lookups.

Mitigation: Use the skill only when sharing those location details with Amap is acceptable, and avoid submitting sensitive private addresses or confidential expansion plans.

Risk: Generated HTML reports are active documents and may execute untrusted content when built from untrusted JSON, user inputs, or API data.

Mitigation: Open only reports produced from trusted inputs and data, preferably in a non-sensitive browser session; use a fixed version that escapes HTML and JavaScript values.

Risk: The report loads Chart.js from an external CDN.

Mitigation: Bundle Chart.js locally or use integrity-pinned dependencies before deploying the skill in controlled or enterprise environments.

## Reference(s):

- [API configuration guide](references/api_config.md)
- [Amap Web Service API key setup](https://console.amap.com/dev/key/app)
- [Amap Web Service API endpoint](https://restapi.amap.com/v3)
- [Baidu Maps heat map fallback reference](https://map.baidu.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, HTML files]

**Output Format:** [Markdown guidance with shell commands, JSON analysis output, and an interactive HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Amap Web Service API key supplied through AMAP_KEY or a command-line argument.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
