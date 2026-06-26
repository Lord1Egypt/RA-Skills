## Description: <br>
Builds SEO keyword strategies from a domain, URL, product, market, or seed topic by combining site crawling, AIsa/DataForSEO keyword data, SERP signals, and LLM-assisted clustering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and SEO practitioners use this skill to research keywords for a website, product, market, or competitor set and turn validated metrics into clusters, opportunity scores, and page recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends target URLs, crawled page excerpts, keyword inputs, competitor names, and SEO strategy context to AIsa/DataForSEO. <br>
Mitigation: Use only approved targets, avoid confidential internal sites unless authorized, and keep AISA_API_KEY private. <br>
Risk: Broad invocation wording could lead to use outside the intended SEO keyword research workflow. <br>
Mitigation: Use this skill for SEO keyword research, confirm the scope before crawling or calling APIs, and avoid generic web research use. <br>


## Reference(s): <br>
- [AIsa API Map for SEO Keyword Research](references/aisa-api-map.md) <br>
- [Keyword Research Report Template](references/report-template.md) <br>
- [AIsa](https://aisa.one) <br>
- [ClawHub Release Page](https://clawhub.ai/bibaofeng/seo-keyword-research-aisa-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and optional JSON data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local crawl profiles, keyword exports, cluster summaries, and SEO roadmap tables when the user requests a full report.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
