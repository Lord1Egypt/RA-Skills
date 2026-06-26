## Description: <br>
Generate XML sitemaps by crawling a website for SEO, site-structure audits, domain page discovery, or search-engine submission, with configurable crawl depth, page limits, and polite delays. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site operators, and SEO practitioners use this skill to crawl an authorized website and produce a standards-compliant sitemap.xml for search-engine submission or site-structure review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The crawler makes network requests to a user-provided website and could burden sites if run without authorization or with aggressive limits. <br>
Mitigation: Run it only against sites you own or are authorized to audit, and keep max-pages, max-depth, delay, and timeout settings reasonable. <br>
Risk: The skill writes a sitemap file to the selected output path. <br>
Mitigation: Choose the output path deliberately, or use stdout when you need to inspect the sitemap before writing a file. <br>
Risk: The script depends on Python packages from the execution environment. <br>
Mitigation: Install requests and beautifulsoup4 from a trusted Python environment before running the crawler. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Johnnywang2001/sitemap-generator) <br>
- [Sitemaps.org Protocol 0.9](http://www.sitemaps.org/schemas/sitemap/0.9) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and XML sitemap output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes sitemap XML to a chosen output path or stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
