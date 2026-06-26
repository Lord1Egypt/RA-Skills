## Description: <br>
Self-improving agent system that analyzes conversation quality, identifies improvement opportunities, and continuously optimizes response strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pp-chicken](https://clawhub.ai/user/pp-chicken) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agent maintainers use this skill to analyze conversation quality, record improvement notes, generate weekly summaries, and propose SOUL.md updates for manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local improvement notes may capture secrets, private user data, or sensitive conversation details if users log them. <br>
Mitigation: Do not log secrets or sensitive details, and periodically review or delete improvement_log.md. <br>
Risk: Suggested SOUL.md changes can affect future agent behavior if applied without review. <br>
Mitigation: Treat suggested SOUL.md changes as recommendations and manually review them before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pp-chicken/xiucheng-self-improving-agent-fixed) <br>
- [Project homepage](https://github.com/xiucheng/self-improving-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Python dictionaries, JSON, Markdown reports, and text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes improvement_log.md in the configured OpenClaw workspace; SOUL.md updates are suggestions for manual review.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
