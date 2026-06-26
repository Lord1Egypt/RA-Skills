## Description: <br>
Social media automation operations assistant that generates and publishes content for Xiaohongshu, Weibo, and Twitter, with scheduled posting and interactive replies from content creation through data review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External social media operators, marketing teams, and developers use this skill to plan, generate, review, schedule, publish, monitor, and reply to content across Xiaohongshu, Weibo, and Twitter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide live posts, replies, and scheduled account actions. <br>
Mitigation: Run dry-run or preview first, then review every post, reply, and scheduled job before execution. <br>
Risk: Platform integrations require OAuth tokens, cookies, or other sensitive credentials. <br>
Mitigation: Use least-privilege tokens, keep credentials in environment variables or a secrets manager, and avoid printing or sharing logs that may contain credentials. <br>
Risk: Generated browser publish commands can take external actions on real social accounts. <br>
Mitigation: Inspect the target account, platform, content, and action before running generated browser commands. <br>
Risk: Automated replies may mishandle ambiguous, legal, personal-information, harassment, or competitor flame-baiting comments. <br>
Mitigation: Flag high-risk or ambiguous comments for manual handling and avoid auto-replying outside approved templates. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/openlark/social-auto-publisher) <br>
- [Content Strategy and Topic Selection Methodology](references/content-strategy.md) <br>
- [Reply Template Library](references/reply-templates.md) <br>
- [Twitter (X) Operations Guide](references/twitter-guide.md) <br>
- [Weibo Operations Guide](references/weibo-guide.md) <br>
- [Xiaohongshu Operations Guide](references/xiaohongshu-guide.md) <br>
- [Xiaohongshu Creator Publish Page](https://creator.xiaohongshu.com/publish/publish) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON content or schedule artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may prepare posts, replies, scheduled jobs, monitoring reports, and platform-specific publish actions for connected social accounts.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
