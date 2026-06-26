## Description: <br>
Automates weekly work report generation by logging into a report system, fetching team report data, summarizing it with AI, and producing a formatted Word document. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaillera999](https://clawhub.ai/user/kaillera999) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and team leads use this skill to collect weekly report entries for a configured team, summarize this week's work and next week's plans, and generate a Word report for review or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles workplace credentials and stores local token and data caches. <br>
Mitigation: Use scoped credentials where possible, protect the working directory, and clear .token_cache and .data_cache after generating the report. <br>
Risk: Report contents may be sent to a configured external AI provider for summarization. <br>
Mitigation: Confirm that the configured LLM provider and base URL are approved for the report contents before use. <br>
Risk: Setup uses remote dependency installers and browser automation dependencies. <br>
Mitigation: Review setup.sh and dependency sources before installation, and run setup in a trusted environment. <br>
Risk: An incorrect report-system URL or LLM base URL could expose credentials or report contents. <br>
Mitigation: Review the configured HTTP report-system URL and LLM base URL before login or generation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kaillera999/weekly-report-openclaw) <br>
- [Configuration Guide](references/configuration.md) <br>
- [Workflow Guide](references/workflow.md) <br>
- [Setup Script](scripts/setup.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime output includes JSON status and generated .docx report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus WEEKLY_REPORT_USERNAME, WEEKLY_REPORT_PASSWORD, and DEEPSEEK_API_KEY; may use local token and data caches during report generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
