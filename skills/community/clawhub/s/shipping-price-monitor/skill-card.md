## Description: <br>
Monitor shipping carrier prices from Excel files and send alerts when prices drop below thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[start-LL04](https://clawhub.ai/user/start-LL04) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Logistics operators and developers use this skill to monitor shipping-carrier spreadsheet price feeds, apply configurable route and equipment thresholds, and notify teams when qualifying lower prices appear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route, carrier, sailing date, and price data can be sent automatically to chat services. <br>
Mitigation: Review notification settings before enabling monitoring and send alerts only to approved WeCom, Feishu, or OpenClaw recipients. <br>
Risk: The default OpenClaw target is a named recipient. <br>
Mitigation: Confirm or change the target recipient before testing or starting monitoring. <br>
Risk: Webhook URLs are sensitive and may expose alert delivery channels if shared. <br>
Mitigation: Store webhook URLs as secrets, prefer known WeCom and Feishu webhook domains, and rotate any webhook that may have been exposed. <br>
Risk: Monitoring a broad folder could process unintended spreadsheets. <br>
Mitigation: Use a dedicated watch folder containing only intended shipping price spreadsheets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/start-LL04/shipping-price-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/start-LL04) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, configuration snippets, and alert text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces alert summaries from Excel rows and configured rules; notifications may be sent through OpenClaw, WeCom, or Feishu.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
