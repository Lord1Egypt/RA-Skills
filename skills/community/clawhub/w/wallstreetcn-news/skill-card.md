## Description: <br>
获取华尔街见闻财经新闻。当用户询问华尔街见闻、wallstreetcn、财经新闻、市场动态、金融资讯、股市行情、热文、头条、搜索文章时使用。使用 web_fetch 直接调用 API 获取最新文章、头条文章、热文和搜索结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wallstreetinsights](https://clawhub.ai/user/wallstreetinsights) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve Wallstreetcn finance news, including latest articles, headline articles, hot articles, and keyword search results. It formats returned article titles, summaries, authors, dates, and links as concise Chinese Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad finance and news prompts may activate this source-specific workflow when the user intended a different news source, language, or output style. <br>
Mitigation: Specify the desired source, language, and output format when invoking the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wallstreetinsights/wallstreetcn-news) <br>
- [Wallstreetcn latest news API](https://api-one-wscn.awtmt.com/apiv1/content/information-flow?channel=global&accept=article&limit=10) <br>
- [Wallstreetcn headline news API](https://api-one-wscn.awtmt.com/apiv1/content/carousel/information-flow?channel=global&limit=10) <br>
- [Wallstreetcn hot articles API](https://api-one-wscn.awtmt.com/apiv1/content/articles/hot?period=all) <br>
- [Wallstreetcn article search API](https://api-one-wscn.awtmt.com/apiv1/search/article?query=关键词&limit=10) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Concise Chinese Markdown with article titles, summaries, source links, authors, and dates.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
