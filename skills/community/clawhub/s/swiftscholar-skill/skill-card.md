## Description:

Integrates the SwiftScholar HTTP API so agents can search literature, submit PDFs or URLs for parsing, retrieve paper analyses, manage favorites, and inspect account usage programmatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tokisakix](https://clawhub.ai/user/tokisakix)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and external users use this skill to guide agents through SwiftScholar literature workflows, including paper search, paper submission, analysis retrieval, favorites management, and account usage checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide uploads of private PDFs, URLs, or notes to the SwiftScholar service.

Mitigation: Confirm with the user before sending private papers, URLs, notes, or other sensitive research material to the service.

Risk: Some guided actions can change the user's SwiftScholar library or consume account quota or points.

Mitigation: Confirm before saving favorites, submitting papers for parsing, or running actions that may consume quota or points.

## Reference(s):

- [SwiftScholar](https://www.swiftscholar.net)
- [ClawHub skill page](https://clawhub.ai/tokisakix/skills/swiftscholar-skill)

## Skill Output:

**Output Type(s):** [guidance, API calls, markdown, configuration]

**Output Format:** [Markdown guidance with HTTP endpoint names, JSON request shapes, and concise user-facing summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a SwiftScholar API key in the execution environment; does not store secrets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
