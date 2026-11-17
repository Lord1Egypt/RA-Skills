## Description:

Provides cloud-backed cross-border ecommerce keyword research and SEO placement reports for Amazon, Shopify, and TikTok Shop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers and agents use this skill to collect product and seed keyword inputs, call the Yufluent cloud service, and review JSON keyword placement suggestions before publishing marketplace or store listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends product and keyword research data to the Yufluent/OpenClaw service.

Mitigation: Use only with data approved for that service and review data handling requirements before running.

Risk: The package may load Python modules from a sibling _shared directory or injected client code that was not part of the reviewed artifact.

Mitigation: Install and run in an isolated environment, and review the loaded client code before use.

Risk: SEO keyword reports may contain incorrect, misleading, restricted, or trademark-sensitive suggestions.

Mitigation: Review suggested keywords against product facts, platform policies, marketplace search reports, and advertising data before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metahuan/skills/yufluentcn-seo-pro)
- [Yufluent SEO Pro homepage](https://www.changzhiai.com/skills/seo-pro)
- [OpenClaw integration](https://claw.changzhiai.com/app/openclaw)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON keyword reports with optional CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKENAPI_KEY and may write the returned report to a user-specified JSON file.]

## Skill Version(s):

1.2.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
