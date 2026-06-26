## Description: <br>
Searches Reddit posts through Apify and helps an agent summarize community sentiment, themes, and notable discussions for a user-provided topic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netmsglog](https://clawhub.ai/user/netmsglog) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill when they want an agent to search public Reddit discussions, inspect returned post metadata, and summarize community sentiment on a specific topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and related request data are sent to Apify/Reddit-related services. <br>
Mitigation: Avoid confidential queries and review topics before running the search. <br>
Risk: The skill requires an APIFY_TOKEN that could be misused if exposed. <br>
Mitigation: Use a limited Apify token and keep it out of source control, logs, shared terminals, and chat transcripts. <br>
Risk: Apify usage may incur costs. <br>
Mitigation: Set spending limits or monitor Apify usage before repeated or broad searches. <br>


## Reference(s): <br>
- [Reddit Explore on ClawHub](https://clawhub.ai/netmsglog/reddit-explore) <br>
- [Apify Setup Guide](references/apify-setup.md) <br>
- [Apify Console](https://console.apify.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary based on JSON Reddit search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, apify-client, and APIFY_TOKEN; search queries are sent to Apify/Reddit-related services.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
