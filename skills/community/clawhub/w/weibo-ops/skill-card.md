## Description: <br>
Weibo Operations automates Weibo write actions through DrissionPage and Chrome CDP, including posting, deleting, reposting, commenting, and liking on weibo.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunwz1115](https://clawhub.ai/user/sunwz1115) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run authenticated Weibo write operations from a local Chrome session, including publishing posts, deleting posts, reposting, commenting, liking, and counting visible posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a logged-in Weibo browser and handles broad Chrome session data through a debuggable browser. <br>
Mitigation: Use a dedicated Chrome profile for Weibo, avoid copying a normal browsing profile, close the CDP browser after use, and delete /tmp/chrome-debug-profile. <br>
Risk: Write actions can change public account state, and delete actions can remove posts without an additional built-in confirmation step. <br>
Mitigation: Require explicit user confirmation before post, delete, repost, comment, or like actions, and review target UID, post ID, text, and delete scope before execution. <br>
Risk: Authentication state can expire and browser automation can fail when Weibo changes its interface. <br>
Mitigation: Verify login state and inspect the browser result after each operation; re-authenticate or stop automation if the page state is unexpected. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and script arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in Chrome profile, DrissionPage, and a Chrome CDP port.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
