# ClawHub Compliance

This package is the registry-facing core profile of `web-search-pro`.

## Audience

This document is for maintainers, reviewers, and security-minded users who need to understand why
the ClawHub package is narrower than the full repository and what the registry-facing trust story
actually is.

## Compliance Posture

The goal of this profile is to keep the published artifact aligned with what the registry can
reason about:

- honest hard requirement disclosure
- explicit optional provider env disclosure
- a narrower runtime surface
- a smaller static scan surface

## Hard Requirements

The only hard runtime requirement is:

- `node`

## Optional Provider Credentials

The following env vars are optional and widen retrieval quality:

- `TAVILY_API_KEY`
- `EXA_API_KEY`
- `QUERIT_API_KEY`
- `SERPER_API_KEY`
- `BRAVE_API_KEY`
- `SERPAPI_API_KEY`
- `YOU_API_KEY`
- `PERPLEXITY_API_KEY`
- `OPENROUTER_API_KEY`
- `KILOCODE_API_KEY`
- `PERPLEXITY_GATEWAY_API_KEY`
- `PERPLEXITY_BASE_URL`
- `SEARXNG_INSTANCE_URL`

No API key is required for the baseline.

## No-Key Baseline

The baseline is real but bounded:

- `ddg` provides best-effort search
- `fetch` provides extract / crawl / map fallback

If the no-key baseline degrades, `doctor.mjs` and `review.mjs` surface that status instead of
pretending the baseline is always healthy.

## Safe Fetch Boundary

Safe Fetch remains the default network boundary:

- only `http` and `https`
- blocks credential-bearing URLs
- blocks localhost / private / metadata targets
- revalidates redirects
- blocks unsupported binary downloads
- keeps JavaScript execution disabled

## Review Surfaces

Use:

- `node scripts/capabilities.mjs --json`
- `node scripts/doctor.mjs --json`
- `node scripts/bootstrap.mjs --json`
- `node scripts/review.mjs --json`

These commands expose:

- configured providers
- no-key baseline status
- activation paths such as native / gateway-backed provider lanes
- federated retrieval summary
- provider health and degradation
