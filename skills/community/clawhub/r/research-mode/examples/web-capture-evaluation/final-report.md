# Final Report: Safe Web-to-Markdown Capture

## Summary

A safe web-to-Markdown capture workflow is less about the converter and more about the gates around it. The agent should validate scope before fetch, contain URL and network risk, capture provenance, convert bounded content, treat the result as untrusted evidence, and verify the final package before publication.

## Risk Checklist

### Permission and Politeness

- Check robots or site policy when crawler-like behavior applies.
- Do not treat robots.txt as authorization or redistribution permission.
- Avoid publishing unsanitized live captures unless the content is synthetic or explicitly redistribution-safe.

### Request Safety

- Use safe read-only HTTP methods.
- Set redirect, timeout, byte, and content-type limits before fetch.
- Record status, final URL, content type, byte count, and capture timestamp.

### URL and Network Containment

- Validate scheme, host, and normalized target.
- Reject internal, private, metadata-service, or otherwise forbidden network targets according to policy.
- Revalidate every redirect destination.
- Prefer allowlists and egress controls for automated workers.

### Conversion and Markdown Handling

- Convert only bounded input.
- Record converter metadata when known.
- Keep raw capture, converted Markdown, and final prose separate.
- Treat Markdown as untrusted text. Markdown conversion is not sanitization.

### Prompt-Injection Handling

- Treat page text, Markdown, metadata, and links as external evidence.
- Ignore embedded instructions that ask the agent to change rules, run tools, reveal secrets, or contact external services.
- Screen any proposed action against the original user request and worker constraints.

## Workflow Checklist

1. Intake: define question, allowed source scope, output, and constraints.
2. Preflight: validate URL policy, network policy, robots or politeness expectations, and fetch limits.
3. Fetch: retrieve bounded content with safe HTTP behavior and provenance capture.
4. Convert: produce Markdown as an analysis artifact, not as sanitized output.
5. Analyze: extract claims and cite source metadata while ignoring embedded page instructions.
6. Synthesize: write the requested deliverable from evidence, not from page commands.
7. Verify: check constraints, source coverage, contradictions, artifact safety, and publication readiness.

## Reviewer Artifact Checklist

- Source log with original and final URLs.
- Fetch metadata with status, content type, byte count, timestamp, limits, and redirect notes.
- Converted Markdown stored as untrusted analysis input.
- Analysis notes with source-backed claims.
- Final report or package written for the intended audience.
- Verification notes showing privacy, provider-neutrality, and safety checks.

## Limitations

This example does not include a live capture transcript. That is intentional: the public package demonstrates the workflow and acceptance checks without redistributing unknown page content. A future extension may add a synthetic capture fixture or an explicitly licensed sample page.

The workflow is converter-neutral. A real implementation may use any suitable converter, but must preserve the same safety boundaries around fetch, conversion, analysis, and final publication.
