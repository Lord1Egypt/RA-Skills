## Description:

Read-only PayPal transaction reconciliation for OpenClaw. Finds a transaction by approximate date, amount, and currency using a narrow search window, identifies the downstream merchant, and captures accounting evidence with minimal browser round-trips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calibhden](https://clawhub.ai/user/calibhden)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance or accounting operators use this skill to reconcile PayPal-backed credit-card charges, identify the downstream merchant, and collect receipt or transaction evidence for records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may expose PayPal activity, receipts, reports, or PDFs that contain sensitive financial records.

Mitigation: Use the skill only with approved access, store exported evidence in an approved location, and delete financial files when they are no longer needed.

Risk: A PayPal reconciliation session could reach screens that move money or change account state.

Mitigation: Keep the workflow read-only and stop before payments, refunds, disputes, account settings, payment methods, or security settings.

Risk: Login, CAPTCHA, OTP, or account verification prompts could expose credentials or authentication secrets.

Mitigation: Do not enter passwords, OTPs, CAPTCHA responses, security answers, or recovery codes; return PAYPAL_LOGIN_REQUIRED for manual authentication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/calibhden/skills/reconcile-paypal)
- [Publisher profile](https://clawhub.ai/user/calibhden)

## Skill Output:

**Output Type(s):** [text, files, guidance]

**Output Format:** [Structured text status report with optional PDF receipt, report, or transaction evidence file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Status values include MATCHED, AMBIGUOUS, NOT_FOUND, PAYPAL_LOGIN_REQUIRED, and BROWSER_TOOL_UNAVAILABLE; matched results include transaction fields, evidence location, confidence, and notes.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter, README, and CHANGELOG state 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
