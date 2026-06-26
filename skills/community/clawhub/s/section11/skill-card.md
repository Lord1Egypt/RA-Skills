## Description: <br>
Section 11 is an evidence-based endurance coaching protocol for analyzing athlete JSON data, reviewing workouts, generating reports, planning training, and answering endurance coaching questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crankaddict](https://clawhub.ai/user/crankaddict) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Athletes, coaches, and agent operators use this skill to turn configured training data into readiness checks, workout reviews, weekly or block reports, and training-plan guidance. On capable agent platforms, it can also prepare calendar, threshold, and annotation changes that should be previewed before confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads sensitive training data and may use Intervals.icu credentials when write features are configured. <br>
Mitigation: Prefer local files or a private repository, use least-privilege tokens, and install only when the publisher and data locations are trusted. <br>
Risk: The skill can fetch mutable protocol and template files when local copies are unavailable. <br>
Mitigation: Pin or vendor protocol files where possible and review fetched protocol changes before relying on coaching output. <br>
Risk: Calendar, threshold, and annotation writes could alter training records if confirmed without review. <br>
Mitigation: Keep preview mode enabled by default and require explicit confirmation before calendar, threshold, or annotation writes. <br>
Risk: Heartbeat automation can run scheduled analysis and write summaries or plans once configured. <br>
Mitigation: Keep heartbeat automation opt-in, limit its credentials, and review the configured schedule, data sources, and notification targets. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/crankaddict/section11) <br>
- [Section 11 Repository](https://github.com/CrankAddict/section-11) <br>
- [Data Mirror Setup](https://github.com/CrankAddict/section-11#2-set-up-your-data-mirror-optional-but-recommended) <br>
- [Section 11 Protocol](https://raw.githubusercontent.com/CrankAddict/section-11/main/SECTION_11.md) <br>
- [Heartbeat Template](artifact/HEARTBEAT_TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and plain-text coaching guidance with optional shell command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses athlete-provided JSON data and dossier files; write actions are optional and should remain previewed until explicitly confirmed.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
