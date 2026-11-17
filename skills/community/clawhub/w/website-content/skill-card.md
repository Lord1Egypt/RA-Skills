## Description:

Helps agents publish or edit live website articles, products, and customer cases through a website content API, with user confirmation required before writes because changes become public immediately and cannot be deleted through the API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xtoyun](https://clawhub.ai/user/xtoyun)

### License/Terms of Use:

MIT-0

## Use Case:

External site operators and their agents use this skill to create or update public website content for articles, products, and customer cases. It is intended for controlled publishing workflows where the user confirms the target site, language, and content before any write operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write operations immediately affect public website content and there is no API delete endpoint.

Mitigation: Confirm the exact target site, content type, language, and final content with the user before writing; use draft or hidden fields for unfinished articles and products when available.

Risk: A read-write website API token can modify live customer content if exposed or misused.

Mitigation: Treat WEBSITE_API_TOKEN as sensitive, avoid printing it to logs or conversations, and rotate it from the customer backend if exposure is suspected.

Risk: Case records do not have a draft or hidden switch, so incorrect case content can remain visible until edited or handled in the backend.

Mitigation: Use extra confirmation for case publishing and verify the created record after submission.

Risk: Language codes that do not match enabled site languages may silently fall back to the default language.

Mitigation: Ask the user which enabled language codes to use and review per-language API results instead of relying only on HTTP status.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xtoyun/skills/website-content)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a read-write website API token and explicit user confirmation before write operations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
