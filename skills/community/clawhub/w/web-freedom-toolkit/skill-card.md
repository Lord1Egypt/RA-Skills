## Description:

Universal Server-Side Web Freedom Toolkit that harmonizes Scrapling self-healing fetches, curl_cffi TLS impersonation, and DrissionPage browser automation for restricted VPS environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biogod2020](https://clawhub.ai/user/biogod2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security researchers use this skill for authorized server-side web automation across stealth fetch, TLS impersonation, and controlled Chromium interaction modes. It is intended for environments where JavaScript-heavy pages or anti-bot controls require stronger automation than ordinary HTTP fetching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-risk browser evasion and takeover capabilities may be misused or affect unintended targets.

Mitigation: Use only for authorized anti-bot or browser automation research in a disposable, isolated container or VM with restricted outbound and internal network access.

Risk: The DevTools relay, no-sandbox browser mode, and takeover scripts can expose browser control and session-sensitive behavior.

Mitigation: Run with no sensitive environment variables and no logged-in browser profile; review these scripts as high-risk items before execution.

Risk: Sensitive capabilities are disclosed but overbroad and weakly controlled according to the authoritative security summary.

Mitigation: Require explicit human approval before execution and keep model invocation disabled for this release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/biogod2020/skills/web-freedom-toolkit)
- [Publisher profile](https://clawhub.ai/user/biogod2020)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact security explanation](artifact/SECURITY_EXPLAINED.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or text automation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Chrome, Xvfb, dbus, and Python packages for Scrapling, curl_cffi, DrissionPage, and lxml; model invocation is disabled in release metadata.]

## Skill Version(s):

8.0.0 (source: server release, artifact _meta.json, artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
