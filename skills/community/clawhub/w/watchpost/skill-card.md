## Description:

Watchpost checks a proposed purchase against merchant signals, listing evidence, and the user's spending rules before an agent pays, including authenticated review-status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lelis92](https://clawhub.ai/user/lelis92)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill before user-requested purchases or subscriptions to submit intended purchase details to Watchpost, explain approval, review, or block outcomes, and check server-side review status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Purchase details or listing evidence may include sensitive account, cookie, or payment data.

Mitigation: Keep WATCHPOST_TOKEN in secret settings and send only relevant listing evidence; omit cookies, payment credentials, hidden authentication fields, and unrelated account data.

Risk: A Watchpost approval could be mistaken for permission to spend money.

Mitigation: Treat approval as advisory and proceed only within the user's existing authorization for the unchanged purchase.

Risk: A failed request, timeout, or invalid response can leave the check unconfirmed.

Mitigation: Do not pay on setup, request, or response errors; inspect the Watchpost dashboard before retrying after a timeout.

## Reference(s):

- [Watchpost homepage](https://watchpost.systems/?ref=clawhub)
- [Watchpost ClawHub skill page](https://clawhub.ai/lelis92/skills/watchpost)
- [Watchpost connection settings](https://app.watchpost.systems/connections?ref=clawhub)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON helper output with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns purchase verdicts, review-status results, setup diagnostics, and local validation messages; it does not make payments or approve reviews.]

## Skill Version(s):

0.1.9 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
