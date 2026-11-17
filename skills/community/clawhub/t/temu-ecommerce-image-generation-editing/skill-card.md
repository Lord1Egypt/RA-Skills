## Description:

Create and edit Temu product submission images, variant sets, package-content graphics, feature galleries, and multi-market campaign bases with reference-guided AI Hive production.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, catalog operators, and ecommerce content teams use this skill to generate and edit Temu-ready product images, SKU variants, package-content visuals, and campaign backgrounds from verified product masters and reference media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An AI Hive API key may be sent to an arbitrary configured API server if --base-url, AI_HIVE_BASE_URL, or local configuration is changed.

Mitigation: Use the default trusted AI Hive endpoint unless you control the server, and rotate the key if it was ever used with an untrusted endpoint.

Risk: The skill can store an AI Hive API key locally for repeated CLI use.

Mitigation: Protect the local configuration file, avoid sharing it, and remove or rotate the key when access is no longer needed.

Risk: Generated product images can introduce inaccurate SKU, package, measurement, or localized-claim details.

Mitigation: Use the documented product master and batch gates: manually verify one master image, isolate variant changes, and add measurements or localized claims only from approved structured data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/temu-ecommerce-image-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key portal](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, files]

**Output Format:** [Markdown guidance with bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI can upload reference media, submit AI Hive image generation tasks, poll task status, and download generated image files; it supports batch count, routing mode, output directory, and no-download mode.]

## Skill Version(s):

1.0.0 (source: release metadata; artifact CHANGELOG top entry 1.3.0 differs)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
