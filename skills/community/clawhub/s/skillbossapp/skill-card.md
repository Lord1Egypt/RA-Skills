## Description:

SkillBoss lets an OpenClaw agent use a single API key and wallet to call paid AI tools for LLMs, web scraping, search, media generation, and email, with cost and receipt metadata returned to the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richiecyq](https://clawhub.ai/user/richiecyq)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use SkillBoss to give OpenClaw agents controlled access to paid model, search, scraping, media generation, and email tools without configuring each provider separately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plugin exposes broad remote tool execution through the generic dispatcher and can send prompts, URLs, scraped content, generated email text, and other tool inputs to SkillBoss and downstream providers.

Mitigation: Install only after reviewing the enabled tools; prefer per-tool allowlists, scoped sub-wallets, low per-call budgets, and human review before enabling the generic dispatcher.

Risk: Email sending can create outbound communications from generated or agent-provided content.

Mitigation: Require human review before enabling or using the email tool, and restrict email access with tool allowlists where OpenClaw supports them.

Risk: Calls to paid downstream tools can incur wallet spend.

Mitigation: Use low per-call limits, scoped sub-wallets, and server-side wallet rules for per-tool, per-day, or per-agent budgets.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/richiecyq/skills/skillbossapp)
- [SkillBoss Website](https://www.skillboss.co)
- [Agent Shopping Protocol v0.1](https://www.skillboss.co/docs/agent-shopping-protocol)
- [SkillBoss Catalog JSON](https://www.skillboss.co/api/catalog)
- [SkillBoss Docs](https://www.skillboss.co/docs)
- [npm Package](https://www.npmjs.com/package/skillboss-openclaw-plugin)

## Skill Output:

**Output Type(s):** [text, markdown, json, images, email action results, configuration guidance]

**Output Format:** [OpenClaw tool results, usually text or JSON with optional generated media outputs and cost, balance, or receipt metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a SkillBoss API key and may send prompts, URLs, scraped content, generated email text, and tool inputs to SkillBoss and downstream providers.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
