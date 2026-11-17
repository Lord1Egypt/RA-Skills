## Description:

Yufluent Visual Craft helps ecommerce teams create Markdown plans for A+ page structures, video storyboards, main-image differentiation briefs, and image compliance checklists through the Yufluent cloud service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, marketplace agencies, and developers use this skill to request cloud-generated visual content planning for Amazon, Shopify, and TikTok listings. It supports A+ page outlines, video scripts, main-image creative briefs, and image compliance review checklists that should be reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product copy, listing context, competitor notes, and image descriptions may be sent to the Yufluent cloud service.

Mitigation: Use only approved ecommerce content, avoid confidential or secret-bearing inputs, and disclose cloud processing to appropriate stakeholders.

Risk: A configurable TOKENAPI_BASE_URL can send user content and the API token to an untrusted endpoint if misconfigured.

Mitigation: Use the official or otherwise trusted HTTPS endpoint, keep TOKENAPI_KEY in environment storage, and avoid untrusted endpoint overrides.

Risk: Generated visual plans and compliance checklists may be incomplete or inconsistent with marketplace policies or advertising rules.

Mitigation: Review outputs manually against the target platform's current policy and applicable advertising requirements before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metahuan/skills/yufluentcn-visual-craft)
- [Yufluent homepage](https://claw.changzhiai.com)
- [Yufluent OpenClaw documentation](https://claw.changzhiai.com/app/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown plans and checklists, with CLI command examples and run metadata when invoked locally]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cloud-backed output; requires TOKENAPI_KEY and may use TOKENAPI_BASE_URL when configured.]

## Skill Version(s):

1.1.2 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
