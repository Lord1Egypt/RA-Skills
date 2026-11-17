## Description:

Recall Local provides local memory search for OpenClaw agents by running a lightweight Node.js server that indexes ~/clawd/memory/, MEMORY.md, and WORKING.md, then exposes keyword search over them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wrentheai](https://clawhub.ai/user/wrentheai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Recall Local to set up and query a local index of OpenClaw memory files when they need to retrieve prior session history, decisions, fixes, or learned context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private agent memory may be exposed through an unauthenticated local web service.

Mitigation: Bind the service to 127.0.0.1, avoid LAN exposure by default, and require authentication before any network-accessible deployment.

Risk: Search responses may expose sensitive memory content or absolute local file paths.

Mitigation: Return only the minimum source metadata needed for users, avoid absolute file paths, and review results before sharing them outside the local machine.

Risk: A persistent LaunchAgent can keep the service running after setup.

Mitigation: Make auto-start an explicit optional step and document how to stop and uninstall the LaunchAgent.

Risk: Empty searches can return recent memory chunks without a specific query.

Mitigation: Reject empty searches or require an explicit user action before showing unfiltered memory content.

## Reference(s):

- [Recall Local skill page](https://clawhub.ai/wrentheai/skills/recall-local)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup, start, health-check, and search guidance for a local memory search service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
