## Description: <br>
AI-powered startup companion for Korean founders. Evaluate business plans, match government funding programs (TIPS/DeepTech/Global TIPS), connect with 3,972+ TIPS-selected startups, get investor recommendations, and integrate with Kakao i OpenBuilder. Features Agentic RAG (HyDE, Multi-Query, CRAG), structured extraction, and Track B financial matching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifeissea](https://clawhub.ai/user/lifeissea) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External startup founders, advisors, and operators use Raon OS to evaluate Korean business plans, identify suitable government funding programs, draft support applications, estimate valuations, and prepare investor-facing summaries through CLI, local API, or chat integrations. <br>

### Deployment Geography for Use: <br>
South Korea-focused <br>

## Known Risks and Mitigations: <br>
Risk: Submitted business plans and PDFs may contain confidential startup information and can be processed by configured LLM, API, Supabase, or widget endpoints. <br>
Mitigation: Use only trusted endpoints, avoid uploading confidential materials to deployments without a privacy policy, and prefer local processing when confidentiality is required. <br>
Risk: API keys and webhook secrets are required or recommended for several integrations. <br>
Mitigation: Store secrets in user-managed environment files with restrictive permissions, never commit real keys, and rotate secrets if exposure is suspected. <br>
Risk: The local HTTP server and Kakao/web widget integrations can expose analysis endpoints if deployed publicly. <br>
Mitigation: Set API and webhook secrets before public exposure, use reverse proxy or firewall controls, and restrict administrative endpoints to trusted hosts. <br>
Risk: Funding, valuation, and investor recommendations may be incomplete or stale relative to official program rules and current market conditions. <br>
Mitigation: Review generated guidance against official program notices, source documents, and qualified professional advice before making funding or investment decisions. <br>


## Reference(s): <br>
- [Raon OS ClawHub release page](https://clawhub.ai/lifeissea/raon-os) <br>
- [TIPS evaluation criteria](references/tips-criteria.md) <br>
- [Government funding program reference](references/gov-programs.md) <br>
- [Startup idea reference database](references/yc-rfs.md) <br>
- [Kakao i OpenBuilder setup guide](KAKAO_SETUP.md) <br>
- [Web chat widget embed guide](widget/EMBED.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON API responses, CLI text, shell commands, configuration snippets, and generated startup analysis or draft content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include 100-point evaluation scores, section-level feedback, funding matches, application drafts, valuation estimates, investor summaries, and local server responses.] <br>

## Skill Version(s): <br>
0.7.28 (source: SKILL.md frontmatter, package.json, release metadata, and CHANGELOG released 2026-02-27) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
