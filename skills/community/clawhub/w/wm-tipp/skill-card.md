## Description: <br>
WM Tipp generates German-language 2026 World Cup match tips with Polymarket odds and sends them to configured Telegram recipients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcbuer](https://clawhub.ai/user/jcbuer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and personal automation users can use this skill to run a scheduled World Cup tipping workflow that reads a local schedule, fetches public Polymarket odds, and posts Markdown-formatted tips to Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram recipient or gateway misconfiguration can send scheduled tips to unintended chats. <br>
Mitigation: Review WM_CHAT_IDS and WM_TELEGRAM_API before running the script, and use a trusted local or HTTPS Telegram gateway. <br>
Risk: Sensitive Telegram configuration in environment variables may be exposed through shell history, logs, or process inspection. <br>
Mitigation: Store WM_CHAT_IDS and WM_TELEGRAM_API in a protected runtime environment and avoid printing or committing them. <br>
Risk: Overriding WM_SKILL_DIR changes where the Polymarket cache file is written. <br>
Mitigation: Leave WM_SKILL_DIR unset unless the cache location has been reviewed and is writable only by the intended user. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jcbuer/wm-tipp) <br>
- [Publisher profile](https://clawhub.ai/user/jcbuer) <br>
- [Polymarket markets API](https://gamma-api.polymarket.com/markets) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Markdown-formatted Telegram messages and console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus WM_TELEGRAM_API and WM_CHAT_IDS environment variables; writes a local Polymarket cache under the skill data directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata, SKILL.md, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
