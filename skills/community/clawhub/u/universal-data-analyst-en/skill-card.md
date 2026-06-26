## Description: <br>
Performs automated data analysis workflows that load datasets, validate data quality, generate LLM prompts for ontology and method selection, create Python analysis scripts, and produce Markdown or HTML reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yamaz49](https://clawhub.ai/user/yamaz49) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to profile uploaded datasets, assess data quality, plan suitable analysis methods, generate executable Python analysis scripts, and assemble report outputs for exploratory or decision-support analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dataset-derived prompts or reports may expose sensitive data to external LLM providers. <br>
Mitigation: Redact sensitive fields before use and review generated prompt files before sending them to any third-party model. <br>
Risk: Generated or supplied Python analysis scripts may perform unsafe or unintended actions when executed. <br>
Mitigation: Review scripts before execution and run them in an isolated environment or container with only the needed files mounted. <br>
Risk: SQL database analysis can expose more data than intended if broad credentials or queries are used. <br>
Mitigation: Use read-only, least-privilege database credentials and narrow SQL queries to the minimum dataset needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yamaz49/universal-data-analyst-en) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Flow Health Monitor Guide](artifact/FLOW_HEALTH_MONITOR_GUIDE.md) <br>
- [Quick Reference](artifact/quick_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, Python code, shell commands, generated prompt files, charts, and HTML or Markdown analysis reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create session directories containing prompt files, validation reports, generated scripts, charts, and report artifacts.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact files also mention 1.0.0, 1.1.0, and 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
