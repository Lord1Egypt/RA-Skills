# Evidence integrity: making a number defensible

Running the circuit is the easy half. This card is about the other half: what
has to travel with a number before anyone should believe it, and what you are
not allowed to say about it.

## The three-layer trust ladder

Name the layer you are actually on. Most projects are on L1 and part of L2, and
claim L3 by accident through loose wording.

| Layer | What it guarantees | How you get there |
| --- | --- | --- |
| **L1 — receipt chain** | The number is reproducible. Job id, device, shots, seed, committed JSON, and a second-engine cross-check travel with it, so anyone can re-run and land in the same place. | The `job_meter` record (`quantum/backends.py`) plus a committed `src/data/demos/*.json`. Nothing extra needed. |
| **L2 — independent arbiters** | The number is not an artefact of one provider or one split. Several engines with independent compilers and noise models agree; matched splits + paired bootstrap on any statistical claim; a per-batch control circuit that fails loudly if the batch was corrupted. | Multi-engine table (see `cross-platform-validation.md`) + the Bell control below. |
| **L3 — cryptographic verification** | The number is trustworthy even if the *server is untrusted*: verified blind computation / verifiable blind error mitigation / logical accreditation on the QPU itself. Evidence would carry `trust_model: "untrusted-server"` and a proof reference. | Ion-trap-class protocols: arXiv:2410.24133 (on-chip verified computation), arXiv:2607.25704 (VBPEC), arXiv:2508.05523 (logical accreditation). **Pre-registered target, not a claim you hold today.** |

Say: *"every number carries receipts and cross-arbiters; the verification line
points at Quantinuum-class ion-trap protocols for the QPU phase."*

Never say: *"our results are cryptographically verified"* — that is L3, and L3
requires a protocol you have actually executed.

## Per-batch Bell control

The cheapest arbiter there is, and the only one that catches a corrupted or
misrouted batch rather than a wrong circuit. A known-fidelity Bell pair rides
along in **every** job, beside the target circuit:

```python
# alongside the target circuit in the same submission
q0, q1 = qubit(), qubit()
h(q0); cx(q0, q1)
output("bell", [measure(q0).read(), measure(q1).read()])
```

An ideal `|Φ+⟩` yields only `00` and `11`. The **anti-correlated count** (`01`
plus `10`) is the control statistic:

- Accept the batch when `anti / shots <= 4 * sqrt(0.5 / shots)` — the same 4σ
  binomial envelope used everywhere else in this skill.
- On a noiseless lane the expected count is exactly 0; anything above the
  envelope means the batch is not the batch you think it is (wrong device,
  wrong bit order, a rebase that changed semantics, or a genuinely degraded
  machine).
- **Fail the whole batch, not the control row.** A control that fails and is
  reported as one bad row among twenty is decoration.
- Record `bell_anticorrelated`, `bell_shots` and the verdict in the dump next to
  the target value, so the check is visible in the artefact and not only in the
  run log.

The Bell control also doubles as a bit-order probe: on a lane where the key
convention is reversed, `01`/`10` still read as anti-correlated, but pairing it
with a deliberately asymmetric circuit (a one-gate X probe) separates the two
failure modes.

## The dequantization gate

Before **any** advantage claim, run the classical surrogate and report the
result whichever way it falls (the Born-Ultimatum discipline, arXiv:2511.01845).
If a classical method reproduces the distribution or the metric within error,
the quantum claim is dissolved — you say so, in the artefact, in the same
sentence as the quantum number.

This is the citation-backed form of the rule already in `SKILL.md` #20: run the
classical baseline *before* writing any quantum code. The gate is not "did the
quantum thing work" but "is there anything here a classical surrogate cannot
do".

## Negative-result discipline

A negative that is committed with receipts is worth more than a positive that is
softened.

- **Withdraw, do not soften.** A result that fails to replicate at larger `n` is
  withdrawn outright, and the withdrawal is the current state. Phrases like
  "preliminary", "trending", or "under further investigation" applied to a
  failed replication are a way of keeping a dead claim alive.
- **Shot-scaling ladder tells shot noise from equivalence.** Run the same
  comparison at 128 / 512 / 2048 shots. If the metric is flat across the ladder
  and the paired CIs cross zero, the honest verdict is *classically
  equivalent*, not *shot-noise-limited*. Only a metric that improves
  monotonically with shots earns "needs more shots". To *seal* the verdict
  rather than merely state it, extend the ladder until no plausible shot budget
  is left unexamined (EndoTrack sealed theirs at five levels, 128 → 32768, with
  7 700 pair-receipts) — a flat curve over two decades of shots is an argument;
  a flat curve over one is an invitation to ask for more shots.

- **Supersession is explicit.** When result B supersedes result A, the artefact
  for A carries the supersession notice and B is what every consumer gets by
  default. Never leave two live artefacts making opposite claims.
- **Fail loud on a missing artefact.** A tool asked for the certified number
  must raise when the current artefact is absent — never fall back to the
  superseded one. A silent fallback turns a withdrawal into a re-publication.
- **Count the closures.** A question is not closed because one experiment came
  back negative; it is closed because several *independent* attempts to open it
  all failed. Report the count and name each closure ("closed five ways: Fourier
  wall / 10q simulation / real-kernel refusal / shot-floor / shot-scaling seal").
  A single negative invites "you didn't try hard enough"; an enumerated set of
  independent closures answers it in advance.
- **`assessed-blocked` is not `not tried`.** When a re-certification is stopped
  by a platform limit rather than by the physics, record it as assessed and
  blocked, with the limit and the error. Leaving it out makes a measured wall
  look like a gap in the work, and someone will eventually "fill" it by
  re-running the thing that cannot run.

## Structural withdrawal — a manifest, not a policy

"Withdraw, don't soften" is a rule a writer can forget at 2am. Make it a
resolver instead.

- One file is the **sole authority** on artefact state: `current` /
  `superseded` / `archived`, keyed by claim kind (EndoTrack's
  `results/evidence_manifest.json`; this project's equivalent is the verdict +
  `NO_CLAIM` registry in `quantum/verdicts_legacy.py` plus the committed dumps).
- Every consumer — MCP tool, route loader, report builder — reads *through* the
  manifest (`read_current_artifact("biomarker_auc")`), never by filename. A
  superseded artefact is then unreachable by construction: you cannot serve
  `..._n28.json` as current because nothing resolves to it.
- The manifest records the supersession edge, so "what replaced this, and when"
  is answerable from the artefact store rather than from a changelog.
- Resolution failure raises. A resolver that falls back to the newest readable
  file re-publishes the withdrawn claim the first time a path changes.

The test to write: assert that the withdrawn kind resolves to the superseding
artefact and that asking for the withdrawn id directly returns its supersession
notice rather than its numbers.


## Forbidden phrasings

Keep this list next to any copy generation:

| Never say | Because |
| --- | --- |
| "cryptographically verified" | That is L3; you are on L2. |
| "ran on H2 / Helios QPU" for an emulator run | An emulator is not a QPU, even when the device name shares a prefix. |
| "beats classical" without the dequantization gate | The gate is the claim's precondition, not its footnote. |
| a withdrawn number quoted as current | Supersession exists precisely to stop this. |
| "quantum advantage" from a single lane | One leg is a rumour (`SKILL.md` #20). |
