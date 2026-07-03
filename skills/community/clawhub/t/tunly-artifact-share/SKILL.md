---
name: "tunly-artifact-share"
description: "Create, publish, share, and verify Tunly artifacts with privacy and versioned links."
license: MIT-0
user-invocable: true
metadata:
  openclaw:
    skillKey: "tunly-artifact-share"
---

# Tunly Artifact Share

Use this skill when a user wants an agent-generated artifact to become a durable Tunly link: a review page, Codex/Claude-style HTML artifact, report, deck, dashboard, evidence bundle, prototype, or generated document that can be shared, revised, audited, and protected by an access policy.

Tunly's promise is not just "make a file." It is: create the artifact, publish it, verify the link, preserve the version, and prove the privacy boundary.

## Goal

Turn agent output into a shareable Tunly artifact with:

- a stable latest link for ongoing review
- an immutable version or revision link for audit
- explicit access mode: public, private, account-only, or concealed unauthorized access
- publish-to-serve verification through Tunly's resolver
- a concise evidence summary the user can trust

This skill is for productized artifact delivery. It is not a generic project-management flow and it is not a temporary local preview workflow.

## Requirements

This skill should remain visible even before the user has a Tunly account. Registration and login are execution gates, not installation gates.

Before publishing, the agent must confirm that the user has access to Tunly:

- A Tunly account or workspace exists.
- The `tunly` CLI or Tunly API client is available.
- Authentication is active through `tunly login`, `tunly whoami`, or an equivalent API token such as `TUNLY_API_TOKEN`.
- The intended access mode is known: public, private, account-only, or concealed unauthorized access.

If Tunly is not installed or the user is not authenticated, stop and guide the user to register or log in. Do not fall back to local files, temporary preview servers, public tunnels, or chat attachments as substitutes for Tunly publishing.

## Use This Skill When

- A Claude, Codex, OpenClaw, or other agent output should become a durable share link.
- The user asks to publish a review page, acceptance report, generated doc, static site, dashboard, prototype, or evidence bundle.
- The artifact needs privacy guarantees instead of an unrestricted public URL.
- The user needs both a mutable latest URL and an immutable version URL.
- The artifact should keep working after the local process, chat session, or dev server exits.
- The user wants share-ready proof: what was published, who can access it, and how it was verified.

## Artifact Types

Tunly can be positioned as the sharing layer for agent-created artifacts:

- Review pages: plans, architecture reviews, launch checks, design reviews.
- Acceptance reports: pass/fail matrix, commands run, commit/deploy ids, residual risks.
- Claude/Codex-style HTML artifacts: interactive pages, dashboards, prototypes, demos.
- Evidence bundles: logs, screenshots, JSON reports, exported traces, signed summaries.
- Durable docs: generated Markdown/HTML/PDF-like static outputs.
- Status surfaces: static dashboards or operations summaries meant for stakeholders.

## Quick Start

1. Check Tunly access.
   - Run `tunly whoami` or the project-approved equivalent when the CLI exists.
   - If not authenticated, ask the user to register or run `tunly login`.
   - If using API-only access, confirm the API token is set and scoped for publishing.

2. Identify the artifact.
   - Path or directory to publish.
   - Intended audience.
   - Access mode.
   - Whether it needs a stable latest URL, immutable version URL, or both.

3. Prepare it for sharing.
   - Prefer static HTML for review surfaces.
   - Include a clear title, decision summary, evidence, risks, and review checklist when relevant.
   - Remove secrets, tokens, private hostnames, personal data, unrelated local paths, and accidental internal context.
   - If the artifact includes screenshots or binary files, treat them as manual privacy review items.

4. Publish through Tunly.
   - Use the available Tunly CLI/API, normally a structured command such as `tunly publish <path> --json` when present.
   - Request the access mode explicitly when the tool supports it.
   - Use a stable namespace/link name for artifacts that will be updated over time.
   - Preserve the structured publish response.

5. Verify the share contract.
   - Confirm latest URL and immutable version/revision id are present as expected.
   - Fetch the latest URL and verify it serves the expected artifact.
   - Fetch the version URL or revision URL and verify it is independently resolvable.
   - Confirm the artifact is served by Tunly, not by a local dev server or tunnel.
   - Verify access behavior matches the requested policy.

6. Report the result.
   - Lead with the latest URL.
   - Include immutable version/revision URL or id.
   - State access mode and verification performed.
   - State anything not verified.

## Privacy Rules

- Default to private/account-only for artifacts that contain project, customer, operational, personal, or unreleased product information.
- Do not downgrade to a public URL because it is faster.
- Do not claim private sharing unless unauthorized access was denied/concealed or Tunly returned an explicit enforceable policy.
- Treat screenshots, videos, PDFs, and unknown binary files as manual privacy review items.
- Strip or redact private paths, tokens, API keys, internal hostnames, bearer strings, cookies, and account identifiers before publishing.

## Versioning Rules

- Latest URL is for collaboration and iteration.
- Version URL or revision id is for audit and acceptance evidence.
- If the user is approving a specific result, include the immutable version link in the final response.
- If only a latest link exists, say that immutable version verification is missing.

## Verification Rules

A Tunly artifact is not done until publish-to-serve is checked.

Required checks:

- Structured publish response exists.
- Latest link fetches successfully when expected.
- Immutable version/revision link fetches successfully when expected.
- Content identity is verified with title, sentinel text, checksum, artifact hash, or expected response body.
- Local preview/dev server dependency is ruled out.
- Access policy is verified or explicitly reported as unverified.

Stop and report a blocker if:

- Tunly account, CLI, API token, or workspace access is missing.
- The publish command returns success but the link cannot be fetched.
- The resolver serves stale or unexpected content.
- Private content is publicly accessible.
- Public content unexpectedly requires authorization.
- The publish response lacks identifiers needed for audit.
- The artifact depends on a running local process.

## Review Page Pattern

For human review artifacts, include:

- Decision summary.
- What changed or what was generated.
- Scope and non-goals.
- Evidence and commands run.
- Pass/fail matrix when relevant.
- Risks and residual gaps.
- Review checklist.
- Latest link and immutable version/revision link after publish.

## Final Response Pattern

Keep the user-facing response short:

```text
Published: <latest_url>
Version: <version_url_or_revision_id>
Access: <public/private/account-only/concealed> verified by <check>
Verified: latest fetch, version fetch, content identity, durability
Unverified: <none or exact gap>
```

## ClawHub Positioning

Describe this skill as Tunly's artifact delivery workflow for AI agents: the layer after Claude/Codex/OpenClaw creates something useful, where Tunly turns it into a durable, shareable, privacy-aware link with evidence.

Install the skill, register or log in to Tunly, then publish agent artifacts as durable links instead of leaving them inside a chat, local folder, temporary server, or one-off attachment.
