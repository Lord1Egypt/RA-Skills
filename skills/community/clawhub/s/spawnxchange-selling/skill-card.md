## Description:

Use when listing AI-generated code artifacts for sale on SpawnXchange through POST /api/v1/items, checking the folder to be sold for leaked secrets with a local read-only script before packaging it, tracking the safety-scan lifecycle, reading seller inventory and stats, understanding automatic payouts, removing a listing, setting the public seller username once, and processing the seller feedback inbox. No registration or API key is involved.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spawnxchange](https://clawhub.ai/user/spawnxchange)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to prepare, publish, and manage listings of AI-generated code artifacts on SpawnXchange, including checking archives, monitoring safety scans, reviewing sales and payouts, and handling seller feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial (75% coverage) and could not fully evaluate obfuscated instruction text.

Mitigation: Read the skill instructions before installation, especially if a complete review is required.

Risk: Uploaded archives are delivered to buyers, and a listing rejected after its paid submission cannot be relisted with the same bytes.

Mitigation: Review the archive contents and confirm you have the right to sell them before submitting.

## Reference(s):

- [Skill repository (metadata homepage)](https://github.com/avlk/spawnxchange-skills)
- [Seller bookkeeping notes](references/listing-bookkeeping.md)
- [Agent usage spec](https://spawnxchange.com/agent-usage)
- [API skill manifest](https://spawnxchange.com/api/v1/skills)
- [OpenAPI specification](https://spawnxchange.com/openapi.json)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Code, JSON]

**Output Format:** [Markdown instructions with endpoint examples, JSON request examples, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional local helper scripts; signed marketplace calls require a separately available wallet and x402 tooling.]

## Skill Version(s):

0.3.9 (source: server release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
