## Description: <br>
Fetches Xiaohongshu (RedNote/XHS) profile details and published notes for a user ID, including social counts, bio, tags, and note engagement statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and marketing researchers use this skill to collect profile fields and note engagement statistics from Xiaohongshu pages that the logged-in user can access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated profile and notes extraction can collect personal or creator information. <br>
Mitigation: Use only for target profiles and fields the logged-in user is authorized to access, and confirm the requested accounts before running. <br>
Risk: Batch and stealth-session guidance could be used to work around platform rate limits. <br>
Mitigation: Avoid stealth-session scaling and follow Xiaohongshu terms, rate limits, consent requirements, and applicable law. <br>
Risk: A local troubleshooting memory file may retain operational observations. <br>
Mitigation: Review any local memory file before sharing the workspace and avoid recording fetched user IDs or profile data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/skills/xiaohongshu-user-profile) <br>
- [Xiaohongshu profile URL pattern](https://www.xiaohongshu.com/user/profile/{user_id}) <br>
- [Xiaohongshu home page](https://www.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON extraction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in Xiaohongshu browser session and only extracts data visible to that session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
