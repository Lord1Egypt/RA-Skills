## Description: <br>
Give OpenClaw full access to Telegram through a user-owned local Telegram session, with options for Chiho.ai Cloud or a self-hosted tgchats runtime. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seichris](https://clawhub.ai/user/seichris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to Telegram through an explicit user-owned account login when bot access is too limited. It supports hosted CRM workflows through Chiho.ai Cloud or self-hosted local operation through tgchats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad account-level Telegram access, including sensitive chats, contacts, metadata, and write-capable workflows. <br>
Mitigation: Use a dedicated Telegram account when possible, connect only an account controlled by the user, and require explicit user approval before sending messages or enabling write-capable automation. <br>
Risk: The hosted Chiho.ai Cloud path may process or store Telegram session data and CRM metadata outside the user's local environment. <br>
Mitigation: Review Chiho.ai data handling before using the cloud path, and choose the self-hosted tgchats runtime when tighter control over messages, contacts, metadata, or session storage is required. <br>
Risk: Agent access tokens and self-hosted Telegram credentials can expose the connected Telegram account if mishandled. <br>
Mitigation: Store tokens and environment variables securely, avoid sharing them in chat or logs, and revoke or rotate credentials when access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seichris/telegram-full-access) <br>
- [telegram-for-ai-agents homepage](https://github.com/chihoai/telegram-for-ai-agents) <br>
- [Local tgchats runtime skill](https://github.com/chihoai/telegram-for-ai-agents/blob/main/skills/tgchats-local/SKILL.md) <br>
- [Telegram workflow catalog](https://github.com/chihoai/telegram-for-ai-agents/blob/main/docs/SKILL_CATALOG.md) <br>
- [Chiho.ai signup](https://chiho.ai/signup) <br>
- [Telegram API application credentials](https://my.telegram.org/apps) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with setup steps and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-authorized Telegram access; self-hosted setup may use TELEGRAM_API_ID, TELEGRAM_API_HASH, and DATABASE_URL.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
