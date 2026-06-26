## Description: <br>
Searches X/Twitter data, monitors accounts and trends, and supports authorized posting and engagement through the AISA relay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search and monitor Twitter/X data, summarize social activity, and carry out authorized posting, reply, like, follow, unfollow, and media workflows through AISA. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform public Twitter/X account actions, including posts, replies, likes, follows, unfollows, and media uploads. <br>
Mitigation: Require explicit human approval for every public action and use only a dedicated or tightly scoped Twitter/X account. <br>
Risk: The configured API key may be exposed in normal command output. <br>
Mitigation: Avoid running status, authorization, or posting commands in logged or shared contexts until API key redaction is fixed. <br>
Risk: Changing the relay endpoint can send requests and credentials to an untrusted service. <br>
Mitigation: Keep TWITTER_RELAY_BASE_URL unset unless the endpoint is fully trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aisadocs/twitter-autopilot-aisa) <br>
- [AISA](https://aisa.one) <br>
- [AISA API Reference](https://docs.aisa.one/reference/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger external Twitter/X read, posting, engagement, and media workflows through AISA APIs when configured and authorized.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
