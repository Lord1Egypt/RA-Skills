## Description: <br>
Research TikTok ads alongside TikTok Shop products and stores using PipiAds ad and TikTok Shop analytics tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanyanggod](https://clawhub.ai/user/fanyanggod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, sellers, and growth teams use this skill to connect TikTok ad creative research with TikTok Shop product and store performance signals. It helps compare creative patterns, product momentum, GMV, sales, pricing, and store positioning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the configured npm MCP server runs third-party package code in the agent environment. <br>
Mitigation: Confirm trust in the pipiads-mcp-server package before installation and deploy only in controlled environments. <br>
Risk: The skill requires PIPIADS_API_KEY and can consume paid API credits during broad searches or detail requests. <br>
Mitigation: Scope the API key to systems you control, monitor billing or credit usage, and ask for category, region, price band, and time window before broad research. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fanyanggod/tiktok-shop-ad-library-analytics) <br>
- [PipiAds homepage](https://www.pipiads.com) <br>
- [PipiSpy account and billing](https://www.pipispy.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with concise setup instructions, research workflow guidance, and summarized analytics findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses PIPIADS_API_KEY and may consume PipiAds account credits during list, search, and detail requests.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
