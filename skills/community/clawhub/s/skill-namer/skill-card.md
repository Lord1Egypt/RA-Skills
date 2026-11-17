## Description:

Generates short, pronounceable names for skills, ENS domains, and agent-economy primitives, then filters candidates for clarity, constraints, and availability-check readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otherpowers](https://clawhub.ai/user/otherpowers)

### License/Terms of Use:


## Use Case:

Developers, product teams, and agents use Skill Namer to generate concise candidate names for skills, domains, products, protocols, and agent-economy primitives, then narrow them with constraints, accessibility checks, and manual availability links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may remember naming preferences for later sessions.

Mitigation: Avoid storing sensitive preferences and review any remembered TLD, provider, or checking-mode defaults before reuse.

Risk: API-based availability checking may require external service credentials.

Mitigation: Use the default manual link mode unless API checks are explicitly needed, and provide API keys only to intended official services.

Risk: Availability guidance can be incomplete when checks are manual, blocked, or provider-specific.

Mitigation: Treat unchecked names as unknown and verify domain or ENS status directly with the provider before claiming or purchasing.

Risk: Generated names can still create trademark, brand-confusion, or social-harm concerns.

Mitigation: Perform legal, brand, accessibility, and harm-aware review before adopting a finalist name.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/otherpowers/skills/skill-namer)
- [Portmanteau Forge Building Blocks](artifact/blocks.md)
- [Root-Words Guidance](artifact/root-words.md)
- [ENS Manager](https://app.ens.domains/)
- [Unstoppable Domains Search](https://unstoppabledomains.com/search)
- [GoDaddy Domain Search](https://www.godaddy.com/domainsearch/find)
- [Namecheap Domain Search](https://www.namecheap.com/domains/registration/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with candidate lists, caveats, manual availability links, and optional shell command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include remembered naming preferences such as favorite TLDs, availability-check mode, and preferred providers when the user sets them.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
