## Description: <br>
Tracks ClawHub skill search ranking across keywords, with single and batch checks, competitor comparison, top-results views, and JSON export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tjefferson](https://clawhub.ai/user/tjefferson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ClawHub skill publishers use this skill to check where a skill appears for search keywords, compare nearby competitors, and export ranking snapshots for ongoing search performance monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords and skill slugs are sent to ClawHub when rank checks are run. <br>
Mitigation: Avoid secrets, private project details, and personal data in queries; review keywords before execution. <br>
Risk: Rankings are real-time snapshots and may change as ClawHub search results change. <br>
Mitigation: Treat results as point-in-time signals and use JSON exports for repeated comparisons over time. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tjefferson/skills-rank) <br>
- [ClawHub Search API Reference](references/api-docs.md) <br>
- [ClawHub Search API endpoint](https://clawhub.ai/api/search?q={keyword}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text summaries, markdown tables, and optional structured JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include rank positions, total result counts, nearby competitors, top results, scores, timestamps, and per-keyword error messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and CHANGELOG.md, released 2026-03-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
