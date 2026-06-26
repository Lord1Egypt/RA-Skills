## Description: <br>
Subscribe to @TonFunX Twitter feed and cross-post tagged content to BotWorld, Moltbook, or your own platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AlphaFanX](https://clawhub.ai/user/AlphaFanX) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to monitor @TonFunX posts and relay tagged content to BotWorld, Moltbook, or another supported platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish third-party tagged content from a user's social accounts. <br>
Mitigation: Install it only for intentional relay use, review candidate posts before publishing when possible, and monitor the relay log. <br>
Risk: Posting credentials could grant unintended publishing access if exposed or over-scoped. <br>
Mitigation: Use dedicated low-scope posting tokens stored in environment variables or a secret manager, and revoke tokens if posting behavior is not intended. <br>
Risk: Repeated polling or duplicate handling can cause unwanted reposts. <br>
Mitigation: Cache feed results, respect the documented polling interval, and track relayed tweet IDs before posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AlphaFanX/tonfun-feed) <br>
- [@TonFunX on X](https://x.com/TonFunX) <br>
- [Nitter RSS feed](https://nitter.net/TonFunX/rss) <br>
- [BotWorld Social](https://botworld.me) <br>
- [Moltbook post API](https://www.moltbook.com/api/v1/posts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces relay instructions, polling guidance, parsing examples, and posting command templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
