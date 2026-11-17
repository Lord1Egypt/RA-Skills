## Description:

Analyzes living-room audio/video from a fixed camera with microphone to estimate family or couple conflict intensity from sound level and body-movement signals and produce low/medium/high reports and reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users, smart-home integrators, and counseling support teams can use this skill to analyze consented household audio/video or URLs for acoustic and visual conflict-intensity indicators, generate structured reports, and retrieve prior reports for the same account context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive household audio/video or video URLs may be processed by the configured backend service.

Mitigation: Use only with explicit consent from affected household members, disclose upload, storage, and retention behavior, and avoid retaining raw media unless strictly necessary.

Risk: Development or private network configuration and debug settings may be unsuitable for a normal release.

Mitigation: Switch to production-scoped HTTPS endpoints, remove private development endpoints, and disable debug logging before deployment.

Risk: Local identity/token storage and account-linked history retrieval can expose sensitive report history.

Mitigation: Restrict history retrieval to the intended account context, protect local storage, and make report access behavior clear to users.

Risk: Conflict-intensity results can be false positives or be misused as legal, therapy, or safety determinations.

Mitigation: Present results as acoustic and visual indicators only, require human review for serious situations, and avoid labels such as perpetrator or victim.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-family-conflict-intensity-detect-analysis)
- [Publisher profile](https://clawhub.ai/user/smyx-sunjinhui)
- [Skill demo](https://lifeemergence.com/sample.html)
- [Family conflict intensity API reference](references/api_doc.md)
- [SMYX analysis API reference](skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown and JSON-style structured analysis reports with optional report links and history tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include conflict intensity level, acoustic metrics, visual metrics, gentle reminder text, recommended action, and report export URL.]

## Skill Version(s):

1.0.8 (source: ClawHub server release; artifact frontmatter declares 1.0.11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
