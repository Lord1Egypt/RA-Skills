## Description: <br>
Tracks product prices on UNIQLO China, stores watched items in a local CSV file, and compares current official page prices with saved baseline prices before responding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yjy233](https://clawhub.ai/user/yjy233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping assistants use this skill to track selected UNIQLO China products, maintain a local watchlist, and check whether watched items have dropped in price. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a local UNIQLO watchlist in uniqlo/uniqlo-price-watch.csv. <br>
Mitigation: Keep the workspace private and remove the CSV file when the watchlist should no longer be retained. <br>
Risk: Optional FireCrawl scraping requires an API key and sends requested UNIQLO URLs to the FireCrawl service. <br>
Mitigation: Use a dedicated or low-privilege FireCrawl key and keep crawler use limited to uniqlo.cn URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yjy233/uniqlo-price-watch) <br>
- [UNIQLO China search](https://www.uniqlo.cn/search.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with price comparisons, local CSV updates, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update uniqlo/uniqlo-price-watch.csv and may use FIRECRAWL_API_KEY for optional FireCrawl scraping.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
