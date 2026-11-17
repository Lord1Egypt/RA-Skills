---
name: soja-trace-evidence-checks
description: Use when an agent needs a public bounded deterministic W04 trace-integrity verification from supplied redacted JSON evidence.
version: 1.1.0
---

# SOJA W04 Trace Integrity Verifier

## Public machine-callable W04

Submit one bounded, redacted expected-versus-observed trace evidence manifest:

```http
POST https://soja-w04-public-evaluate.slowsleeper1.workers.dev/v1/trace-integrity-verifier/evaluate
Content-Type: application/json
```

- Maximum request payload: **64 KiB**.
- No API key is currently required.
- The result is deterministic and machine-readable JSON.
- Responses use `Cache-Control: no-store`.
- Invalid JSON, unsupported methods/routes/content types, oversized payloads, secret-bearing input, unsupported resources, and invalid bounded inputs are safely rejected.

## Request

```json
{
  "resource": "trace-integrity-verifier",
  "request_id": "example-001",
  "input": {
    "expected": {"trace_ids": ["trace-a", "trace-b"], "links": [["trace-a", "trace-b"]]},
    "observed": {"trace_ids": ["trace-a"], "links": []}
  }
}
```

`request_id` is a non-empty string up to 128 characters. `trace_ids` and link values must be strings. The verifier compares only supplied evidence; absence of supplied evidence is not proof of runtime failure.

## Response

```json
{
  "invocation_status": "COMPLETED",
  "request_id": "example-001",
  "resource": "trace-integrity-verifier",
  "result": {
    "status": "INCOMPLETE",
    "complete": false,
    "expected_trace_count": 2,
    "observed_trace_count": 1,
    "missing_trace_ids": ["trace-b"],
    "missing_links": [["trace-a", "trace-b"]]
  }
}
```

## Safety and limits

Do **not** submit secrets, credentials, tokens, customer data, production traces, or other sensitive payloads. No customer storage, telemetry, configured secrets, payment, checkout, or source download is provided.

A Cloudflare Workers Rate Limiting binding is configured at a nominal 10 requests per 60 seconds. Cloudflare enforcement is location-dependent and eventually consistent and should not be interpreted as a strict globally synchronized request ceiling.

## Evidence boundary

Public availability and controlled tests are not commercial evidence. Paid invocations, customers, Tier C/A evidence, payments, and revenue remain zero.

## W05

The evaluation cost-reconciliation sentinel remains descriptor-only and is not publicly callable.
