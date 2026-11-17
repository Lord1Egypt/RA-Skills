## Description:

WodeApp AI Engine lets agents use one WODEAPP_API_KEY to access text, vision, audio, video, page building, visual workflows, digital humans, and multi-engine video through MCP and REST.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diankourenxia](https://clawhub.ai/user/diankourenxia)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to connect an agent to WodeApp's unified AI platform, create and publish projects, generate pages and assets, run visual workflows, and access multimodal AI capabilities with a single API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through broad remote project and workflow actions, including publishing, deleting, rolling back, messaging, and workflow execution.

Mitigation: Require explicit user confirmation before actions that publish, delete, roll back, send messages, or run workflows.

Risk: Real projects or business integrations may be affected if a broad API key is used.

Mitigation: Use project-scoped WODEAPP_API_KEY values with billing caps and revoke keys that are no longer needed.

Risk: Uploaded files and generated URLs may expose sensitive data.

Mitigation: Avoid sensitive uploads and do not send confidential or personal data unless the user has explicitly accepted the handling risk.

Risk: Published project subdomains may expose MCP or workflow endpoints if they remain unauthenticated.

Mitigation: Do not expose project subdomains until endpoint authentication and access controls are confirmed.

Risk: Evidence notes inconsistent privacy disclosures.

Mitigation: Review data handling expectations before connecting real projects, customer data, or business integrations.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/diankourenxia/skills/wodeapp-ai)
- [WodeApp homepage](https://wodeapp.ai)
- [WodeApp API skills](https://wodeapp.ai/api-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown with inline JSON, configuration snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include remote project URLs, generated asset URLs, workflow results, and confirmation steps for destructive or publishing actions.]

## Skill Version(s):

1.0.18 (source: ClawHub release metadata; artifact frontmatter reports 2.8.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
