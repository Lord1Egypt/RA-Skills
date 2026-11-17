# Quantinuum Nexus: submitting real jobs

The Selene lane is free and offline. Nexus is the online lane — emulators with the vendor
error model and, with access, real H-series hardware. This card is the documented workflow
(Nexus user guide + `qnexus` 0.48.2 API reference) with field corrections attached. Where
the docs and hard-won experience disagree, the **verified** note wins and the conflict is
stated.

Account-layer concerns — quotas, roles, groups, priority, who can see your job — are in
`references/nexus-admin.md`. Read that before a shared-account or hackathon run.

## Login and project

```python
import qnexus as qnx

qnx.auth.login()                     # device-code flow; qnx.login() is the same call
project = qnx.projects.get_or_create(name="MyProject")
qnx.context.set_active_project(project)
```

Login persists across processes; do not re-prompt inside a sweep loop.

Verified mechanics (qnexus 0.48.2, headless sandbox):

- `qnx.auth.login()` prints a 6-char user code and a `verification_uri_complete`, tries
  `webbrowser.open` (a no-op headless — the link is printed anyway), then **blocks polling**
  until the user clicks "allow device". Run it in the background and tail the log, or the
  call eats the whole command timeout. There is no separate "poll later" entry point.
- Tokens land in **`~/.qnx/auth`** (`CONFIG.token_path`), *not* `~/.qnexus/`. The docs only
  say "clear tokens from the file system" without naming a path — this one is observed, not
  documented. On an ephemeral sandbox home it is wiped on rebuild; expect to redo the login.
- `qnx.auth.is_logged_in()` and `qnx.users.get_self()` are the cheap verification pair; the
  latter returns a `UserRef` with `id` and `display_name`.
- Non-interactive alternatives: `qnx.auth.login_no_interaction(user, pwd)` and
  `qnx.auth.login_with_token(refresh_token)` (in-memory, nothing written to disk — the right
  one for CI or multi-account use).
- Import gotcha: `qnexus` imports `selene_core`, so the environment also needs `guppylang`
  installed. `pip install qnexus` alone fails at import with
  `ModuleNotFoundError: No module named 'selene_core'`.

## Projects, properties and naming — make a sweep findable

A project name is unique **per creating user only**; another user's project can share your
name. Never identify a project by name alone across accounts — carry the `ProjectRef.id`.

Properties are Nexus's typed metadata, and they are the difference between a sweep you can
re-query in a month and a pile of anonymous jobs. Declare them on the project first, then
stamp them on every job:

```python
qnx.projects.add_property(name="gate",  property_type="string", project=project)
qnx.projects.add_property(name="shots", property_type="int",    project=project)
qnx.projects.add_property(name="seed",  property_type="int",    project=project, required=False)

with qnx.context.using_properties(gate="G16", shots=2048, seed=7):
    job = qnx.start_execute_job(...)      # properties merge in from context
```

- Only four types: `bool`, `int`, `float`, `string`. `required=True` makes the API reject a
  collaborator who omits the value.
- **Properties propagate**: a resource created by a job inherits the job's properties, so a
  stamped execute job yields a stamped result. This is free provenance — use it.
- Explicit `properties=` on a call beats the context value.
- `qnx.projects.summarize(project)` gives a one-shot DataFrame of the project's contents.
- Deletion is two-step: `qnx.projects.update(project, archive=True)` then
  `qnx.projects.delete(project)`.

**Stamp from the context, not from a per-call argument.** Wrap the whole submission —
upload, compile, execute, and the `save_ref` metadata write — in one
`using_properties(**axes)` block (`ExitStack` if you also enter `using_project`), and pass
no `properties=` downstream. Three things follow: every resource the submission creates
carries the same coordinate even on a partial retry; nothing downstream has to remember to
thread the axes through; and the metadata you persist locally can be read back out of
`qnx.context.get_active_properties()`, so the disk cache cannot disagree with what Nexus
actually stamped. Keep the explicit-argument path only as the older-client fallback, chosen
by whether `get_active_properties()` returns anything. Enter the context inside the
per-cell call so it exits on the way out — a context leaked past a failed submission stamps
the *next* cell with the failed cell's band.


## The compile → execute → download flow

Four steps, in order: **upload → compile → execute the compiled ref → download**.
Skipping the upload is the gap most copy-paste examples leave open — a local
`pytket.Circuit` is not submittable; `programs=` wants a Nexus ref.

```python
circuit_ref = qnx.circuits.upload(circuit, name="run-01-circ")   # -> CircuitRef

compile_job = qnx.start_compile_job(
    programs=[circuit_ref],
    backend_config=config,
    optimisation_level=2,            # 0 for gate-count benchmarks, 2 for cheapest run
    name="compile-run-01",
)
qnx.jobs.wait_for(compile_job)
compiled_ref = qnx.jobs.results(compile_job)[0].get_output()

exec_job = qnx.start_execute_job(
    programs=[compiled_ref],
    n_shots=[2048],
    backend_config=config,
    name="exec-run-01",
    max_cost=[20.0],                 # hard HQC ceiling — see "Cost control"
)
qnx.jobs.wait_for(exec_job)
result = qnx.jobs.results(exec_job)[0].download_result()
```

`programs=` is the current keyword on both `start_compile_job` and `start_execute_job`.
`circuits=` is its **deprecated** spelling: older examples and older agents still emit it,
and it surfaces as a deprecation warning or a schema error rather than a clean rename hint.
Always write `programs=`.

`qnx.compile(...)` and `qnx.execute(...)` are blocking convenience wrappers over the same
two `start_*` calls (`timeout=300.0` default) — fine for a one-off, wrong for a sweep, where
you want the ref so a resumed run can re-attach.

### Which result method — `get_output()` vs `download_result()`

The two job types return different ref classes and their accessors are **not**
interchangeable. This is the most common `AttributeError` on the stack:

| Job | `qnx.jobs.results(job)[0]` is | Accessor | Wrong call gives |
| --- | --- | --- | --- |
| compile | `CompilationResultRef` | `.get_output()` → the compiled `CircuitRef` | `CompilationResultRef has no attribute 'download_result'` |
| execute | `ExecutionResultRef` | `.download_result()` → `BackendResult` / `QsysResult` / `QIRResult`, then `.get_counts()` or `.get_empirical_distribution()` | `ExecutionResultRef has no attribute 'get_output'` |

Read the error as "wrong job type in hand", not "broken qnexus" — it almost always means a
compile ref and an execute ref got crossed in a resume or re-attach path.

### Pre-flight, before the first API call

Four checks, in order; each has a distinct failure signature and none of them is worth
debugging after submission:

1. **Interpreter** — run with the environment that actually holds `qnexus` (the project's
   `.pydeps`/venv binary, never bare system `python3`); otherwise
   `ModuleNotFoundError: No module named 'qnexus'`.
2. **Session** — `qnx.auth.is_logged_in()`; mint via device authorization if not.
3. **Active project** — resolve by name from `qnx.projects.get_all()` (with an explicit
   fallback name and a loud `RuntimeError` listing what *is* available) and call
   `qnx.context.set_active_project(project)`; otherwise `NoActiveProjectError` or a bare 403
   several calls later.
4. **Config family** — `QuantinuumConfig` for H-series, `HeliosConfig`/`HeliosEmulatorConfig`
   for Helios; the wrong family reads like an entitlement error (`code: 14`).

Notes and sharp edges:

- **Does the execute job require a prior compile?** The reference signature accepts a plain
  `CircuitRef` (or `HUGRRef`/`QIRRef`) and states no ordering rule. In practice, executing a
  ref that Nexus has not compiled for that backend fails with `entry not found in database`
  — a *wrong-ref* error, not "backend down". Compile first; treat the docs' permissiveness
  as untested.
- `qnx.jobs.get(id=…)` is **keyword-only** (confirmed by the published signature). Positional
  calls raise.
- Job/circuit refs carry `.id`; store that string in the per-row cache so a resumed sweep can
  re-attach to an in-flight job instead of resubmitting it.
- Up to **300 programs in a single job** — batch a sweep's cells rather than firing 300 jobs.
- `skip_intermediate_circuits=True` is the compile-job default; set it `False` only when you
  actually want per-pass circuits (`CompilationResultRef.get_passes()` → `CompilationPassRef`
  with `.pass_name`, `.get_input()`, `.get_output()`). That per-pass lineage is the honest way
  to show *what the compiler did*, and it is the Nexus analogue of the local TKET lane in
  `references/pytket.md`.

## Job lifecycle, waiting and recovery

`JobStatusEnum` in full: `SUBMITTED`, `QUEUED`, `RUNNING`, `RETRYING`, `CANCELLING`,
`COMPLETED`, `CANCELLED`, `ERROR`, `TERMINATED`, `DEPLETED`.

`DEPLETED` means the allowance ran out mid-job. It is a distinct outcome from `ERROR` and
must be reported as such — the circuit was fine, the budget was not.

```python
qnx.jobs.status(job).status
qnx.jobs.wait_for(job, timeout=3600)          # raises JobError on ERROR/CANCELLED/DEPLETED/TERMINATED
qnx.jobs.cancel(job)
qnx.jobs.retry_submission(job)                # retries ERROR items by default
```

`wait_for` takes a `strategy`: `WebsocketStrategy` (jobs under ~10 min), `PollingStrategy`
(exponential backoff, robust for long jobs), `HybridStrategy` (websocket then polling — the
recommended default). A long hardware job on a bare websocket is how you lose a run to a
dropped connection, so pass `HybridStrategy` or `PollingStrategy` explicitly for anything
queued behind other users.

**Never resubmit to get a past result.** Query it:

```python
rows = qnx.jobs.get_all(
    project=project,
    properties={"gate": "G16"},
    job_status=[qnx.jobs.JobStatusEnum.COMPLETED],
    page_size=50,
).df()
job = qnx.jobs.get(id="…")
res = qnx.jobs.results(job)[0].download_result()
```

`get_all` filters on project, properties, `job_status`, `job_type`, creator, created/modified
windows, and paginates. `allow_incomplete=True` on `jobs.results` returns
`IncompleteJobItemRef` placeholders for a partially finished batch instead of raising.

### Resuming a paid-for sweep

Wrap that query in a command rather than an ad-hoc script — a sweep loses its process often
enough (rollback, dropped websocket, sandbox timeout) that recovery has to be a one-liner or
it turns into a resubmission. This repo's is `python -m quantum.resume`:

```bash
python -m quantum.resume --backend hardware --job-id exec-1 exec-2   # ids in hand
python -m quantum.resume --backend hardware --from-dump demos/x.json # ids in a dump
python -m quantum.resume --backend hardware --gate G16               # no ids at all
```

Design points worth copying:

- **Recover the decode width from the job, not from memory.** The `n_qubits` property stamped
  at submission is what makes a job re-decodable months later; without it you are guessing at
  the bit width of a result you already paid for.
- **Report a non-COMPLETED job, don't raise on it.** One `DEPLETED` id must not abandon the
  other nine. Map the status to a plain-English reason (`DEPLETED` = budget, `ERROR` =
  retryable, `QUEUED` = come back later).
- **Keep the billed HQC in the meter.** A re-fetch has no local estimate (no program in hand),
  but it still has a real cost from `qnx.jobs.cost(job)`. Dropping it makes a resumed sweep
  look free, which is how a run's true cost gets lost.
- **Cache the shots on disk keyed by job id**, so the second resume is a file read and the
  driver's row loop can consume it exactly like a locally executed row.



## Cost control — the only real spend guard

Nexus quotas do **not** cover hardware. `check_quota` passing says nothing about whether you
can afford an H-series job (see `references/nexus-admin.md`). Three real controls:

| Call | When | What it gives |
| --- | --- | --- |
| `qnx.circuits.cost(ref, n_shots, backend_config)` | before submitting | HQC estimate — **runs a costing job** on a dedicated device and shows up in the portal |
| `max_cost=[…]` on `start_execute_job` | at submission | per-job-item HQC ceiling; the job stops rather than overspends |
| `qnx.jobs.cost(job)` / `cost_confidence(job)` | after | actual HQC, and per-item (cost, confidence) pairs |

`QuantinuumConfig.max_cost` is **deprecated** — pass `max_cost` as an execute-job parameter
instead. `max_batch_cost` still lives on the config for batched submissions.

A local formula (`5 + n_shots·(2q + 1q/10)/5000`) is fine for planning the shape of a sweep,
but never quote it as *the* cost in a write-up when `qnx.jobs.cost` can give the real number.

Record it per job rather than recomputing it later. One meter record per job — mode
(`emulator | dry | live | refetch`), device, job id, qubits, shots, seed, estimated HQC, billed
HQC — collected into the dump's `execution` block is what turns a dry-run vs live-run comparison
into a diff instead of an argument. A re-fetched job has no estimate (there is no program in
hand) but it still has a real billed cost; carry it, or a resumed sweep reports itself as free.
See `references/sweep-runner.md` (§Per-job meters).



## Backend matrix (what is actually reachable)

Read the widths off the account's backends page, not the datasheet: the number a hosted
emulator exposes is its own ceiling. On an emulator-only account (observed 2026-08-23)
`H2-Emulator` advertises **26 qubits** even though H2-1 is a 56-qubit machine, and
`Helios-1E-lite` advertises 26 against a 98-qubit Helios-1. Pinning the published width
lets a 30-qubit circuit sail through preflight and get rejected by Nexus.

| Backend | Qubits (observed) | Config | Noise | Notes |
| --- | --- | --- | --- | --- |
| `H1-1LE` | 20 | `QuantinuumConfig` | noiseless | cheap sanity leg |
| `H1-Emulator` | 20 | `QuantinuumConfig` | full error model | H1-class |
| `H2-1LE` | 26 | `QuantinuumConfig` | noiseless | the default "real stack, no noise" leg |
| `H2-Emulator` | 26 | `QuantinuumConfig(..., noisy_simulation=True)` | full error model | the noise-ladder workhorse |
| `Helios-1E-lite` | 26 | **`HeliosConfig`** | emulated | passing `QuantinuumConfig` here fails |
| `aer_simulator`, `_statevector`, `_unitary` | 26 | `AerConfig` | ideal | Nexus-hosted Qiskit — the independent-simulator leg, no local install |
| `QulacsBackend` | 20 | `QulacsConfig` | ideal | second independent simulator |
| `Selene`, `SelenePlus` | 26 | `SeleneConfig` / `SelenePlusConfig` | ideal + configurable | the local emulator, submitted remotely |
| `H1-1`, `H2-1`, `H2-1SC` (real QPU) | — | — | — | not listed on a plain account; no submission surface |

The config class is a *family* property, and the families are not interchangeable. A name
submitted through the wrong class is accepted at job creation and refused at submission with
`You do not have access to this machine (code: 14)` — an access error for a typing mistake.
Switch on the family (`H1-`/`H2-` → `QuantinuumConfig`, `Helios*` → `HeliosConfig`, `aer*` →
`AerConfig`, Qulacs/Selene → their own), and print the reachable list grouped by family so the
fix is visible in the error itself.

Only score a circuit's gate set against the H-series native set for H-series and Helios
backends. Aer/Qulacs/Selene do not rebase onto `PhasedX/Rz/ZZPhase/ZZMax`, so applying that
check there refuses ops the backend runs perfectly well — leave the gate check unknown and
skipped instead.

`QuantinuumConfig` defaults worth knowing: `noisy_simulation=True` (so an "emulator" is noisy
unless you say otherwise), `no_opt=True`, `allow_implicit_swaps=True`, `leakage_detection=False`.
Turn `leakage_detection` on when the experiment cares about leakage, and remember it changes
the shot record.

`SeleneConfig` / `SelenePlusConfig` expose the same simulator and error-model taxonomy as the
local lane (`Statevector`, `Stabilizer`, `MatrixProductState`, `Coinflip`, `ClassicalReplay`;
`NoErrorModel`, `DepolarizingErrorModel`, `QSystemErrorModel`, `HeliosCustomErrorModel`), so a
Selene experiment can be lifted onto Nexus without rewriting the noise ladder. `n_qubits` on
those configs is **deprecated** — pass it per job item on the execute call.

## The Helios lane

`Helios-1E-lite` runs fine on an emulator-only account. It fails in four distinct ways first,
and only the first one *looks* like an entitlement problem:

1. **`system_name` defaults to the QPU.** `HeliosConfig()` is `system_name="Helios-1"` — the
   hardware system. Submitting the bare config asks for a machine you have no entitlement for
   and is refused at *submission* with
   `You do not have access to this machine (code: 14)`. Pass the device explicitly:

   ```python
   from quantinuum_schemas.models.backend_config import HeliosEmulatorConfig
   config = qnx.HeliosConfig(
       system_name="Helios-1E-lite",
       emulator_config=HeliosEmulatorConfig(n_qubits=n_qubits),
   )
   ```

2. **Emulation requires an `emulator_config`.** Without one, job creation fails with HTTP 400
   `"Helios emulation must have an emulator_config set."`
3. **`n_qubits` must be explicit per job item.** Missing it gives HTTP 400
   `"max-qubits/n_qubits must currently be set explicitly per job item."` The schema defaults
   (statevector simulator, QSystem `alpha` error model, Helios runtime) are the
   vendor-realistic lane.
4. **Helios takes HUGR, not pytket, and does not compile.** Upload the Guppy program with
   `qnx.hugr.upload(...)` and execute the returned ref directly — `start_compile_job` only
   accepts source circuits, so skip it entirely for this target (the same is true of the
   `*LE` backends). A gate-set preflight must whitelist HUGR runtime/extension ops
   (`QAlloc`, `QFree`, `Measure`, `MeasureFree`, `Reset`, `helios.*`) or it will reject a
   perfectly valid program.
5. **Results are `QsysResult`, not `BackendResult`.** Helios returns
   `hugr.qsystem.result.QsysResult` — Guppy-style tagged entries per shot, with no
   `get_shots` and no `get_empirical_distribution`. Decode `result.results[i].entries`.

**Listed is not reachable — but check your own config before blaming the account.** A backend
that appears in `get_all()` can still fail at submission with
`Submission error: You do not have access to this machine (code: 14)`. That message is
*sometimes* a real entitlement gap and *often* a client-side field you never set (the Helios
`system_name` above is the canonical case). Diff the config class and every name field against
the device you meant before writing "unreachable" into a results table. When it genuinely is an
access gap, the failure arrives on the *execute job*, after upload and after the job id exists,
so a sweep must catch it per cell, keep the ids, and carry on: one inaccessible machine must
not cost you the lanes that worked. Report the lane with its real error rather than shipping a
three-engine table as a four-engine one.


Always confirm against the live account rather than this table:

```python
print(qnx.devices.get_all().df()[["backend_name", "device_name", "nexus_hosted"]])
```


## Sizing: the timeout cliff

Noisy emulator jobs are the expensive ones. Observed ceiling: **≤ ~17 qubits AND/OR ≤ 2048
shots**. A 25-qubit × 8192-shot noisy job sat in `RUNNING` for ~3 h and then raised
`TimeoutError` — no partial result, no refund of wall-clock. Noiseless backends are far more
forgiving. Plan the qubit budget before submitting, and split a wide experiment into several
narrow jobs rather than one wide one (up to 300 programs per job).

There is a second, sharper ceiling on the hosted Selene lane, and it is about
**depth**, not width. `SelenePlus` (MPS simulator + `HeliosRuntime` +
`QSystemErrorModel`) runs 17-qubit *plain* circuits fine, but 17 qubits with
Toffoli/CSWAP depth dies with `Unexpected end of stream` — reproducibly, across
three different circuit structures. That is a server-side size limit, not a
circuit bug and not a transport glitch: do not spend a debugging session
bisecting your kernel over it. Record the affected leg as **assessed-blocked**
with the error string and re-certify on a backend that takes the depth
(`H2-Emulator` carried the equivalent 17q run), rather than leaving the row
looking untried.

Two naming traps in the same lane: `SelenePlus` accepting `HeliosRuntime` is an
**emulator** capability and never "ran on Helios", and `QulacsBackend`
(verified with a 14q GHZ giving correct physics) is a fast CPU statevector via
pytket — also an emulator. Both share a prefix or a runtime name with something
that sounds like hardware.


## Bit order — calibrate before you trust anything

`download_result()` returns a pytket `BackendResult` / `QsysResult` / `QIRResult`; the counts
and distribution accessors belong to **pytket**, not qnexus, and the Nexus docs say nothing
about them. Observed on a live H2-1LE run: `get_distribution()` is deprecated in favour of
`get_empirical_distribution()` / `get_probability_distribution()`, and the returned dict is
keyed by **tuples of ints**, indexed by qubit:

```python
for key, p in dist.items():
    assert key[8] == 0          # int 0, NOT the string "0"
```

`key[q]` is qubit `q` in circuit order. Qiskit bitstrings are the **reverse** convention
(`k[0]` is the MSB), so any analysis ported from a Qiskit notebook is wrong by a mirror until
proven otherwise.

**Calibration probe**: submit a tiny job that applies `X` to exactly one known qubit and
measures all, then assert the returned key has the 1 in the expected slot. Do this once per
backend, per shape change. It costs seconds and catches the single most expensive class of
silent bug.

**Smell test after any post-selection**: a post-selected/error-detected fidelity can never
exceed the ideal noiseless value. If `F_det > F_ideal`, the bit order or the accept mask is
wrong — do not report the number.

`ExecutionResultRef.download_backend_info()` returns the pytket `BackendInfo` snapshot that
was in force for that run. Pull it alongside the result: it is the calibration provenance
for the number you are about to publish.

## Job-failure taxonomy

| Symptom | Cause | Fix |
| --- | --- | --- |
| `entry not found in database` | executed a non-compiled ref | execute the compiled ref |
| `TimeoutError` after hours in `RUNNING` | oversized noisy job | cut qubits or shots |
| status `DEPLETED` | allowance exhausted mid-job | budget/quota, not a circuit bug — report as such |
| status `ERROR` | transient or real | `qnx.jobs.retry_submission(job)` once; investigate if it repeats |
| backend/config mismatch error on Helios | `QuantinuumConfig` used | switch to `HeliosConfig` |
| `access to this machine (code: 14)` on `Helios-1E-lite` | `HeliosConfig()` defaulted to `system_name="Helios-1"` | pass `system_name=<device>` explicitly |
| 400 `Helios emulation must have an emulator_config set` | no `emulator_config` | `HeliosEmulatorConfig(n_qubits=N)` |
| 400 `max-qubits/n_qubits must ... be set explicitly per job item` | `n_qubits` omitted | set it on the emulator config / job item |
| `QsysResult has no attribute get_empirical_distribution` | Helios/HUGR lane | decode `result.results[i].entries` |
| `jobs.get()` TypeError | positional id | `jobs.get(id=…)` |
| `ModuleNotFoundError: No module named 'qnexus'` | ran under system python, not the env holding `qnexus` | invoke the `.pydeps`/venv interpreter explicitly |
| `NoActiveProjectError` / bare 403 on a valid session | no active project in context | resolve from `qnx.projects.get_all()`, then `qnx.context.set_active_project(project)` |
| `ExecutionResultRef has no attribute 'get_output'` | compile accessor on an execute job | `download_result()` — see "Which result method" |
| deprecation/schema error naming `circuits` | old keyword | `programs=[...]` |
| distribution keys compare false against `"0"` | keys are int tuples | compare against ints |
| job queued far longer than a colleague's | lower priority (1–10, default 5) | admin-set; see `nexus-admin.md` |

## Reporting discipline

Every Nexus number in a write-up carries: backend name, shot count, seed, job id, actual HQC
cost from `qnx.jobs.cost`, and the date. Timeouts, cancellations, `DEPLETED` and reverts get
recorded with their cause — an honest failed leg is evidence; a quietly dropped one is a
fabrication. See `references/cross-platform-validation.md` for how the Nexus leg fits into a
multi-leg proof.

## Submit-time persistence

The dangerous window in a cloud sweep is between "Nexus accepted the job" and "shots came
back". If the process dies in it, the job still runs and is still billed, but nothing local
knows its id — the result exists only in the web console, and the next run pays for the same
cell again. Close the window by persisting the id the moment it exists:

```python
def run(self, program, *, n_shots, seed, on_submit=None, **props):
    ref = qnx.start_execute_job(..., max_cost=[...])
    if on_submit is not None:
        on_submit(str(ref.id))          # driver writes the cache row here
    ...
```

and in the driver:

```python
def _submitted(job_id: str) -> None:
    write_row(tag, {"status": "submitted", "job_id": job_id,
                    "band": K, "noise_scale": scale})

row = read_row(tag)
if row and row.get("job_id"):
    shots = backend.fetch_result(row["job_id"])   # re-attach, never resubmit
else:
    shots = backend.run(program, ..., on_submit=_submitted)
```

Rule: **a cell that has a job id is never a cell to submit.** The loop's first action is
re-attachment, submission is the fallback.

### Save the `Ref`, not just the id

An id string only recovers the job while `qnx.jobs.get(id=...)` still resolves it — live
session, right active project, compatible client. `qnx.filesystem.save` persists the `Ref`
object itself and is the documented durability path:

```python
job_id = str(exec_job.id)
qnx.filesystem.save(ref=exec_job, path=store / f"{job_id}.execute.ref.json", mkdir=True)
# ... and a sidecar of your own, so recovery knows the decode width and the
# sweep coordinates without a network round-trip:
(store / f"{job_id}.meta.json").write_text(json.dumps(
    {"job_id": job_id, "n_qubits": n, "shots": s, "gate": g, "band": K, "noise_scale": x}))
```

Then make recovery prefer it: `get_job()` tries `qnx.filesystem.load(path=...)` first and
falls back to `jobs.get`, and the resume CLI treats the ref store as an id source of last
resort — so a sweep whose dump never got written is still recoverable from disk alone.
Wrap every write: a failure to persist must never take down a job Nexus has already
accepted and billed. The refs are session artefacts — gitignore them; the committed
evidence stays the dump's `execution` block.

Reference implementation: `quantum/nexus_refs.py`, saved from `NexusBackend._submit`
before `on_submit` fires, consumed by `quantum/resume.py --from-refs`.

## Stamp the sweep coordinates

`device / shots / seed / driver / n_qubits` identify a *run*. They do not identify which cell
of the sweep it measured. Declare the sweep axes in the property schema too:

```python
JOB_PROPERTIES = (
    ("gate", "string"), ("driver", "string"),
    ("n_qubits", "int"), ("shots", "int"), ("seed", "int"),
    # Sweep coordinates. Without these a recovered job cannot be mapped back to
    # the cell it measured, and the only options left are guessing from
    # submission order or paying for the row again.
    ("band", "int"), ("noise_scale", "float"),
)
```

Recovering ten unstamped jobs and matching them to an ideal success curve *looks* like
analysis and is guessing. Add the axes before the sweep, not after the loss.

## Filter EXECUTE before reading results

`qnx.jobs.get_all(project=…, properties=…)` returns the COMPILE jobs alongside the EXECUTE
jobs that consumed them. Reading result fields off a compile row raises `AttributeError`:

```python
jobs = [j for j in qnx.jobs.get_all(project=proj, properties=props).list()
        if j.job_type == qnx.models.JobType.EXECUTE]
band = job.annotations.properties.get("band")   # stamped props live here
```

## Device login

The device-authorization path drifts between `qnexus` releases — `/device/authorize` answers
`{"detail":"Not Found"}`; the working path at the time of writing is
`/device/device_authorization`. Read it out of the installed `qnexus.client.auth` rather than
a remembered URL, then poll `/device/token` until the user approves and `write_token` the
refresh/access pair.

Run the poller **in the background** (`nohup … &`, print the code from its log). A foreground
poller races the command timeout and dies while the user is still on the approval screen, and
the code it printed is then dead too.
