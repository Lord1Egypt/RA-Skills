## Description:

Deploy and serve LLM models on GPU, compare GPU pricing, launch vLLM on Modal, RunPod, Cerebrium, Cloud Run, Baseten, or Azure with spot instance fallback, and create an OpenAI-compatible inference endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[choprahetarth](https://clawhub.ai/user/choprahetarth)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to deploy, inspect, manage, and tear down GPU-backed LLM inference services across serverless and spot cloud providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide users toward cloud actions that create infrastructure costs.

Mitigation: Use least-privilege cloud credentials, monitor cloud costs, and validate provider configuration before deployment.

Risk: The skill can propose commands that expose inference endpoints publicly.

Mitigation: Avoid public endpoint options except for controlled testing and review access settings before deployment.

Risk: The skill can propose destroy commands that remove deployments.

Mitigation: Check current deployments with list or status commands before running destroy commands, especially commands targeting all deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/choprahetarth/skills/tandemn-tuna)
- [Tandemn Tuna project homepage](https://github.com/Tandemn-Labs/tandemn-tuna)
- [Tandemn Tuna support issues](https://github.com/Tandemn-Labs/tandemn-tuna/issues)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that create, expose, list, inspect, or destroy cloud GPU deployments.]

## Skill Version(s):

0.0.1 (source: SKILL.md frontmatter, clawhub.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
