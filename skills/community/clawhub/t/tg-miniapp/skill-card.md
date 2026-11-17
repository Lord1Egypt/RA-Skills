## Description:

Helps developers build and debug Telegram Mini Apps with guidance and code for safe areas, fullscreen behavior, BackButton handlers, inline sharing, position:fixed issues, and React gotchas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenith2828](https://clawhub.ai/user/zenith2828)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build or debug Telegram Mini Apps, especially issues involving WebApp APIs, safe areas, fullscreen mode, native sharing, BackButton behavior, and React rendering patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment guidance includes unpinned npx Wrangler commands.

Mitigation: Pin Wrangler and deployment tools in project dependencies, commit a lockfile, and run staged deployments before production.

Risk: The debug overlay could expose platform and viewport diagnostics if intentionally enabled in production.

Mitigation: Keep the debug overlay limited to localhost or explicit debug mode, and avoid force-enabling it in production builds.

## Reference(s):

- [Telegram Mini App Knowledge Base](references/KNOWLEDGE.md)
- [Telegram Mini App React Hooks](references/hooks.ts)
- [Telegram Mini App React Components](references/components.tsx)
- [Telegram Mini Apps Docs](https://core.telegram.org/bots/webapps)
- [@telegram-apps/sdk](https://github.com/Telegram-Mini-Apps/telegram-apps)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with TypeScript, TSX, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes copy-paste React hooks and components; no runtime execution by the skill itself.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
