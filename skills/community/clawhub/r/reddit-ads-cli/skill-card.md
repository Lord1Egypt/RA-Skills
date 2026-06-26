## Description: <br>
Reddit Ads data analysis and reporting via reddit-ads-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bin-huang](https://clawhub.ai/user/bin-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketers, analysts, and developers use this skill to query Reddit Ads accounts, inspect campaign hierarchy, generate performance reports, review creatives, check pixels, and explore audience or targeting data through the reddit-ads-cli command line tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Reddit Ads OAuth access token and may expose sensitive advertising account data if credentials or command output are shared carelessly. <br>
Mitigation: Use the least-privileged token available, keep credentials out of chat and logs, and store tokens only in the documented environment variable or credentials file. <br>
Risk: The skill depends on the external reddit-ads-cli npm package for Reddit Ads API access. <br>
Mitigation: Install only after trusting the external package source and review commands before running them, especially commands that appear to change audiences or account data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bin-huang/reddit-ads-cli) <br>
- [reddit-ads-cli documentation](https://github.com/Bin-Huang/reddit-ads-cli) <br>
- [Reddit Ads API v3 docs](https://ads-api.reddit.com/docs/v3) <br>
- [Reddit OAuth2 authentication](https://github.com/reddit-archive/reddit/wiki/OAuth2) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying CLI returns pretty-printed JSON by default and supports compact JSON for piping.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
