## Description: <br>
按Agent类型（认知运营型/行为执行型/桥接调度型）差异化评分——每个Agent类型有独立的信任分权重系数。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and governance teams use this documentation skill to compare rating criteria for cognitive-operation, action-execution, and bridge-scheduling agents. It provides trust-score weighting guidance and curl examples for trying the linked governance API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The provided curl examples send governance keys and registration data to an external Cloudflare-tunnel endpoint. <br>
Mitigation: Confirm the service is trusted before use, avoid sensitive agent names, and use only test or least-privilege governance keys. <br>


## Reference(s): <br>
- [V19 Agent Rating on ClawHub](https://clawhub.ai/liuyanfeng1234/v19-agent-rating) <br>
- [V19 Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto) <br>
- [V19 Trust Engine](https://clawhub.com/skills/v19-trust-engine) <br>
- [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with tables and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; examples require user-run curl commands against an external governance endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
