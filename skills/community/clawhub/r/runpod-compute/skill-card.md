## Description:

RunPod API integration with API key authentication. Create and manage GPU clusters, serverless endpoints, templates, and secrets for ML inference and distributed computing workloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect OpenClaw to RunPod through ClawLink and manage GPU compute resources for ML training, inference, and distributed computing workloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on ClawLink as an external plugin and credential proxy for a RunPod API key.

Mitigation: Use a dedicated, least-privileged RunPod API key where possible and install the skill only when the ClawLink trust boundary is acceptable.

Risk: RunPod write actions can create or change clusters, endpoints, templates, secrets, registry credentials, and SSH-related account settings.

Mitigation: Review previews before writes, require explicit confirmation for create, update, and delete actions, and monitor RunPod for unexpected resource or credential changes.

## Reference(s):

- [RunPod API Documentation](https://docs.runpod.io)
- [GPU Cloud Pods](https://docs.runpod.io/pods)
- [Serverless Endpoints](https://docs.runpod.io/serverless-endpoints)
- [Templates](https://docs.runpod.io/templates)
- [Secrets Management](https://docs.runpod.io/secrets)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/runpod-compute)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown]

**Output Format:** [Markdown with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides ClawLink tool discovery, previews, confirmations, and RunPod API calls; does not require users to paste RunPod API keys into chat.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
