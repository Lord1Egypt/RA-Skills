## Description: <br>
Qwen Orchestrator provides Qwen Chat access through Puppeteer browser automation, with daemon mode, session continuity, health checks, graceful shutdown, PM2 management, and optional web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ciklopentan](https://clawhub.ai/user/ciklopentan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query Qwen Chat for code analysis, review, generation, text analysis, summarization, translation, and Qwen-backed web search when they have an authenticated Qwen Chat browser session but no API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, pasted text, stdin, and session context are sent to Qwen Chat through an authenticated browser session. <br>
Mitigation: Use a dedicated Qwen account and avoid sending secrets, regulated data, proprietary content, or other sensitive material. <br>
Risk: The skill uses a persistent logged-in browser service and stores browser-control state locally. <br>
Mitigation: Keep the skill directory private, protect local runtime state, and disable or review PM2 startup and daemon endpoint files when a persistent service is not desired. <br>
Risk: Qwen UI selector changes can affect model selection, search toggles, authentication checks, or session continuity. <br>
Mitigation: Run dry-run health checks, inspect visible mode when selector warnings appear, and end or recreate affected sessions after continuity failures. <br>


## Reference(s): <br>
- [Qwen Chat](https://chat.qwen.ai/) <br>
- [Qwen Orchestrator on ClawHub](https://clawhub.ai/ciklopentan/qwen-orchestrator) <br>
- [Publisher profile](https://clawhub.ai/user/ciklopentan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown returned from Qwen Chat, with shell commands and configuration snippets when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports stdin prompts, named sessions, daemon-backed responses, optional web search, and configurable preferred model selection.] <br>

## Skill Version(s): <br>
1.5.8 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
