## Description: <br>
Today Earnings retrieves Yahoo Finance earnings-calendar data for a selected date through a local Chrome extension and Native Messaging flow, returning ticker, earnings timing, and market-cap data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lhl09120](https://clawhub.ai/user/lhl09120) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance-focused agent users use this skill to install a local Chrome-based collection path and fetch a single day's public Yahoo Finance earnings-calendar entries as structured data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires loading a local Chrome extension and registering a Native Messaging host. <br>
Mitigation: Install it only on a trusted local machine, verify the extension ID during setup, and remove the extension and native-host registration when no longer needed. <br>
Risk: Results depend on Yahoo Finance page availability and page structure. <br>
Mitigation: If results are empty or requests time out, verify the Yahoo Finance earnings-calendar page manually and review the documented parsing assumptions. <br>


## Reference(s): <br>
- [Usage Guide](references/usage_guide.md) <br>
- [Yahoo Finance Earnings Calendar Technical Reference](references/yahoo_earnings_calendar.md) <br>
- [Technical Design](design.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/lhl09120/today-earnings) <br>
- [Yahoo Finance Earnings Calendar](https://finance.yahoo.com/calendar/earnings?day=YYYY-MM-DD&offset=0&size=100) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runtime output is a JSON array with code, earningType, and numeric marketCap fields.] <br>

## Skill Version(s): <br>
4.3.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
