## Description: <br>
This skill looks up Xiaohongshu / XHS / RedNote creator profile data through SocialDataX, including account basics, homepage information, and audience metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve read-only Xiaohongshu creator profile information from SocialDataX by user ID or profile URL/share text. The skill helps report available profile facts such as names, platform IDs, bio, verification, audience counts, IP location, and gender when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Returned creator profile fields such as follower counts, gender, and IP location are third-party data. <br>
Mitigation: Handle returned profile data according to the user's privacy and compliance requirements. <br>
Risk: The skill requires a SOCIALDATAX_API_KEY for SocialDataX lookups. <br>
Mitigation: Provide the key through the SOCIALDATAX_API_KEY environment variable and avoid exposing it in prompts, command history, or shared output. <br>
Risk: Profile facts and strategic interpretation can be conflated in agent responses. <br>
Mitigation: Separate returned profile facts from any analysis or recommendation. <br>


## Reference(s): <br>
- [SocialDataX homepage](https://socialdatax.com/?from=clawhub) <br>
- [ClawHub skill listing](https://clawhub.ai/devinchen2014/skills/socialdatax-xhs-creator-profile) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON profile data returned by SocialDataX CLI or MCP tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOCIALDATAX_API_KEY, node, and npm; use either a Xiaohongshu user ID or a profile URL/share text for a single lookup.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
