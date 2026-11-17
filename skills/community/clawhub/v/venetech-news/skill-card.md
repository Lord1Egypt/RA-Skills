## Description:

Venetech News helps agents gather and summarize technology, startup, AI, fintech, crypto, innovation, and digital entrepreneurship news with emphasis on Venezuelan and Latin American context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oscarmiranda90](https://clawhub.ai/user/oscarmiranda90)

### License/Terms of Use:


## Use Case:

External users and content teams use this skill to request concise technology and startup news briefings focused on Venezuela and Latin America. The skill guides agents to gather RSS and web-source headlines, deduplicate similar items, group them by editorial category, and summarize them with regional context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance can install unpinned Python packages while bypassing system package protections.

Mitigation: Run dependency installation in a virtual environment or container and pin package versions before operational use.

Risk: The skill gathers live news from RSS and web pages, so source availability, robots.txt requirements, and rate limits can affect results.

Mitigation: Prefer RSS feeds when available, respect robots.txt, use a real User-Agent, and keep requests to no more than one per second per domain.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/oscarmiranda90/skills/venetech-news)
- [Banca y Negocios Tecnologia](https://bancaynegocios.com/tecnologia/)
- [Con-Cafe RSS Feed](https://con-cafe.com/feed/)
- [El Estimulo Tecnologia](https://elestimulo.com/tecnologia/)
- [El Nacional Tecnologia](https://www.elnacional.com/tecnologia/)
- [El Pitazo Tecnologia](https://elpitazo.net/tecnologia/)
- [Xataka RSS Feed](https://www.xataka.com/rss)
- [Hipertextual RSS Feed](https://hipertextual.com/feed)
- [FayerWayer RSS Feed](https://www.fayerwayer.com/feed/)
- [TechCrunch RSS Feed](https://techcrunch.com/feed/)
- [Ars Technica RSS Feed](https://feeds.arstechnica.com/arstechnica/index)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown news briefings with categorized summaries, source URLs, and optional shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries should be concise, avoid reproducing full articles, and preserve source attribution.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
