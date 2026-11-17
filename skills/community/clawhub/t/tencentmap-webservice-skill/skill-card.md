## Description:

Tencent Map JavaScript GL development guidance for agents that help developers build, review, and debug map initialization, overlays, layers, events, visualization, search, routing, geocoding, administrative districts, IP location, geometry, 3D model display, and performance optimization code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get Tencent Map JSAPI GL guidance, code examples, API usage details, and best practices for web map and geospatial visualization features. It is intended for normal agent-assisted development workflows where the user can provide or obtain a Tencent Maps API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The temporary-key workflow asks the user for a phone number and SMS code and may expose tokens or API keys in command output, logs, or local files.

Mitigation: Prefer a restricted user-provided TMAP_JSAPI_KEY, avoid running the workflow on shared machines, and rotate or revoke any key that may have been exposed.

Risk: The workflow can store Tencent Maps key material in ~/.tencentmap/tempkey.json as local plaintext configuration.

Mitigation: Review local file permissions, remove stale temporary-key files when no longer needed, and avoid committing or sharing the configuration file.

Risk: The skill is a large development reference and may guide code generation that calls Tencent Maps APIs incorrectly if examples are not checked against the included docs.

Mitigation: Review generated code against the bundled API reference and demos before deployment, especially API parameters, enabled libraries, browser requirements, and key handling.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/tencent-adm/skills/tencentmap-webservice-skill)
- [Tencent Map JSAPI GL overview](https://lbs.qq.com/webApi/javascriptGL/glGuide/glOverview)
- [Skill entry and reference index](artifact/SKILL.md)
- [Repository README](artifact/README.md)
- [Temporary key workflow guide](artifact/tencentmap-jsapi-gl-skill/tempkey-guide.md)
- [Tencent Maps API reference](artifact/tencentmap-jsapi-gl-skill/references/api_reference.md)
- [JSAPI GL reference docs](artifact/tencentmap-jsapi-gl-skill/references/jsapigl/docs/)
- [Visualization reference docs](artifact/tencentmap-jsapi-gl-skill/references/visualization/docs/)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference TMAP_JSAPI_KEY and local Tencent Maps documentation or demos when producing examples.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
