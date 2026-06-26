## Description: <br>
This skill helps agents search WeChat articles through BrowserAct and return full article content with article metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccmagia2-gif](https://clawhub.ai/user/ccmagia2-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect full WeChat article bodies, titles, authors, publication dates, image URLs, and source links for content monitoring, media research, trend tracking, competitor analysis, and knowledge-base building. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and retrieved content are sent to BrowserAct for WeChat article extraction. <br>
Mitigation: Use the skill only when BrowserAct's data handling is acceptable, avoid confidential search terms, and keep BROWSERACT_API_KEY in the local environment. <br>
Risk: Large extraction limits can increase runtime and expose more third-party content than intended. <br>
Mitigation: Start with modest extraction limits and review results before increasing the limit for batch research. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ccmagia2-gif/wechat-article-search-api-skill) <br>
- [BrowserAct API key console](https://www.browseract.com/reception/integrations) <br>
- [BrowserAct workflow API endpoint](https://api.browseract.com/v2/workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal logs followed by text or JSON-like article results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and BROWSERACT_API_KEY; outputs may include article URLs, publication dates, authors, image URLs, body content, and titles.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
