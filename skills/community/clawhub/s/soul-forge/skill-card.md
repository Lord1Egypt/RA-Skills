## Description: <br>
SoulForge analyzes local session patterns and proposes reviewed updates to an OpenClaw SOUL.md file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Taha2053](https://clawhub.ai/user/Taha2053) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users use SoulForge to observe local conversation history, surface behavioral patterns, and decide whether proposed SOUL.md edits should be applied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a persistent local behavioral profile from session history. <br>
Mitigation: Install only if local cross-session profiling is acceptable, and periodically inspect or delete memory/observations.json and backups. <br>
Risk: Approved proposals can change long-term SOUL.md behavior. <br>
Mitigation: Review proposed diffs carefully, avoid --auto-accept unless the behavior is understood, and use backups to restore prior SOUL.md versions when needed. <br>
Risk: Automatic observation may collect patterns when manual-only use is preferred. <br>
Mitigation: Disable automatic observation with the documented soulforge observe setting and run reflection or forge steps only when explicitly needed. <br>


## Reference(s): <br>
- [SoulForge on ClawHub](https://clawhub.ai/Taha2053/soul-forge) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown and plain-text reports, proposed diffs, and local SOUL.md/backups files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with no declared external endpoints or credential requirements; may write approved SOUL.md changes and local memory/backups.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
