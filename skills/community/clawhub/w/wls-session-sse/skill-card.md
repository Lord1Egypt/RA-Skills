## Description: <br>
WLS runtime engineer skill for session isolation, Session Server behavior, and cooperative SSE runtime implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiweline](https://clawhub.ai/user/aiweline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement and review WLS session isolation, Session Server flows, and cooperative SSE streaming behavior, including validation on dedicated non-production WLS instances. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Testing against production WLS instances or real login/session data could expose sensitive state or disrupt live users. <br>
Mitigation: Use a dedicated non-production WLS instance on a non-default port and avoid real production login or session data during validation. <br>
Risk: Generated session or SSE changes could introduce blocking loops, raw session access, or incomplete stream shutdown behavior. <br>
Mitigation: Review generated code for framework session abstractions, cooperative delay patterns, SseWriter usage, heartbeat behavior, and explicit stream completion or close handling. <br>
Risk: A validation WLS instance left running after testing could continue consuming resources or expose test endpoints. <br>
Mitigation: Confirm the dedicated validation instance is stopped after verification and include that confirmation in the final report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiweline/wls-session-sse) <br>
- [AI-ENTRY.md](AI-ENTRY.md) <br>
- [CLAUDE.md](CLAUDE.md) <br>
- [Session development skill](dev/ai/skills/session-development/SKILL.md) <br>
- [SSE streaming skill](dev/ai/skills/sse-streaming/SKILL.md) <br>
- [Weline framework runtime skill](dev/ai/skills/weline-framework-runtime/SKILL.md) <br>
- [Runtime and process skill](dev/ai/skills/runtime-and-process/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include WLS validation evidence and confirmation that the dedicated validation instance was stopped.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
