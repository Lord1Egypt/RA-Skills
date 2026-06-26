## Description: <br>
Convert a markdown file containing SQL queries into a BI dashboard specification and UI scaffold, including query parsing, metric and dimension inference, chart recommendation, filter design, and layout generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bamboo9805](https://clawhub.ai/user/bamboo9805) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to turn SQL markdown collections into dashboard artifacts, static UI scaffolds, and optional local demo services. It is intended for prototype BI workflows where SQL-derived metrics, dimensions, filters, charts, and layout need to be generated quickly for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated backend and frontend demo services may expose sensitive SQL-derived business metadata if run beyond a local development environment. <br>
Mitigation: Review generated service code and keep demo services bound to local, trusted environments unless they are hardened for deployment. <br>
Risk: Generated dashboards can reflect incorrect metric, dimension, filter, or chart inferences from heuristic SQL parsing. <br>
Mitigation: Review generated query catalogs, semantic catalogs, chart plans, and dashboard specifications before using them for business decisions. <br>
Risk: Generated UI output can rely on external CDN assets that may not meet production availability or supply-chain requirements. <br>
Mitigation: Vendor or pin external assets before production use. <br>


## Reference(s): <br>
- [SQL style guide](references/sql_style.md) <br>
- [Chart rules](references/chart_rules.md) <br>
- [Dashboard layout rules](references/layout_rules.md) <br>
- [Python 3.11 installation guide](references/install_python311.md) <br>
- [ClawHub skill page](https://clawhub.ai/bamboo9805/sql-to-bi-builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus generated JSON, HTML, JavaScript, CSS, Python service code, and configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates local files including query_catalog.json, semantic_catalog.json, chart_plan.json, dashboard.json, a static UI scaffold, and optional backend/frontend demo services.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
