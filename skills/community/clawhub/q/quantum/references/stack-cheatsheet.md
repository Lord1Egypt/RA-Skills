# Unified stack cheat sheet — primitive → workflow stage

One table per library, built from the crawled corpus (`quantum/docs_crawler/`),
mapping each core primitive onto the stage of *our* pipeline where it belongs.

Status column: **use** = called somewhere in `quantum/` today · **open** =
documented, applicable, not adopted · **n/a** = documented but out of scope here.

Pipeline spine:

```text
model → kernel → compile → verify → execute → recover → analyse → publish
```

## Guppy — the kernel stage

`guppylang>=1.0`. 257 doc pages, 377 snippets, **zero drift** (everything we call
is documented).

| Primitive | What it does | Our stage | Status |
| --- | --- | --- | --- |
| `@guppy` on a module-level function | the kernel itself; source is read via `inspect.getsource`, so it must live in a real `.py` file | kernel | use |
| `angle(x)` | rotation in **halfturns**; divide any explicit π out of a paper formula first | kernel | use |
| `measure(q).read()` / `measure_array` | v1 measurement; returns a `Measurement`, not a bool | kernel | use |
| `output(...)` | v1 result emission (was `result`) | kernel | use |
| `qubit()`, `discard`, `array` | allocation and cleanup; `discard` after `measure` aborts the QIR lane | kernel | use |
| `guppylang.std.qsystem` (`phased_x`, `rz`, `zz_phase`, `zz_max`) | native H-series gate set, halfturns, one-to-one with pytket natives | compile/kernel | use |
| `guppy.load_pytket` | drop a compiled pytket circuit straight into a kernel | compile → kernel bridge | **open** |
| `guppy.nat_var` / `type_var` / `type_alias` | width-generic kernels; would collapse our per-n kernel factories into one definition | kernel | **open** |
| `guppy.struct` | typed record passed through a kernel | kernel | open |
| `guppy.comptime` | compile-time evaluation of host values | kernel | open |
| `guppy.overload` | one name, several signatures | kernel | open |

Next: `references/guppy-language.md`, `references/guppy-v1-migration.md`,
`references/driver-pattern.md`.

## pytket — the compile and verify stages

Richest snippet source in the corpus (750 blocks from 28 user-guide pages), zero
drift on what we call.

| Primitive | What it does | Our stage | Status |
| --- | --- | --- | --- |
| `QuantinuumBackend(device_name, api_handler=QuantinuumAPIOffline())` | offline compile to H-series natives — no credentials, no HQCs | compile | use |
| `get_compiled_circuit(c, optimisation_level=0|1|2)` | the independent check on a rewriter's 2q count | compile | use |
| `add_blank_wires` | re-pad dropped idle wires; without it a TVD reads 1.0 | verify | use |
| `Circuit.get_unitary()` | dense oracle; compare global-phase-free at 1e-9 | verify | use |
| `Ry/Rz/ZZPhase` params | halfturns, same as Guppy `angle()` — never multiply by π | kernel/compile | use |
| `compare_unitaries` / `compare_statevectors` | vendor's own equivalence oracle, a second opinion beside ours | verify | **open** |
| `Backend.get_operator_expectation_value` | expectation of a `QubitPauliOperator` end-to-end | analyse | **open** |
| `pytket.utils.expectation_from_counts / _shots` | expectation from raw shot tables — replaces our hand arithmetic | analyse | **open** |
| `partition.measurement_reduction` | groups commuting Pauli terms into measurement circuits | analyse | **open** |
| `pytket-qir`, `qircheck` | QIR emission and static validation | publish (restricted) | use |

Never score approximation families (AQFT band truncation) with a compiler: a
correctness-preserving pass cannot find them. Next: `references/pytket.md`,
`references/qir-lane.md`.

## Selene — the local execute stage

106 doc pages but only 39 snippets: most pages are autodoc stubs, so the corpus
is thin here and our own `quantum/emulate.py` is the better reference.

| Primitive | What it does | Our stage | Status |
| --- | --- | --- | --- |
| `program.emulator(n_qubits=…).with_shots(…).with_simulator(Quest()).with_error_model(…).with_seed(…).run()` | the v1 execution path; pass the `@guppy` program, never `.compile()` | execute | use |
| `selene_sim.build(...)` | our entry point behind the legacy `run_shots` shim — **undocumented in any snippet** | execute | use (drift) |
| `IdealErrorModel` / `DepolarizingErrorModel` / `SimpleLeakageErrorModel` | the only noise models that ship; no coherent/T1-T2 model exists | execute | use |
| `OptimizationLevel.Classical` | pin it for gate-count benchmarks — v1 optimises on compile | compile | use |
| `shot.entries` | per-shot decode | analyse | use |
| `selene_sim.result_handling.parse_shot` + `hugr.qsystem.result` | the documented structured-result path we hand-roll | analyse | **open** |
| `selene_sim.event_hooks` | runtime instrumentation hooks | execute | open |
| `SelenePlusConfig` (via Nexus) | hosted Selene, for cross-checking a local sweep | execute | **open** |

Next: `references/selene-runtime.md`, `references/sweep-runner.md`.

## qnexus — the cloud execute and recover stages

The drift list here is exactly our cost-guard and resume surface: `HeliosConfig`,
`auth.login` / `login_with_token` / `is_logged_in`, `devices.get_all`,
`jobs.HybridStrategy`, `jobs.cost`, `jobs.get`, `users.get_self`. Undocumented is
not unsupported — it is unversioned. Pin `qnexus` and keep them behind
`tests/fake_qnexus.py`.

| Primitive | What it does | Our stage | Status |
| --- | --- | --- | --- |
| device-authorization login (`/device/device_authorization`) | session mint; read the path out of the installed `qnexus.client.auth`, poll in the background | execute | use |
| `projects.get_or_create` / `add_property(name, property_type=…)` | typed provenance schema; properties propagate onto every resource a job creates | execute | use |
| `qnx.context.using_properties(...)` / `get_active_properties()` | wrap the whole submission (upload + compile + execute + local `save_ref` metadata) in one block and pass no `properties=`; read back what Nexus will stamp so the disk cache can't disagree | execute | use |
| `QuantinuumConfig` / `HeliosConfig(system_name=…, emulator_config=…)` / `AerConfig` / `QulacsConfig` / `SeleneConfig` | config class is a **family** property; the wrong one fails as `code: 14`, which reads like an entitlement error | execute | use |
| `qnx.projects.get_all()` → `qnx.context.set_active_project(...)` | pre-flight: resolve the project by name and set it before any other call, or later calls fail as `NoActiveProjectError`/403 | execute | use |
| `qnx.circuits.upload(circuit, name=…)` → `CircuitRef` | the missing first step: `programs=` takes a Nexus ref, never a local `pytket.Circuit` (`circuits=` is the deprecated keyword) | execute | use |
| `start_compile_job(optimisation_level=…)` → execute the **compiled** ref | Nexus refuses to execute an uncompiled ref (Helios/`*LE` take HUGR directly instead); compile results use `.get_output()`, execute results use `.download_result()` — not interchangeable | execute | use |
| `download_result().get_empirical_distribution()` | int-tuple keys indexed by qubit; calibrate with a one-gate X-probe before trusting bit order | analyse | use |
| `QsysResult.results[i].entries` | Helios/HUGR decode — no `get_empirical_distribution` | analyse | use |
| `qnx.filesystem.save` + our `save_ref`/`verify_ref` | persist the job `Ref` at submit time, then checksum it: `schema`/`ref_sha256`/`ref_bytes` plus a self-excluding `meta_sha256`. `resume` verifies by default and skips (never guesses) a failing record; absent sidecar = `unverifiable`, pre-schema = `legacy` (upgrade with `--restamp`) | recover | use (`quantum/nexus_refs.py`) |
| `devices.supports_shots(config)` | pre-submission capability probe; a distribution-only backend takes the job and returns results a shot decoder can't read | execute | use (`_check_supports_shots`) |
| `max_cost=[…]` on `start_execute_job` | the only real *server-side* spend guard, and it is **per job** — quotas do not cover hardware at all | execute | use |
| client-side spend ledger | batch circuit breaker `max_cost` cannot be: estimate booked at submit time, next cell refused past `NADARASA_MAX_TOTAL_HQC` | execute | use (`quantum/backends.py: SpendLedger`) |
| `circuits.cost(...)` / `jobs.cost(job)` | pre-estimate (itself billable — keep behind `NADARASA_COST_PROBE=1`) and the real billed figure to report | publish | use |

| `jobs.get_all(project=…, properties=…, job_status=[…])` | re-attach a lost sweep; filter `job_type == EXECUTE` and read `annotations.properties` | recover | use |
| `jobs.results(job, allow_incomplete=True)` | harvest a partially finished batch after a reset | recover | **open** |
| `qnx.filesystem.save/load` | persist a job `Ref` to disk — the documented submit-time durability path | recover | **use** (`quantum/nexus_refs.py`) |
| `retry_submission(retry_status=…, remote_retry_strategy=FULL_RESTART)` / `cancel` / `delete` | the recovery cases we previously improvised | recover | **open** |
| `wait_for(..., HybridStrategy/PollingStrategy)` | websocket default drops on long queues | execute | use |
| `devices.supports_shots(config)` | preflight before spending | execute | **open** |

Next: `references/nexus-jobs.md`, `references/nexus-admin.md`,
`references/quantinuum-docs-corpus.md`.

## Systems user guide — the access stage

59 pages, 609 snippets, and a *combined* Guppy + pytket + qnexus corpus
(`guppylang.std.qsystem` appears 12x). Canonical source for access, queueing and
HQC costing — read it before any spend decision, not the library docs.

| Topic | Our stage | Status |
| --- | --- | --- |
| HQC cost model and per-device rates | publish (meter) | use |
| Queue priority 1–10, admin-set, default 5 | execute | use |
| Per-backend widths — an account's emulator ceilings, not the published QPU widths | execute | use |
| Which device family accepts pytket vs HUGR | execute | use |

## The rest of the stack

| Library | Reality | Our stage | Status |
| --- | --- | --- | --- |
| **InQuanto** (126 pages, 1174 snippets) | `express` is a ready-made molecular-system shortcut for anything H2/ethylene-shaped; `ansatzes`, `protocols`, `states`, `extensions.pyscf` would replace our hand-built Hamiltonians | model | **open — own gate, new dependency** |
| **lambeq** (82 pages, 529 snippets) | `lambeq.backend.{grammar,quantum,tensor}` + torch; compositional NLP, disjoint from this programme | — | n/a |
| **Quantum Origin** (52 pages, **5 snippets**) | CLI and concept prose, not a Python API surface | — | n/a |

## The spine, with the primitive to reach for

| Step | Reach for | Non-negotiable |
| --- | --- | --- |
| model | NumPy/SciPy exact statevector (InQuanto `express` when we adopt it) | run the **classical baseline before any quantum code** |
| kernel | `@guppy` in a real file; temp-module driver for parameterisation | `angle()` is halfturns |
| compile | offline `QuantinuumBackend`, or `OptimizationLevel.Classical` to freeze counts | pad with `add_blank_wires` |
| verify | dense unitary oracle at 1e-9, global-phase-free | a semantics-changing optimiser looks like the best optimiser |
| execute | Selene locally; Nexus with `max_cost` + stamped properties | stamp the **sweep coordinates** (`band`, `noise_scale`), not just run metadata |
| recover | `python -m quantum.resume`, `jobs.get_all` by property | write the cache row at **submit** time — a submitted job is already billed |
| analyse | `4·√(0.5/shots)` threshold; Bell control per batch | a failed control fails the **whole batch** |
| publish | committed `src/data/demos/*.json` + provenance hash + `job_meter` | name the trust layer (L1/L2/L3); never "cryptographically verified", never "ran on the QPU" for an emulator |

Refresh the corpus behind this sheet with
`python -m quantum.docs_crawler.{fetch,extract,audit}`.

Quickstart notebooks generated from this corpus: see `references/quickstart-notebooks.md`.
