## Description:

RunningHub helps agents use the RunningHub cloud ComfyUI platform to run AI workflows for image generation, video generation, video synthesis, face swapping, and workflow management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yfy-ai](https://clawhub.ai/user/yfy-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to guide agents in calling RunningHub API endpoints, selecting the China or international platform, running ComfyUI workflows, checking task status, and managing workflow resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, workflow inputs, uploaded media, task identifiers, and API keys may be sent to RunningHub endpoints.

Mitigation: Use the skill only when third-party RunningHub API use is intended, avoid submitting sensitive data unless approved, and store API keys in a secure secret store.

Risk: Some workflow runs may incur account charges.

Mitigation: Confirm before publishing, changing, or running workflows that could consume paid RunningHub resources.

Risk: The artifact notes API-key requirements and concurrency limits for RunningHub workflows.

Mitigation: Configure a valid API key before use and design calls to respect platform rate or concurrency limits.

## Reference(s):

- [ClawHub Runninghub Skill](https://clawhub.ai/yfy-ai/skills/runninghub)
- [RunningHub China Platform](https://www.runninghub.cn)
- [RunningHub International Platform](https://www.runninghub.ai)
- [RunningHub API Documentation](https://www.runninghub.cn/call-api)
- [RunningHub Works Square](https://www.runninghub.cn/works-square)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown with endpoint references and JavaScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include RunningHub API endpoints, workflow identifiers, task identifiers, and API-key handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
