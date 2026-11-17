## Description:

Provides Tencent Map JavaScript GL guidance, API references, and examples for building and debugging web map features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to answer Tencent Map JSAPI GL questions, generate map and visualization code examples, and troubleshoot API usage for web map applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide account-linked Tencent Map key enrollment using a phone number and SMS verification code.

Mitigation: Use an existing TMAP_JSAPI_KEY when possible, provide verification codes only in a trusted session, and avoid sharing codes in logs, screenshots, or copied examples.

Risk: The skill can contact Tencent LBS services and create or reuse API keys.

Mitigation: Review the key-enrollment flow before installation if only documentation support is needed, and confirm the account and terms before running key-related commands.

Risk: Generated phone and key records may be saved locally in plaintext.

Mitigation: Use restrictive local file permissions, avoid shared machines, and remove or rotate stored keys when they are no longer needed.

## Reference(s):

- [Tencent Map JSAPI GL Overview](https://lbs.qq.com/webApi/javascriptGL/glGuide/glOverview)
- [Temporary Experience Key Guide](tencentmap-jsapi-gl-skill/tempkey-guide.md)
- [AI Scenario Key API Reference](tencentmap-jsapi-gl-skill/references/api_reference.md)
- [JSAPI GL Documentation](tencentmap-jsapi-gl-skill/references/jsapigl/docs/)
- [Visualization Documentation](tencentmap-jsapi-gl-skill/references/visualization/docs/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown responses with JavaScript or HTML examples, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference TMAP_JSAPI_KEY or a local Tencent Map temporary key configuration when a key is needed.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence; artifact frontmatter says 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
