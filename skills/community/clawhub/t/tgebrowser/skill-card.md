## Description:

Operates TgeBrowser via MCP tools for managing environments, groups, proxies, browser automation, status checks, and full browser control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuguang2025](https://clawhub.ai/user/tuguang2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage TgeBrowser browser profiles and automate browser sessions through MCP tools, including lifecycle operations, proxy and fingerprint configuration, navigation, interaction, screenshots, and status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives agents broad control over browser profiles, cookies, screenshots, fingerprints, cache, and profile deletion.

Mitigation: Require explicit user confirmation and a specific profile selection before cookie access, screenshots, fingerprint changes, cache clearing, or deletion.

Risk: Existing profiles and cookies may expose sensitive session data during automation.

Mitigation: Prefer temporary or purpose-created browser profiles for automation and avoid reading, storing, or sharing cookies unless the user explicitly requests it.

Risk: Browser deletion and cache clearing are destructive actions.

Mitigation: Confirm the target envId or userIndex, verify whether the browser is open, and close the browser before clearing cache or deleting a profile.

Risk: WebSocket browser connection URLs and screenshots can reveal local browser state or sensitive page content.

Mitigation: Keep connection URLs session-scoped and local, and review screenshot or page-content capture requests for sensitive data before executing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tuguang2025/skills/tgebrowser)
- [Environment Management](references/environment-management.md)
- [Group Management](references/group.md)
- [System](references/system.md)
- [Proxy Management](references/proxy.md)
- [Proxy Config](references/proxy-config.md)
- [Fingerprint Config](references/fingerprint.md)
- [Browser Kernel Config](references/kernel-config.md)
- [Random UA Version Enum](references/ua-version.md)
- [Chrome TLS Cipher Suites](references/tls-cipher.md)
- [Country Code](references/country-code.md)
- [Tool Schema](schema.json)

## Skill Output:

**Output Type(s):** [guidance, configuration, tool calls]

**Output Format:** [Markdown guidance with JSON-style MCP tool arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser automation actions, screenshots, page content, cookie or User-Agent reads, profile updates, and deletion or cache-clearing commands when invoked by an agent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
