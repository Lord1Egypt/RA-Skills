## Description:

Provides read-only reports on a Vercel site's errors, traffic, and speed, including runtime error logs, failing requests, page views, visitors, top pages, referrers, and Core Web Vitals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anatoli-iliev](https://clawhub.ai/user/anatoli-iliev)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and site operators use this skill to inspect Vercel project health through recent errors and logs, traffic analytics, top pages and referrers, and Speed Insights/Core Web Vitals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured Vercel token can expose the Vercel data visible to that token.

Mitigation: Use the least privileged read scope that supports the needed project, and prefer an environment variable or secret-reference configuration over storing the token in OpenClaw config.

Risk: Request-log output may contain application secrets, personal data, or operational context.

Mitigation: Quote only the minimum log output needed to answer the user's question and avoid forwarding logs to unrelated services.

Risk: Optional external setup commands can run changing third-party code while a token is present.

Mitigation: Pin or avoid commands such as npx vercel@latest when working in an environment that has a Vercel token configured.

## Reference(s):

- [Openclaw Vercel Insights repository](https://github.com/anatoli-iliev/openclaw-vercel-insights)
- [API notes](artifact/docs/api-notes.md)
- [CLI contract](artifact/docs/cli-contract.md)
- [OpenClaw setup guide](artifact/docs/openclaw-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with shell commands and tabular CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Vercel reporting; JSON and CSV output are available for supported CLI queries.]

## Skill Version(s):

1.1.1 (source: frontmatter, pyproject.toml, CHANGELOG released 2026-08-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
