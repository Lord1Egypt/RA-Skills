## Description: <br>
Remember-this trigger: memory updates + recall for preferences, goals, boundaries, prior work, decisions, dates, and todos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AchalS-iglu](https://clawhub.ai/user/AchalS-iglu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to maintain structured local memory about preferences, goals, boundaries, prior work, decisions, dates, and todos so future responses can be personalized and prior context can be recalled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory files may retain private, stale, or inaccurate user context. <br>
Mitigation: Review MEMORY.md and dated memory notes periodically, correct or delete stale entries, and honor user requests to forget information immediately. <br>
Risk: Sensitive personal details could be saved if the user explicitly asks for them to be remembered. <br>
Mitigation: Avoid storing sensitive details unless the user clearly requests retention, and prefer concise behavioral context over raw conversation logs. <br>
Risk: Inferred hypotheses about the user may be mistaken. <br>
Mitigation: Tag inferred memories as hypotheses with confidence, validate them through lightweight check-ins, and discard or demote unvalidated assumptions. <br>


## Reference(s): <br>
- [Templates](references/templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/AchalS-iglu/remember-me) <br>
- [Publisher Profile](https://clawhub.ai/user/AchalS-iglu) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Files] <br>
**Output Format:** [Markdown memory entries and guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or updates local MEMORY.md and dated memory notes when the agent follows the skill workflow.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
