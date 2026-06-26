## Description: <br>
Helps agents produce SEO and generative-engine optimization guidance for ranking in search engines and increasing citation readiness in AI search answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gingiris](https://clawhub.ai/user/gingiris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, developer-relations, and founder-led growth teams use this skill to generate SEO/GEO content plans, article templates, schema guidance, audit checklists, and distribution commands for public web content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys for services such as Dev.to or IndexNow could be exposed or mishandled. <br>
Mitigation: Keep credentials in environment variables or a secret manager and avoid placing real keys in prompts, examples, logs, or generated documents. <br>
Risk: Generated curl commands may submit URLs or publish public content to external services. <br>
Mitigation: Require explicit user approval before running any command that posts, publishes, or transmits content externally. <br>
Risk: SEO/GEO recommendations may be inaccurate, outdated, or unsuitable for a specific brand or jurisdiction. <br>
Mitigation: Have a human reviewer validate claims, sources, canonical URLs, crawler directives, and publishing decisions before release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gingiris/seo-geo-playbook) <br>
- [IndexNow endpoint](https://www.bing.com/indexnow) <br>
- [Schema.org](https://schema.org) <br>
- [Google Rich Results Test](https://search.google.com/test/rich-results) <br>
- [Growth tools](https://gingiris.github.io/growth-tools/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that submit URLs or publish content to external services when the user supplies credentials.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
