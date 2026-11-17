## Description:

Generates a daily status and usage report across services such as GitHub, Vercel, Docker Hub, OpenRouter, OpenAI, Anthropic, Tailscale, and ClawHub using credentials supplied at runtime or from keys.env, and skips sources when required values are missing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikikari](https://clawhub.ai/user/kikikari)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to collect a daily, source-by-source status and usage snapshot for connected services. It is intended for on-demand or scheduled reporting where missing credentials should result in explicit no-data sections rather than invented values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on provider credentials that may be kept in plaintext in keys.env or browser localStorage.

Mitigation: Use narrowly scoped, read-only, short-lived tokens where possible; keep keys.env out of version control; avoid admin keys unless required; do not host the dashboard on shared or untrusted origins; rotate or revoke tokens after use.

Risk: The release evidence flags the package as suspicious because it handles high-value API or admin credentials and references a browser dashboard that is absent from the artifact files.

Mitigation: Review the package before use, confirm any dashboard file separately before relying on browser behavior, and prefer server or CI execution for providers that should not expose credentials in a browser.

Risk: Some provider APIs can fail or be unavailable from browser execution because of CORS or authentication restrictions.

Mitigation: Use the documented server or scheduled-task path for authenticated REST calls, and report actual HTTP failures or no-data states rather than synthesizing status values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kikikari/skills/tagesstatus-live-public)
- [Skill instructions](artifact/SKILL.md)
- [Package README](artifact/README.md)
- [Credential template](artifact/keys.env.template)
- [ClawHub skill API endpoint pattern](https://clawhub.ai/api/v1/skills/{slug})

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with TL;DR, per-source sections, error log, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not display credentials; sources with missing required tokens or identifiers are skipped and reported as no data.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
