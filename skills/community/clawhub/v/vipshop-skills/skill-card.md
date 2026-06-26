## Description: <br>
唯品会 is a Vipshop shopping assistant skill pack for product search, product details, promotion discovery, image-based product search, and local login-session management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viphgta](https://clawhub.ai/user/viphgta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers use this skill through an agent to search Vipshop products, inspect product details, browse promotions, find similar products from images, and manage a local Vipshop login session when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill manages a Vipshop login session locally and reuses it across search, detail, promotion, and image-search workflows. <br>
Mitigation: Install only after reviewing the login behavior, keep local session files private, and require explicit user approval before login handoff. <br>
Risk: Generated exchange-token links, QR-token output, and logs may contain sensitive session material. <br>
Mitigation: Treat those outputs as sensitive, avoid sharing logs or generated links, and redact session-bearing values before storing or forwarding results. <br>
Risk: The release security verdict is suspicious because automatic login, session-token use, token-bearing link output, and runtime skill-install authority require user review. <br>
Mitigation: Review the skill and security summary before deployment, restrict use to trusted environments, and require explicit approval before any auto-install or credential-related action. <br>


## Reference(s): <br>
- [Vipshop User Login API Reference](artifact/vipshop-user-login/references/api_reference.md) <br>
- [Vipshop User Login Integration Guide](artifact/vipshop-user-login/references/integration_guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/viphgta/vipshop-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries and tables with JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product links, product images, prices, promotion details, login status, QR login guidance, and token-bearing exchange links.] <br>

## Skill Version(s): <br>
1.0.12 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
