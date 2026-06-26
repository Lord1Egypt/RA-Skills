## Description: <br>
Looks up Douyin creator profile data, including account basics, creator positioning, profile details, and audience scale, through SocialDataX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Douyin creator profile information from SocialDataX when given a sec_user_id, profile URL, short link, or shared profile text. It supports read-only profile reporting and separates returned profile facts from strategic interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a SocialDataX API key for data calls. <br>
Mitigation: Use the documented SOCIALDATAX_API_KEY environment variable and keep production credentials out of ordinary agent sessions. <br>
Risk: Returned social profile data may be incomplete, stale, or unsuitable for unsupported strategic conclusions. <br>
Mitigation: Report available profile fields as facts and keep strategic interpretation separate from the returned data. <br>
Risk: The skill runs a Node package or MCP tool to make external read-only data requests. <br>
Mitigation: Use the declared socialdatax-skills package and the documented SocialDataX homepage, and avoid login, posting, liking, commenting, or account-change workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/devinchen2014/socialdatax-douyin-creator-profile) <br>
- [SocialDataX API Access](https://socialdatax.52choujiang.com/?from=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON from CLI or MCP tool calls, with Markdown guidance for agent responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only profile fields may include name, platform IDs, bio, verification status, follower count, following count, received like count, IP location, and gender when available.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
