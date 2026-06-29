## Description: <br>
Build Telegram vertical AI agent prototypes with a Python starter template for intent classification, lead scoring, CRM, routing, follow-up, analytics, tier gating, and tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oturans](https://clawhub.ai/user/oturans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold Telegram vertical AI agents for narrow business workflows such as tax assistance, real estate CRM, dental reception, legal intake, and e-commerce support. It guides customization of seed data, intent patterns, routing rules, pricing tiers, follow-up sequences, tier limits, and tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The template is clean local code, but production use with real Telegram bots, CRMs, calendars, payment systems, bank statements, receipts, or customer data requires additional hardening. <br>
Mitigation: Before real deployment, add proper secret management, HTTPS and webhook validation, access controls, consent notices, data minimization, retention and deletion rules, audit logging, and confirmation steps for sensitive actions. <br>
Risk: The starter template uses mock data and local SQLite persistence; replacing mocks with real systems can expose customer or business data if done without controls. <br>
Mitigation: Keep development data synthetic until integrations are hardened, and review storage paths, retention behavior, access boundaries, and audit logging before storing real data. <br>
Risk: Domain examples include tax, real estate, healthcare, legal, payments, and customer-support workflows where incorrect automation can create user harm or compliance risk. <br>
Mitigation: Use human review and explicit confirmation for sensitive recommendations, filings, payments, legal intake, healthcare triage, property offers, and other high-impact actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oturans/test-template-starter-pack) <br>
- [Publisher profile](https://clawhub.ai/user/oturans) <br>
- [GUIDE.md](artifact/GUIDE.md) <br>
- [Real Estate CRM Agent example brief](artifact/examples/realestate-brief.md) <br>
- [SelfBot Russian Self-Employed Tax Assistant example brief](artifact/examples/selfbot-brief.md) <br>
- [Claw Mart upgrade path](https://shopclawmart.com) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown guidance with Python code templates and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local Python starter template, example briefs, configuration instructions, and test-running guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
