## Description:

Dispatch paid tasks to physical robots via the Robot Task Protocol (RTP) on the Spraay x402 gateway, with payment held in escrow until the robot completes the work, or register and manage a robot to earn from tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and robot operators use the skill to discover robots, inspect capabilities and pricing, dispatch and monitor paid tasks, and register or manage their own robots on the RTP network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dispatching a task can move or actuate real hardware and incurs a dispatch payment plus the robot's task fee.

Mitigation: Confirm the target robot, task parameters, environmental safety, and total fee with the user before dispatch; check the robot profile and use a wallet with spending limits.

Risk: Reporting a task complete releases its escrow payment, while robot updates and deregistration can take effect immediately.

Mitigation: Verify the task outcome before reporting completion, and confirm the robot ID, intended change, and consequences before any operator mutation.

Risk: Gateway ownership enforcement and escrow guarantees have not been independently tested.

Mitigation: Use a trusted gateway and do not rely on escrow or ownership checks as independently verified guarantees.

## Reference(s):

- [Robot Task Protocol specification](https://github.com/plagtech/rtp-spec)
- [RTP TypeScript SDK](https://github.com/plagtech/rtp-sdk)
- [RTP Python SDK](https://github.com/plagtech/rtp-python-sdk)
- [Spraay app](https://spraay.app)
- [Spraay documentation](https://docs.spraay.app)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON API requests and responses, with shell command examples and concise workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes robot and task identifiers, status and result data, and payment instructions when returned by the gateway.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
