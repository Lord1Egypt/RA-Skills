## Description: <br>
Helps agents use the X/Twitter API to read tweets, post tweets or threads, reply, send DMs, search, and view analytics with user-provided credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[klemenska](https://clawhub.ai/user/klemenska) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and account operators use this skill to let an agent prepare and run X/Twitter API actions such as posting, replying, direct messaging, searching, and checking engagement analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post tweets, replies, media, and direct messages through the user's X/Twitter account. <br>
Mitigation: Require explicit review of the exact tweet, reply, media, recipient, or DM text before allowing write commands. <br>
Risk: Credentials used by the skill can authorize account actions. <br>
Mitigation: Use the least-privileged tokens possible and prefer environment variables or a secret manager over a plaintext credentials file. <br>
Risk: X API tier limits and rate limits can block reads, searches, analytics, or repeated actions. <br>
Mitigation: Confirm the API tier before use and monitor rate-limit responses for timeline, mentions, search, analytics, and posting workflows. <br>


## Reference(s): <br>
- [Twitter API v2 Rate Limits](references/api-limits.md) <br>
- [Twitter Search Operators](references/search-operators.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with CLI commands and plain-text API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided X/Twitter API credentials; write actions should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
