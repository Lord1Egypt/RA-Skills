---
name: rez-resolve
description: "Rez resolve and solver internals — how the solver works, reading -v debug output, conflicts, cycles and total reductions, graph inspection, patching, caching and timestamps. Use when the user asks how the solver works or how to read its -v output. For a resolve that already failed and needs attributing, use rez-resolve-troubleshooting. Covers Rez 3.4.0."
---

# Rez resolve and solver

> **One-sentence summary**: the solver narrows *scopes* of candidate variants until each contains
> exactly one variant; if it cannot, it reports the failure reason — a conflict, a cycle, or a
> total reduction.

Skill scope: how the solver works and how to read its output. For request/version syntax see
`rez-core-concepts`; for the CLI surface see `rez-cli`. For a failing resolve you need to attribute,
see `rez-resolve-troubleshooting`.

## The algorithm

State model:

- A **phase** is one state of the solve; it holds a list of **scopes**.
- A **scope** is one package request plus the list of variants matching it.

Five operations drive a phase (EXTRACT, MERGE-EXTRACTIONS, INTERSECT, ADD, REDUCE). A sixth,
SPLIT, is the **cross-phase** operation that runs when a phase can go no further:

| Operation | What happens |
|---|---|
| **EXTRACT** | a dependency common to *all* variants in a scope is pulled out |
| **MERGE-EXTRACTIONS** | extracted requests are merged; may simplify, or conflict |
| **INTERSECT** | an extracted dependency narrows an existing scope — or conflicts |
| **ADD** | an extraction introduces a new package → new scope |
| **REDUCE** | a scope drops variants that conflict with another scope |
| **SPLIT** | phase is exhausted but unsolved → split the first multi-variant scope into two phases, push both |

The solver keeps a **phase stack** (not recursion): pop a phase, solve it; if exhausted, split and
push two; if solved, done; if failed, pop — empty stack means **no solution**.

Two implementation notes that explain its behavior and speed:

- Scopes cache a set of package families to **skip unnecessary reductions** — reducing a `foo`
  scope that only touches `python`/`bah` against `maya` is effectively a no-op.
- Solver objects are **immutable**; each change creates a new object built on a shallow copy.
  That is copy-on-demand, so phases on the stack share state cheaply.

## Reading `-v` debug output

Enable with `rez-env -v`, up to `-vvv`.

### Scope syntax

| Notation | Meaning |
|---|---|
| `[foo==1.2.0]` | one variant; *null* variant (package has no variants) |
| `[foo-1.2.0[1]]` | one variant; the 1-index variant of `foo-1.2.0` |
| `[foo-1.2.0[0,1]]` | two variants from one package version |
| `foo[1.2.0..1.3.5(6)]` | 6 variants across 6 package versions |
| `foo[1.2.0..1.3.5(6:8)]` | 8 variants across 6 package versions |
| trailing `*` | the scope still has outstanding extractions |

### Output sections in order

```
request: foo-1.2 bah-3 ~foo-1            # initial request, printed once
merged request: foo-1.2 bah-3            # simplified; ~foo-1 absorbed by foo-1.2
pushed {0,0}: [foo==1.2.0[0,1]]* bah[...] # phase pushed: {stack depth, phases solved at depth}
--------------------------------------------------------------------------------
SOLVE #1...
--------------------------------------------------------------------------------
popped {0,0}: ...
EXTRACTING:
extracted python-2 from [foo==1.2.0[0,1]]*
MERGE-EXTRACTIONS:
merged extractions are: python-2 utils-1.2+
INTERSECTING:
python[2.7.3..3.3.0(3)] was intersected to [python==2.7.3] by range '2'
ADDING:
added utils[1.2.0..5.2.0(12:14)]*
  REDUCING:
  removed blah-35.0.2[1] (dep(python-3.6) <--!--> python==2.7.3)
  [blah==35.0.2[0,1]] was reduced to [blah==35.0.2[0]]* by python==2.7.3
```

`<--!-->` marks a conflict between two requirements.

## Failure modes

| Failure | Message | Usual cause |
|---|---|---|
| **Dependency conflicts** | `The following package conflicts occurred: (...)` | two requirements that cannot both hold |
| **Cycle** | `A cyclic dependency was detected: ...` | packages depending on each other in a loop |
| **Total reduction** | all variants of a scope removed | rarer; usually a conflicting *intersect* fails first |

Typical output:

```
The context failed to resolve:
The following package conflicts occurred: (.foo-1 <--!--> .foo-2)
```

## Triage workflow

Work cheapest-first; do not jump to `-vvv`.

1. **Reproduce without entering a shell**
   ```bash
   rez-env <reqs> --output context.rxt     # or -o
   ```
2. **Ask rez what it thinks**
   ```bash
   rez-env <reqs> -v          # solver steps
   rez-context --so           # source order of the last resolve
   rez-status                 # environment/repo sanity
   ```
3. **Inspect the failure graph** — usually the fastest way to see *who* introduced a requirement
   ```bash
   rez-env <reqs> --fail-graph                 # render on failure
   rez-context --dependency-graph              # dot graph of the resolve
   rez-context --print-graph                   # compact text graph
   rez-env <reqs> --max-fails N                # collect more than the first failure
   ```
4. **Find the real requirer** — the package you *asked* for is rarely the one causing it
   ```bash
   rez-depends <pkg>          # reverse lookup: who depends on <pkg>
   rez-search <pkg>           # what versions exist
   ```
5. **Narrow the request** — bisect: drop requests until it resolves, then add back.
6. **Only then** go to `-vvv`.

## Common causes and fixes

| Symptom | Cause | Fix |
|---|---|---|
| Wrong version resolved | an earlier `packages_path` entry shadows it at version level | check `rez-config packages_path`; try `--no-local` |
| Variant unexpected | variants not mutually exclusive and discriminator absent from request | pin the discriminator in the request, or set `variant_select_mode` |
| Local package not picked up | not installed, or not on path | `rez-build --install`, then check `~/packages` |
| Package silently ignored | repo-level filter, or package ignored | `rez-config package_filter`, `rez-pkg-ignore` |
| Missing variant requirement | variant lacks a requirement you expect | `error_on_missing_variant_requires` (default `True`) |
| Windows resolve gets Linux variant | local Linux-only package shadows the released Windows one | `--no-local`, or install the variant locally |
| Resolve slow | large repos, no caching | check `resolve_caching`, `memcached_uri` |

## Patching

When a dependency is wrong but you cannot edit it yet, patch at resolve time:

```bash
rez-env <reqs> --patch
rez-env <reqs> --patch --patch-rank 3      # apply additional patches
```

## Caching

Two independent caches, both easy to blame wrongly:

- **Resolve caching** (`resolve_caching`, default `True`) — cached resolves can be returned with a
  *stale* timestamp. Bypass with `rez-env --no-cache`.
- **Package caching** (`default_cachable`, default `False`) — package payloads copied to
  `cache_packages_path`. When retargeted, `REZ_<PKG>_ROOT` changes but `REZ_<PKG>_ORIG_ROOT`
  keeps the original.

Memcached (`memcached_uri`) can back both. If a resolve returns something impossible, retry with
`--no-cache` **before** investigating the solver.

## Timestamps

Resolves carry a timestamp, so a resolve is reproducible later.

To **pin** a resolve to a point in time, pass `rez-env -t/--time` (epoch time such as `1393014494`,
or a relative time such as `-10s`, `-5m`, `-0.5h`, `-10d`). That is the input that controls the
solve — it ignores packages released after the given time.

`REZ_USED_TIMESTAMP` and `REZ_USED_REQUESTED_TIMESTAMP` are **outputs only** — Rez sets them in the
resolved environment, and nothing reads them back to influence a later solve. Exporting them by
hand will **not** reproduce a historical resolve; use `-t/--time` for that.

`warn_untimestamped` / `warn_all` surface packages that resolved without one.

## Useful knobs

| Setting | Default | Effect |
|---|---|---|
| `resolve_caching` | `True` | cache resolves |
| `variant_select_mode` | `version_priority` | variant preference strategy |
| `implicit_packages` | `~platform=={system.platform}`, `~arch=={system.arch}`, `~os=={system.os}` | weak system constraints |
| `package_filter` | `None` | hide packages from resolves |
| `error_on_missing_variant_requires` | `True` | fail on incomplete variant requirements |
| `memcached_uri` | `[]` | back the caches with memcached |
| `max_fails` (CLI) | `-1` | how many failures to report |

## Agent workflow

1. Reproduce with `-o context.rxt`; never debug inside an interactive subshell.
2. Read `--fail-graph` / `--print-graph` before reading verbose logs — the graph is smaller and
   answers "who required this" directly.
3. Use `rez-depends` for reverse lookups rather than grepping every `package.py`.
4. Bisect the request; keep the failure minimal.
5. Confirm the fix with a fresh resolve, and re-check with `--no-cache` if anything looked stale.
