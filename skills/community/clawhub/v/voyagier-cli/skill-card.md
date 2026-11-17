## Description:

Book real travel from your terminal - search flights, hotels and activities, plan trips, and check out with a price-gated booking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[demmersong](https://clawhub.ai/user/demmersong)

### License/Terms of Use:

MIT-0

## Use Case:

External travel advisors and AI agents use this skill to install and operate the Voyagier CLI for planning, searching, quoting, sending, and price-gated booking of travel itineraries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned or untrusted @voyagier/cli package can expose the agent environment to supply-chain risk.

Mitigation: Use a pinned and trusted @voyagier/cli version before installation.

Risk: Voyagier personal access tokens grant authenticated account access if exposed.

Mitigation: Protect the PAT like a password and avoid printing or passing it in command arguments.

Risk: Book and send commands can create real charges or email clients.

Mitigation: Require explicit user approval before any book or send command, and use dry-run or price gates before checkout.

Risk: Custom API endpoints can redirect authenticated workflows outside the expected Voyagier service.

Mitigation: Avoid custom API endpoints unless you control them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/demmersong/skills/voyagier-cli)
- [Voyagier API endpoint](https://travel.voyagier.com/api)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON]

**Output Format:** [Markdown with inline bash commands and JSON-oriented CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the voyagier CLI binary and a Voyagier personal access token for authenticated workflows.]

## Skill Version(s):

2.14.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
