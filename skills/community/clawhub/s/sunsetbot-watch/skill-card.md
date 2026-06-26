## Description: <br>
Automates sunset glow forecast queries on sunsetbot.top for a requested city and optional date, extracting vividness and aerosol (AOD) values and returning a formatted assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weiwei106](https://clawhub.ai/user/weiwei106) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check sunset glow potential for a specified city and date, with vividness and aerosol readings interpreted into a short forecast-style result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation sends the requested city and date to sunsetbot.top. <br>
Mitigation: Avoid entering sensitive locations or dates, and review the external site interaction before use in restricted environments. <br>
Risk: Forecast values and derived conclusions may be incomplete, unavailable, or misleading if the external page changes or returns stale data. <br>
Mitigation: Review the extracted vividness and aerosol values and treat the conclusion as forecast guidance rather than a guaranteed outcome. <br>


## Reference(s): <br>
- [Sunsetbot detailed forecast page](https://sunsetbot.top/detailed/) <br>
- [ClawHub skill page](https://clawhub.ai/weiwei106/sunsetbot-watch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with date, vividness, aerosol, and conclusion fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires browser access to sunsetbot.top and sends the requested city and date to that site.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
