## Description: <br>
Search X (Twitter) posts using the xAI API. Use when the user wants to find tweets, search X/Twitter, look up what people are saying on X, or find social media posts about a topic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jaaneek](https://clawhub.ai/user/Jaaneek) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to search current X/Twitter posts through xAI Grok and receive readable results with author details and citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a user-provided xAI API key and sends search queries to xAI. <br>
Mitigation: Use a dedicated API key where possible, avoid committing keys to source control or shared configuration, and monitor quota or costs. <br>
Risk: Returned X/Twitter content may be untrusted or misleading. <br>
Mitigation: Verify important claims through the citations and original posts before relying on the results. <br>


## Reference(s): <br>
- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search) <br>
- [xAI Console](https://console.x.ai) <br>
- [ClawHub X Search listing](https://clawhub.ai/Jaaneek/x-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown text with citations and optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Searches may be filtered by handles, excluded handles, date range, and image or video understanding flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
