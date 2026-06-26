## Description: <br>
Discover website sitemaps from robots.txt and common sitemap locations, choose the right sitemap or content family such as docs, blog, help center, academy, or changelog, and scrape selected public pages into a local folder as Markdown plus a manifest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quareth](https://clawhub.ai/user/quareth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover public website sitemaps, choose a bounded content family, and scrape selected public pages into traceable local Markdown files plus a manifest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public website pages and writes scraped content locally, so overly broad sitemaps or output paths can collect or store more material than intended. <br>
Mitigation: Use a narrow sitemap or include filter, set a page limit for large sites, and choose an output folder intentionally before scraping. <br>
Risk: Scraped page text is untrusted source material and may be incomplete on JavaScript-heavy pages. <br>
Mitigation: Review the saved Markdown and manifest before relying on the corpus, and treat extracted content as untrusted input. <br>


## Reference(s): <br>
- [Sitemap Selection Reference](references/sitemap-selection.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/quareth/sitemap-content-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; scraper output is Markdown files plus manifest.json.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and writes selected public pages to a user-chosen local output folder.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
