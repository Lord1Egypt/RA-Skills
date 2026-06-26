## Description: <br>
Crawl websites with Tavily and save extracted pages as local markdown for offline use or analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evanYDL](https://clawhub.ai/user/evanYDL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to crawl documentation, knowledge bases, or website sections through Tavily and either return focused crawl results or save page-level markdown files for offline analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tavily receives crawl targets, crawl options, and semantic instructions supplied to the skill. <br>
Mitigation: Avoid internal or regulated sites unless approved, keep crawl scope and limits narrow, and review saved markdown before feeding it into another agent. <br>
Risk: The skill can use local Tavily OAuth state when an explicit API key is not set. <br>
Mitigation: Prefer setting TAVILY_API_KEY explicitly and confirm the account and token context before running crawls. <br>
Risk: First-run OAuth may launch an unpinned npm helper. <br>
Mitigation: Use an explicit Tavily API key or review the OAuth helper behavior before allowing the first-run authentication flow. <br>


## Reference(s): <br>
- [ClawHub Skill: Tavily Crawl](https://clawhub.ai/evanYDL/tavily-crwal) <br>
- [Tavily](https://tavily.com) <br>
- [Tavily Crawl API endpoint](https://api.tavily.com/crawl) <br>
- [Tavily Map API endpoint](https://api.tavily.com/map) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [JSON-formatted Tavily crawl results and optional markdown files saved per crawled page.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When an output directory is supplied, the script saves each crawled page as a separate markdown file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
