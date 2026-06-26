## Description: <br>
Security-hardened self-improvement skill for OpenClaw that captures learnings, errors, and corrections with human approval gates, sanitization, audit tooling, and promotion rate limiting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gateswell](https://clawhub.ai/user/gateswell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve corrections, failures, feature requests, and recurring workflow lessons across OpenClaw sessions while keeping promotions human-reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs can retain sensitive, stale, or misleading workspace context. <br>
Mitigation: Use the skill only in non-sensitive workspaces, avoid logging secrets, run the sanitization and audit scripts, and periodically inspect .learnings files. <br>
Risk: The security evidence flags an undocumented promotion-gate bypass. <br>
Mitigation: Review promotion-gate.sh before installation and do not use the bypass path unless a human explicitly accepts the exact change and reason. <br>
Risk: Promoted learnings can change future agent behavior or core agent guidance. <br>
Mitigation: Require explicit human approval after showing the proposed rule, target file, original learning entry, recurrence count, and context. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gateswell/safe-self-improvement) <br>
- [Publisher profile](https://clawhub.ai/user/gateswell) <br>
- [Project homepage declared by artifact metadata](https://github.com/gateswell/safe-self-improvement-agent) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [Original Self-Improving Agent background reference](https://github.com/peterskoett/self-improving-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown entries, approval prompts, shell command invocations, and local configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local .learnings markdown files and promotion state; no external network calls are described by the artifact.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
