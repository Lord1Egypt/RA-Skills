## Description: <br>
Interprets East Asian Four Pillars / Saju charts from already-derived pillars using calm, evidence-first, rule-based analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[honeybearsoup](https://clawhub.ai/user/honeybearsoup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and practitioners use this skill to interpret already-derived Saju/Four Pillars charts, separating structural findings from conditional meaning and practical reading. When birth date/time conversion is requested, it can provide a first-pass local pillar calculation with explicit ambiguity notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Birth date/time conversion can vary for zi-hour handling, leap lunar month input, or school-specific month-boundary rules. <br>
Mitigation: Use a reliable manse calendar source for full derivation and explicitly review uncertain calendar assumptions before relying on calculated pillars. <br>
Risk: Saju interpretation can be overstated as deterministic claims about health, disaster, relationships, or life outcomes. <br>
Mitigation: Use conditional language, anchor readings in structural signals, and avoid deterministic or high-impact predictions. <br>
Risk: The optional calculator depends on korean_lunar_calendar for year, month, and day pillars. <br>
Mitigation: Verify the dependency and manually review calculator output for strict use. <br>


## Reference(s): <br>
- [Saju Interpreter Rules](references/rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/honeybearsoup/saju-interpreter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown responses with optional JSON from the local pillar calculator] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses conditional interpretation language; optional calendar calculation requires the korean_lunar_calendar dependency and manual review of ambiguous cases.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
