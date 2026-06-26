## Description: <br>
Writes and rewrites research-driven SEO and generative-engine-optimization pages using competitive SERP, keyword, and optional Search Console data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gbessoni](https://clawhub.ai/user/gbessoni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content teams use this skill to turn a target keyword or existing page into a competitive SEO page with gap analysis, structured content, verification tags, tables, and schema markup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use SEO API credentials and optional read-only Google Search Console access. <br>
Mitigation: Use only credentials intended for this workflow, keep ~/.config/seo-agi/.env permissions restricted, and review access before installation. <br>
Risk: Generated research and page outputs can include sensitive keyword, site, or campaign data saved locally. <br>
Mitigation: Review ~/Documents/SEO-AGI and ~/.local/share/seo-agi for saved outputs and handle those files according to the site's data policy. <br>
Risk: Bundled scripts install or use Python dependencies for SEO research workflows. <br>
Mitigation: Prefer a virtual environment for dependency installation and inspect configuration before running live API workflows. <br>


## Reference(s): <br>
- [SEO AGI ClawHub release](https://clawhub.ai/gbessoni/seo-agi) <br>
- [Page Templates Reference](artifact/references/page-templates.md) <br>
- [Content Quality Checklist](artifact/references/quality-checklist.md) <br>
- [Schema Markup Patterns](artifact/references/schema-patterns.md) <br>
- [DataForSEO](https://dataforseo.com) <br>
- [Google Rich Results Test](https://search.google.com/test/rich-results) <br>
- [Schema.org Validator](https://validator.schema.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown pages with YAML frontmatter, HTML or Markdown tables, JSON-LD schema blocks, verification tags, and optional JSON research artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save research, briefs, pages, and rewrites to local SEO-AGI output directories when the user runs bundled scripts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
