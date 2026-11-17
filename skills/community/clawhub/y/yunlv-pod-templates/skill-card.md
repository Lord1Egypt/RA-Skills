## Description:

Provides ready-to-use POD design keyword templates, title templates, listing copy guidance, pricing references, and helper commands for print-on-demand product listings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, creators, and ecommerce operators use this skill to draft POD design prompts, listing titles, product descriptions, pricing references, and launch checklists for platforms such as Amazon, Etsy, TikTok Shop, Shopify, and Redbubble.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release requests a Yunlv TradeGPT API token and may send POD category or platform descriptions to an external service.

Mitigation: Install only if that data flow is acceptable, keep TRADEGPT_API_KEY scoped and rotated, and make remote generation an explicit opt-in step before production use.

Risk: Generated POD copy, design prompts, product claims, pricing suggestions, and platform guidance may be inaccurate, policy-sensitive, or commercially risky if published without review.

Mitigation: Treat outputs as drafts and verify IP, trademark, product material claims, shipping coverage, sizing, pricing, and platform policy before publishing listings.

Risk: The bundled title-template helper script contains behavior that should be tested before relying on generated command output.

Mitigation: Run the CLI in a controlled environment and validate outputs before using them in an agent workflow or production listing process.

## Reference(s):

- [POD Design Keywords](references/pod_design_keywords.md)
- [POD Title Templates](references/pod_title_templates.md)
- [POD Listing Copy](references/pod_listing_copy.md)
- [Yunlv Homepage](https://yunlvai.com)
- [Yunlv TradeGPT API](https://api.yunlvai.com)
- [ClawHub Skill Listing](https://clawhub.ai/wangm-a3/skills/yunlv-pod-templates)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, reusable text templates, JSON-formatted CLI output, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require TRADEGPT_API_KEY for remote Yunlv TradeGPT API-assisted generation; shipped reference templates can be used locally.]

## Skill Version(s):

1.1.0 (source: server release metadata and clawhub.yaml; SKILL.md lists 1.0.2 and _meta.json lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
