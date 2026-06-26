## Description: <br>
Automated social media manager that plans, writes, schedules, and analyzes content across X/Twitter, LinkedIn, Instagram, TikTok, Facebook, and Pinterest, with Buffer or Postiz scheduling support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Batsirai](https://clawhub.ai/user/Batsirai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and social media operators use this skill to plan content calendars, draft platform-specific posts, queue or schedule approved posts, review analytics, and prepare engagement replies for connected social channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connected Buffer or Postiz credentials can give the skill authority to queue, schedule, or publish real social posts. <br>
Mitigation: Use a dedicated .env file with only the intended social-media API keys, prefer draft mode for first runs, and require final human confirmation before queueing, scheduling, or publishing. <br>
Risk: The security review notes that the skill's safety claims and examples do not consistently make live posting behavior clear. <br>
Mitigation: Review the exact account, channel, post content, and scheduled time before executing generated scheduling commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Batsirai/social-media-engine) <br>
- [Buffer Setup Guide](tools/buffer-setup.md) <br>
- [Postiz Setup Guide](tools/postiz-setup.md) <br>
- [Content Calendar Template](templates/content-calendar.md) <br>
- [Postiz Documentation](https://docs.postiz.com) <br>
- [Postiz Application Repository](https://github.com/gitroomhq/postiz-app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include content calendars, post drafts, reply drafts, scheduling commands, analytics summaries, and setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
