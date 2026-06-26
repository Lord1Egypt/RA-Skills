## Description: <br>
X Ads data analysis and reporting via x-ads-cli for checking ad performance, campaign stats, account structure, creatives, targeting, conversions, billing, and reach. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bin-huang](https://clawhub.ai/user/bin-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing analysts, growth teams, and developers use this skill to query X/Twitter Ads accounts with x-ads-cli, retrieve JSON analytics, inspect campaign entities, and prepare performance or billing reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive ad account, billing, audience, payment-method, and conversion details. <br>
Mitigation: Use least-privilege X Ads credentials and avoid printing, sharing, or retaining raw sensitive details unless needed for the task. <br>
Risk: OAuth credentials are required to access X Ads data. <br>
Mitigation: Store credential files securely, prefer scoped credentials where available, and verify credentials before running account or reporting commands. <br>
Risk: The workflow depends on installing and using the referenced x-ads-cli package. <br>
Mitigation: Install only when the package and its npm/GitHub provenance are trusted for the intended environment. <br>


## Reference(s): <br>
- [x-ads-cli documentation](https://github.com/Bin-Huang/x-ads-cli) <br>
- [X Ads API introduction](https://docs.x.com/x-ads-api/introduction) <br>
- [X Ads API campaign management](https://docs.x.com/x-ads-api/campaign-management) <br>
- [X Ads API analytics](https://docs.x.com/x-ads-api/analytics) <br>
- [X Ads API getting started](https://docs.x.com/x-ads-api/getting-started) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [x-ads-cli command outputs are JSON; synchronous stats requests support up to 7 days per request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
