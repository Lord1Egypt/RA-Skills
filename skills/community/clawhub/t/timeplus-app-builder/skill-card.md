## Description: <br>
Use when creating, packaging, or installing a Timeplus app (.tpapp) by converting SQL resources and dashboards into an installable app package, writing manifests, applying template variables, building dashboard JSON, or debugging install failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gangtao](https://clawhub.ai/user/gangtao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, package, install, and troubleshoot Timeplus .tpapp bundles that provision streaming DDL resources and dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Timeplus app bundles can create persistent server resources such as streams, views, tasks, alerts, inputs, external streams, Python UDFs, named collections, and dashboards. <br>
Mitigation: Review generated manifests, DDL files, dashboard JSON, webhook targets, package lists, scheduled tasks, alerts, input bindings, and external stream definitions before installing an app. <br>
Risk: App configuration may include sensitive credentials that are rendered into install-time resources. <br>
Mitigation: Review secret config fields and named collections before installation, and avoid placing credentials directly in Python UDF bodies or visible resource definitions. <br>


## Reference(s): <br>
- [Dashboard JSON Specification](references/dashboard-spec.md) <br>
- [Timeplus Documentation](https://docs.timeplus.com) <br>
- [Timeplus Proton Repository](https://github.com/timeplus-io/proton) <br>
- [Sprig Template Functions](https://masterminds.github.io/sprig/) <br>
- [Timeplus SQL Guide](https://github.com/timeplus-io/AgentSkills/tree/main/timeplus-sql-guide) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with YAML, SQL, JSON, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include .tpapp directory structure, manifest.yaml fields, DDL templates, dashboard JSON, install commands, and debugging guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
