## Description:

途牛旅游CLI技能 helps agents use the tuniu CLI to search and book flights, hotels, attraction tickets, trains, cruises, and holiday travel products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonardoooooo](https://clawhub.ai/user/leonardoooooo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel agents use this skill to route travel requests through the tuniu CLI for search, comparison, and booking workflows across flights, hotels, tickets, trains, cruises, and holiday products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to install or update mutable npm packages.

Mitigation: Prefer a reviewed, pinned tuniu-cli version and confirm package installation or update steps before execution.

Risk: The skill may write or update local agent skill directories.

Mitigation: Review target directories and requested permissions before allowing skill installation or updates.

Risk: Booking calls can send passenger, contact, or payment-adjacent travel information to Tuniu services.

Mitigation: Confirm before booking calls, keep TUNIU_API_KEY in a protected secret store, and avoid exposing credentials or personal information in logs or responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leonardoooooo/skills/tuniu-cli)
- [ClawHub publisher profile](https://clawhub.ai/user/leonardoooooo)
- [Tuniu Open Platform API key portal](https://open.tuniu.com/mcp/login)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with tuniu CLI commands and JSON argument examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, npm, tuniu CLI >=1.0.7, and TUNIU_API_KEY.]

## Skill Version(s):

1.0.5 (source: server release; artifact frontmatter reports 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
