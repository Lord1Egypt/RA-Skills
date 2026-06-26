## Description: <br>
Helps agents guide Telegram Mini App development and debugging across safe areas, fullscreen mode, BackButton handlers, sharing, position:fixed issues, and React gotchas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zenith2828](https://clawhub.ai/user/Zenith2828) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to get practical guidance and reusable React examples for Telegram Mini Apps, especially around layout, sharing, BackButton behavior, fullscreen mode, and mobile testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sharing and backend examples may touch real bot or user data if copied directly into production. <br>
Mitigation: Review and adapt the sharing/backend examples before connecting production bot tokens, user identifiers, or live user data. <br>
Risk: Debug overlay options can expose runtime diagnostics if enabled in production. <br>
Mitigation: Keep DebugOverlay forceShow and ?debug=1 disabled in production unless those diagnostics are intentionally exposed. <br>


## Reference(s): <br>
- [Telegram Mini App Dev on ClawHub](https://clawhub.ai/Zenith2828/tg-miniapp) <br>
- [Telegram Mini App Knowledge Base](references/KNOWLEDGE.md) <br>
- [React Hooks Reference](references/hooks.ts) <br>
- [React Components Reference](references/components.tsx) <br>
- [Telegram Mini Apps Docs](https://core.telegram.org/bots/webapps) <br>
- [@telegram-apps/sdk](https://github.com/Telegram-Mini-Apps/telegram-apps) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with TypeScript, TSX, CSS, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advisory implementation patterns and copy-paste React examples; users should adapt and test them in their own Telegram Mini App environment.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
