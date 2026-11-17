## Description:

Collects Xiaohongshu posts and comments for a research topic, synthesizes a daily roundup, and optionally publishes it back to Xiaohongshu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhrli324](https://clawhub.ai/user/zhrli324)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run a configurable daily Xiaohongshu research digest workflow for selected AI research topics, inspect generated drafts, and publish them from a logged-in Xiaohongshu account when approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can automate public Xiaohongshu posts from a logged-in account without a per-post approval gate.

Mitigation: Run dry runs first, inspect post_draft.json before publishing, and avoid unattended --publish cron jobs until approval or account controls are added.

Risk: Failure logs may expose per-feed tokens from Xiaohongshu collection calls.

Mitigation: Limit access to logs, avoid sharing raw failure output, and rotate or stabilize the logged-in session if sensitive feed tokens appear.

Risk: Collected Xiaohongshu content is untrusted input that may be noisy or misleading.

Mitigation: Review generated digests and drafts before use, keep request volume conservative, and tune topic keywords and retrieval limits to reduce low-signal content.

## Reference(s):

- [XHS Research Daily Operations](references/operations.md)
- [ClawHub skill page](https://clawhub.ai/zhrli324/skills/xhs-research-daily)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown digests, JSON digest and post draft files, and command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally publish generated post content through a logged-in Xiaohongshu account.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
