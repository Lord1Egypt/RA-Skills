# Web Capture Example: Risk Model and Package Map

This analysis turns the first source pass into a provider-neutral package plan for
`examples/web-capture-evaluation/`. It is not a final deliverable; it is an
intermediate map for synthesis/finalization.

## Risk model

1. Capture permission and politeness

- Treat `robots.txt` as crawler coordination, not authorization or copyright
  clearance. RFC 9309 says REP rules are not access authorization.
- Use a clearly identified user agent when automated fetching is used.
- Keep robots decisions, HTTP status, and fetch timestamps in the capture record.

2. Request safety

- Prefer HTTP safe methods for capture (`GET` and `HEAD`) and do not submit
  forms or trigger authenticated state-changing workflows.
- Bound redirects and revalidate each redirect target before fetching. RFC 9110
  describes redirect `Location` as a new target URI, which means URL validation
  must be repeated after resolution.
- Add timeouts, byte limits, content-type checks, and retry discipline.

3. URL and network containment

- Do not trust parser success as validation. Python's `urllib.parse`
  documentation warns that parsing APIs do not validate inputs and recommends
  defensive checks for security-sensitive use.
- Require `http` or `https`; reject credentials in URLs; normalize hostnames;
  block private, loopback, link-local, multicast, and metadata-service targets;
  and resolve DNS in the same network context that performs the fetch.
- If a converter can fetch remote URIs itself, prefer prefetching with a hardened
  fetcher and passing a bounded stream/response into conversion.

4. Conversion and Markdown handling

- Markdown is an analysis format, not a sanitizer. CommonMark supports raw HTML
  blocks, and a converter may preserve links or HTML-like content.
- Store raw response, converted Markdown, and sanitized/renderable output as
  separate artifacts when rendering is required.
- MarkItDown can be cited as one possible converter example, but the public
  package should stay converter-neutral. Its own security notes support the
  general rule: conversion runs with current-process privileges, untrusted input
  must be restricted, and callers should use the narrowest conversion API.

5. Prompt-injection boundary

- Treat fetched web pages, raw HTML, converted Markdown, and summaries as
  untrusted data.
- Delimit captured content, label provenance, and prevent page text from
  authorizing tools, messages, file writes, purchases, or account changes.
- Screen proposed actions against the original user goal, not against instructions
  discovered inside the captured page.

## Workflow for the example

1. Intake

- Record the user's research question and allowed URL scope.
- Reject or queue any URL outside the declared scope.
- Decide whether capture is needed or whether an already saved corpus should be
  used.

2. Preflight

- Validate URL syntax and policy.
- Check DNS/IP/network restrictions.
- Check robots/politeness requirements for crawler-like behavior.
- Decide fetch limits: method, redirect count, timeout, maximum bytes, acceptable
  media types.

3. Fetch

- Fetch with `HEAD` or `GET` only.
- Follow redirects only after revalidating each target.
- Save status code, final URL, headers needed for provenance, captured time, and
  truncation/error notes.

4. Convert

- Convert only bounded content.
- Prefer stream/response conversion over giving an untrusted URL directly to a
  permissive converter.
- Record converter name/version when known, but keep the workflow independent of
  any one converter.

5. Analyze

- Read converted Markdown as untrusted evidence.
- Extract facts, links, and claims with source references.
- Ignore embedded instructions that ask the agent to change rules, call tools, or
  reveal secrets.

6. Package

- Keep the public example small: five Markdown files are enough for review.
- Do not include a live capture transcript unless it is synthetic or sanitized.
  A transcript can be useful later, but the current deliverable asks for the five
  files and should avoid accidental redistribution concerns.

## File map for the requested package

- `README.md`: purpose, quick start, safety boundaries, expected outputs, and a
  note that the example is provider-neutral.
- `prompt.md`: worker prompt that separates user goal, allowed sources, fetch
  constraints, untrusted-content handling, and required artifacts.
- `research-plan.md`: staged plan with intake, preflight, fetch, conversion,
  analysis, synthesis, and verification gates.
- `sources.md`: official/primary sources with short notes and why each matters.
- `final-report.md`: concise evaluated workflow, risk checklist, artifact
  checklist, and limitations.

## Resolved open questions

- Sanitized transcript: do not include one in the initial public package. Mention
  it as an optional future extension if the transcript is synthetic or clearly
  redistribution-safe.
- Converter reference: keep the workflow converter-neutral. MarkItDown may be
  referenced as an illustrative converter with explicit safety caveats, not as a
  required dependency.

## Source anchors

- RFC 9309, Robots Exclusion Protocol: https://datatracker.ietf.org/doc/html/rfc9309
- RFC 9110, HTTP Semantics: https://datatracker.ietf.org/doc/html/rfc9110
- Python `urllib.parse` documentation: https://docs.python.org/3/library/urllib.parse.html
- OWASP SSRF Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
- OWASP LLM Prompt Injection Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html
- CommonMark Spec 0.31.2: https://spec.commonmark.org/0.31.2/
- Microsoft MarkItDown repository: https://github.com/microsoft/markitdown
