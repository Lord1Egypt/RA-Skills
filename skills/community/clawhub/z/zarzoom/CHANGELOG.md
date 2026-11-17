# Changelog

All notable changes to the ZARZOOM Skill for OpenClaw.

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-08-14

### Added
- Initial release.
- Tool: submit an article to ZARZOOM's compliance pipeline (with optional images via the presigned R2 upload flow).
- Tool: submit a short (50–150 words, optional image).
- Tool: submit a video (MP4 / WebM, optional thumbnail).
- Tool: check the status of a submission (pending / approved / rejected) and read its per-platform eligibility.
- Tool: list the customer's submissions, filterable by status.
- Tool: list the customer's approved content (articles / shorts / videos).
- Tool: pull analytics — overview, top performers, per-platform breakdown.
- Tool: check per-post status across platforms after admin approval + engine fan-out.
- Tool: discover which platforms the customer has connected and what each one's limits are.
- Error-handling instructions for 401, 422, 429, 5xx responses with concrete recovery steps.
- README + reference guides for endpoint usage, error codes, and worked examples.

### Notes
- Authentication uses customer-managed `zarz_live_*` API keys — no OAuth.
- The Skill speaks only to `https://zarzoom.com/api/v1/*` over HTTPS.
- No data passes through ClawHub or any third-party server.
