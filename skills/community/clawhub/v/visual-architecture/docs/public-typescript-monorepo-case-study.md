# Public TypeScript Monorepo Case Study

This case study is intentionally generic. It is modeled on the shape of a serious private TypeScript monorepo without publishing private repo names, file paths, client data, or deployment details.

## Scenario

A product repo contains a web client, API server, editor extension, shared packages, backend modules, realtime gateway, API client, and database layer. A human reviewer wants the agent to explain the architecture without inventing systems or leaking private details.

## Surfaces

- Client app: routes, feature modules, hooks, and UI state.
- Server app: HTTP entrypoint, controllers, services, and background jobs.
- Editor extension: local command surface that calls the product API.
- Shared packages: types, API client, validation helpers, and config.
- Backend modules: domain services, auth/session rules, import/export jobs, and queue workers.
- Realtime gateway: websocket or event bridge for collaborative state.
- Database layer: migrations, repositories, and persistence boundaries.
- Proof bundle: generated SVG/HTML, receipt JSON, share card, and source-evidence drilldown.

## Extraction Claims

Visual Architecture should identify these surfaces as a reviewable starter map, not as a final omniscient diagram. The value is a deterministic artifact the reviewer can correct: nodes, edges, evidence, confidence, and receipt quality are all visible.

## Review Path

1. Extract a repo map.
2. Inspect evidence and confidence.
3. Run layout for a readable first pass.
4. Bundle the artifact.
5. Use the gallery to review the map and receipts.
6. Correct the JSON spec when the tool is wrong.

## Public Boundary

The public artifact uses generic names and source descriptions only. It does not publish private application names, internal hostnames, customer names, environment values, or proprietary code structure.
