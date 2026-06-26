## Description: <br>
Self-reflection + Self-criticism + Self-learning + Self-organizing memory. Agent evaluates its own work, catches mistakes, and improves permanently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiyi-9](https://clawhub.ai/user/yiyi-9) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to add local self-reflection and memory routines that capture corrections, preferences, and reusable lessons across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps local cross-session memory, which can create privacy risk if secrets, sensitive personal data, or overly broad user context are stored. <br>
Mitigation: Avoid storing secrets or sensitive personal data, inspect ~/self-improving/ periodically, and honor the documented export and deletion controls. <br>
Risk: Stored preferences or lessons can become stale, too broad, or wrong for a new project context. <br>
Mitigation: Keep inferred rules tentative until validated, cite memory sources when applying them, and resolve conflicts by specificity and recency. <br>
Risk: Memory edits, exports, or full-wipe commands can remove or expose local memory unexpectedly. <br>
Mitigation: Review AGENTS.md, SOUL.md, HEARTBEAT.md, and ~/self-improving/ changes before applying them, and confirm destructive or export actions first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yiyi-9/self-improving-1-2-10) <br>
- [Skill homepage](https://clawic.com/skills/self-improving) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file templates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local files under ~/self-improving/ and emphasizes source-tracked memory actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter: 1.2.10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
