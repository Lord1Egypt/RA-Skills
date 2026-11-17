## Description:

Provides Tencent Map JavaScript GL guidance, API references, demos, and setup help for building map and visualization features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, review, or debug Tencent Map JSAPI GL code for map initialization, overlays, layers, events, controls, search, routing, geocoding, administrative areas, IP location, geometry, 3D models, and visualization layers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The temporary-key flow can send a phone number and SMS verification code to Tencent LBS endpoints.

Mitigation: Use the temporary-key flow only after reviewing the Tencent terms and privacy notices; prefer setting TMAP_JSAPI_KEY manually when possible.

Risk: The temporary-key flow stores the resulting API key locally in plaintext.

Mitigation: Secure or delete ~/.tencentmap/tempkey.json after use, and avoid the flow on shared or untrusted machines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tencent-adm/skills/tencentmap-jsapi-gl-skill)
- [Tencent Map JSAPI GL overview](https://lbs.qq.com/webApi/javascriptGL/glGuide/glOverview)
- [API reference](tencentmap-jsapi-gl-skill/references/api_reference.md)
- [Temporary key guide](tencentmap-jsapi-gl-skill/tempkey-guide.md)
- [JSAPI GL documentation](tencentmap-jsapi-gl-skill/references/jsapigl/docs/)
- [Visualization documentation](tencentmap-jsapi-gl-skill/references/visualization/docs/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, command examples, and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Tencent Map JSAPI key through TMAP_JSAPI_KEY or the local temporary-key configuration flow.]

## Skill Version(s):

1.0.4 (source: server release metadata; skill frontmatter reports 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
