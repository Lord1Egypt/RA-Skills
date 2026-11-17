## Description:

Screenclaw helps agents operate Windows desktop software by using grid-labeled screenshots to locate visible UI targets, then issuing mouse, keyboard, screenshot, and recording/template commands through the ScreenClaw service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ginsing1226](https://clawhub.ai/user/ginsing1226)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use Screenclaw when Windows desktop applications, mobile emulators, games, or websites cannot be controlled through Playwright, CLI, or application APIs. It supports visible UI operation, screenshot-based verification, and reusable scenario templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Desktop-control and delegated modes can operate sensitive screens or destructive dialogs.

Mitigation: Use delegated or desktop automation only after explicit review, and avoid passwords, payments, security prompts, destructive dialogs, and confidential screens.

Risk: The executable install path and release source require trust review before use.

Mitigation: Install from a trusted ScreenClaw release source and prefer a pinned, verified binary.

Risk: Remote API use, screenshots, file upload behavior, and plaintext token handling can expose sensitive data or credentials.

Mitigation: Keep the API bound to localhost or HTTPS trusted origins, avoid remote servers unless necessary, and rotate away from the documented default token.

## Reference(s):

- [ScreenClaw GitHub releases](https://github.com/GinSing1226/ScreenClaw/releases)
- [ScreenClaw GitHub repository](https://github.com/GinSing1226/ScreenClaw)
- [Connection configuration](references/config.md)
- [Unified script usage](scripts/README.md)
- [Self-check procedure](references/self_check.md)
- [Scenario templates](references/scenarios/README.md)
- [Recording to scenario workflow](references/scenarios/recording_to_scenario.md)
- [Window screenshot API](references/api/screenshot.md)
- [Desktop screenshot API](references/api/desktop_screenshot.md)
- [Delegated mode API](references/api/delegated.md)
- [Batch API](references/api/batch.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, markdown]

**Output Format:** [Markdown guidance with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local screenshot paths, API response summaries, coordinate values, and reusable scenario template files when the ScreenClaw service is used.]

## Skill Version(s):

0.1.7 (source: ClawHub release evidence, created 2026-06-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
