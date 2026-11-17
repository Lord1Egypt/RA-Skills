# The receipt envelope — one schema, four grades

A number without its execution conditions is a rumour with a decimal point. The
fix is not "remember to mention the shots": it is a **named block with a
version**, attached to every committed result, plus a script that grades every
artefact against it. EndoTrack ships this as `qas/envelope/0.1`; the design
transfers directly.

## The block

Attach one of these to every result artefact — not to the run log, to the
artefact that gets read:

```json
{
  "schema": "qas/envelope/0.1",
  "claims": ["AQFT_k1 beats QFT_full at p=1e-3, n=16"],
  "engine": "H2-Emulator",
  "backend_qualifier": "emulator",
  "shots": 2048,
  "seed": 20260826,
  "commit": "a1b2c3d",
  "envelope": 0.0442,
  "verdict": "PASS"
}
```

Field notes, each earned the hard way:

- **`claims`** is a list of sentences, not a topic. If you cannot write the
  claim as a sentence that could be false, the artefact is not making a claim
  and belongs on the no-claim list instead.
- **`backend_qualifier`** exists so `engine` can never be read as hardware.
  `emulator` / `simulator` / `hardware`, always present, never inferred from the
  device name — `H2-Emulator` and `H2-1` differ by one word.
- **`envelope`** is the statistical tolerance the verdict was decided against,
  computed, not remembered: `4·√(0.5/shots)` for a probability comparison
  (`SKILL.md` #3). Storing it means a later reader can re-decide the verdict
  without re-deriving the threshold.
- **`seed` + `commit`** are what make the row reproducible. A missing commit
  turns every other field into a claim about code that no longer exists.

## The four grades

The audit script (`tools/validate_receipts.py` in EndoTrack) walks every
artefact and grades it. Four outcomes, because two are not enough:

| Grade | Meaning | What to do |
| --- | --- | --- |
| `PASS` | Envelope present, complete, internally consistent | Nothing |
| `GAP` | Envelope present but a field is missing or null | Fill it; do not downgrade the claim |
| `STRUCTURAL` | No envelope at all — the artefact predates the schema | Migrate, or put it on the no-claim list |
| `FAIL` | Envelope present and **contradicted** by the artefact (verdict disagrees with the criteria, shots disagree with the envelope) | Block the build |

The distinction that matters is `GAP` vs `FAIL`. Missing information is not a
lie, and collapsing the two either blocks builds over paperwork or lets a
contradiction through as "incomplete". Same rule as the device matrix's
`unknown` (`SKILL.md` #56): absence and refusal are different verdicts.

## How this maps onto what this project already emits

We have the pieces, spread across three places, which is why nothing can audit
them as a unit:

| Envelope field | Where it lives today |
| --- | --- |
| `claims` | `verdict` + `verdict_criteria[].statement` in each dump |
| `engine`, `backend_qualifier` | the `execution` block's meter (`mode`, `device`) |
| `shots`, `seed` | the meter |
| `commit`, artefact digest | `quantum/provenance.py` (`artifact_sha256`) |
| `envelope` | recomputed ad hoc per driver from `4*sqrt(0.5/shots)` |
| `verdict` | top-level `verdict`, guarded by `tests/test_evidence_chain.py` |

Convergence path, when it is worth a gate: emit one `receipt` block per dump
built from those existing sources, extend `tests/test_evidence_chain.py` to
grade `PASS/GAP/STRUCTURAL/FAIL` instead of pass/skip, and let the no-claim
registry absorb the `STRUCTURAL` rows that are genuinely claimless. Until then,
treat this file as the target shape, not as something we ship.

## The rule that survives even without the tooling

Never display a result number without its engine qualifier and its shot count in
the same view. Every certified figure on a page, in a table, or in a chat reply
carries where it ran and how many shots it took — because that is the pair a
reader needs to know whether to believe it.
