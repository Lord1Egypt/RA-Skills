## Description: <br>
Analyze Zhihu hot trends and community dynamics to generate high-engagement answer strategies and first drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and content teams use this skill to analyze Zhihu topic opportunities, identify content gaps, plan answer strategies, and draft markdown-ready responses tailored to a domain or topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live scraping or trend collection may conflict with Zhihu rules or collect unnecessary content data. <br>
Mitigation: Treat live scraping as a separate user-approved action, check Zhihu rules first, avoid collecting unnecessary data, and do not store copied answer text. <br>
Risk: Generated drafts may include fabricated personal claims, unsupported statistics, or unsuitable advice in sensitive topics. <br>
Mitigation: Review drafts before publishing, verify statistics and claims, and add appropriate disclaimers for medical, legal, or financial topics. <br>


## Reference(s): <br>
- [Zhihu Content Strategist on ClawHub](https://clawhub.ai/harrylabsj/zhihu-content-strategist) <br>
- [Engagement Patterns Reference](references/engagement_patterns.json) <br>
- [Topic Templates Reference](references/topic_templates.json) <br>
- [Input Schema](schemas/input.schema.json) <br>
- [Output Schema](schemas/output.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces topic recommendations, gap matrices, strategy briefs, answer drafts, publishing timing, tags, promotion hooks, and warnings.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
