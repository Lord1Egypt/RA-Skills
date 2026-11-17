## Description:

Automatically reads the current day's Xiaohongshu video and caption files from a local folder, connects to Chrome, and publishes the content to a logged-in Xiaohongshu account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weishuai34-bit](https://clawhub.ai/user/weishuai34-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and operators who publish Xiaohongshu video posts use this skill to automate upload, title and body entry, topic insertion, and publishing from an existing logged-in Chrome session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish real Xiaohongshu posts from a logged-in account without a final confirmation step.

Mitigation: Narrow the trigger and add a final confirmation or draft mode before allowing publication.

Risk: The skill uses the user's Chrome session through a fixed remote debugging port.

Mitigation: Use an isolated browser profile instead of the primary Chrome profile and protect access to port 9222.

Risk: The skill reads local media and text files and saves diagnostic screenshots.

Mitigation: Verify the exact media and title files before running and remove or protect diagnostic screenshots after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weishuai34-bit/skills/xiaohongshu-publish-auto)
- [Xiaohongshu creator publishing page](https://creator.xiaohongshu.com/publish/publish)

## Skill Output:

**Output Type(s):** [Text, Files, Browser automation]

**Output Format:** [Console status text, browser-side publishing actions, and PNG diagnostic screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local media and title files under ~/Movies/小红书英语 and a logged-in Chrome session exposed on remote debugging port 9222.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
