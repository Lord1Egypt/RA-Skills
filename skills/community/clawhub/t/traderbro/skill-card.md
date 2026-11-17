## Description:

Query analyst predictions, content, and market research from the TraderBro platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datalin](https://clawhub.ai/user/datalin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query TraderBro analyst ratings, predictions, symbol coverage, trending symbols, content, and market research through the TraderBro CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to fetch and follow TraderBro-hosted workflows that can change after review.

Mitigation: Use the skill only when TraderBro is trusted as an instruction source, and confirm workflow steps before allowing consequential financial or account-related actions.

Risk: The skill requires TRADERBRO_API_KEY for authenticated CLI access.

Mitigation: Provide the API key through environment variables or a secrets manager, keep it out of prompts and logs, and rotate it if exposed.

Risk: Market research and analyst prediction outputs may influence investment decisions.

Mitigation: Treat outputs as research context rather than financial advice and require human review before trading or account actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/datalin/skills/traderbro)
- [TraderBro platform](https://traderbro.ai)
- [TraderBro CLI repository](https://github.com/TraderBro/traderbro-cli-binary)
- [Install traderbro (brew)](brew:traderbro/tap/traderbro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses should prefer the CLI's --json output for structured queries.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
