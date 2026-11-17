## Description:

Creates production-ready virtual-host product video workflows, scripts, prompts, AI-HIVE commands, and quality checklists from authorized materials and verified product facts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, private-domain operators, cross-border sellers, and product teams use this skill to turn virtual-host product-video requests into auditable production plans, scripts, prompts, AI-HIVE generation commands, and acceptance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE API-key use and configurable endpoint routing can expose account access if credentials are broad or the endpoint is untrusted.

Mitigation: Use a scoped, revocable API key; avoid overriding AI_HIVE_BASE_URL or --base-url unless the endpoint is trusted; and do not place real API keys in files, logs, screenshots, or version control.

Risk: Paid generation, media upload, and downloads can create account-cost and file-safety exposure.

Mitigation: Review prompts, routing, model configuration, and price snapshots before paid calls; start batch work with a small sample; and download outputs into a low-risk directory.

Risk: Virtual-host product videos can mislead viewers if they imply unauthorized likeness use, live interaction, current pricing, inventory, platform approval, or unverified product claims.

Mitigation: Require authorized materials and current product facts, mark unconfirmed facts as pending verification, avoid impersonation or fabricated testimonials, and keep human review before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/virtual-host-product-video-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE OpenAPI endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE task records, price snapshots, downloaded file locations, and video acceptance results when generation is explicitly approved.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
