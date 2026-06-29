## Description: <br>
XPeng Monitor aggregates XPeng China delivery lead-time data and Europe BEV registration data into model-level tables, reports, and summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[svenzhexu](https://clawhub.ai/user/svenzhexu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to answer XPeng delivery and market-monitoring questions by fetching China model lead times and Europe BEV registration data. It produces tabular results, JSON summaries, and concise analysis for the requested market scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may request eu-evs.com credentials and can retain session cookies in scripts/.eu-session.json. <br>
Mitigation: Use a dedicated eu-evs.com account with a unique temporary password, never reuse an important password, and delete scripts/.eu-session.json after use if session retention is not desired. <br>
Risk: Europe BEV results cover only eu-evs.com countries that disclose daily data and can be misread as total Europe-wide XPeng sales. <br>
Mitigation: Label outputs as a limited daily-disclosure-country view and avoid presenting the numbers as total European market sales. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/svenzhexu/xpeng-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/svenzhexu) <br>
- [XPeng store car series API](https://store.xiaopeng.com/api/v1/client/orion/carSeries/navigationBar) <br>
- [eu-evs.com XPENG daily BEV data template](https://eu-evs.com/brands/XPENG/ALL_DAILY/Models-Daily/Year/${year}) <br>
- [eu-evs.com registration page](https://eu-evs.com/register) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables and prose, compact JSON, and Node.js command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or reuse scripts/.eu-session.json for eu-evs.com session cookies when login is required.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
