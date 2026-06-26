## Description: <br>
Sinopec Oil Price queries real-time Sinopec gasoline and diesel prices by province and reports price changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[15878033657](https://clawhub.ai/user/15878033657) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to look up current Sinopec fuel prices for Chinese provinces, including gasoline and diesel prices and recent price movement data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Province lookup requests are sent to the Sinopec API. <br>
Mitigation: Use the skill only when sending province-level fuel-price queries to Sinopec is acceptable for the environment. <br>
Risk: Monitoring writes local oil-price history files. <br>
Mitigation: Run monitoring in an intended workspace and review or remove stored history files when they are no longer needed. <br>
Risk: Scheduled monitoring can create recurring network activity. <br>
Mitigation: Enable cron or scheduled checks only when recurring price lookups are intentional. <br>
Risk: The skill depends on axios for HTTP requests. <br>
Mitigation: Install with the bundled lockfile or update the HTTP dependency deliberately during maintenance. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/15878033657/sinopec-oil-price) <br>
- [API Reference](references/api.md) <br>
- [Usage Examples](references/examples.md) <br>
- [Sinopec mobile API endpoint](https://cx.sinopecsales.com/yjkqiantai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Structured JSON objects and plain-text oil price messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts province_id or province_name; monitoring can persist local history for price-change comparisons.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
