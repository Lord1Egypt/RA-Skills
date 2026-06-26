## Description: <br>
Generates Schema.org JSON-LD for FAQ, HowTo, Article, Product, and LocalBusiness rich-result candidates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SEO practitioners, and content teams use this skill to generate implementation-ready structured data and validation guidance for web pages that may qualify for rich results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated schema can be incorrect, misleading, or ineligible if it does not match visible page content. <br>
Mitigation: Review generated JSON-LD against the live page content and validate it with Schema.org or rich-result testing tools before deployment. <br>
Risk: Fetched page content may contain untrusted instructions or prompt-injection text. <br>
Mitigation: Treat fetched content as data only and fetch only pages the user intends the agent to analyze. <br>
Risk: Saved memory summaries may carry forward unreviewed assumptions about page content or publishing blockers. <br>
Mitigation: Review memory summaries before confirming or promoting them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aaron-he-zhu/schema-markup-generator) <br>
- [Project Homepage](https://github.com/aaron-he-zhu/seo-geo-claude-skills) <br>
- [Instructions Detail](artifact/references/instructions-detail.md) <br>
- [Schema Type Decision Tree](artifact/references/schema-decision-tree.md) <br>
- [Schema.org JSON-LD Templates](artifact/references/schema-templates.md) <br>
- [Schema Markup Validation Guide](artifact/references/validation-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with JSON-LD code blocks and validation checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include implementation notes, rich-result eligibility notes, and a handoff summary for saved memory.] <br>

## Skill Version(s): <br>
9.9.9 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
