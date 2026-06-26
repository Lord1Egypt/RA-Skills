## Description: <br>
Self Improving Compound is a portable agent memory and self-improvement system that uses a SQLite-backed learning engine, optional cron audits, daily memory digests, and promotion workflows to capture corrections, errors, and reusable lessons for future agent work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lingmafuture](https://clawhub.ai/user/lingmafuture) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give an agent a durable local learning loop for corrections, tool gotchas, recurring failures, daily factual memory, and promotion of proven lessons into workspace instructions or skills. It is best suited for non-trivial workflows where repeated mistakes or missing context would otherwise recur across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation and workspace data through local memory, learning stores, cron collectors, hooks, and digest files. <br>
Mitigation: Enable collectors, hooks, and cron jobs deliberately; confirm workspace root, timezone, delivery target, and helper paths before use, and avoid feeding the skill secrets or raw private transcripts. <br>
Risk: Automated promotion can write lessons into agent instruction or control-plane files. <br>
Mitigation: Review generated learning and promotion files before accepting changes, and avoid auto-promotion unless the deployment is comfortable with the agent modifying files such as AGENTS.md. <br>
Risk: Cron audits that lack a verified context collector can miss relevant context or report a false success. <br>
Mitigation: Use a deterministic recent-context collector when conversation-aware cron jobs are enabled, and require blocked reporting when the collector cannot access the target transcript. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lingmafuture/self-improving-compound) <br>
- [README](README.md) <br>
- [Entry formats](references/entry-formats.md) <br>
- [Daily Memory Digest Integration](references/daily-memory-digest.md) <br>
- [Heartbeat guidance](references/heartbeat-guidance.md) <br>
- [Platform setup](references/platform-setup.md) <br>
- [Promotion and extraction](references/promotion-and-extraction.md) <br>
- [Hermes Integration Notes](references/hermes-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, and local file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory, learning, queue, dashboard, and promotion artifacts when the user enables the bundled helpers.] <br>

## Skill Version(s): <br>
6.2.5 (source: server release evidence, artifact metadata, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
