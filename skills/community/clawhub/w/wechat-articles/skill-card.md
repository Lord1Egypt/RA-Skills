## Description: <br>
Searches for WeChat public-account articles by keyword and extracts readable content from mp.weixin.qq.com article links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johan-oilman](https://clawhub.ai/user/johan-oilman) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to find public WeChat articles, read pasted WeChat article URLs, and extract article titles, authors, summaries, and paragraph text for follow-on analysis or summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch user-supplied URLs over the network. <br>
Mitigation: Use it only with WeChat public-account searches and mp.weixin.qq.com article links; avoid unrelated or internal URLs. <br>
Risk: Search terms and article URLs may reveal sensitive interests or private research topics. <br>
Mitigation: Avoid private search terms and review queries before running the search scripts. <br>
Risk: Playwright mode installs and runs Chromium plus additional Python packages. <br>
Mitigation: Install only in environments where those browser and network dependencies are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johan-oilman/wechat-articles) <br>
- [Project homepage declared by artifact](https://github.com/johan-oilman/wechat-articles) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Plain text summaries and Python dictionaries returned or printed by the bundled scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search URLs may be time-sensitive; article reading can use requests/BeautifulSoup or Playwright with Chromium.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
