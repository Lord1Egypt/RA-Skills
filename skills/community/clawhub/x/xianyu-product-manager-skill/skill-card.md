## Description:

Intelligent product management for AI service providers on Xianyu platform with professional templates, dry-run review, and enforced confirmation for product creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crab-xieyujin](https://clawhub.ai/user/crab-xieyujin)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and AI service providers use this skill to prepare, preview, and create Xianyu marketplace listings for AI services with reusable templates, listing data, poster prompts, and batch workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create real Xianyu marketplace listings through unsafe and batch paths.

Mitigation: Run dry_run first and avoid unsafe methods unless automation is tightly controlled.

Risk: A hard-coded fallback account can be used if user_name is omitted.

Mitigation: Always pass the intended user_name explicitly before creating listings.

Risk: Credential misuse or configuration mistakes could affect a valuable marketplace account.

Mitigation: Use limited credentials and install only when marketplace listing creation is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crab-xieyujin/skills/xianyu-product-manager-skill)
- [OpenClaw source listing](https://clawhub.com/skills/xianyu-product-manager)
- [Goofish homepage](https://www.goofish.pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, JSON-like listing payloads, and generated poster prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can preview listings with dry_run before creation; batch operations are capped at 20 products.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
