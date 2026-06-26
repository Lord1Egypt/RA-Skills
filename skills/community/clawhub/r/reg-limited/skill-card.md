## Description: <br>
Vehicle restriction query and reminder tool for Chinese cities. Query daily restrictions and set scheduled reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chandler0714](https://clawhub.ai/user/chandler0714) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Drivers and automation agents use this skill to query Chinese city vehicle restriction rules, check whether a plate is restricted today, and manage local restriction reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved reminders may include vehicle plate numbers in a local plaintext configuration file. <br>
Mitigation: Protect or delete ~/.reg-limited/config.json when plate numbers are sensitive. <br>
Risk: The CLI fetches Beijing restriction data online and may fall back to local rules if the request or parsing fails. <br>
Mitigation: Verify important restriction results against official traffic sources before relying on them. <br>
Risk: The artifact describes Feishu or Telegram-style notification channels, but the current script only stores local reminder records. <br>
Mitigation: Treat reminder commands as local configuration management unless a future version implements external notifications. <br>


## Reference(s): <br>
- [Reg Limited ClawHub Release](https://clawhub.ai/chandler0714/reg-limited) <br>
- [Beijing Traffic Management Bureau Restriction Page](https://jtgl.beijing.gov.cn/jgj/lszt/659722/660341/index.html) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON responses and CLI command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store reminder entries, including plate numbers, in ~/.reg-limited/config.json.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
