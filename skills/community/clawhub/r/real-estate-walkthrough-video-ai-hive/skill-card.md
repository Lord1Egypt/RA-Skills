## Description:

This skill helps real estate marketing, home design, hospitality, and spatial design teams turn authorized property images or renderings into walkthrough video plans, prompts, AI-HIVE video tasks, and acceptance checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External real estate marketing, home design, short-stay rental, and spatial design teams use this agent to plan and generate property walkthrough videos from authorized spatial media, platform requirements, budget constraints, and review criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or media files may be sent to the configured AI-HIVE service endpoint.

Mitigation: Use the default AI-HIVE endpoint unless the destination is fully trusted, avoid exposing API keys in logs or files, and upload only media the user is comfortable sending to the service.

Risk: The skill stores AI-HIVE credentials in a local configuration file.

Mitigation: Treat ~/.ai-hive/config.json as a secret, keep restrictive file permissions, and prefer an isolated Python environment with reviewed dependencies.

Risk: Generated walkthrough videos can misrepresent real property details if source facts are incomplete or unverified.

Mitigation: Require human review for area, lighting, facilities, views, brand claims, and other factual property details before publication.

Risk: Video generation calls may incur cost.

Mitigation: Confirm prompts, model mode, routing choice, and price snapshot before submitting tasks, and run small samples before batch generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/real-estate-walkthrough-video-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown with inline shell commands and optional JSON task or blueprint files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit AI-HIVE API tasks and download generated media after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
