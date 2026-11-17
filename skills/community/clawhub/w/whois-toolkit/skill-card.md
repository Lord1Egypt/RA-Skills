## Description:

Domain WHOIS lookup toolkit for querying registrar, creation/expiry dates, nameservers, status, and registrant info.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site reliability engineers, security analysts, and domain administrators use this skill to inspect domain registration details, check renewal timing, and collect structured WHOIS data for user-selected domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Domain names are sent to external WHOIS infrastructure during lookups.

Mitigation: Use the skill only with user-chosen domains and avoid submitting sensitive internal or unintended domain names.

Risk: The --server option can direct queries to a user-specified WHOIS host.

Mitigation: Use --server only with WHOIS hosts the user trusts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnywang2001/skills/whois-toolkit)
- [Publisher profile](https://clawhub.ai/user/johnnywang2001)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON from WHOIS lookup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include raw WHOIS responses when requested]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
