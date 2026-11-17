## Description:

Helps agents research Xiaohongshu/RED public trend signals, generate and rewrite notes, verify claims, originality, and compliance, analyze authorized account data, and manage reviewed draft publishing and post-publish review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuboboo](https://clawhub.ai/user/xuboboo)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketing teams, and developers use this skill to connect agents to Xiaohongshu/RED content research, note generation, compliance checks, authorized account analysis, and controlled publishing workflows. It is intended for reviewed, authorized workflows rather than scraping, captcha bypass, fake engagement, or plagiarism.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network downloads and external content ingestion can expand the skill's network and supply-chain attack surface.

Mitigation: Install only in an isolated, trusted environment, use trusted image and search providers, and enforce outbound network controls.

Risk: Browser publishing, post-publish sync, and secrets infrastructure can expose account sessions or approval tokens if enabled before the reported issues are fixed.

Mitigation: Avoid enabling those workflows until the security issues are fixed, require HTTPS for secrets infrastructure, and keep account sessions and approval tokens tightly scoped.

Risk: Enterprise Vault/OIDC behavior and identity-derived file writes may be unsafe if tenant identifiers are not validated.

Mitigation: Keep enterprise Vault/OIDC features disabled until tenant-identifier validation issues are fixed and enforce tenant, role, and provider controls before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuboboo/skills/xiaohongshu-viral-note-agent-skill)
- [Research Protocol](artifact/references/research-protocol.md)
- [Content Generation](artifact/references/content-generation.md)
- [Verification Workflow](artifact/references/verification-workflow.md)
- [Browser Authentication](artifact/references/browser-authentication.md)
- [Auto Publishing](artifact/references/auto-publishing.md)
- [Enterprise Governance](artifact/references/enterprise-governance.md)
- [Supply Chain Security](artifact/references/supply-chain-security.md)
- [MCP, A2A, and Streaming](artifact/references/mcp-a2a-streaming.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Structured JSON delivery packages and Markdown/text note drafts, with CLI/API guidance for operational workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishing, browser login, account analytics, and enterprise workflows require explicit authorization, configured providers, and human review gates.]

## Skill Version(s):

5.15.0 (source: server release evidence; artifact metadata is 5.14.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
