## Description: <br>
Fetches WeChat public account article content from mp.weixin.qq.com links and extracts the article body. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaozs-com](https://clawhub.ai/user/xiaozs-com) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch a WeChat public account article, extract its title and body text, and save reviewable local artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The fetch script can open a supplied URL in Chrome, including non-WeChat URLs. <br>
Mitigation: Use only public mp.weixin.qq.com article links and avoid private, internal, or untrusted URLs. <br>
Risk: The skill persists fetched article content and screenshots to a user-selected directory. <br>
Mitigation: Choose an output folder that can be reviewed and cleaned up after execution. <br>
Risk: The dependency requirement allows newer DrissionPage versions. <br>
Mitigation: Pin and review dependencies before use in controlled environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiaozs-com/weixin-fetcher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands] <br>
**Output Format:** [Markdown article text, standard output text, and a PNG screenshot file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes article_content_weixin.md and article_screenshot_weixin.png to the selected output directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
