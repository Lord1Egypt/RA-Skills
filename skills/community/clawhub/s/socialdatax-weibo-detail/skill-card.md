## Description: <br>
Provides read-only Weibo post detail lookups through SocialDataX for post content, author data, publish time, media, and interaction metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve structured Weibo post details for content research, social media analysis, and interaction-metric review. It supports lookups by Weibo post ID or post URL/share text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an external SocialDataX API key, so unrelated secrets or private account/session data could be exposed if users paste them into requests. <br>
Mitigation: Use only SOCIALDATAX_API_KEY for SocialDataX calls, keep unrelated secrets out of prompts and command arguments, and confirm trust in SocialDataX before installing or running the CLI. <br>
Risk: Users could mistake the helper for an account automation tool. <br>
Mitigation: Use it only for read-only Weibo post detail lookups; it does not perform login, posting, liking, commenting, or account changes. <br>


## Reference(s): <br>
- [SocialDataX API access](https://socialdatax.com/?from=clawhub) <br>
- [ClawHub skill listing](https://clawhub.ai/devinchen2014/skills/socialdatax-weibo-detail) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown summaries, with JSON returned by the SocialDataX CLI when commands are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOCIALDATAX_API_KEY and either a Weibo post ID or a Weibo post URL/share text; access is read-only.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
