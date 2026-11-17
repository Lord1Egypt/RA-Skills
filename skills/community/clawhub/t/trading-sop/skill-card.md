## Description:

Trading SOP routes A-share trading requests into daily market review, individual-stock research, first-board overnight decision, and optional simulated-trade workflows, then summarizes actionable decision support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fize](https://clawhub.ai/user/fize)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to coordinate A-share trading preparation, intraday and post-market reviews, individual-stock research, and first-board overnight decisions. The skill emphasizes data-completeness gates, downstream skill orchestration, risk review, and concise SOP-style reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional local dashboard may expose report contents through browser-facing APIs and unsafe Markdown rendering.

Mitigation: Use the dashboard only with trusted report files, keep it bound to localhost, stop it after use, avoid placing sensitive reports in the served directory, and request removal of wildcard CORS plus sanitization or disabling of raw HTML rendering.

Risk: Trading guidance can become misleading when required market data or downstream skill outputs are missing or unverified.

Mitigation: Preserve the skill's data-completeness gates: stop the SOP chain when core data cannot be verified, report the blocking reason, and treat generated recommendations as decision support requiring user review.

## Reference(s):

- [Trading SOP ClawHub listing](https://clawhub.ai/fize/skills/trading-sop)
- [SOP-A daily market workflow](references/sop-a-daily.md)
- [SOP-B individual stock research workflow](references/sop-b-stock.md)
- [SOP-C first-board overnight workflow](references/sop-c-firstboard.md)
- [SOP summary report template](templates/sop_summary.md)
- [Evaluation scenarios](evals/evals.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and reports, with optional shell commands for subordinate workflow execution and the local dashboard.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill writes SOP report files under a workspace report/ directory when executed and can optionally serve a local dashboard for browsing reports and charts.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
