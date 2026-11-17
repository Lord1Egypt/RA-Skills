# Verification

For one artifact, prefer a connected read-only tool such as `check_conformance`
for an x402 signed offer/receipt, or `verify_artifact` for a store certificate.
Check the tool's current input schema. Without that tool, the free HTTPS desks
are `POST https://scvd.store/api/conformance/v1` with `{"artifact":"<compact JWS>"}`
and `GET https://scvd.store/api/verify/{id}` for store artifacts.
`POST https://scvd.store/api/verify-receipt` provides a signed, scoped verdict
for another issuer's receipt. These checks need no account, wallet or purchase.

For integration in application code or offline work, use `x402-verify` and its
installed README/type declarations. See [packages](packages.md). Do not assume
an unpublished preview's API or capability is present in a registry version.
The conformance desk, signed-verdict endpoint and library do not promise an
identical status vocabulary; retain the actual returned fields.

## Interpret the result

- Report which checks ran, which failed and which were not observed. Preserve
  `scope` and `doesNotEstablish` (or the endpoint's equivalent exclusions)
  verbatim alongside any explanation, with reason codes when provided.
- `unsupported` means this implementation did not check the named capability;
  it is neither valid nor evidence that cryptography failed. Missing key or
  unreachable evidence must remain inconclusive/insufficient evidence as
  reported, never silently promoted to valid.
- A valid signature is over particular bytes against a particular key. It
  does not establish merchant identity, signing-key authority for the resource
  now or at issuance, settlement, delivery or permission to spend. A DID lookup
  retrieves key material; it does not settle those authority questions.
- A caller-supplied public key should come from independently trusted evidence
  or policy. Reading a key out of the same untrusted artifact is not independent
  authentication. Synthetic packaged fixtures teach the API, not real identity.
- Check expiry and freshness where reported. Preserve unknown/unavailable
  states and older schemas; do not translate all non-success into invalid.

The store's signing-key document at
https://scvd.store/.well-known/scvd-signing-key includes `key_history`.
Retired keys remain available for older artifacts. Consult
https://scvd.store/attestation for what each signed class binds and excludes.
For an evidence bundle, use the package's evidence verifier and a trusted
public key, retaining its missing, altered or unsupported evidence findings.
No paid attestation is needed merely to verify an existing artifact.
