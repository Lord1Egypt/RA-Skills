## Description:

Amazon Shopper helps an agent search anonymous Amazon.es product listings, compare availability and normalized value metrics such as EUR per kg or GB, and recommend buyable top options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill for iterative Amazon.es shopping decisions when they need a ranked shortlist rather than raw links. It is not intended for account-specific delivery promises, live price tracking, or purchases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional off-Amazon research path can fetch arbitrary HTTPS search-result URLs without the same public-network guard used elsewhere.

Mitigation: Keep AMAZON_SHOPPER_ALLOW_WEB_RESEARCH unset unless third-party lookups are acceptable, and run the skill in a constrained environment without access to sensitive internal network services.

Risk: The skill has network and local subprocess behavior.

Mitigation: Install only in environments with a trusted PATH and review configured LLM CLI, ImageMagick, Apify, and Amazon Creators API settings before use.

Risk: Runtime tests were not run in the security scan environment because Node v20.20.0 was available and the package expects Node 22.5+ with node:sqlite.

Mitigation: Run the offline test suite under Node 22.5+ before deployment or release promotion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/globalcaos/skills/tinker-amazon-shopper)
- [Publisher profile](https://clawhub.ai/user/globalcaos)
- [Apify integration settings](https://console.apify.com/settings/integrations)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON command output with concise Markdown shopping guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stateful CLI workflow; subcommands emit one JSON object on stdout, while human-readable details go to stderr.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
