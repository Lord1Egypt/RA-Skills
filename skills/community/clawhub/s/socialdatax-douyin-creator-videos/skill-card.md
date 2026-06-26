## Description: <br>
Helps agents retrieve and summarize Douyin creator works, image/text posts, short-drama series, recent publishing activity, and related creator content data through SocialDataX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch creator work lists or series data by profile URL or creator ID, then summarize publishing activity, media links, engagement counts, and author facts for content research and benchmarking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses SOCIALDATAX_API_KEY for external SocialDataX data calls. <br>
Mitigation: Configure the API key only in the runtime environment and avoid placing secrets in prompts, files, or shared output. <br>
Risk: Using unbounded pagination can return more creator content than intended. <br>
Mitigation: Set page or item limits for exploratory work and preserve returned pagination tokens exactly when continuing a result chain. <br>
Risk: Returned social media metadata, media links, and engagement counts may be incomplete or change over time. <br>
Mitigation: Treat returned data as source evidence from the API response and review summaries before using them for decisions. <br>


## Reference(s): <br>
- [SocialDataX API access](https://socialdatax.52choujiang.com/?from=clawhub) <br>
- [ClawHub skill page](https://clawhub.ai/devinchen2014/socialdatax-douyin-creator-videos) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with optional shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SOCIALDATAX_API_KEY and may include pagination tokens, creator identifiers, media links, interaction counts, and author facts returned by SocialDataX.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
