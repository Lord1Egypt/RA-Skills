## Description: <br>
Design and harden AdMapix-style raw data workflows for creative, app, ranking, revenue, and analytics datasets before they become dashboards or agent tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, growth analysts, and agent builders use this skill to plan reproducible raw-to-clean data workflows for AdMapix-style advertising, app analytics, ranking, revenue, and creative datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The broad trigger wording may activate the skill for generic data, ETL, revenue, or ranking requests outside the intended AdMapix-style workflow. <br>
Mitigation: Confirm the request is about AdMapix-style raw advertising or app-market data before relying on the skill's recommendations. <br>
Risk: Workflow advice for raw data pipelines can lead to misleading dashboards or agent outputs if provenance, schema drift, or partial exports are missed. <br>
Mitigation: Keep immutable raw captures separate from cleaned outputs, record source and transform metadata, and review validation checks before publishing downstream results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/software-data-admapix-raw-developer-helper-040526) <br>
- [Requirement Plan](references/requirement-plan.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with optional code snippets, validation rules, data-model outlines, checklists, and implementation plans.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source-to-table maps, audit-trail fields, local CSV/JSON/SQLite/DuckDB prototyping steps, and consumer-facing caveats.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
