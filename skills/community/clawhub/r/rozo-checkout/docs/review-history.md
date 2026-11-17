# Review history

[← back to the README](../README.md) · [Safety design](safety.md)

This tool moves other people's money. It was reviewed adversarially before it
was written, again after it was written, and again after the first real payment.
This page is the record of that.

## Design review — 3 rounds, before any code existed

The design was written as a plan document and reviewed by an independent model
with a standing instruction to hunt for anything that could lose funds. No code
was written until the plan passed with no P0 findings.

| Round | Verdict |
|---|---|
| 1 | 6 P0, 7 P1, 2 P2 — plan revised |
| 2 | still had P0s: several round-1 fixes were incomplete, plus one new P0 — plan revised again |
| 3 | no P0 — implementation began |

The P0s were about the plan being wrong regarding the payment rails, not about
style. Among them: the reuse rule was mis-stated (an existing order is reused
whenever it is merely unexpired, not only when it is unpaid); the binding
confirmation was placed before the deposit details existed, so it could not
bind them; and the payment link could be consumed by another payer between the
quote and the signature, which needed a re-check immediately before paying.

## Code review — 2 rounds, after implementation

| Round | Verdict |
|---|---|
| 1 | 8 P0, 10 P1, 5 P2 |
| 2 | 20 of 23 resolved; 3 residual findings, then fixed |

The round-1 P0s were the interesting ones, and each is now a real code path
with its own error code and tests:

- the confirmation gate and the `--send` opt-in were documented but not
  actually enforced
- the send-once claim was a check-then-act race that two concurrent processes
  could both pass
- an unreadable `amountReceived` was treated as "no money received" rather than
  as money
- the post-create comparison ignored security-critical fields when they were
  simply absent
- payability was not re-proved immediately before signing, and incomplete
  upstream state read as payable
- deposit instructions were not validated for completeness before being shown
- provider errors could leak credential-bearing URLs
- the tracked-secret check failed open when it could not consult git

## First real payment

A live payment then settled in about a minute — and surfaced four more defects,
all fixed in 0.1.3:

- the built bundles crashed on newer Node because the bundler's CommonJS shim
  was incomplete; it had never been caught because only `--help` was ever run
  against a built bundle. The test suite now executes every bundle.
- the Stellar memo type was not stated anywhere, and sending that memo with the
  wrong type loses the payment. It is `MEMO_TEXT`, and the deposit block now
  says so.
- reusing an existing unpaid order, and asking for a coin that differs from it,
  both read as errors rather than as the ordinary situations they are
- nothing showed how long an order had left, and a real payment nearly missed
  its window

## What this means for a reader

Every finding above is closed, and the behaviours they produced are covered by
the test suite, which runs entirely offline against recorded fixtures. The full
list of what this tool refuses to do, and why, is in
[docs/safety.md](safety.md).

The detailed review transcripts are kept internally; they quote source from
private repositories and so are not published here. The findings themselves are
summarised above in full — nothing material is omitted.
