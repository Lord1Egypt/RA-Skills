## Description:

技能路由枢纽 helps OpenClaw route requests across many skills by grouping scenarios, selecting the top three relevant skills, and lowering priority for skills recorded as unsuccessful.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freak30](https://clawhub.ai/user/freak30)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to classify a request into a scenario bucket and select a small set of relevant skills for the agent to activate. It is intended to reduce routing overhead when many skills are installed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The router persistently logs snippets of routed request text in local plaintext history.

Mitigation: Avoid routing secrets, credentials, private code, or sensitive personal data through the skill unless logging is removed, minimized, or access-controlled.

Risk: Routing history can influence future skill recommendations and returned skill IDs may be used by downstream activation systems.

Mitigation: Validate selected skill IDs and require review before any downstream system automatically activates or executes returned skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freak30/skills/skill-router-xiaoz)
- [Publisher profile](https://clawhub.ai/user/freak30)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Console text and JSON-like route result objects, with Python and shell usage examples in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the request, detected scene, selected skill IDs, and routing reason; execution may append local routing history.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version note)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
