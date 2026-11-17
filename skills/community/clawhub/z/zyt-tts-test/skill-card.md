## Description:

Use Chanjing TTS API to convert text to speech by listing voices, creating synthesis tasks, and polling task status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyuting214](https://clawhub.ai/user/zuoyuting214)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate Chinese or English speech with Chanjing TTS, including voice listing, synthesis task creation, task polling, and returning remote audio URLs with subtitle timestamps when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores app_id, secret_key, and cached access_token in a local JSON credentials file.

Mitigation: Keep ~/.chanjing or CHANJING_CONFIG_DIR private, avoid shared directories, and restrict access to the credentials file.

Risk: Credentials are sent to Chanjing's API to obtain access tokens.

Mitigation: Install and use the skill only when the user intends to use Chanjing TTS and accepts the credential flow.

Risk: Some scripts named in the documentation were not present in the reviewed artifact, so functionality may be incomplete.

Mitigation: Verify the installed artifact includes the expected workflow scripts before relying on the complete TTS flow.

## Reference(s):

- [Chanjing Open API](https://open-api.chanjing.cc)
- [Zyt TTS on ClawHub](https://clawhub.ai/zuoyuting214/skills/zyt-tts-test)
- [Publisher profile](https://clawhub.ai/user/zuoyuting214)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns remote audio URLs by default and may include subtitle timestamps from the API response; it does not download audio unless the user explicitly asks.]

## Skill Version(s):

0.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
