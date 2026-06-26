## Description: <br>
Self-reflection + Self-criticism + Self-learning + Self-organizing memory. Agent evaluates its own work, catches mistakes, and improves permanently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aysun168](https://clawhub.ai/user/aysun168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to help an agent learn from explicit corrections, self-reflection, failed operations, and repeated workflow lessons while keeping memory organized in local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can retain corrections, preferences, workflow patterns, or other personal context longer than intended. <br>
Mitigation: Install only when cross-session memory is desired, avoid sensitive personal, credential, financial, health, location, or third-party details, and periodically inspect or delete ~/self-improving/. <br>
Risk: Workspace steering changes can alter future agent behavior through AGENTS.md, SOUL.md, and HEARTBEAT.md. <br>
Mitigation: Review the exact proposed changes before setup and keep edits narrow, visible, and reversible. <br>
Risk: The optional Proactivity companion may require a separate install and network access. <br>
Mitigation: Skip the companion unless the user explicitly agrees, then review the installed companion skill before continuing setup. <br>
Risk: Server evidence says GitHub import provenance is unavailable for this version. <br>
Mitigation: Treat provenance as unavailable and verify the publisher profile, skill page, and artifact contents before relying on the release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aysun168/self-improving-bak) <br>
- [Skill homepage](https://clawic.com/skills/self-improving) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Security boundaries](artifact/boundaries.md) <br>
- [Setup guide](artifact/setup.md) <br>
- [Memory operations](artifact/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory files under ~/self-improving/ and optional workspace steering files when the user installs and configures the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.2.16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
