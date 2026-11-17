## Description:

OpenAI-compatible translation proxy for Yandex Cloud Foundation Models (YandexGPT).

This skill is ready for commercial/non-commercial use.

## Publisher:

[smvlx](https://clawhub.ai/user/smvlx)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run a local OpenAI-compatible endpoint that translates model-listing and chat-completion requests to Yandex Cloud Foundation Models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts an unauthenticated local proxy that uses Yandex credentials.

Mitigation: Use a dedicated least-privilege Yandex API key, run the proxy only on trusted machines, and add local authentication and request limits before use on shared systems.

Risk: The setup flow stores Yandex credentials in a local environment file.

Mitigation: Set ~/.openclaw/yandexgpt.env to owner-only permissions and rotate the key if the file may have been exposed.

Risk: The configuration patch script modifies the OpenClaw configuration and can use OPENCLAW_CONFIG.

Mitigation: Back up openclaw.json before running the patch script and avoid untrusted OPENCLAW_CONFIG values.

Risk: The process scripts use shared temporary PID and log paths.

Mitigation: Avoid running on shared machines unless private runtime files are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smvlx/skills/yandexgpt-skill)
- [Project homepage](https://github.com/smvlx/openclaw-ru-skills)
- [Publisher profile](https://clawhub.ai/user/smvlx)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, curl, YANDEX_API_KEY, and YANDEX_FOLDER_ID; creates or updates local OpenClaw configuration and starts a local proxy process.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
