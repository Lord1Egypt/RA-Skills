## Description: <br>
Captures agent learnings, errors, corrections, and feature requests in local markdown files so future sessions can improve recurring workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuliyuan2026](https://clawhub.ai/user/wuliyuan2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture corrections, command failures, knowledge gaps, feature requests, and recurring best practices as local learning records. The captured records can later be promoted into agent guidance, project memory, or reusable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs can capture secrets, private command output, raw transcripts, or proprietary information if users record too much detail. <br>
Mitigation: Keep secrets, tokens, environment variables, raw transcripts, private command output, and proprietary data out of .learnings and workspace memory files; use sanitized summaries instead. <br>
Risk: Optional hook scripts add reminders by inspecting prompt or command contexts, and broad user-global hook configuration can affect unrelated projects. <br>
Mitigation: Review the shell scripts before enabling hooks, prefer project-scoped configuration in trusted workspaces, and enable command-output inspection only when that behavior is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wuliyuan2026/self-improvement-local) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and local file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agents may create or append local .learnings/*.md files when following the workflow; optional hooks emit short reminder text.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
