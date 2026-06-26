## Description: <br>
Publish content to Mastodon. Use when you need to post a Mastodon status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[behrangsa](https://clawhub.ai/user/behrangsa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to publish, schedule, and attach media to Mastodon statuses from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish real Mastodon posts, schedule posts, and upload local media using the configured account token. <br>
Mitigation: Before each run, confirm the exact text, media files, visibility, account, and scheduled time with the user. <br>
Risk: The skill requires a Mastodon access token that can post on behalf of the account. <br>
Mitigation: Use a least-privilege token where possible, keep it out of prompts and files, and revoke it when it is no longer needed. <br>
Risk: Media attachment paths can point to local files. <br>
Mitigation: Confirm file paths before upload and avoid attaching sensitive files or secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/behrangsa/tootbot) <br>
- [Publisher profile](https://clawhub.ai/user/behrangsa) <br>
- [Clawdbot](https://github.com/anthropics/clawdbot) <br>
- [Claude Code skills documentation](https://code.claude.com/docs/en/skills) <br>
- [Mastodon example instance](https://mastodon.social) <br>
- [ClawdHub listing](https://clawdhub.com/skills/tootbot) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Mastodon posting requests using JSON status objects; output should be read and summarized for the user.] <br>

## Skill Version(s): <br>
0.5.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
