## Description: <br>
World Cup 2026 is a Chinese-language match-watching assistant that ranks fixtures, filters low-value games, surfaces rivalry and long-odds matches, and returns concise Markdown tables in chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External football fans use this skill to choose which 2026 World Cup matches to watch, inspect a team's schedule, find high-intensity or high-odds fixtures, and get lightweight score predictions from bundled local data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Predictions, odds, rankings, and match data may be unofficial or stale. <br>
Mitigation: Verify sports data against current authoritative sources before relying on schedules, odds, rankings, or predictions. <br>
Risk: The skill can update bundled schedule, odds, or ranking JSON files when the user explicitly requests updates. <br>
Mitigation: Review proposed JSON changes before accepting them and keep version history or backups for local data files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/world-cup-2026) <br>
- [Skill README](artifact/README.md) <br>
- [Score Prediction Model](artifact/assets/prediction.md) <br>
- [Intensity Scoring Method](artifact/assets/scoring.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown tables and short prose in chat] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to BJT match times, returns filtered match lists rather than full schedules, and does not generate HTML.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
