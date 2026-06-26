## Description: <br>
Universal Data Analyst helps analyze uploaded tabular datasets by loading data, checking quality, generating LLM prompts for ontology and analysis planning, producing Python analysis scripts, and creating analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yamaz49](https://clawhub.ai/user/yamaz49) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other external users can use this skill to profile CSV, Excel, Parquet, JSON, or SQL-backed datasets, plan suitable analysis methods, generate Python analysis scripts, and produce data quality and analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate and run Python analysis scripts, which may behave unexpectedly or act on local data. <br>
Mitigation: Review generated scripts before execution and run them only in a restricted workspace or sandbox. <br>
Risk: Generated prompts may include dataset-derived content that could expose confidential, personal, regulated, or production data to an external LLM. <br>
Mitigation: Redact sensitive values and obtain approval before sending prompts or data summaries to external LLM providers. <br>
Risk: The skill supports SQL-backed data analysis and could be pointed at production databases. <br>
Mitigation: Use read-only database credentials, avoid production databases, and limit access to the minimum dataset needed for analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yamaz49/universal-data-analyst) <br>
- [README](artifact/README.md) <br>
- [Skill Overview](artifact/SKILL.md) <br>
- [Quick Reference](artifact/quick_reference.md) <br>
- [Flow Health Monitor Guide](artifact/FLOW_HEALTH_MONITOR_GUIDE.md) <br>
- [Updates](artifact/UPDATES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, HTML reports, JSON quality reports, Python scripts, generated prompts, chart files, and shell or Python usage snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates session-scoped analysis outputs; generated Python scripts and prompts should be reviewed before use with sensitive data or production systems.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata; artifact docs mention 1.0.0 and v1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
