## Description: <br>
Audits websites for traditional SEO health and AI search visibility, generating prioritized reports with actionable fixes and ready-to-use prompts for AI coding agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imrishit98](https://clawhub.ai/user/imrishit98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and site owners use this skill to audit live websites or local codebases for SEO health, AI search visibility, crawlability, schema, content quality, and prioritized remediation work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL mode can make outbound requests to user-provided websites and optional Google PageSpeed endpoints. <br>
Mitigation: Use URL mode only for sites the user intends to audit, and avoid private staging or internal domains unless that access is expected. <br>
Risk: Codebase mode can read relevant project files and optional product marketing context from the local workspace. <br>
Mitigation: Run codebase scans only in projects the user wants reviewed and avoid including unrelated sensitive files in the audit scope. <br>
Risk: SEO and AI-visibility recommendations may affect public indexing, crawler access, and published marketing content. <br>
Mitigation: Review proposed changes before implementation, especially robots.txt, noindex, schema, citations, and generated content updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imrishit98/seo-and-llm-rankings) <br>
- [SEO & GEO Audit Checklist](references/seo-checklist.md) <br>
- [AI Citation Scoring Framework](references/ai-citation-scoring.md) <br>
- [GEO Methods](references/geo-methods.md) <br>
- [Platform Ranking Factors](references/platform-ranking-factors.md) <br>
- [JSON-LD Schema Templates](references/schema-templates.md) <br>
- [Fix Prompt Templates](references/fix-prompt-templates.md) <br>
- [Content Creation Prompt Templates](references/content-prompt-templates.md) <br>
- [AI Writing Detection](references/ai-writing-detection.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with prioritized findings, inline shell commands, code/configuration examples, and agent-ready remediation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include URL fetch diagnostics, SEO and AI visibility scores, issue severity levels, and concrete next steps.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
