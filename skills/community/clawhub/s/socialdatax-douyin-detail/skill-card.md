## Description: <br>
Retrieves structured Douyin work details for content analysis, including post details, interaction metrics, image/text details, and related media fields through SocialDataX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve read-only social media work details from SocialDataX for Douyin content research and interaction analysis. The artifact also documents Weibo and WeChat Channels detail retrieval through the same API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Douyin-focused name understates that the artifact also covers Weibo and WeChat Channels detail retrieval. <br>
Mitigation: Confirm the intended platform before running a lookup and disclose when using non-Douyin commands. <br>
Risk: The skill requires SOCIALDATAX_API_KEY for SocialDataX data calls. <br>
Mitigation: Use a scoped SocialDataX key, keep it in environment variables, and avoid sharing it in prompts or logs. <br>


## Reference(s): <br>
- [SocialDataX API access homepage](https://socialdatax.52choujiang.com/?from=clawhub) <br>
- [ClawHub skill page](https://clawhub.ai/devinchen2014/socialdatax-douyin-detail) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the SocialDataX CLI prints JSON containing platform, tool, arguments, and data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, npm, and SOCIALDATAX_API_KEY; detail lookups are read-only.] <br>

## Skill Version(s): <br>
0.1.8 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
