## Description: <br>
SkillForge API 服务发现 - 自动发现和调用付费 AI 服务。当 OpenClaw Agent 需要某个能力但本地没有时，自动查找并推荐可用服务。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leongfans](https://clawhub.ai/user/leongfans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to detect when an OpenClaw task needs an external paid API, discover matching SkillForge services, and invoke a selected service after user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Service discovery and invocation can send user-provided data to configured paid third-party AI services. <br>
Mitigation: Require the agent to show the selected service, destination, data to be sent, and expected price before invoking a service; do not send secrets, regulated data, or private files unless the provider is trusted. <br>
Risk: Invocations may create billable usage through the configured SkillForge account. <br>
Mitigation: Use a dedicated revocable API key, keep a low max_cost_per_call setting, and require user approval before paid calls. <br>
Risk: A non-HTTPS platform URL can expose API credentials and request data in transit. <br>
Mitigation: Prefer an HTTPS SKILLFORGE_API_URL for production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leongfans/skillforge-discovery) <br>
- [Publisher Profile](https://clawhub.ai/user/leongfans) <br>
- [SkillForge Repository](https://github.com/skillforge/skillforge-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Structured JSON results and human-readable Markdown-style service lists, invocation status, billing details, and error messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, SKILLFORGE_API_URL, and SKILLFORGE_API_KEY; service invocation may send user-provided input to configured third-party providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
