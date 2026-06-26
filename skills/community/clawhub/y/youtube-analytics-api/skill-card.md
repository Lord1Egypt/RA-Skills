## Description: <br>
Access the YouTube Analytics API through Maton-managed OAuth to retrieve channel reports and manage video, playlist, and channel analytics groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query YouTube channel metrics such as views, watch time, subscribers, revenue, and performance by dimensions like day, country, or video. It also guides management of YouTube Analytics groups when the user has authorized the connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Maton API key and connected OAuth account can expose YouTube Analytics data for authorized channels. <br>
Mitigation: Keep MATON_API_KEY private, install only when the agent should access YouTube Analytics through Maton, and scope use to the intended connected account. <br>
Risk: Requests may target the wrong YouTube Analytics account when multiple Maton connections exist. <br>
Mitigation: List active connections and include the correct Maton-Connection header whenever multiple accounts are available. <br>
Risk: Group management operations can create, update, delete, add, or remove analytics groups and group items. <br>
Mitigation: Require the agent to list and confirm exact groups, items, and intended effects before any create, update, delete, or removal action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/youtube-analytics-api) <br>
- [Maton Homepage](https://maton.ai) <br>
- [YouTube Analytics API Overview](https://developers.google.com/youtube/analytics) <br>
- [YouTube Analytics API Reference](https://developers.google.com/youtube/analytics/reference) <br>
- [YouTube Analytics Metrics](https://developers.google.com/youtube/analytics/metrics) <br>
- [YouTube Analytics Dimensions](https://developers.google.com/youtube/analytics/dimensions) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with JSON examples and inline Python, JavaScript, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an authorized YouTube Analytics connection; API responses are JSON from the proxied YouTube Analytics service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
