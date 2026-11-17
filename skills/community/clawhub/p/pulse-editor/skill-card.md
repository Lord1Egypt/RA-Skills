## Description:

Generate and build Pulse Apps using the Vibe Dev Flow API. Use this skill when the user wants to create, update, or generate code for Pulse Editor applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shellishack](https://clawhub.ai/user/shellishack)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to create, update, build, and publish Pulse Editor applications through the Pulse Editor Vibe Dev Flow API. It is useful when application generation should run through Pulse Editor's cloud service instead of local code generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and app-generation details are sent to Pulse Editor's cloud service, and generated apps may be published through that service.

Mitigation: Avoid including secrets or private business data in prompts, and use the skill only when publication through Pulse Editor is acceptable.

Risk: The skill requires a Pulse Editor API key for authenticated requests.

Mitigation: Use a dedicated API key, store it in an environment variable or secure secret store, and do not hardcode it in examples or generated code.

Risk: Example dependency installation may affect the local development environment if run directly.

Mitigation: Run examples in an isolated project or virtual environment and pin dependencies when adapting the examples.

## Reference(s):

- [Pulse Editor Documentation](https://docs.pulse-editor.com/)
- [Pulse Editor API Reference](https://docs.pulse-editor.com/api-reference)
- [Get Pulse Editor API Key](https://docs.pulse-editor.com/api-reference/get-pulse-editor-api-key)
- [Pulse Editor GitHub](https://github.com/ClayPulse/pulse-editor)
- [ClawHub Skill Page](https://clawhub.ai/shellishack/skills/pulse-editor)

## Skill Output:

**Output Type(s):** [API Calls, Code, Shell commands, Configuration instructions, JSON, Guidance]

**Output Format:** [Markdown guidance with code examples and JSON artifact output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Server-Sent Events streaming and returns published app links, source archive links, app IDs, and versions when generation completes.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
