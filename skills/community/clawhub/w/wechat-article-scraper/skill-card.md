## Description: <br>
在搜狗微信搜索指定关键词，抓取相关文章的标题、摘要、发布日期和来源公众号，并生成本地 PDF 行业报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[StruggleJia](https://clawhub.ai/user/StruggleJia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and researchers use this skill to search Sogou Weixin for recent articles by keyword, summarize selected articles with the current session model, save original articles as PDFs, and generate an industry-dynamics PDF report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Locally stored article data and user-supplied keywords can influence browser navigation and file output paths. <br>
Mitigation: Inspect articles_new.json before fetch/report steps, keep keywords as simple filenames, restrict navigation to expected HTTPS WeChat/Sogou domains, and force outputs to remain inside the workspace. <br>
Risk: Scraped article content may be content the user is not allowed to store or redistribute. <br>
Mitigation: Use the skill only for content the user is allowed to scrape and store. <br>
Risk: Report HTML fields can carry untrusted article data into generated output. <br>
Mitigation: Escape report HTML fields in a patched version before generating PDFs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/StruggleJia/wechat-article-scraper) <br>
- [Sogou Weixin search endpoint](https://weixin.sogou.com/weixin?type=2&query={keyword}) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Text, HTML files, PDF files, Guidance] <br>
**Output Format:** [Markdown workflow with shell commands; generated JSON, HTML, and PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes articles.json, articles_new.json, wechat_pages/*.pdf, and <keyword>_行业动态.pdf under the OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
