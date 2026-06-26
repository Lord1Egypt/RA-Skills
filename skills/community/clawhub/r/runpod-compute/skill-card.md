## Description: <br>
RunPod API integration with API key authentication. Create and manage GPU clusters, serverless endpoints, templates, and secrets for ML inference and distributed computing workloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML engineers use this skill to connect OpenClaw to RunPod through ClawLink, inspect GPU compute options, and manage pods, clusters, serverless endpoints, templates, secrets, registry credentials, and user settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate write actions that create paid GPU resources or modify RunPod infrastructure. <br>
Mitigation: Review previews carefully and require explicit user confirmation before create, update, or delete operations. <br>
Risk: The skill depends on sensitive RunPod API credentials and can manage secrets or registry authentication. <br>
Mitigation: Use ClawLink-hosted credential handling and avoid sharing API keys or secret values in chat. <br>
Risk: GPU type availability, pricing, and regional capacity can change frequently. <br>
Mitigation: Check live RunPod GPU availability before deploying pods, clusters, or endpoints. <br>


## Reference(s): <br>
- [RunPod API Documentation](https://docs.runpod.io) <br>
- [RunPod GPU Cloud Pods](https://docs.runpod.io/pods) <br>
- [RunPod Serverless Endpoints](https://docs.runpod.io/serverless-endpoints) <br>
- [RunPod Templates](https://docs.runpod.io/templates) <br>
- [RunPod Secrets Management](https://docs.runpod.io/secrets) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/runpod-compute) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ClawLink-mediated RunPod tool calls; write actions should be previewed and confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
