## Description: <br>
Searches the web across Baidu, Bing, and DuckDuckGo and can crawl pages without requiring API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yejinlei](https://clawhub.ai/user/yejinlei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current web search results, run deeper searches, or crawl specific web pages when internet access is appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External web requests and page crawling can disclose sensitive queries or access private/internal URLs from the runtime environment. <br>
Mitigation: Use only with non-sensitive queries and public URLs unless the runtime has reviewed network egress controls. <br>
Risk: The skill depends on web-search, crawling, and browser automation packages that can change behavior across releases. <br>
Mitigation: Review and pin dependency versions before deployment, and re-scan the skill after dependency changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yejinlei/web-search-ex-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [JSON objects containing search results, crawl metadata, snippets, and extracted markdown or text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results default to 5 and are capped at 20; crawled text is truncated in script output.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
