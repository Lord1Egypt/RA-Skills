## Description: <br>
Extracts structured data from websites, including tables, lists, prices, articles, and metadata, using dependency-free HTML parsing with optional caching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jlacroix82](https://clawhub.ai/user/jlacroix82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Smart Scraper to turn public web pages or supplied HTML into concise structured summaries for tables, lists, prices, article previews, links, images, and metadata. It can also monitor page changes by storing and comparing local snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided target URLs over the network and can retrieve page contents from those sites. <br>
Mitigation: Use it only with public, non-sensitive URLs and avoid authenticated, internal, or private pages. <br>
Risk: Scraped page data or watch-mode snapshots may persist locally, including titles, headings, paragraphs, links, prices, images, and metadata. <br>
Mitigation: Use --no-cache when privacy matters and manually clear memory/scraper-cache and memory/scraper-cache/diffs after sensitive runs. <br>
Risk: Bundled documentation contains inconsistent statements about cache defaults and watch-mode persistence. <br>
Mitigation: Follow the server security guidance and current root skill documentation: treat caching and snapshots as possible local persistence and review flags before use. <br>
Risk: Regex-based HTML parsing does not execute JavaScript and may miss or misread dynamic pages. <br>
Mitigation: Use the extracted output as a structured aid, verify important results against the source page, and use a browser-based tool for JavaScript-rendered sites. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jlacroix82/skills/smart-scraper-web) <br>
- [ClawHub Security Audit](https://clawhub.ai/jlacroix82/smart-scraper-web/security-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI summaries and Markdown usage guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local cache files when caching or watch snapshots are enabled; network requests are limited to public http/https targets.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
