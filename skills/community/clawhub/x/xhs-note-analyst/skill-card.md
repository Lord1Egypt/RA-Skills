## Description:

Analyzes your Xiaohongshu creator analytics, compares recent posts with popular posts on similar topics, and produces an HTML report with funnel diagnostics and improvement actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fatmind](https://clawhub.ai/user/fatmind)

### License/Terms of Use:

MIT-0

## Use Case:

Xiaohongshu creators use their own logged-in creator account to diagnose recent posts' reach, clicks, retention, engagement, and follower growth, then compare posts with public search results and plan improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access to a logged-in Xiaohongshu creator session and downloaded creator analytics exposes sensitive account data.

Mitigation: Install only if comfortable granting session and Downloads access; review the generated report and locally stored analytics before sharing.

Risk: The bundled obfuscated LLM helper makes its behavior difficult to review.

Mitigation: Prefer a readable helper and pinned installation versions; review the skill before running it with sensitive data.

## Reference(s):

- [XHS Account Analyzer release](https://clawhub.ai/fatmind/skills/xhs-note-analyst)
- [Required webclaw3 browser runtime](https://clawhub.ai/fatmind/skills/webclaw3-browser-automation)

## Skill Output:

**Output Type(s):** [HTML report, Markdown summary, Guidance]

**Output Format:** [Local HTML report with structured JSON results and Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes per-post metrics, funnel diagnostics, comparable posts, and suggested actions; comparisons may be marked partial when qualifying results are insufficient.]

## Skill Version(s):

1.1.6 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
