## Description:

Dispatch tasks to ThinkForce AI agents through REST API workflows for creating, assigning, running, polling, and managing missions and subtasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ade5791](https://clawhub.ai/user/ade5791)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to operate ThinkForce missions: resolve company context, create and decompose missions, assign agents, wire dependencies, run subtasks, poll results, and handle lifecycle actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct agents to use stored credentials and interact with authenticated services.

Mitigation: Require explicit user approval before credential use and avoid exposing credential values in prompts, outputs, screenshots, or shared mission artifacts.

Risk: Mission sharing, invitations, public uploads, and authenticated screenshots can expose sensitive customer or internal data.

Mitigation: Use private or expiring links where possible and require explicit consent before sharing, inviting collaborators, uploading public files, or capturing authenticated pages.

Risk: The skill includes destructive lifecycle operations such as mission deletion, member revocation, and cancellation of in-flight work.

Mitigation: Confirm destructive actions with the user immediately before execution and read current mission state before applying changes.

Risk: External vendor forwarding and paid API usage can create data-handling and cost exposure.

Mitigation: Review the mission context before forwarding data to vendors, prefer minimum necessary data, and surface budget or cost information when relevant.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ade5791/skills/thinkforce)
- [ThinkForce Application](https://app.thinkforce.ai)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, JSON payloads, Shell commands, Configuration]

**Output Format:** [Markdown with HTTP, JSON, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint patterns, request bodies, polling rules, lifecycle controls, and consent cautions for mission sharing and destructive actions.]

## Skill Version(s):

2.0.11 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
