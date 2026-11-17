# Parameter sweeps: `SweepSpec` + `SweepRunner`

`quantum/sweep.py` factors the temp-file render / import / compile / run loop into a reusable object. Use it for any new experiment that sweeps a parameter grid; hand-rolled loops should only survive for legacy parity checks.

## Shape

```python
from quantum.sweep import SweepSpec, SweepRunner

def template(p: dict) -> str:
    return f"""
from quantum.nadarasa_g1_lib import guppy, qubit, h, rz, angle, measure, result, cphase_h
@guppy
def program() -> None:
    # ... bake p["s"], p["N"], p["n"] into source ...
"""

spec = SweepSpec(
    name="g1_via_sweep",
    params=[{"s": s, "N": 16, "n": 4} for s in range(16)],
    template=template,
    n_qubits=lambda p: p["n"] + 1,
    post=lambda shots, p: {"s": p["s"], "histogram": ...},
    shots=200,
)
result = SweepRunner().run(spec)   # -> SweepResult(rows=[...], elapsed_sec, shots_per_row)
```

`SweepRunner` owns:
- `tempfile` rendering under `selene_sweep_progs/`
- `importlib.util` import with `sys.path.insert(0, ROOT)`
- unique module names via `uuid.uuid4().hex[:6]`
- execution through the Guppy v1 emulator builder (`quantum/emulate.py` shim: `build(mod.program)` + `runner.run_shots(Quest(), ...)`)
- per-shot `(label, value)` → `dict[str, int]` flattening

The driver only writes `template`, `n_qubits`, and `post`.

## Rules

1. **One stable `*_lib.py` per experiment family.** Templates `import` helpers by name; never inline `@guppy` helpers into the rendered source (same rule as `driver-pattern.md`).
2. **`post` is pure host code.** Use `Counter`, NumPy, etc. — anything heavy goes here, not inside the kernel.
3. **`SweepResult.rows` is the JSON.** Dump `dataclasses.asdict(result)` straight to `src/data/demos/<name>.json` and render via the `selene_run` schema (`references/selene-run-schema.md`).

## Parity check pattern

When migrating an existing hand-rolled driver to `SweepRunner`, keep the original around and assert the headline metrics are byte-identical modulo timestamps. `quantum/nadarasa_g1_via_sweep.py` is the canonical example — it reproduces `src/data/demos/nadarasa_g1.json` peak positions and per-slope shot histograms exactly.

## When NOT to use it

- Single-shot one-off experiments — a direct `program.emulator(...)` call is fine.
- Anything where the kernel structure changes per row (different qubit counts AND different gate topology). `SweepRunner` handles per-row `n_qubits` but assumes a single `template` callable; branching topologies belong in separate sweeps.

## Resumable sweeps

Long Selene sweeps blow past sandbox / CI timeouts (typically 10 minutes). A single interrupted run must not discard completed cells — cache each row to disk **before** moving to the next, and drive the sweep from an outer resume loop.

### Per-row cache pattern

```python
CACHE = Path("_cache_2q_noise")
CACHE.mkdir(exist_ok=True)

for conj_i, conj in enumerate(conjectures):
    for level in noise_levels:
        tag = f"conj_{conj_i}_s{shots}_g{grid}_p{level:.4f}"
        out = CACHE / f"{tag}.json"
        if out.exists():
            continue                                # already done, skip
        row = run_one(conj, level, shots, grid)     # the expensive call
        out.write_text(json.dumps(row))             # commit before next iter
```

Rules:

1. **Filename must fully identify the row.** Include every sweep axis, plus `shots` and `grid`, so a partial cache from a different parameter set is never silently reused.
2. **Write atomically after the shots complete**, not before — a half-written row is worse than a missing one.
3. **Skip on `exists()`**, don't diff timestamps. Re-invocation should be a pure no-op for finished cells.
4. **Finalize step** at the end of the driver: once `len(list(CACHE.iterdir())) == expected_total`, merge cache files into a single `src/data/demos/<experiment>.json` and delete `CACHE`. Never ship the cache dir itself to the frontend.

### Outer resume loop

Run the driver under a shorter-than-sandbox timeout in a bash `while` loop until the cache is full:

```bash
TOTAL=50
while [ "$(ls _cache_2q_noise 2>/dev/null | wc -l)" -lt "$TOTAL" ]; do
  PYTHONPATH=.pydeps PYTHONUNBUFFERED=1 \
    timeout 580 python3 -m quantum.pqp_frontier.noise_2q || true
done
```

`|| true` keeps the loop alive across SIGTERM from `timeout`. The driver's `if out.exists(): continue` guard makes each restart cheap.

### When to skip

One-off experiments with < ~120 s wall time don't need a cache — a single `timeout 580 python -m ...` invocation is enough. The cache pattern is for anything that could plausibly need more than one sandbox turn to finish.

## Per-job meters

The per-row cache answers "which cells finished". It does not answer "what did this cost, on what device, with which seed" — and on a paid lane that second question is the one you cannot reconstruct afterwards. Emit **one uniform meter record per job**, from every lane, and collect them into the dump's `execution` block.

`quantum/backends.py` builds them:

```python
from quantum.backends import job_meter, meter_totals, meters_table

job_meter(
    mode="live",              # emulator | dry | live | refetch
    device="H2-1LE",
    n_qubits=6, shots=512, seed=17,
    gate="G16", driver="qpde.sweep",
    estimated_hqc=5.0384,     # None on lanes that never estimate
    hqc_cost=5.11,            # None until actually billed
    max_cost_hqc=25.0, user_group="…", submitted_at="…",
)
```

Rules that make the records worth having:

1. **`None` means "this lane genuinely has no such value", never "unknown".** An emulator row has no `estimated_hqc`; a re-fetched row has no estimate either (there is no program in hand) but it *does* have a real `hqc_cost` from `qnx.jobs.cost(job)`. Conflating the two is how a resumed sweep starts reporting itself as free.
2. **Derive `cost_delta` / `cost_ratio` at write time**, not at read time, so a shipped JSON answers "was the estimate honest?" without arithmetic in the frontend. Both stay `None` unless the job was billed.
3. **Collect globally, not per driver.** `quantum.emulate` accumulates whatever the active backend recorded, and `SweepRunner.execution()` defaults `meters=` to that collection — so a driver gets the figures in its dump without plumbing anything. `meters_table(...)` prints the same records as a console table for a dry-run vs live-run diff.

## Resuming a paid hardware sweep

A sweep loses its process more often than you'd like (rollback, dropped websocket, sandbox timeout). Nexus has still finished those jobs and still billed them, so recovery must be a re-attach, never a resubmission. Fetch the jobs into the resume cache first:

```bash
python -m quantum.resume --backend hardware --job-id exec-1 exec-2
python -m quantum.resume --backend hardware --from-dump src/data/demos/x.json
python -m quantum.resume --backend hardware --gate G16 --dry-run
```

Then hand them to the runner:

```python
SweepRunner(resume_from="G16")              # gate label → load_sweep(gate=…)
SweepRunner(resume_from=["exec-1", "exec-2"])  # explicit ids, oldest first
```

Each row consumes the next cached job's shots instead of executing; once the queue empties, rows fall through to normal execution, so a half-finished sweep completes without re-buying the finished part. `execution()` prepends the resumed jobs' meters and their ids, so the dump still reports the original run's true cost.

Four details make a resume work months later:

1. **Recover the decode width from the job**, via the `n_qubits` property stamped at submission — not from a constant in the driver, which will have moved on.
2. **Report a non-`COMPLETED` job and skip it.** One `DEPLETED` id must not abandon the other nine; map the status to a plain reason (budget / retryable / still queued).
3. **Keep the billed HQC in the meter** even though the re-fetch has no estimate.
4. **Cache shots + properties + meter on disk by job id**, so the second resume is a file read and the row loop consumes it exactly like a locally executed row.

An unknown id must fail loudly with the command that would fix it, rather than silently executing the row and buying the shots a second time.


## Cloud rows have three states, not two

A local row is either cached or absent. A cloud row is `submitted` (job id, no shots yet),
`completed` (shots present), or `error` (guard rejection, dry-run stub, transient failure) —
and the three demand different handling on resume:

| State | Resume action |
| --- | --- |
| `completed` | skip |
| `submitted` | `fetch_result(job_id)` — already billed, never resubmit |
| `error` / dry-run stub | **purge before resuming**, then treat as absent |

The purge step matters: a dry-run stub or a hardware-guard rejection cached as a row makes the
sweep look finished at rows that were never executed. Delete them explicitly at the start of a
resume rather than letting the "row exists" check swallow them.

Two failure modes that only show up on a real paid sweep:

- **A driver that reads an env flag but not `--execute` submits nothing while reporting
  progress.** Make the live/dry switch a single explicit argument the driver logs on startup.
- **Background workers survive a session loss.** They keep looping against a dead token,
  re-submitting or spinning. Kill them *first* in any recovery — see
  `references/lovable-orchestration.md` (§Sandbox-reset recovery).
