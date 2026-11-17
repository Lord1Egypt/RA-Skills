## Description:

Qwen Orchestrator provides Qwen Chat access through Puppeteer browser automation with a CDP interceptor, a persistent daemon, health checks, graceful shutdown, PM2 management, and `.qwen.json` configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ciklopentan](https://clawhub.ai/user/ciklopentan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to consult Qwen Chat from OpenClaw workflows for code analysis, review, generation, text analysis, summarization, translation, and optional web-search-backed answers without configuring a direct API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent Chromium/PM2 daemon can retain authenticated Qwen browser state.

Mitigation: Install only in an environment where that local login state is acceptable, and prefer a dedicated low-privilege account.

Risk: Prompts sent through the browser flow may include sensitive local content if users pipe files or secrets into the CLI.

Mitigation: Avoid sending secrets or sensitive files unless the destination service and account posture are approved for that data.

Risk: Qwen UI selector drift, authentication changes, or session hydration lag can break mode selection, search toggles, or follow-up continuity.

Mitigation: Use the documented dry-run, health-check, visible repair, and session reset commands before trusting follow-up output.

Risk: Local mode and daemon mode share a Chromium profile.

Mitigation: Use daemon mode for normal operation or stop the daemon before local browser runs to avoid profile lock and state conflicts.

## Reference(s):

- [Qwen Orchestrator on ClawHub](https://clawhub.ai/ciklopentan/skills/qwen-orchestrator)
- [Qwen Chat](https://chat.qwen.ai/)
- [README.md](README.md)
- [REFERENCE.md](REFERENCE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown emitted to stdout, often with code, shell command, or configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local sessions for follow-up context; diagnostics and runtime state remain local.]

## Skill Version(s):

1.5.8 (source: server release evidence, package.json, artifact metadata, SKILL.md heading)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
