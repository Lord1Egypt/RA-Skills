## Description:

Helps app owners draft specific replies to unanswered App Store and Google Play reviews, with guardrail checks and configurable posting workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafalzawadzki](https://clawhub.ai/user/rafalzawadzki)

### License/Terms of Use:

MIT-0

## Use Case:

App owners and their teams use this skill to review unanswered store feedback, draft tailored replies, and submit approved responses through connected App Store Connect or Play Console accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A scheduled run may publish replies without per-reply approval when an auto-apply rule allows it.

Mitigation: Start with interactive drafts; before scheduling, require human approval or remove automatic apply_action calls, and review auto-apply rules.

Risk: API keys and downloaded playbooks need protection from exposure or unreviewed changes.

Mitigation: Protect API keys and pin playbooks to a reviewed revision.

## Reference(s):

- [REST API fallback](reference/api.md)
- [AppGoat REST API](https://api.appgoat.ai/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls]

**Output Format:** [Short review reply drafts and Markdown tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to 30 replies per run; Play replies are limited to 350 characters and App Store replies follow a 600-character house rule.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
