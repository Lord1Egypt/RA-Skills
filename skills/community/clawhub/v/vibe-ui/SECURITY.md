# Security Policy

## Supported Versions

The current supported version is `1.0.x`.

## Reporting A Vulnerability

Please report security, privacy, or provenance concerns through GitHub Security Advisories if available, or open a concise GitHub issue.

Include:

- Vibe UI version.
- Node.js version and OS.
- Command or workflow used.
- Steps to reproduce.
- Whether the issue involves local files, generated artifacts, package output, or upstream resources.

## Privacy Scope

Vibe UI is local-first. Normal CLI usage does not upload project files, page content, generated prompts, reports, or browsing history. The default workflow does not call model APIs.

`scripts/sync-open-design.mjs` is the explicit networked maintenance command for refreshing bundled upstream resources.
