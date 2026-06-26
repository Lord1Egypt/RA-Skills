## Description: <br>
Advanced web content extraction skill for OpenClaw using a multi-tier fallback strategy across Jina, Scrapling, and WebFetch with intelligent routing, caching, quality scoring, and domain learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xcjl](https://clawhub.ai/user/0xcjl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract readable text or Markdown from web pages, articles, dynamic sites, and WeChat official account articles while receiving extraction metadata such as source URL, tier used, cache status, and quality score. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested URLs may be fetched through Jina when Tier 1 is used, which can expose sensitive internal or private URLs to a third-party service. <br>
Mitigation: Avoid sensitive internal URLs unless using a local-only tier, and use a limited Jina API key when Tier 1 is enabled. <br>
Risk: Extracted content, URL-derived cache entries, quota state, and learned domain routes can be stored locally. <br>
Mitigation: Configure cache and learning paths deliberately, limit retention for sensitive work, and clear cache or learning data after sensitive use. <br>
Risk: The optional Scrapling setup may install or invoke npm and npx tooling. <br>
Mitigation: Review the installer before running it and install optional Node.js tooling only in environments where that package source and execution model are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xcjl/web-reader-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [JSON-like result object containing extracted content and metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes title, content, URL, extraction tier, quality score, cache status, learned domain tier, and error details when extraction fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
