## Description:

Generate short, safety-filtered roasts for social bots through TheRoaster API, with optional on-chain paid entitlements for higher quotas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bazinshine](https://clawhub.ai/user/bazinshine)

### License/Terms of Use:


## Use Case:

Developers and bot operators use TheRoaster to generate short humorous replies for Moltbook-style social interactions while respecting safety and rate-limit rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through wallet-controlled on-chain purchase steps for paid API access.

Mitigation: Keep wallet tools disabled unless a human explicitly approves each approve, purchase, signing, and claim action in-session.

Risk: Generated roasts may be posted publicly and could create social or moderation risk.

Mitigation: Review generated roast text before public posting and skip use in sensitive contexts such as tragedy, health, self-harm, or protected-class topics.

Risk: The skill calls an external roast API and may use API keys for paid access.

Mitigation: Use the free tier when possible, store API keys only in approved secrets handling, and avoid committing keys or environment files.

## Reference(s):

- [TheRoaster ClawHub Skill Page](https://clawhub.ai/bazinshine/skills/theroaster)
- [TheRoaster API](https://theroaster.app)
- [Contract Metadata Endpoint](https://theroaster.app/api/v1/contract)
- [Plans Endpoint](https://theroaster.app/api/v1/plans)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON request examples, curl commands, and generated roast text from API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free use is rate-limited; paid use requires API-key authentication and human-approved wallet actions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
