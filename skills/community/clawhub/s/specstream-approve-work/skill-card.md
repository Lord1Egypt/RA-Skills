## Description:

Approve an exact price, up to the maximum the person set. This starts paid work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[specstream](https://clawhub.ai/user/specstream)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to start paid SpecStream work after a person or standing authority approves the reviewed quote, exact scope, and maximum spend. It also guides recovery of unclear requests and tracking of delivered results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Starting work can incur charges through the configured SpecStream account.

Mitigation: Approve the reviewed quote, exact work scope, and maximum spend; keep any standing authority narrowly bounded.

Risk: The remote service's enforcement of approval and spending controls was not verified.

Mitigation: Check request status and resulting account charges through trusted account records, and do not proceed when authority or balance is missing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/specstream/skills/specstream-approve-work)
- [SpecStream MCP service](https://api.specstream.ai/mcp)

## Skill Output:

**Output Type(s):** [API Calls, Guidance]

**Output Format:** [Structured MCP requests and concise status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts paid work only after approval of the reviewed quote, scope, and spending limit.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
