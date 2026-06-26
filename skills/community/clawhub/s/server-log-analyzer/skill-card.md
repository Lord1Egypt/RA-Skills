## Description: <br>
Analyzes server log files to detect problems, extract performance metrics, and provide troubleshooting insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengaojian](https://clawhub.ai/user/chengaojian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to inspect structured server logs, identify errors and Python exceptions, summarize performance metrics, and guide troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Log files may contain secrets, tokens, personal data, or confidential production details. <br>
Mitigation: Provide only intended log files and review logs for sensitive data before analysis. <br>
Risk: Broad trigger phrases could activate the skill unexpectedly. <br>
Mitigation: Use explicit prompts and confirm the target log file before running analysis. <br>


## Reference(s): <br>
- [Server Log Analyzer](https://clawhub.ai/chengaojian/server-log-analyzer) <br>
- [Log Reference](references/log_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal report or JSON with summary, exceptions, performance, issues, and module statistics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local log files as input; no external dependencies are documented.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
