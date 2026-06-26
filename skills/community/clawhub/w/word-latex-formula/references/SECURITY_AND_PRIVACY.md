# Security and Privacy Notes

## Local processing by default

The rule-based path is local-only. The tool reads the user's Word document from disk, converts legacy formats through local Microsoft Word or LibreOffice when needed, scans text runs, and writes a new `.docx` with editable OMML equations. It does not contact any external server during scan, rule decision, apply, or local Web preview generation.

## Why external data may be sent

Academic formulas are often ambiguous: a fragment can be a real formula, a feature code, a citation, a page range, or ordinary prose. AI review is optional and exists to improve classification accuracy and normalize complex formula text into editable LaTeX before OMML conversion.

External data is sent only after the user explicitly enables AI review from the CLI or Web UI and provides an API key, base URL, and model name. The destination is the user-configured OpenAI-compatible endpoint, not a hard-coded service.

## What is sent during AI review

The AI payload is limited to formula-candidate records:

- candidate id
- extracted formula-like text
- nearby paragraph context needed for classification
- local LaTeX draft when available
- confidence or default local action
- requested model name

The built-in AI review path does not upload the entire Word document, embedded files, images, or generated output document. Context is included because it is necessary to distinguish formulas from references, URLs, feature-code lists, headings, and prose.

## API keys and persistence

API keys are supplied by the user through command parameters, environment variables, or the local Web UI configuration. The ClawHub package does not include any real key. The Web UI can write a local `.env` file only on the user's machine, so repeated local runs do not require re-entering model settings.

## Failure behavior

AI calls use a timeout and retry policy. If a batch still fails, the tool falls back to a local rule, keep, or review strategy selected by the user. This prevents the overall task from blocking on network or vendor availability.

## User-facing disclosure

Before enabling AI review, tell the user that formula candidates and nearby text snippets will be sent to the configured model endpoint. For sensitive manuscripts, recommend the local rule-based workflow or a self-hosted model endpoint.
