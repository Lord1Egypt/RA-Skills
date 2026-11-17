## Description:

Audits websites for traditional SEO health and AI search visibility, then generates prioritized reports with actionable fixes and ready-to-use prompts for AI coding agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imrishit98](https://clawhub.ai/user/imrishit98)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and site owners use this skill to audit live websites or local codebases for SEO and generative engine optimization gaps, then produce prioritized findings and prompts to implement fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch user-supplied URLs, including internal or private-network URLs.

Mitigation: Run it only against sites you own or are authorized to audit, and avoid internal or private-network URLs unless explicitly intended.

Risk: The skill includes fallback guidance for WAF or bot-detection blocks.

Mitigation: Do not use bypass-style fetching against protected sites; switch to user-provided HTML or source-code mode when automated access is blocked.

## Reference(s):

- [SEO and LLM Rankings on ClawHub](https://clawhub.ai/imrishit98/skills/seo-and-llm-rankings)
- [AI Citation Scoring Framework](references/ai-citation-scoring.md)
- [Platform Ranking Factors](references/platform-ranking-factors.md)
- [GEO Methods](references/geo-methods.md)
- [JSON-LD Schema Templates](references/schema-templates.md)
- [SEO and GEO Audit Checklist](references/seo-checklist.md)
- [AI Writing Detection](references/ai-writing-detection.md)
- [Fix Prompt Templates](references/fix-prompt-templates.md)
- [Content Creation Prompt Templates](references/content-prompt-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown audit reports with tables, inline shell commands, and optional prompt or code snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output varies by audit mode: live URL scan or local codebase scan.]

## Skill Version(s):

1.1.0 (source: evidence release and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
