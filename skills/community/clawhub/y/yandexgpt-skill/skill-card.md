## Description: <br>
OpenAI-compatible translation proxy for Yandex Cloud Foundation Models (YandexGPT). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smvlx](https://clawhub.ai/user/smvlx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run a local OpenAI-compatible proxy that routes chat completion requests to YandexGPT models. It helps configure credentials, start and stop the proxy, inspect status, and patch OpenClaw provider configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a Yandex API key and folder ID in a local environment file. <br>
Mitigation: Keep the environment file private, avoid committing it, and rotate the Yandex API key if it may have been exposed. <br>
Risk: Prompts sent through the proxy are forwarded to Yandex Cloud. <br>
Mitigation: Use the proxy only with data that is allowed by the user's organization and Yandex Cloud account policies. <br>
Risk: The patch script modifies the OpenClaw configuration file. <br>
Mitigation: Back up and review ~/.openclaw/openclaw.json before running the patch script. <br>
Risk: The proxy runs as a background localhost service on port 8444. <br>
Mitigation: Use the status and stop scripts to confirm the proxy state and stop it when it is not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smvlx/yandexgpt-skill) <br>
- [Project homepage](https://github.com/smvlx/openclaw-ru-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and OpenAI-compatible JSON endpoint behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, curl, YANDEX_API_KEY, and YANDEX_FOLDER_ID; the local proxy listens on port 8444 by default.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
