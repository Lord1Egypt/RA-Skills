## Description: <br>
报告工具包-免费版 helps individual developers and small projects configure data sources, schedules, output formats, and delivery channels for recurring reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and small project maintainers use this skill to define report data sources, schedules, formats, and delivery channels for recurring personal or project reports such as revenue summaries, GitHub activity reports, and system usage reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad execution and database-related authority for report data sources, including command and query-style inputs. <br>
Mitigation: Use only explicit report configurations from trusted sources, avoid command data sources unless the exact command is harmless and necessary, and review database or shell actions before execution. <br>
Risk: Scheduled reports and email delivery can run or send information without enough confirmation if configured too broadly. <br>
Mitigation: Confirm scheduled jobs and email delivery settings before enabling them, and keep generated report destinations limited to intended recipients and paths. <br>
Risk: API and SMTP credentials may be exposed if copied into shared terminals, recorded sessions, or report configuration files. <br>
Mitigation: Store credentials in controlled environment variables and avoid pasting secrets into shared or recorded terminals or persisted report configs. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML, bash, and JSON examples; generated reports may be text, Markdown, or HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The free edition describes up to five report configurations and supports chat, file, and email delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
