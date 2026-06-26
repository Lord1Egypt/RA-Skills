## Description: <br>
Lifecycle guard. Route to preflight or runtime. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yxf203](https://clawhub.ai/user/yxf203) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route safety work between preflight skill review and runtime action checks. It helps review skill artifacts, triage tool use, and produce advisory guard responses before higher-risk actions proceed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guard may slow workflows with additional warnings, replanning, or confirmation prompts. <br>
Mitigation: Use it where stricter skill review and runtime safety checks are desired, and expect confirmation steps for sensitive files, tool use, code execution, external calls, deletion, and memory writes. <br>
Risk: The guard is advisory and does not by itself provide sandboxing, rollback, or technical enforcement. <br>
Mitigation: Pair the guidance with normal environment controls, review diffs or dry runs before state changes, and keep explicit user authorization for high-risk actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yxf203/skill-sonar) <br>
- [Skill route](artifact/SKILL.md) <br>
- [Preflight guard](artifact/preflight/preflight-guard.md) <br>
- [Runtime guard](artifact/runtime/runtime-guard.md) <br>
- [Triage checklist](artifact/runtime/checklists/triage-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown safety guidance and guard decision summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory output; security evidence shows no automatic execution, credential use, installation scripts, or external data transfer.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter: 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
