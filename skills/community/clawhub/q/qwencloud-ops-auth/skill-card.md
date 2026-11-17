## Description:

Configures QwenCloud authentication, API-key setup, endpoint selection, and 401 troubleshooting for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure QwenCloud API credentials, distinguish standard API keys from Coding Plan keys, and troubleshoot authentication failures without exposing secrets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API keys, .env files, and OSS credentials.

Mitigation: Use placeholders by default, avoid plaintext secret output, add .env files to .gitignore, and let the agent store real secrets only after explicit user approval.

Risk: The skill includes an update-check path that may install or run other skills through unpinned commands.

Mitigation: Inspect and pin the installer or source before running update installation commands, or skip that path unless skill modification is explicitly intended.

Risk: Confusing Coding Plan keys with standard QwenCloud API keys can cause failed calls or unintended pay-as-you-go charges.

Mitigation: Use standard sk- keys for API scripts, reserve sk-sp- keys for coding agents, and verify usage in the listed QwenCloud billing pages.

## Reference(s):

- [QwenCloud Authentication Skill](https://clawhub.ai/cuixiaoyang123/skills/qwencloud-ops-auth)
- [Coding Plan vs Standard API Key](references/codingplan.md)
- [Custom OSS Storage for File Uploads](references/custom-oss.md)
- [Official Documentation URLs](references/sources.md)
- [Agent Compatibility](references/agent-compatibility.md)
- [QwenCloud API Key Management](https://home.qwencloud.com/api-keys)
- [QwenCloud OpenAI Compatibility](https://docs.qwencloud.com/api-reference/preparation/install-sdk)
- [QwenCloud Coding Plan Overview](https://docs.qwencloud.com/coding-plan/overview)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct users to create local output under output/qwencloud-ops-auth/ for verification evidence.]

## Skill Version(s):

0.2.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
