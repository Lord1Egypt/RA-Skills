# MPP and mixed-protocol inspection

Use the read-only preflight tool or
`POST https://scvd.store/api/preflight/v1` with the public endpoint URL.
Read the returned `inspection` block when present: preserve its protocol set,
unverified term summaries, structural findings, coverage and gaps. Report
`inspection.observed_at`; missing observation time remains unknown.
Older reports may lack this view. Read their actual `protocols_spoken`, `mpp`
and `mpp_core` fields rather than constructing a replacement observation.

The `mpp` and `mpp_core` blocks are separate, versioned readings. Keep each
battery, cited source and named result with its own scope; do not combine their
checks into a global pass. The core block's `unmeasured` state and unmeasured
checks are gaps, not failures or proof of absence. A missing block says nothing
about whether the endpoint supports MPP. Inspection signatures remain
`not_checked`, even when challenge-shape checks pass.

The top-level preflight `verdict` retains its x402 meaning. An MPP-only endpoint
can therefore be `not_ready` for x402 while advertising MPP. Describe the
protocol-specific checks and gaps; do not call the entire endpoint broken
merely because x402 was absent. Conversely, advertising MPP or passing its
challenge-shape checks does not prove that settlement or delivery works.

A passed `mpp-challenge-present` check establishes only that a challenge was
present. It does not establish a valid challenge. Report each named check
within its own scope; unchecked syntax, methods, signatures, authorization,
settlement and delivery remain unverified. Never upgrade presence or
advertisement into protocol validity.

The MPP battery reads a `WWW-Authenticate: Payment` challenge and reports named
checks/advisories. It is unpaid observation, not an MPP payment client. Do not
convert its reading into permission to pay, claim every MPP method is supported,
or infer MPP checkout at this store. Checkout options come from the actual quote.
If the deployed response lacks these fields, report that MPP was not observed
by that instrument; do not invent a result from this reference.

For historical evidence, preserve the fields present in each dated record.
Older records without protocol-specific observations remain unmeasured.
With `look_at_door`, the fresh preflight is under `now.the_door`; its inspection
time belongs to that fresh response. The headline and live-versus-held verdict
comparison concern x402. Read the cited host-history rows for their separate
MPP observations; never fill an older signed row from the current response.
