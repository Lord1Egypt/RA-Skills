## Description: <br>
Generate production-grade website pages and reusable page templates with SEO metadata, AI-answer discoverability structure, FAQs, schema guidance, crawl and index recommendations, and launch QA checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucel017](https://clawhub.ai/user/brucel017) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, content editors, SEO owners, and marketing teams use this skill to turn product positioning or page intent into deployable website page copy and implementation guidance. It is suited for homepages, landing pages, product and feature pages, category or collection pages, documentation pages, FAQs, comparison pages, pricing pages, and reusable page templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate broadly for website copy requests and produce Chinese output by default. <br>
Mitigation: State language and scope requirements explicitly when invoking it, especially when a non-Chinese output or narrow page task is needed. <br>
Risk: Optional web research prompts may include confidential launch plans, competitive details, or unreleased product claims. <br>
Mitigation: Avoid providing sensitive business information unless disclosure to the agent environment is intended. <br>
Risk: SEO or GEO guidance can become misleading if a request asks for hidden keywords, hidden prompts, fake reviews, ranking guarantees, or unverified current search policy claims. <br>
Mitigation: Use the skill's safe alternatives: reject deceptive SEO tactics, label unverified assumptions, avoid ranking guarantees, and ensure structured data matches visible page content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/brucel017/seo-geo-page-factory) <br>
- [Input Contract](artifact/references/input-contract.md) <br>
- [Output Contract](artifact/references/output-contract.md) <br>
- [SEO/GEO Rules](artifact/references/seo-geo-rules.md) <br>
- [Page-Type Playbook](artifact/references/page-type-playbook.md) <br>
- [Schema Playbook](artifact/references/schema-playbook.md) <br>
- [Fallback Rules](artifact/references/fallback-rules.md) <br>
- [Quality Gates](artifact/references/quality-gates.md) <br>
- [Page Template Outline](artifact/assets/page_template_outline.md) <br>
- [Regression Evaluation Set](artifact/evals/evals.json) <br>
- [Schema.org](https://schema.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Structured Markdown with optional JSON-LD, HTML head tag, robots, and implementation code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are Chinese by default unless the user requests another language, and follow a fixed nine-section page-deliverable structure.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
