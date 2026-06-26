## Description: <br>
SocialDataX Douyin Comments helps agents retrieve and analyze Douyin comments and replies for audience feedback, sentiment themes, pain points, FAQs, and discussion summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to retrieve Douyin comment threads or replies with a SocialDataX API key, then summarize themes, sentiment signals, objections, pain points, FAQs, and discussion patterns. The artifact also documents Weibo and WeChat Channels comment retrieval, so users should review the broader platform coverage before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires SOCIALDATAX_API_KEY for SocialDataX data calls. <br>
Mitigation: Install it only when comfortable granting the SocialDataX CLI access to that key, keep the key in environment variables, and review retrieved data before sharing it. <br>
Risk: The Douyin-focused listing understates that the artifact also documents Weibo and WeChat Channels comment retrieval. <br>
Mitigation: Review the broader platform coverage before use and constrain prompts, CLI commands, or MCP calls to the intended platform. <br>
Risk: Unbounded pagination options such as --all can retrieve more comments than intended. <br>
Mitigation: Use page limits or --max-items for controlled retrieval unless exhaustive collection is explicitly required. <br>


## Reference(s): <br>
- [SocialDataX API access homepage](https://socialdatax.52choujiang.com/?from=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include paginated comment data, merged item counts, reply metadata, media URLs, and analysis summaries.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
