## Description: <br>
Draft, rewrite, adapt, and publish social media posts with an approval-first workflow across Facebook, X, and Reddit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[normandmickey](https://clawhub.ai/user/normandmickey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to turn ideas, links, announcements, product updates, images, or sourced context into platform-specific drafts and approval-ready publishing packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured platform credentials can be used to publish public posts from the user's accounts. <br>
Mitigation: Keep credentials least-privileged and private, run dry-runs first, and require explicit approval of the account, platform, text, image, and destination before live publishing. <br>
Risk: Reddit publishing outside the user's own subreddit can create moderation or account risk. <br>
Mitigation: Limit Reddit posting to the user's own subreddit unless the user explicitly chooses another destination and confirms they understand the moderation risk. <br>
Risk: Social posts about factual, current, financial, legal, policy, or technical topics can become misleading if drafted from thin context. <br>
Mitigation: Ground drafts in source context, keep claims aligned with evidence, and avoid confident explanations when sourcing is insufficient. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/normandmickey/social-draftsmith) <br>
- [Facebook Graph API v23.0](https://graph.facebook.com/v23.0) <br>
- [X API v2](https://api.twitter.com/2) <br>
- [Reddit OAuth API](https://oauth.reddit.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown social post drafts, approval packages, and optional shell commands for dry-run or approved publishing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Approval-first; live publishing requires configured platform credentials and explicit user approval.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
