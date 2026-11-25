# Source Model

Every evidence source is represented as a source context. Source contexts keep credentials, hosts, disclosure rules, and claim provenance separated.

## Source Context Fields

Use this structure in the evidence log:

- `id`: stable short identifier such as `github-public-rajain5` or `github-enterprise-webex`.
- `type`: `linkedin-profile`, `local-docs`, `confluence`, `jira`, `github-public`, `github-enterprise`, `job-posting`, `job-search-result`, `peer-market-research`, or `profile-picture`.
- `display_name`: user-facing source label.
- `host`: source host or workspace, such as `github.com`, a GitHub Enterprise hostname, Jira site, Confluence site, or local folder path.
- `identity`: username, email, display name, or user-provided identity used for attribution.
- `credential_boundary`: connector account, CLI profile, browser/session label, or other retrieval context label; never tokens, cookies, passwords, or raw credential material.
- `access_method`: connector, CLI, local file, pasted export, public web, or manual notes.
- `scope`: repositories, spaces, projects, folders, date ranges, keywords, issue keys, page titles, or PR numbers.
- `inventory_reference`: row, file path, query, URL, or connector result set listed in `source-inventory.md`.
- `tool_usage_reference`: row or command entry listed in `tool-usage-log.md`.
- `disclosure_level`: public, internal-summary-only, confidential, excluded, or unknown.
- `quoting_rule`: quote, summarize-only, anonymize, exclude, or ask-before-use.
- `status`: used, skipped, unavailable, narrowed, or needs-user-input.

Create a separate source context for each host + identity + credential boundary. Do not merge evidence across GitHub Cloud, GitHub Enterprise, or multiple accounts on the same host unless the user explicitly confirms they are the same professional identity and disclosure rules match.

When private and public sources are both used, create `disclosure-approval-queue.md` for any claim that crosses source boundaries or needs public wording approval. Keep source IDs visible in evidence and review artifacts so final outputs can be audited without exposing credentials or private URLs.

## GitHub Public

Use `github-public` for open-source or public GitHub Cloud evidence. Public evidence can support visible open-source sections, repository links, project bullets, and community impact.

Record:

- GitHub username.
- Repository full names.
- Authored PRs.
- Reviewed PRs.
- Issues opened or resolved.
- Commits when available.
- Release, maintainer, or ownership signals.
- Public visibility confirmation.

## GitHub Enterprise

Use `github-enterprise` for employer-owned or private GitHub hosts. Keep each enterprise host as a separate source context.

Record:

- Enterprise hostname.
- Organization.
- Enterprise username or email.
- Repository names only when the user permits them.
- Authored PRs, reviewed PRs, issues, commits, and date ranges in scope.
- Disclosure rule for repository names, product names, customer names, and metrics.

Default GitHub Enterprise evidence to `summarize-only` unless the user explicitly permits names or exact metrics.

## Local Documents

Use `local-docs` for user-approved folders, exported documents, architecture notes, project summaries, downloaded Confluence or Jira exports, PDFs, Word documents, Markdown, text files, logs, spreadsheets converted to text, or other local evidence.

Always inventory the full approved folder tree before extraction:

- Enumerate recursively with `rg --files <approved-folder>` when available.
- Use a `find` fallback if `rg` is unavailable or unsuitable.
- Do not stop at the first subfolder or only inspect files in the top-level directory.
- Keep each approved root as a separate source context when roots have different confidentiality or ownership rules.
- Record skipped files with a reason instead of omitting them.

For each local file, record:

- Relative path from the approved root.
- File extension and detected content type when obvious.
- Scan status: scanned, skipped-unsupported-format, skipped-too-large, skipped-binary, skipped-permission, duplicate, or needs-user-input.
- Extraction method: direct read, markdown/text read, JSON/YAML parse, HTML/XML text extraction, PDF text extraction, DOCX text extraction, converted export, or manual summary.
- Project names, dates, technologies, metrics, decisions, and user-action signals found.
- Whether raw file names can appear in final outputs.

Do not treat a missing parser as a reason to ignore the file. Record the file in `source-inventory.md`, mark the limitation, and ask for conversion or manual summary when the file looks important.

## Confluence

Use `confluence` for pages returned from user-approved CQL searches or specific page references.

Record:

- Site or workspace.
- CQL query or page identifiers.
- Page title handling rule.
- Space key.
- Date range.
- Disclosure level.

## Jira

Use `jira` for issues returned from user-approved JQL searches.

Record:

- Site or workspace.
- JQL query.
- Project keys.
- Fields retrieved.
- Issue key handling rule.
- Date range.
- Disclosure level.

## LinkedIn

Use `linkedin-profile` for exports, pasted text, user notes, or user-approved manually provided public profile text only. Do not automate LinkedIn scraping, whether logged-in or public, and do not bypass rate limits, access controls, robots restrictions, or platform controls.

Record:

- Source form: export, pasted text, user notes, or user-approved manually provided public profile text.
- Profile URL when user provides it.
- Date collected.
- Sections included.

## Job Posting and Market Research

Use `job-posting` for a specific job listing. Use `peer-market-research` for public role and market calibration.

Research may inform keyword coverage, role framing, and gap analysis. It must not create unsupported experience claims.

Use `job-search-result` rows in `source-inventory.md` for live job search results. Include source URL, company, role, location, remote status, posting date when available, search date, and whether the listing text was accessible. Dynamic job postings require current search or user-provided posting text; do not rely on stale memory.

## Profile Picture

Use `profile-picture` only for a user-provided local image path or attachment. Do not search for or scrape profile pictures.

Record:

- Local image path or attachment label.
- Whether the user requested use in the designed resume.
- Whether the image should be embedded, linked by local path, or omitted from shared artifacts.
- Any user-provided cropping or style preference.

## Inventory Helper Contract

The local inventory helper writes first-pass rows with these fields:

- Relative path.
- Extension.
- Status.
- Extraction method.
- Size in bytes.
- Modified time.
- Notes.

Statuses are first-pass coverage statuses. The agent may update `source-inventory.md` after extraction, parsing, duplicate detection, user summaries, or other evidence review changes the status or notes for a source.
