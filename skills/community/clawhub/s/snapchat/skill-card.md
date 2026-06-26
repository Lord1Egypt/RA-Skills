## Description: <br>
Snapchat Marketing API integration with managed OAuth for managing ad accounts, campaigns, ad squads, ads, creatives, audiences, targeting, and performance reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External advertisers, marketers, and developers use this skill to connect a Snapchat Marketing API account through Maton and manage advertising resources, reporting, targeting, and public ads library lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Maton API credentials provide access to the connected Snapchat Marketing API account. <br>
Mitigation: Install only when Maton-brokered Snapchat access is intended, keep MATON_API_KEY secret, and avoid exposing it in logs, prompts, or shared files. <br>
Risk: Campaign, budget, targeting, creative, audience, and delete actions can materially change an advertising account. <br>
Mitigation: Review the target resource and intended effect, then require explicit user approval before create, update, or delete requests. <br>
Risk: When multiple Snapchat connections exist, requests could affect the wrong account. <br>
Mitigation: Use the Maton-Connection header to select the intended connection before account-specific requests. <br>


## Reference(s): <br>
- [Maton](https://maton.ai) <br>
- [Snapchat Ads API Introduction](https://developers.snap.com/api/marketing-api/Ads-API/introduction) <br>
- [Snapchat API Patterns](https://developers.snap.com/api/marketing-api/Ads-API/api-patterns) <br>
- [Snapchat Campaign Management](https://developers.snap.com/api/marketing-api/Ads-API/campaigns) <br>
- [Snapchat Creative Management](https://developers.snap.com/api/marketing-api/Ads-API/creatives) <br>
- [Snapchat Targeting](https://developers.snap.com/api/marketing-api/Ads-API/targeting) <br>
- [Snapchat Ads Gallery API](https://developers.snap.com/api/marketing-api/Ads-Gallery-Api/using-the-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with HTTP endpoint examples and inline bash, Python, and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and, for account-specific actions, a connected Snapchat OAuth account.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
