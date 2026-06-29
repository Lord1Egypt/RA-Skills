## Description: <br>
Uandai platform -- configure API access, package OpenClaw workspace zip, upload agents, delete trainer-owned agents, list subscriptions, and invoke runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uandai](https://clawhub.ai/user/uandai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure Uandai API access, package OpenClaw workspaces for upload, manage trainer-owned agents, and invoke subscribed agents through Uandai workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Uandai API keys and access tokens for account actions. <br>
Mitigation: Install only if you trust Uandai with the API key, keep setup in a private session, never echo the full key, and rotate the key if it is exposed. <br>
Risk: The skill can upload, invoke, and delete trainer-owned agents. <br>
Mitigation: Review prompts before upload, invocation, proposal submission, or deletion, and confirm required user-sourced fields and agent identifiers before calling endpoints. <br>


## Reference(s): <br>
- [Uandai Programmatic API documentation](https://api.uandai.ai/docs/programmatic-api) <br>
- [ClawHub listing](https://clawhub.ai/uandai/skills/uandai-ai) <br>
- [Programmatic API guide](references/programmatic-api.md) <br>
- [Agent packaging guide](references/agent-packaging.md) <br>
- [OpenClaw integration guide](references/openclaw-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code blocks, HTTP examples, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires UANDAI_API_KEY, UANDAI_API_ORIGIN, and APP_SITE_URL; exchanges raw API keys for access tokens before business API calls.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
