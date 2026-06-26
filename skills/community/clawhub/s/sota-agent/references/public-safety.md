# Public Safety

Use this reference before sharing or publishing SOTA-agent artifacts.

## What must not ship

- secrets, tokens, API keys, cookies, passwords
- private datasets, hidden benchmark ids, or customer names
- internal experiment URLs
- raw notebook links
- local debug endpoints or private session aliases
- absolute local filesystem paths
- private model registry locations
- unpublished paper PDFs or copyrighted attachments you do not have the right to redistribute

## Public-safe defaults

- keep artifact references sanitized by default
- prefer benchmark ids over local paths
- prefer paper titles and public URLs over private folders or local PDF paths
- prefer summary tables over raw debug dumps

## Review checklist

1. Search for secrets and secret-shaped env vars.
2. Search for absolute paths and raw notebook URLs.
3. Search for customer names, dataset slugs, or hidden benchmark identifiers.
4. Confirm the promoted score is tied to the right benchmark and not to an internal-only evaluation surface.
5. Review the changelog and summary text for private names or infra terms.

## Practical review step

Run the local release-safety checker before publishing. It should report only
finding categories for private paths, local endpoints, or credential-shaped
text; do not print, copy, or store any matching value.
