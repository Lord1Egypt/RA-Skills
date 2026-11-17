## Description:

小鹿选房 helps users search Shenzhen housing information, including second-hand homes, rentals, new homes, purchase options, bargain listings, price comparisons, transactions, communities, school districts, and schools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangjike](https://clawhub.ai/user/fangjike)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to ask an agent for Shenzhen real-estate search, comparison, transaction, community, school district, and school information. The agent can run the Xiaolu House CLI as needed and return concise housing summaries with relevant links and configuration guidance.

### Deployment Geography for Use:

China (Shenzhen-focused)

## Known Risks and Mitigations:

Risk: The skill asks the agent to execute an unpinned external npm CLI for housing queries and configuration.

Mitigation: Review the package before use, prefer a pinned and reviewed version, and confirm CLI commands before execution.

Risk: The CLI can handle local configuration and API-key setup.

Mitigation: Confirm any config-changing command before it runs and avoid exposing API keys in prompts, logs, or shared outputs.

Risk: Housing responses may include broker-contact or mini-program links that function as commercial calls to action.

Mitigation: Present such links transparently and let users decide whether to follow them or contact brokers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fangjike/skills/shenzhen-house)
- [Xiaolu House homepage](https://github.com/fanggeek/xiaolu-house)
- [Xiaolu House Claw setup](https://www.xiaoluxuanfang.com/claw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Natural-language Markdown with inline CLI commands and housing result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include mini-program links, broker-contact calls to action, API-key setup guidance, and rate-limit retry guidance.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
