## Description: <br>
Manage VK.com (Vkontakte) community: post content (text, photos, videos) and handle messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RuslanLanket](https://clawhub.ai/user/RuslanLanket) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External community managers and developers use this skill to publish VK wall content, upload photos and videos, read conversations, reply to visitors, and monitor new messages through VK Long Poll. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for broad VK account or community permissions, including long-lived offline access. <br>
Mitigation: Use the narrowest VK token that works, avoid offline full-rights user tokens where possible, and keep tokens out of shared terminals and logs. <br>
Risk: The skill can publish, delete, message, mark messages as read, and call VK API methods that affect a live community. <br>
Mitigation: Manually approve posts, message actions, deletions, and raw VK API calls before execution; leave auto-mark-as-read off unless intentional. <br>
Risk: Long Poll monitoring can continue processing incoming messages if no limit is set. <br>
Mitigation: Set an explicit polling time limit and review incoming-message handling before running the poll command. <br>


## Reference(s): <br>
- [VK API & CLI Guide](references/api.md) <br>
- [Skill page](https://clawhub.ai/RuslanLanket/vk) <br>
- [Publisher profile](https://clawhub.ai/user/RuslanLanket) <br>
- [VK developer documentation](https://dev.vk.com) <br>
- [VK Host token helper](https://vkhost.github.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI commands may print JSON API responses or attachment identifiers.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a VK access token and Node.js runtime.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
