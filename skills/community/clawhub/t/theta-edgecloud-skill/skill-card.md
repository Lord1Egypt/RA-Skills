## Description: <br>
Theta EdgeCloud runtime for OpenClaw cost optimization: route eligible AI, media, inference, and GPU workloads through Theta EdgeCloud with secure command-scoped auth, dry-run safety, and on-demand Qwen3/chat support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zeuslabsllc](https://clawhub.ai/user/zeuslabsllc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect OpenClaw workflows to Theta EdgeCloud for AI inference, media, video, GPU deployment, chatbot/RAG, billing, and readiness operations while keeping authentication scoped to invoked commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Theta credentials are required for live API operations. <br>
Mitigation: Use user-supplied credentials through the runtime secret provider or environment variables, and do not bundle or commit API keys. <br>
Risk: Deployment, video, wallet, and on-demand operations can mutate Theta resources or spend credits. <br>
Mitigation: Start with THETA_DRY_RUN=1, use budget caps for smoke tests, and require explicit approval before live paid or mutating operations. <br>
Risk: Private prompts, documents, media, or paid workloads may be sent to Theta services. <br>
Mitigation: Confirm the data and workload are appropriate for Theta EdgeCloud before routing them through this skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zeuslabsllc/theta-edgecloud-skill) <br>
- [Theta EdgeCloud on-demand endpoint](https://ondemand.thetaedgecloud.com) <br>
- [Theta EdgeCloud controller endpoint](https://controller.thetaedgecloud.com) <br>
- [Theta EdgeCloud API endpoint](https://api.thetaedgecloud.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance, shell command examples, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime commands may return dry-run previews, readiness status, inference responses, deployment state, balance snapshots, or redacted validation summaries.] <br>

## Skill Version(s): <br>
0.1.26 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
