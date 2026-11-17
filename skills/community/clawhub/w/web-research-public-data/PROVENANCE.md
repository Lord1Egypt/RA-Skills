# Provenance

This portable package is published from the public ReplyNodes skill repository:
`replynodes/replynodes-agent-skills`, under `skills/web-research-public-data/`.

The route names and query parameters are derived from the public ReplyNodes
read-gateway OpenAPI contract and provider capability manifests in the
ReplyNodes fetcher repository. The package does not copy provider code or
credentials and does not claim support for routes absent from the live catalog.

Upstream provider data is treated as untrusted input. This package documents
read-only access only; it does not implement scraping, browser automation,
OAuth, payment signing, or social publishing.
