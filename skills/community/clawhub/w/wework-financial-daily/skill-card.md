## Description: <br>
Generates a daily financial analysis teaching report with BTC and AAPL chart examples, saves an HTML courseware file, uploads the report, and sends a WeCom message summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leozhang1431](https://clawhub.ai/user/leozhang1431) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, educators, and developers use this skill to automate a daily financial technical-analysis lesson, including generated HTML courseware, chart images, and a WeCom notification. It is intended for teaching and report delivery workflows, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedded WeCom and MinIO credentials may expose messaging or storage accounts. <br>
Mitigation: Remove embedded credentials, rotate any exposed values, and load secrets only from protected user-controlled configuration. <br>
Risk: Generated reports may be published to public external storage. <br>
Mitigation: Make external upload opt-in, use private storage or short-lived links, and review report contents before sharing. <br>
Risk: Scheduled execution with administrator or highest privileges increases the impact of misuse or compromise. <br>
Mitigation: Run scheduled tasks as a normal user with the minimum permissions required. <br>
Risk: Simulated financial data may be mistaken for current market data or investment guidance. <br>
Mitigation: Clearly label simulated data and keep the teaching disclaimer visible in generated reports and messages. <br>


## Reference(s): <br>
- [Cron setup reference](references/cron-setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/leozhang1431/wework-financial-daily) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [HTML report file, Markdown WeCom message, chart images, and setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured WeCom and storage credentials; generated market data is simulated unless the user replaces the data source.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
