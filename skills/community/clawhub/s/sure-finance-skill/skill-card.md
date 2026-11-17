## Description:

Sure Finance API skill for personal finance insights, account and transaction operations, tags and categories management, imports, and chat workflows in Sure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[secondport](https://clawhub.ai/user/secondport)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance users use this skill to inspect Sure accounts and transactions, build finance summaries, manage tags/categories/imports, and safely create or update Sure records through authenticated API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and sensitive finance data may be sent to an untrusted or non-HTTPS Sure server.

Mitigation: Install only when the Sure server is trusted, use an https:// SURE_BASE_URL except for explicit localhost development, and never print API keys or tokens.

Risk: Imports and transaction operations can change financial records.

Mitigation: Require explicit user confirmation before imports or transaction changes, then re-fetch changed records to verify the result.

Risk: Optional self-hosting setup downloads Docker files from mutable remote URLs.

Mitigation: Treat self-hosting as privileged setup and review, pin, and verify downloaded files before running docker compose.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/secondport/skills/sure-finance-skill)
- [Sure API Playbooks](artifact/docs/api-playbooks.md)
- [OpenClaw Compatibility Guide](artifact/docs/openclaw-compatibility.md)
- [Self-Hosting Quickstart](artifact/docs/self-hosting-quickstart.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and concise structured summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Sure API responses as input; redacts secrets and should require confirmation before imports or transaction changes.]

## Skill Version(s):

0.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
