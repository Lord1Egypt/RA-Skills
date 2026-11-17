## Description:

Searches WeChat public-account articles through WeRead search and returns article titles, publishers, dates, summaries, and direct WeChat article links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kanikig](https://clawhub.ai/user/kanikig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need recent WeChat public-account search results with publication metadata and direct article links, especially when ordinary web search or WeRead API paths do not provide the same coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can expose a browser-control CDP port that can control an authenticated browser session.

Mitigation: Use an isolated browser profile, keep CDP local or otherwise unreachable from the LAN, and remove any temporary portproxy or firewall rules after use.

Risk: A documented API key appears in the artifact and should not be trusted as private.

Mitigation: Treat the key as compromised; rotate or disable it where possible and avoid relying on embedded secrets from the release.

Risk: Login QR codes, cookies, and open tabs may expose unrelated accounts or session data during browser automation.

Mitigation: Use a dedicated WeRead/browser profile, avoid unrelated tabs or accounts, delete temporary QR/login artifacts, and verify cleanup after each run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kanikig/skills/wechat-search-weread)
- [Detailed workflow](artifact/references/detailed-workflow.md)
- [Extraction pattern](artifact/references/extraction-pattern.md)
- [CDP patterns](artifact/references/cdp-patterns.md)
- [WSL CDP browser](artifact/references/wsl-cdp-browser.md)
- [WeRead API limitations](artifact/references/api-limitations.md)
- [LLM filter pattern](artifact/references/llm-filter-pattern.md)
- [Topology optimization filter](artifact/references/topology-optimization-filter.md)
- [Edge CDP scroll issue](artifact/references/edge-cdp-scroll-issue.md)
- [agent-browser dependency](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, code, guidance]

**Output Format:** [Markdown search summary with article links, plus JSON result files and browser-automation command/code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result data is written to /tmp/urls.json; the default user-facing response shows a top-results list and summary counts.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
