## Description:

Guides agents in using RunningHub AI through RHMCP to generate images, videos, or audio and choose apps, parameters, polling, storage, and retries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airix315](https://clawhub.ai/user/airix315)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to route media-generation requests to RunningHub AI apps, fill required parameters, manage asynchronous polling, and return generated media URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup asks users to clone and build external RHMCP code without a pinned commit or release.

Mitigation: Install only a reviewed, pinned RHMCP version in a sandbox or low-privilege environment before enabling the skill.

Risk: The skill requires a RunningHub API key and local configuration files.

Mitigation: Use least-privilege credentials, keep production secrets out of install and build steps, and rotate the key if it is exposed.

Risk: Prompts, image URLs, uploaded media, and generated outputs may be sent to RunningHub or related infrastructure.

Mitigation: Do not submit private, regulated, or sensitive content unless that cloud sharing is approved for the use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/airix315/skills/runninghub-skill)
- [RHMCP project](https://github.com/AIRix315/RHMCP)
- [OpenClaw](https://openclaw.ai)
- [RunningHub](https://www.runninghub.cn)
- [Recommended apps](references/recommended-apps.json)
- [Templates](references/templates.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline JavaScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance can include RunningHub app aliases, parameter defaults, polling intervals, storage recommendations, and generated media URLs returned by RHMCP tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
