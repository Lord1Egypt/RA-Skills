## Description:

RollingGo Hotel CN helps agents search, compare, price-check, and guide hotel bookings through RollingGo's hotel service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dreamtzlong](https://clawhub.ai/user/dreamtzlong)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to find hotels by location, budget, star rating, amenities, or brand, compare options, check live room prices, and proceed through a guarded booking flow. The skill also supports order lookup after user authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can interact with a real hotel booking service, collect contact details, create orders, issue payment links, and read booking history.

Mitigation: Require explicit user confirmation before locking prices or creating orders, verify contact details before booking, and treat authorization and payment links as sensitive.

Risk: The skill asks agents to install or update mutable executable tooling from RollingGo npm and GitHub release channels.

Mitigation: Review the skill before installation, trust only the intended RollingGo distribution channels, and prefer a pinned, verified, skill-local executable before using it for bookings.

Risk: The security summary reports Windows wrapper patterns that can turn user-provided booking text into shell execution risk.

Mitigation: Run the skill in a least-privileged environment and avoid passing unvalidated free text through shell execution paths.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dreamtzlong/skills/rollinggo-hotel-cn)
- [CLI Command Parameters](references/cli-params.md)
- [RollingGo Hotel CLI Releases](https://github.com/RollingGo-AI/oauth-hotel-cli/releases/latest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with structured hotel cards, booking prompts, authorization links, payment links, and agent-executed command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user-facing prices, hotel images, booking status, authorization links, and payment links; technical identifiers are intended to be hidden from the end user.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact frontmatter reports 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
