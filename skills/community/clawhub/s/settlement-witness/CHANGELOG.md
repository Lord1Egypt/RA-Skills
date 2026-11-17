# CHANGELOG

## 0.1.4

- Packaging-only release, no content change from 0.1.3. 0.1.2's publish
  accidentally bundled a stray `scripts/__pycache__/*.pyc`; the immediate
  0.1.3 republish fixed that but left `SKILL.md`'s own frontmatter
  `version:` field at `0.1.2`, so the published CLI version tag (`0.1.3`)
  and the file's self-reported version drifted apart. 0.1.4 reconciles
  them — the same class of version/frontmatter drift this skill's own
  0.1.2 entry (below) already fixed once for the key registry.

## 0.1.2

- **Root cause fixed**: `keys/sar-keys.json` and the `SKILL.md` frontmatter
  `version` field had drifted out of sync with the actual bundled key set and
  with each other (`SKILL.md` still said `0.1.0` while `CHANGELOG.md` already
  documented a `0.1.1` bundling change). This release reconciles both.
- Refreshed `keys/sar-keys.json` to the full, current 8-entry canonical SAR
  registry (was stale at 3 entries: `-01`/`-02`/`-03` only, no lifecycle
  data). Bundled snapshot is byte-identical to the canonical registry
  (sha256 `2da5285f458af9f3369e5baddd953164834d961161c87c9594b823ce251a4f6b`,
  confirmed 2026-07-19).
  See `sar-prod-ed25519-05` — the current active production signer — did not
  verify locally before this release; it now does.
- Added `scripts/registry_snapshot.py`: lifecycle-aware registry loading and
  classification (current-active / historical-retired / documented-non-
  operational-duplicate / reserved / legacy-unclassified / unknown /
  wrong-profile), scoped to the `sar_settlement_witness_signing` profile.
  Pins and enforces the bundled snapshot's SHA-256 (fails closed on mismatch)
  unless `SAR_KEYS_REGISTRY_PATH` is explicitly overridden.
- `verify_receipt.py` output now reports `signer_lifecycle_status`,
  `trusted_current_production_signer`, `trusted_historical_signer`,
  `registry_snapshot_sha256`, and `offline_verification_note` alongside the
  existing `valid`/`receipt_id`/`kid`/`verdict`/`errors` fields.
  `valid: true` is never conflated with `trusted_current_production_signer:
  true` — a retired key's historical receipt still verifies, but is never
  represented as a current-production-signer claim.
  `sar-prod-ed25519-02` (documented non-operational duplicate of `-03`'s
  public-key bytes) is never reported as an independently active signer.
- Added `fixtures/sar-v0.1-current-kid05.json` (a real, current, `-05`-signed
  production receipt) and `tests/test_registry_lifecycle.py` (duplicate-key,
  reserved-key, unknown-key, wrong-profile-key, snapshot-hash-pinning, and
  zero-egress coverage). `scripts/verify_receipt.py --self-test` now checks
  six fixtures, not four.
- Does not change signing behavior (this skill never signs), does not add a
  hosted dependency, does not weaken fail-closed verification, and does not
  add scoring/reputation behavior.
- **Corrected the "Optional remote receipt issuance" section**, which was
  stale against the production attest contract as of the 2026-08-26 D31
  auth hardening: wrong route (`/settlement-witness` instead of
  `/settlement-witness/attest`), no auth headers (every copy/paste example
  now 401s), and the retired `{"expected": ...}` spec shape instead of
  `ds.evaluation.deterministic_acceptance_spec.v0.1`. Also corrected the
  issued-receipt profile name to `settlement-witness-verified-v0.2` (was
  described as "SAR v0.1"). Local verification behavior is unchanged — this
  section only documents the optional remote-issuance request/response.

## 0.1.1

- Bundled the full current SAR public key registry (`sar-prod-ed25519-01`,
  `sar-prod-ed25519-02`, `sar-prod-ed25519-03`) in `keys/sar-keys.json`
- Added a current kid-03 production-signer fixture
  (`fixtures/sar-v0.1-current-kid03.json`) as an offline test vector
- Extended `scripts/verify_receipt.py --self-test` to cover the kid-03 fixture
- Ensures local verification works for current DefaultVerifier SAR receipts
  (signed by `sar-prod-ed25519-03`) as well as bundled historical fixtures
- Clarified in SECURITY.md that local verification requires the receipt's
  `verifier_kid` to be present in the pinned local registry

## 0.1.0

- Added local-first SAR v0.1 receipt verification via `scripts/verify_receipt.py`
- Added offline verifier requiring no network and no DefaultVerifier availability
- Added signed PASS, FAIL, and INDETERMINATE fixture receipts as test vectors
- Added tampered fixture expected to fail cryptographic verification
- Added bundled public key registry (`keys/sar-keys.json`)
- Added EGRESS.md with explicit offline/optional-network split and domain declaration
- Added SECURITY.md with trust model, non-claims, and key pinning policy
- Added spec/canonicalization.md with SAR v0.1 digest and signature rules
- Rewrote SKILL.md with proper ClawHub frontmatter (`name`, `description`, `version`, `metadata.openclaw`)
- Clarified that network is optional and only used for: remote signed receipt emission, receipt ID resolution, public key refresh, chain/correlation lookup
- Removed positioning language that implied DefaultVerifier executes tasks, approves actions, or controls funds

Earlier versions (0.0.4, 0.0.5) focused on remote DefaultVerifier receipt
issuance via the REST endpoint and MCP adapter. v0.1.0 makes local receipt
verification the default first path; remote issuance remains available but is
explicitly optional.
