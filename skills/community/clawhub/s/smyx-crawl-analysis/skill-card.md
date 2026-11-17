## Description:

Analyzes videos of reptiles and arachnids for visible health concerns and returns a structured Pet Safety Guardian health report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners can submit a reptile or arachnid video for a visual health assessment, care suggestions, and a structured report, or retrieve previous reports. The results are for reference and do not replace advice from a qualified veterinarian.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports potential privacy exposure and security weaknesses alongside account handling and monitoring beyond video analysis.

Mitigation: Avoid installation unless the added history, account, and camera functions are needed and acceptable; review data handling before use.

Risk: ClawScan reports possible analysis even when an export-only choice is selected.

Mitigation: Do not rely on export-only mode to prevent analysis; confirm its behavior and avoid submitting sensitive video until resolved.

Risk: The security review is incomplete because a local path-like reference could not be resolved.

Mitigation: Treat the review as incomplete until the unresolved reference is assessed.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill introduction and demo](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-crawl-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured health report with visual observations, potential health concerns, care suggestions, and report links; available as JSON or text/Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One analysis report per submitted video; results are informational and do not replace veterinary diagnosis.]

## Skill Version(s):

1.0.19 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
