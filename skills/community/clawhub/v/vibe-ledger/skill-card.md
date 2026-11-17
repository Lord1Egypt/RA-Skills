## Description:

Explain an AI-built app and check it against the user's requests with an offline report that maps the code, tracks requirements from conversations, and records evidence-backed findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dong845](https://clawhub.ai/user/dong845)

### License/Terms of Use:

MIT

## Use Case:

Developers and app builders use Vibe Ledger to understand how an AI-generated project is organized and check what was built against their requests. It creates a local report from supported Claude Code or Codex conversation logs and project code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation excerpts or secrets in reports and run files could expose private information.

Mitigation: Process only projects and logs you are authorized to review, inspect generated files, and remove sensitive content before sharing a report.

Risk: The optional retention setting changes Claude Code settings.

Mitigation: Review the proposed retention change and opt in only when you want to keep conversations longer.

## Reference(s):

- [Source repository](https://github.com/dong845/vibe-ledger)
- [ClawHub skill release](https://clawhub.ai/dong845/skills/vibe-ledger)
- [Publisher profile](https://clawhub.ai/user/dong845)

## Skill Output:

**Output Type(s):** [HTML report, Analysis, Guidance]

**Output Format:** [Single offline HTML report with an interactive project flowchart, requirements review, and overview]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated locally; may include selected conversation quotes and code excerpts]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
