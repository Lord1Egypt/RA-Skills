## Description: <br>
VeneTech News helps agents gather and summarize technology, startup, AI, fintech, crypto, innovation, and digital entrepreneurship news with emphasis on Venezuelan and Latin American context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oscarmiranda90](https://clawhub.ai/user/oscarmiranda90) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to produce concise Venezuelan and Latin American technology news briefings, newsletter-style summaries, and category roundups from RSS feeds and permitted public pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes scraping guidance that may bypass publisher access controls. <br>
Mitigation: Prefer RSS feeds and permitted public pages; avoid rotating proxies or undocumented internal APIs unless explicit authorization and site terms allow them. <br>
Risk: The skill may fetch public news sources and install Python parsing dependencies. <br>
Mitigation: Review network requests and dependency installation commands before running them in a local or production environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oscarmiranda90/venetech-news) <br>
- [Con-Cafe RSS feed](https://con-cafe.com/feed/) <br>
- [Xataka RSS feed](https://www.xataka.com/rss) <br>
- [FayerWayer RSS feed](https://www.fayerwayer.com/feed/) <br>
- [TechCrunch RSS feed](https://techcrunch.com/feed/) <br>
- [Ars Technica RSS feed](https://feeds.arstechnica.com/arstechnica/index) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown news briefing with source links and optional shell or Python snippets for feed collection] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries should be brief, include source URLs, avoid reproducing full articles, respect robots.txt and rate limits, and prefer RSS feeds when available.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
