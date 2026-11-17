## Description: <br>
Shopify助手-免费版 helps individual sellers and small ecommerce teams customize Shopify themes, manage products and collections, improve basic SEO, and use Shopify CLI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and small Shopify sellers use this skill for Shopify theme customization, Liquid template examples, product and collection management guidance, basic SEO improvements, and Shopify CLI operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate or run Shopify CLI commands that authenticate to a store, pull theme files, or push theme changes. <br>
Mitigation: Confirm the target store and theme before command execution, prefer draft or unpublished themes, and require explicit approval before `shopify auth login`, `shopify theme pull`, or `shopify theme push`. <br>
Risk: Theme code or configuration changes could affect a live storefront if applied directly. <br>
Mitigation: Keep a backup, review generated Liquid, JSON, and CSS changes before writing files, and test changes in a preview or unpublished theme before publishing. <br>
Risk: Generated Shopify guidance may be incomplete for complex business, SEO, or deployment decisions. <br>
Mitigation: Use the skill for scoped Shopify build tasks and have a qualified reviewer validate complex store, SEO, and deployment changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/shopify-helper-tool-free) <br>
- [Source Skill Artifact](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Liquid, JSON, and shell command examples; optional structured JSON responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Shopify CLI commands and theme file changes; command execution, file writes, authentication, theme pulls, and theme pushes should require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
