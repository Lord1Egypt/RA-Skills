## Description:

Use Chanjing text-to-digital-person APIs to create AI portrait images, turn them into talking videos, optionally run LoRA training, poll async tasks, and explicitly download generated assets when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyuting214](https://clawhub.ai/user/zuoyuting214)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run Chanjing text-to-digital-person workflows that create portrait images, convert selected images into talking videos, optionally train LoRA models, poll asynchronous task status, and save generated assets only when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Chanjing app_id, secret_key, and cached access tokens locally.

Mitigation: Install and configure it only for intended Chanjing API use, keep the credentials file private, and use CHANJING_CONFIG_DIR when credentials should be isolated from the default user profile.

Risk: Generated portrait images and talking videos may contain sensitive personal or brand media.

Mitigation: Review generated outputs before sharing them and request downloads only when local persistence under outputs/text-to-digital-person/ is intended.

## Reference(s):

- [Chanjing Open API](https://open-api.chanjing.cc)
- [reference.md](reference.md)
- [examples.md](examples.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown with inline bash commands, task identifiers, URLs, and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images or videos are saved under outputs/text-to-digital-person/ only when explicitly requested.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
