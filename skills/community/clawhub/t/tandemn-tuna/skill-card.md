## Description: <br>
Deploy and serve LLM models on GPU. Compare GPU pricing. Launch vLLM on Modal, RunPod, Cerebrium, Cloud Run, Baseten, or Azure with spot instance fallback. OpenAI-compatible inference endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[choprahetarth](https://clawhub.ai/user/choprahetarth) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to deploy, manage, check, and tear down GPU-backed LLM inference services across serverless and spot infrastructure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create real cloud GPU infrastructure that may incur cost. <br>
Mitigation: Use least-privilege provider credentials, confirm the target account, project, or subscription before deployment, and monitor budgets. <br>
Risk: Deployments may expose public endpoints when public access is requested. <br>
Mitigation: Avoid public endpoints unless authentication, rate limits, logging, and budget monitoring are in place. <br>
Risk: Bulk teardown can remove active deployments. <br>
Mitigation: Confirm any destroy-all request explicitly before running it. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/choprahetarth/tandemn-tuna) <br>
- [Project homepage](https://github.com/Tandemn-Labs/tandemn-tuna) <br>
- [Support issues](https://github.com/Tandemn-Labs/tandemn-tuna/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes provider setup steps, deployment commands, status and cost commands, and teardown guidance.] <br>

## Skill Version(s): <br>
0.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
