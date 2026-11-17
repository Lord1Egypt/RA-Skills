## Description:

Look up domain WHOIS registration info, including registrar, creation date, expiry date, nameservers, and domain status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogue-agent1](https://clawhub.ai/user/rogue-agent1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, and external users use this skill to inspect WHOIS registration details for domains, including registrar, dates, nameservers, and status. It can return parsed text, raw WHOIS responses, or JSON from direct WHOIS queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WHOIS lookups require outbound network access and may be directed to arbitrary WHOIS servers through the --server option.

Mitigation: Use trusted WHOIS servers, restrict arbitrary server overrides in shared environments, and review destinations before running the command.

Risk: Large or slow WHOIS responses can consume time or memory in automated workflows.

Mitigation: Add a response-size cap and overall deadline before using the skill in exposed or high-volume automation.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON with command-line examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries WHOIS servers over the network and may return raw registrar responses.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
