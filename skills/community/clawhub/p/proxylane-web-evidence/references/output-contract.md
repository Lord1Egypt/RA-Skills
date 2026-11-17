# Outcome contract v1.0

Every source outcome contains `schema_version`, `mode`, `status`, `proof_mode`, `observed_at`, `observations`, `diagnostics`, and `evidence`. Successful bounded collections add `coverage` and `proxy` declarations. An optional separate `egress_probe` records its endpoint, IP and observation time, with `country_verified=false` and `target_request_ip_verified=false`.

| Status | Meaning and useful next action |
|---|---|
| `ok` | Required semantic fields were extracted within this mode's boundary. Currently a complete returned caption track can qualify. Read proof_mode first. |
| `partial` | Useful bounded observations exist, but comments, XHS coverage, regional context, checkout or currency remain incomplete/unverified. |
| `no_data` | Missing captions, missing offer fields, empty comments or an AI answer without external citations. Do not manufacture content. |
| `blocked` | Explicit source/proxy rejection, challenge, yt-dlp failure or MCP rejection. Inspect diagnostics and the supported upstream route. |
| `unsupported_surface` | Reviewed Google DOM or required upstream MCP tools are missing/ambiguous. Update a verified contract, not fallback to unrelated links. |
| `missing_session` | Existing XHS login was not positively confirmed. Operator login/session setup is separate. |
| `missing_input` | Supply the named connection/identity/DOM contract/MCP endpoint. |
| `input_error` | Bounds, URLs, required identity or connection format are invalid. |
| `missing_dependency` | Install the named library/executable in the isolated runtime. |
| `timeout` | Total or source deadline expired. Partial files, if present, are not a complete outcome. |
| `error` | Unexpected transport/shape failure or semantic target mismatch; inspect the diagnostic code. |

`fixture_demo` is the aggregate demonstration status, always `proof_mode=fixture`. Fixtures use a fixed timestamp, synthetic records and no network. A live outcome has `proof_mode=live`, even if it reports a block; that means a live attempt, not successful source proof.

`evidence[]` contains the selected source input after redaction, a SHA-256 of the serialized redacted bytes, byte count, and either a relative `.raw.json` path or inline input. The hash describes persisted redacted evidence, not the unredacted upstream response. Caption raw input includes timing/language; comments include selected yt-dlp source fields; Google includes the visible answer/citation attributes and selector contract; XHS includes parsed detail JSON; live price evidence includes selected DOM fields or the matching Product JSON-LD. Full browser state, scripts, cookie jars and screenshots are not archived.

Source identity and timestamp link to an observation, not a promise that a later visit reproduces personalized/dynamic content. Captions can be generated or translated upstream. Comment sampling preserves ids and text but does not score sentiment, estimate demand, infer authors' locations or claim representativeness. XHS descriptions exclude image content unless separately read. Google `regional_validation` remains `unverified`; `gl`, language, proxy input and footer observations do not establish regional causality. Amazon price text preserves its currency symbol, with typed `price` and `currency` null when unconfirmed. A JSON-LD Offer needs an exact SKU/productID, one explicit Offer, finite price, ISO currency and schema.org availability; its truth at checkout is unverified.

Exit code 0 means `ok`, `partial` or the synthetic aggregate demo. Other outcomes exit 2. Invalid CLI syntax is an argparse usage error on stderr, distinct from a source collection outcome. Capture the emitted JSON before relying on the process exit code.
