# Enterprise Redaction and Audit

Use this reference when evidence comes from GitHub Enterprise, Confluence, Jira, private repositories, private documents, internal architecture docs, incidents, customer work, or confidential metrics.

## Source Identity Separation

Keep these separate unless the user explicitly confirms they can be merged:

- GitHub Cloud identity.
- GitHub Enterprise identity.
- Jira identity.
- Confluence identity.
- LinkedIn identity.
- Local document author identity.

Each source context must record host, identity, credential boundary, approved scope, disclosure level, and quoting rule. Do not blend public open-source claims with private enterprise claims when the disclosure rules differ.

## Approval Queue

Create `disclosure-approval-queue.md` when final outputs might contain:

- Internal project names.
- Customer, partner, or vendor names.
- Private repository names.
- Jira issue keys.
- Confluence page titles.
- Private URLs or hostnames.
- Exact private metrics.
- Sensitive architecture, incident, security, or compliance details.
- Profile pictures or image metadata.
- Low-confidence claims.

Every queued item needs a proposed treatment: use as-is, sanitize, generalize, ask before use, or exclude.

## Redaction Review

Create `final-redaction-review.md` before delivering final resume, cover letter, LinkedIn recommendations, or visual artifacts when private sources were used.

The review should confirm:

- No credentials, tokens, cookies, private URLs, or secrets appear in outputs.
- Internal names are sanitized unless approved.
- Customer names and exact private metrics are sanitized unless approved.
- Private repository names and issue IDs are removed unless approved.
- Low-confidence claims are excluded or marked for user confirmation.
- Visual artifacts do not embed unapproved profile images.
- Evidence and tool logs keep enough provenance for audit without leaking secrets.

## Sanitization Patterns

Use specific but safe phrasing:

- Replace a private platform name with "internal developer platform" or a user-approved generic label.
- Replace a customer name with "enterprise customer", "regulated customer", or the industry segment.
- Replace an exact metric with a rounded or relative metric when exact numbers are sensitive.
- Replace private repository names with technology or system descriptions.
- Replace Jira and Confluence identifiers with evidence references in the private evidence log only.

Do not make sanitized wording so vague that the user's ownership or impact disappears. Ask the user for a public-safe phrasing when the balance is unclear.
