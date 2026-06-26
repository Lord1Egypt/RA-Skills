## Description: <br>
Log in to X/Twitter via a real browser session and perform actions including posting, replying, reposting, liking, and bookmarking tweets through Playwright. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanghanjun2](https://clawhub.ai/user/zhanghanjun2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and operators use this skill to authenticate a saved browser session and perform X/Twitter account actions without the official X API. It is intended for controlled posting, reply, repost, like, unlike, bookmark, and unbookmark workflows where each live action is confirmed before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable X/Twitter login cookies for a live account. <br>
Mitigation: Protect or delete ~/.openclaw/auth/x-twitter/cookies.json when finished, and never commit or share the saved cookie file. <br>
Risk: The skill can perform live account actions such as posting, replying, reposting, liking, and bookmarking. <br>
Mitigation: Confirm the exact text, target tweet, and intended action before every write operation. <br>
Risk: Browser automation may conflict with platform expectations around automated activity. <br>
Mitigation: Install and use the skill only when intentional browser control of the account is acceptable for the user's X/Twitter account and workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhanghanjun2/x-twitter-browser) <br>
- [Publisher profile](https://clawhub.ai/user/zhanghanjun2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and concise status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local Python scripts that may open or control a browser session using saved X/Twitter cookies.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata; artifact frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
