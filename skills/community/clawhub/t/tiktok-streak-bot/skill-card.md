## Description: <br>
Browser-automated TikTok streak messaging skill using Playwright that sends daily messages to configured usernames with state tracking, retry control, and optional content discovery via hashtags or keywords. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrblackeg](https://clawhub.ai/user/mrblackeg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to automate daily TikTok streak messages to a configured list of usernames while tracking state to avoid duplicate sends in the same day. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable TikTok account cookies in data/cookies.json. <br>
Mitigation: Use a dedicated or low-risk account, keep data/cookies.json out of shared folders and source control, and remove or rotate the session after use. <br>
Risk: The skill can send scheduled messages automatically from the authenticated account. <br>
Mitigation: Review data/usernames.json, the configured daily limit, and message or discovery settings before enabling scheduled execution. <br>
Risk: Automated TikTok messaging may create account or platform-policy consequences. <br>
Mitigation: Use only where this automation is acceptable for the account and operating context, and stop or rotate credentials if TikTok challenges or blocks the session. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mrblackeg/tiktok-streak-bot) <br>
- [Overview](references/overview.md) <br>
- [Architecture](references/architecture.md) <br>
- [TikTok Selectors](references/selectors.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Python execution logs and JSON state or cookie files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Updates data/state.json and data/cookies.json after browser automation runs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
