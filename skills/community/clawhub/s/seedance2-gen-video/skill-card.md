## Description:

Generates, edits, and extends videos with Volcengine Doubao Seedance 2.0 models from text, image, video, and audio references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fackee](https://clawhub.ai/user/fackee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative automation users use this skill to generate, edit, or extend short videos through the Volcengine Seedance 2.0 API. It helps agents collect generation parameters, install the required SDK, run the bundled command-line script, and interpret the resulting video URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper loads local .env files and may expose broader environment configuration than the skill requires.

Mitigation: Run it in a dedicated environment that contains only ARK_API_KEY and avoid shared .env files with unrelated secrets.

Risk: Prompts, media URLs, and optional web-search requests are sent to Volcengine for generation.

Mitigation: Submit only prompts and media URLs that are intended for that service.

Risk: The Volcengine SDK dependency can change behavior if installed without a pinned version.

Mitigation: Pin and review the volcengine-python-sdk[ark] dependency before deployment.

Risk: Generated video URLs are temporary and valid for 24 hours.

Mitigation: Download or transfer generated videos promptly after a successful task.

## Reference(s):

- [Seedance 2.0 API Parameter Reference](references/api-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/fackee/skills/seedance2-gen-video)
- [ClawHub Publisher Profile](https://clawhub.ai/user/fackee)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script may return a generated video URL that is valid for 24 hours.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
