## Description: <br>
Snapchat Ads data analysis and reporting via snapchat-ads-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bin-huang](https://clawhub.ai/user/bin-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and marketing operators use this skill to query Snapchat Ads account structure, campaign performance, audience data, delivery status, and billing details through a read-only CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses sensitive Snapchat Ads business data, including billing, member, audience, and customer-related details. <br>
Mitigation: Use a least-privilege Snapchat OAuth token and request only the data needed for the user's task. <br>
Risk: Outputs may include OAuth tokens, identifiers, customer or audience details, and financial data. <br>
Mitigation: Redact sensitive values unless the user explicitly needs them for the current analysis. <br>


## Reference(s): <br>
- [SnapChat Ads CLI on ClawHub](https://clawhub.ai/bin-huang/snapchat-ads-cli) <br>
- [snapchat-ads-cli documentation](https://github.com/Bin-Huang/snapchat-ads-cli) <br>
- [Snapchat Marketing API overview](https://developers.snap.com/api/marketing-api/Ads-API) <br>
- [Snapchat Marketing API authentication](https://developers.snap.com/api/marketing-api/Ads-API/authentication) <br>
- [Snapchat Marketing API measurement](https://developers.snap.com/api/marketing-api/Ads-API/measurement) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI returns pretty-printed JSON by default and compact JSON when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
