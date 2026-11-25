# Privacy and Sanitization

## Defaults

- Public GitHub evidence may be named when the repository is public and the user approves.
- GitHub Enterprise evidence is summarized and anonymized by default.
- Jira and Confluence evidence is summarized and anonymized by default.
- LinkedIn content is used only from exports, pasted text, user notes, or user-approved manually provided public profile text.
- Do not automate LinkedIn scraping, whether logged-in or public, and do not bypass rate limits, access controls, robots restrictions, or platform controls.
- Credentials, tokens, cookies, private URLs, and secrets are never copied into outputs.
- Profile pictures are used only when user-provided and are never uploaded to external design services automatically.

## Sanitization Rules

Before final resume, cover letter, or LinkedIn wording:

- Replace internal repository names with generic system descriptions unless approved.
- Replace customer names with industry or segment descriptions unless approved.
- Replace Jira IDs with generic references unless approved.
- Replace Confluence page titles with project themes unless approved.
- Replace private URLs with source-context references in the evidence log only.
- Round or generalize sensitive metrics when the user asks for confidentiality.
- Use local image paths or user-approved embedded image references for designed resumes; omit images from shared artifacts when the user has not approved image sharing.

## Claim Confidence

Use high confidence when direct source evidence supports the claim and the user's role is clear.

Use medium confidence when the source supports the project but the user's exact role, metric, or scope needs interpretation.

Use low confidence when the claim comes from weak evidence, inferred role ownership, stale documents, or conflicting sources.

Low-confidence claims cannot be used in final outputs without user confirmation.

## User Review Gate

Pause for user review before final wording when outputs include:

- Internal project names.
- Exact confidential metrics.
- Customer or partner names.
- Private repository names.
- Jira issue keys.
- Confluence page titles.
- Security-sensitive architecture details.
- Profile pictures or image metadata in shared artifacts.
- Any low-confidence claim.

## Disclosure Approval Queue

Create `disclosure-approval-queue.md` before final user-facing wording when private or enterprise evidence could appear in outputs. Queue each internal name, customer name, repository name, Jira key, Confluence title, exact private metric, sensitive architecture detail, profile picture, or low-confidence claim.

Each item needs a proposed treatment:

- Use as-is only when explicitly approved.
- Sanitize with a generic but specific description.
- Generalize a metric, customer, or system name.
- Ask before use.
- Exclude from final outputs.

## Final Redaction Review

Create `final-redaction-review.md` before delivering final outputs when private sources were used. Confirm that credentials, secrets, private URLs, unapproved names, unapproved exact metrics, low-confidence claims, and unapproved profile images are not present in the final resume, cover letter, LinkedIn text, or visual artifacts.
