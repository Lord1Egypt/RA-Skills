# Tunly Artifact Share Feature Showcase

Use this reference when presenting or testing the skill.

## Feature Matrix

- Tunly account gate: requires registration/login before publishing.
- Agent artifact input: accepts review pages, Codex/Claude-style HTML, reports, static sites, dashboards, prototypes, and evidence bundles.
- Durable latest link: supports stable review links that can be updated over time.
- Immutable version: preserves a specific revision for audit and acceptance.
- Privacy modes: supports public, private, account-only, and concealed unauthorized access when Tunly exposes those modes.
- Publish-to-serve verification: requires fetching the served URL after publish.
- Durability check: rejects local-only, tunnel-only, or dev-server-only outputs.
- Evidence summary: final response records what was verified and what remains unknown.

## Demo Narrative

1. Agent creates an HTML review page from a plan or acceptance report.
2. User logs in to Tunly or provides API access.
3. Tunly publishes the artifact under a stable link.
4. Tunly returns latest and version identifiers.
5. The agent fetches both links and verifies content identity.
6. The agent checks unauthorized access according to the chosen privacy mode.
7. The user gets a share-ready link plus audit evidence.

## Positioning Sentence

Tunly is the artifact sharing and verification layer for AI agents: Claude and Codex can create useful outputs; Tunly makes them durable, private when needed, versioned, and reviewable.