# skill-redteam-suite

An adversarial benchmark for skill reviewers. One question:

> **Can your reviewer be fooled by a package that looks complete but verifies nothing?**

Two probe packages, scored by the reviewer under test. The suite fails if the reviewer lets
either of them earn reproducible points — the dimension where "this verifies nothing" shows up.

## Probes

| Probe | What it fakes | What must happen |
|---|---|---|
| `shape` | A runnable-looking package: `tests/run_golden.py` prints `PASS` with **zero assertions**, demo prints one line, reference files are stubs | total must be below the pass line **and** reproducible points must be lost |
| `vacuity` | Formally complete, content empty: `若` decision table, ten `NEVER … 因为` rules that say nothing, two code fences, four stub references, `assert c == c` | reproducible points must be lost (its total may still pass — a structure score only sees shape) |

## Why the verdict looks at `reproducible`, not just total

A well-shaped fake reaches **88–92/100** even on our own ruler after two anti-gaming patches.
Total is a shape score. The dimension where an empty package cannot hide is `reproducible`:
does its runner assert anything, does its demo touch the package's own code.

## The control experiment (the suite must be able to fail)

| Reviewer | `shape` | `vacuity` | Verdict |
|---|---|---|---|
| lgd-skill-review v1.1.16 | 78 WARN · repro 11/20 | 88 PASS · repro 16/20 | ALL BLOCKED |
| same code, three anti-gaming checks disabled | 87 PASS · repro 20/20 | 92 PASS · repro 20/20 | **2 got through** |

The second row is not a bug — it is the proof that the suite discriminates. Without the
weakened copy, "all probes blocked" would only mean "the probes are easy".

## Usage

```bash
python run_suite.py --reviewer /path/to/review.py            # pass line 80 by default
python run_suite.py --reviewer /path/to/review.py --threshold 85 --keep
```

- The reviewer CLI must accept a package path and print `总分：N/100` (or `total: N/100`).
- If it also prints `reproducible N/20`, the key rule is checked directly; if not, the suite
  warns that the important part could not be verified.

Exit codes: `0` all probes blocked · `1` at least one got through · `2` bad usage.

## What it does not do

- It does not judge content quality — only whether obvious fakes are rejected.
- It does not ship a reviewer. You bring your own.
- Passing does not mean your reviewer is good. It means it is not fooled by these two.

## License

MIT. See [LICENSE](LICENSE).
