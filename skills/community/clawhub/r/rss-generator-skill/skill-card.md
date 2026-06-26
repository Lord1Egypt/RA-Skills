## Description: <br>
Generate valid RSS 2.0 or Atom 1.0 feeds from web pages that contain post lists but lack a native feed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kidehen](https://clawhub.ai/user/kidehen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, publishers, and content operators use this skill to turn public blog, news, or article-list pages into synthetic RSS 2.0 or Atom 1.0 feeds when no native feed is available. It helps inspect the page, extract post metadata, validate feed structure, and provide XML or a self-hostable discovery wrapper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches web pages and can use optional headers, so private URLs, tokenized URLs, cookies, bearer tokens, API keys, or sensitive request headers could be exposed to the selected fetch route. <br>
Mitigation: Use the skill only with public pages unless the operator intentionally wants those values sent through the selected fetch route; do not provide credentials or sensitive headers. <br>
Risk: Synthetic feeds can contain incomplete or estimated metadata when source pages lack dates, summaries, or stable post structures. <br>
Mitigation: Validate generated RSS or Atom output with the included checklist, label estimated dates, and review extracted items before publishing the feed. <br>
Risk: Full-text mode fetches each discovered post URL and can increase request volume or hit rate limits. <br>
Mitigation: Keep the default item limit, warn before fetching more than 20 items, and respect robots.txt and site access restrictions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kidehen/rss-generator-skill) <br>
- [URIBurner WEB_FETCH OpenAPI definition](https://linkeddata.uriburner.com/chat/functions/openapi.yaml) <br>
- [Protocol routing](references/protocol-routing.md) <br>
- [Post extraction rules](references/extraction-rules.md) <br>
- [Feed templates](references/feed-templates.md) <br>
- [Validation checklist](references/validation-checklist.md) <br>
- [HTML feed discovery wrapper template](references/html-wrapper-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown containing RSS or Atom XML code blocks, optional shell commands, and optional generated XML or HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output saves a feed XML file; optional modes include raw XML, an HTML discovery wrapper, preview output, validation guidance, and full-text extraction.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill title) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
