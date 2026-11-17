## Description:

Purple Flea Agent Domains is a domain registration and management API guide for AI agents that need to check availability, purchase domains with USDC on Base, manage DNS records, inspect domains, top up wallet balance, browse supported TLD pricing, or use the referral program.

This skill is ready for commercial/non-commercial use.

## Publisher:

[purple-flea](https://clawhub.ai/user/purple-flea)

### License/Terms of Use:


## Use Case:

Developers and external agents use this skill to interact with Purple Flea's domain API for domain search, registration, wallet funding, and DNS record management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through paid domain purchases and USDC spending.

Mitigation: Require explicit user approval before wallet funding, domain purchase, or any action that spends USDC.

Risk: The skill includes DNS update and deletion workflows that can disrupt active domains.

Mitigation: Require explicit confirmation before DNS updates or deletions, and show the domain, record type, name, and value before applying changes.

Risk: The referral guidance can persistently steer future agent behavior if placed in a system prompt or shared agent profile.

Mitigation: Keep referral codes optional, visible, and scoped to an individual transaction; do not add referral-routing text to persistent prompts or shared profiles.

## Reference(s):

- [API Reference](references/api.md)
- [Purple Flea Agent Domains](https://domains.purpleflea.com)
- [Purple Flea Agent Domains LLMs.txt](https://domains.purpleflea.com/llms.txt)
- [ClawHub Skill Page](https://clawhub.ai/purple-flea/skills/purpleflea-domains)
- [Publisher Profile](https://clawhub.ai/user/purple-flea)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks and API endpoint tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes example curl commands, endpoint descriptions, pricing notes, and DNS record guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
