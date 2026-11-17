## Description:

Provision and manage on-demand GPUs on VAST.ai, including search by GPU and price, renting containers, retrieving SSH details, and checking account balance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sschepis](https://clawhub.ai/user/sschepis)

### License/Terms of Use:

ISC

## Use Case:

Developers and engineers use this skill to find, rent, connect to, and monitor VAST.ai GPU instances from an agent or CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create paid VAST.ai cloud instances without code-enforced confirmation, spending limits, or teardown support.

Mitigation: Use a limited VAST.ai API key where possible, manually verify the offer, hourly price, account balance, and stop plan before renting, and add confirmation, spending-limit, and teardown controls before treating the skill as low risk.

Risk: Debug logging may expose sensitive API or account details if enabled.

Mitigation: Keep DEBUG unset during normal use and rotate the VAST.ai API key if it appears in logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sschepis/skills/vast-ai)
- [Publisher profile](https://clawhub.ai/user/sschepis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-like command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform authenticated VAST.ai API calls that search offers, rent instances, retrieve SSH connection strings, and report account balance.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
