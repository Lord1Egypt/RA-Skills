## Description: <br>
Automate Twitter/X growth and content operations by discovering AI trends, generating tweets, posting to X, finding follow-back threads, commenting for engagement, quoting viral tweets, and supporting follower growth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelcey2023](https://clawhub.ai/user/kelcey2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate a Twitter/X account for AI and Tech Twitter content workflows, including trend discovery, tweet drafting, posting, quote-tweeting, and growth engagement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish, reply, quote, comment, or follow from a logged-in X account. <br>
Mitigation: Use only an account intentionally designated for automation and require manual review before any external account action. <br>
Risk: Some workflows rely on hardcoded local helper paths and external scripts without clear account scoping. <br>
Mitigation: Inspect and configure helper scripts and paths before use, and verify the active browser session belongs to the intended account. <br>
Risk: Automated report-posting workflows can promote a fixed ZeeLin report URL from the user's account. <br>
Mitigation: Confirm the report URL, generated text, and posting intent before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kelcey2023/zeelin-twitter-x-auto-ops) <br>
- [X platform](https://x.com) <br>
- [Hacker News Algolia API](https://hn.algolia.com/api/v1/search?query=AI&tags=story&hitsPerPage=5) <br>
- [THU ZeeLin Reports](https://thu-nmrc.github.io/THU-ZeeLin-Reports/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated tweet text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open browser pages and invoke local shell scripts that publish, quote, comment, or follow through a logged-in X account.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
