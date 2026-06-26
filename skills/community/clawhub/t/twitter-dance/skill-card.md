## Description: <br>
Automates X/Twitter posting and account workflows with apidance.pro scripts, optional Kimi-generated tweet drafts, account statistics, notifications, replies, and engagement analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Evan-y25](https://clawhub.ai/user/Evan-y25) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and social media operators use this skill to generate drafts, publish or batch publish posts, inspect account activity, and automate replies or engagement workflows for an X/Twitter account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform live actions on an X/Twitter account, including posting, replying, following, unfollowing, deletion, and bulk engagement. <br>
Mitigation: Use a test or low-risk account first, prefer draft or dry-run modes, and add a human confirmation step before any live account-changing action. <br>
Risk: The artifact includes unsafe credential examples and behavior that may print sensitive token-related data in terminal output. <br>
Mitigation: Rotate any credentials copied from documentation, avoid shared terminals and CI logs, and review output before sharing logs. <br>
Risk: The server security verdict is suspicious and recommends manual review before use. <br>
Mitigation: Review and scan the scripts before deployment, then restrict credentials to the minimum account and API permissions needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Evan-y25/twitter-dance) <br>
- [apidance.pro documentation](https://doc.apidance.pro) <br>
- [QUICK_START.md](QUICK_START.md) <br>
- [AUTO-REPLY-GUIDE.md](AUTO-REPLY-GUIDE.md) <br>
- [GRAPHQL_API_GUIDE.md](GRAPHQL_API_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces commands and generated post content that can trigger live X/Twitter account actions when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
