## Description: <br>
Reads and summarizes WeChat Official Account articles from mp.weixin.qq.com URLs, extracting article text and optionally capturing a full-page screenshot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reedchan7](https://clawhub.ai/user/reedchan7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to read, summarize, analyze, or screenshot WeChat Official Account articles when standard fetching methods cannot access the content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses browser automation and anti-bot evasion to access WeChat articles. <br>
Mitigation: Restrict use to expected mp.weixin.qq.com article URLs and review the skill before deployment. <br>
Risk: The skill can automatically create and share full-page screenshots that may include private, paid, or sensitive article content. <br>
Mitigation: Make screenshot sharing opt-in or review screenshots before sending them in sensitive channels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/reedchan7/wxmp-reader) <br>
- [Publisher profile](https://clawhub.ai/user/reedchan7) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown summary with optional JSON article extraction and PNG screenshot file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries should match the user's language and avoid reproducing the full article.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
