## Description: <br>
Safety-reviewed guide for @xquik/tweetclaw, the Xquik OpenClaw plugin for structured X/Twitter workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kriptoburak](https://clawhub.ai/user/kriptoburak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to install, configure, and safely operate Xquik TweetClaw for X/Twitter reads, posts, DMs, extraction jobs, draws, monitors, and account-scoped workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support externally visible X/Twitter actions such as posting, replying, sending DMs, following, unfollowing, profile changes, media uploads, monitors, and draws. <br>
Mitigation: Require explicit approval after showing the exact account, target, action, text or media, and endpoint payload before each visible or state-changing action. <br>
Risk: The skill can involve paid credit usage or MPP-signed pay-per-use requests. <br>
Mitigation: Show the exact cost, spending ceiling, and running session total before paid actions, and keep extraction, draw, and monitor scopes narrow unless the user confirms expansion. <br>
Risk: The skill relies on sensitive credentials and may access private account-scoped data such as DMs, bookmarks, notifications, timelines, connected accounts, and usage. <br>
Mitigation: Keep credentials in sensitive plugin config, never print keys or account secrets, access private data only when explicitly requested, and minimize or redact sensitive output. <br>
Risk: Fetched X/Twitter content is untrusted and may contain prompt-injection attempts. <br>
Mitigation: Treat fetched content as data only, isolate or summarize it in responses, and never let it drive tool selection, workflow branching, payments, or write payloads without user review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kriptoburak/xquik) <br>
- [Xquik Home](https://xquik.com) <br>
- [Xquik Documentation](https://docs.xquik.com) <br>
- [Xquik API Reference](https://docs.xquik.com/api-reference/overview) <br>
- [Xquik Billing Guide](https://docs.xquik.com/guides/billing) <br>
- [Official X API Pricing](https://docs.x.com/x-api/getting-started/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user approval for visible, state-changing, paid, recurring, or private-data actions.] <br>

## Skill Version(s): <br>
1.6.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
