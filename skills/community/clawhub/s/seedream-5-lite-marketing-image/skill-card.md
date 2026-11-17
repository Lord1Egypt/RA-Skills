## Description:

Generates and adapts Seedream 5.0 Lite marketing visuals for campaign key art, advertising creative, social posts, banners, email, and landing pages through AI Hive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, designers, and developers use this skill to generate campaign image concepts and channel-specific variants from prompts and reference images. Human reviewers should finalize copy, prices, legal terms, campaign mechanics, and brand approvals before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An API key can be sent to an unintended endpoint if the base URL is overridden.

Mitigation: Use only the intended AI Hive HTTPS endpoint and avoid setting --base-url, AI_HIVE_BASE_URL, or config base_url to untrusted values.

Risk: The init flow stores an API key in ~/.ai-hive/config.json.

Mitigation: Use an isolated environment, restrict local file access, and rotate the key if the configuration file may have been exposed.

Risk: Reference images selected by the user are uploaded to the provider.

Mitigation: Use only approved assets and avoid uploading confidential, regulated, or unlicensed images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedream-5-lite-marketing-image)
- [AI Hive API key page](https://ai-hive.iclip.cn/chat)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands; runtime outputs include JSON task records and downloaded image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports reference images, batch generation, routing mode, model parameters, output directory selection, and no-download submission mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
