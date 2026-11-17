---
name: rez-resolve-troubleshooting
description: "Diagnosing Rez resolve failures — a command-by-command triage path for 'The context failed to resolve', package conflicts, request version conflicts, implicit package failures, variant selection failures, missing packages or versions, filtered or ignored packages, and stale resolve caches. Use when rez-env, rez-build or rez-test fails to resolve and you need to find the culprit, not just read the solver. Covers Rez 3.4.0."
---

# Rez resolve failure troubleshooting

> **One-sentence summary**: capture the failure without entering a shell, read the failure path that
> rez already printed, classify it into one of six causes, then confirm with the cheapest command
> that can rule a cause in or out.

Skill scope: **diagnosing a failure that already happened**. For how the solver works and how to read
`-v` traces see `rez-resolve`; for request and version syntax see `rez-core-concepts`; for the command
surface see `rez-cli`.

## Step 0 — capture the failure

Never start by debugging inside a subshell; `rez-env` drops you into an interactive shell on success
and hides the structured output on failure. Write the context to a file instead:

```bash
rez-env <reqs> -o context.rxt          # also stores a FAILED resolve
rez-env <reqs> -o -                    # or write it to stdout
```

The stored `.rxt` keeps `failure_description`, so you can re-inspect it later with `rez-context`:

```bash
rez-context context.rxt --so            # what was requested, and the source order
rez-context context.rxt --print-graph   # dot graph of the failed resolve
```

Two traps in that pair, both verified against `src/rez/cli/context.py`:

- **`-i` is `--interpret` on `rez-context`, not `--input`** (it *is* `--input` on `rez-env`, so the
  same short flag means opposite things on the two commands). Passing `-i` sends the call down the
  interpret branch, where `--so` and the graph flags are skipped, and a failed context raises
  `ResolvedContextError: Cannot perform operation in a failed context` — the one case this skill
  exists for.
- **`--dependency-graph` needs a solved context**, because it calls `get_dependency_graph()`. Use
  `--print-graph` (or `--pg`), which calls `rc.graph()` and works on a failed resolve. On a failed
  context it prints the `CONFLICT` edge directly:

  ```text
  digraph g {
  _1 [fillcolor="#F6F6F6", fontsize="10", style="filled,dashed", label="python-2"];
  _2 [fillcolor="#F6F6F6", fontsize="10", style="filled,dashed", label="!python-2"];
  _1 -> _2 [arrowsize="1", color="red", fontcolor="red", style="bold", label="CONFLICT"];
  }
  ```

  Of the other graph flags: `-d` / `--dependency-graph` also fails, because it calls
  `get_dependency_graph()`, which is decorated `@_on_success`. But `-g` / `--graph` is fine — it uses
  `rc.graph()`, the same undecorated call as `--print-graph`, so it does render the failure graph. It
  just needs Graphviz `dot` on `PATH`, and fails with `FileNotFoundError` when it is missing; that is
  an environment problem, not a failed-context one.

## Step 1 — read what rez already told you

A failed resolve prints three blocks, in this order. They are the whole diagnosis; everything after
this step only confirms it.

```
The context failed to resolve:
The following package conflicts occurred: (python-2.7 <--!--> python-3)

Resolve paths starting from initial requests to conflict:
  my_tool --> my_lib-1.2 --> python-3

To see a graph of the failed resolution, add --fail-graph in your rez-env or rez-build command.
```

| Block | Tells you |
|---|---|
| `The context failed to resolve:` + reason | the failure class (see the table below) |
| `Resolve paths starting from initial requests to …` | **who** pulled in the offending requirement: it reads left (your request) to right (the conflict), so read it backwards to find the culprit |
| `--fail-graph` hint | the visual version of the same path |

The reason line comes from `failure_description`; the path lines come from
`rez.utils.resolve_graph.failure_detail_from_graph`, which finds the `CYCLE` edge first and the
`CONFLICT` edge second. `<--!-->` marks two requirements that cannot both hold. In `(A <--!--> B)`,
`A` is the dependency that a package's variants share and `B` is the request it conflicts with — so
`B` is usually the thing to change. A leading `.` on a name marks an **ephemeral** package, which is
resolved but not actually installed into the environment.

If the paths block is empty, the failure is a total reduction (all variants of a scope were removed)
rather than a conflict — go to cause 5.

## Step 2 — classify and confirm

Work through the causes cheapest-first. Each has one command that confirms it.

| # | Cause | Signature | Confirm with |
|---|---|---|---|
| 1 | **Request version conflict** | `(python-2.7 <--!--> python-3)` — both sides the same package | `rez-depends <pkg>` |
| 2 | **Package conflict** | `(maya-2019 <--!--> !maya-2019)` — different packages, or an explicit `!` | `rez-depends A`, `rez-depends B` |
| 3 | **Implicit package** | conflict mentions `platform`, `arch`, `os`; or a package vanishes only on this machine | `rez-env <reqs> --ni` |
| 4 | **Variant selection** | wrong variant chosen, or variant subpath missing | `rez-config variant_select_mode`, `rez-env <reqs> -v` |
| 5 | **Total reduction / no candidates** | no conflict edge; `The context failed to resolve` with no named pair | `rez-search <pkg>`, `rez-env --no-filters` |
| 6 | **Package or version not found** | `PackageFamilyNotFoundError` / `PackageNotFoundError` | `rez-search <pkg>`, `rez-config packages_path` |

Also rule out a **stale cache** before anything else — see the last section.

### Cause 1 — request version conflict

Two requirements on the same package cannot both hold. Rez reports the two ranges.

```bash
rez-env my_tool my_lib -o /tmp/c.rxt   # (python-2.7 <--!--> python-3)
rez-depends python                     # reverse lookup: who depends on python
```

The package you asked for is rarely the culprit. The paths block names the chain from your request
down to the conflict; `rez-depends <pkg>` is the reverse lookup that confirms it from the other
direction — it lists the packages that depend on `<pkg>`. Then:

- **Loosen the tighter request.** `foo-1.2+<1.3` may be stricter than reality requires — a range like
  `foo-1.2+<2` often resolves. Check what actually exists with `rez-search foo`.
- **Use a weak reference** when you want "if present, it must be in this range" rather than a hard
  requirement: `rez-env foo '~nuke-9.rc2'`. This is how DCC packages constrain an embedded python
  without forcing it into every environment.
- **Use the conflict operator** to exclude a specific bad version: `rez-env maya_utils '!maya-2015.6'`.
- **Bisect**: drop requests one at a time until it resolves, then add back to find the pair.

### Cause 2 — package conflict

Two *different* packages are mutually exclusive, usually because a package declared `!other`.

```bash
rez-depends A                          # reverse lookup: who depends on A
rez-env <reqs> --max-fails 5           # collect several failures, not just the first
rez-env <reqs> --fail-graph            # render the resolve graph image
```

`--max-fails N` matters when the first failure is a symptom: resolving it can expose a second,
unrelated conflict that is the real one. The default is `-1` (report everything).

### Cause 3 — implicit packages

Rez adds `implicit_packages` to **every** request. The defaults are weak requirements:

```python
implicit_packages = [
    "~platform=={system.platform}",
    "~arch=={system.arch}",
    "~os=={system.os}",
]
```

Because they are weak (`~`), they do not force those packages into the resolve; they constrain them
**only if present**. A platform-dependent package that is present therefore has to match the current
machine, and that is usually the real cause when a resolve fails on one OS but not another.

```bash
rez-env <reqs> --ni                    # retry with no implicit packages at all
rez-config implicit_packages           # what is actually configured
```

- **`--ni` makes it resolve** → an implicit package is the constraint. Look for a package whose
  variants or `requires` name `platform`, `arch` or `os`, and check it was built for this machine.
- **`--ni` still fails** → the conflict is in your own request; go back to causes 1 and 2.
- Do not "fix" this by editing `implicit_packages` globally. It is the mechanism that stops a
  Linux-built variant from being selected on Windows; removing it trades a clear failure for a
  silently wrong environment.

### Cause 4 — variant selection failure

Two distinct failures look similar, so separate them first:

**Wrong variant chosen.** When variants are not mutually exclusive, which one you get is a
*preference*, not a guarantee. `version_priority` (the default) prefers variants whose packages have
higher versions, giving priority to packages that appear in the request, then to packages listed
earlier in the variant. `intersection_priority` instead prefers the variant with the most packages
present in the request, with version as a tiebreak.

```bash
rez-config variant_select_mode         # which mode is active
```

Rez cannot compare versions across different packages, so with variants like `["maya-2016"]` and
`["houdini-14"]` the choice is effectively arbitrary unless the discriminator is in the request. Fix
it by **naming the discriminator in the request** — `rez-env geocache maya` — not by reordering
variants and hoping. Remember a transitive dependency can still overrule the preference.

**Wrong or missing variant requirement.** Variants are appended to `requires` per variant, so a
variant that omits a requirement you expect will not constrain anything:

```bash
rez-config error_on_missing_variant_requires   # default True
rez-env <reqs> -v                              # see which variant scope survived
```

**Useful extra checks** when the resolved variant is not the one you built:

```bash
rez-env <reqs> --nl                    # ignore ~/packages — a local build may be shadowing
rez-env <reqs> --no-local              # long form of the same flag
```

A locally installed package sits at the front of `packages_path` and will shadow the released one,
including shadowing a Windows resolve with a Linux-only local build.

### Cause 5 — total reduction, and nothing found at all

If every variant of a scope is removed there is no conflict edge to print, so the paths block is
empty. The candidates were eliminated one by one. Find out what *does* exist:

```bash
rez-search <pkg>                       # every version rez can see
rez-search <pkg> --latest              # just the newest
rez-search <pkg> -f '{qualified_name}' # just the names, one per line
rez-search 'foo<2'                     # narrow by a real version range
rez-env <reqs> --no-filters            # retry with package filters disabled
rez-env <reqs> --exclude '*.beta'      # reproduce a filter locally
rez-env <reqs> --paths <path>          # retry against a specific search path
```

Three `rez-search` rules that matter here, all verified against a real repository:

- **A bare name already lists every version.** With the default `--type auto`, `rez-search <pkg>`
  resolves to a single family and lists all of its versions:

  ```text
  $ rez-search foo
  foo-1.0.0
  foo-1.1.0
  foo-2.0.0
  ```

  You do **not** need to add a version range to list versions.
- **`<pkg>-*` is not a version range, and matches nothing.** `foo-*` is not a valid requirement, so
  `package_search.py` falls back to treating the whole string as a glob on the *family name*, and
  `fnmatch('foo', 'foo-*')` is false. It returns `No matching family found` (exit 1) on every
  repository, which looks like "the package doesn't exist" but is the pattern never matching.

  | To do this | Write |
  |---|---|
  | list every version of one package | `rez-search foo` |
  | narrow to a range | `rez-search 'foo-1'` / `rez-search 'foo<2'` |
  | list versions across several families | `rez-search 'foo*' --type package` |

  A glob that matches **one** family still degrades correctly to versions (`rez-search 'f*'` lists
  the `foo` versions), but a glob matching **two or more** families degrades to a family list
  (`rez-search '*'` prints `bar` and `foo`). Force versions with `--type package`.
- **`-f` / `--format` takes an argument.** It is `-f FORMAT`, not a boolean flag; `rez-search <pkg>
  --format` exits 2 with `expected one argument`. It only changes the output template. `--latest`
  works with a bare name: `rez-search foo --latest` prints `foo-2.0.0`.

Package filters hide packages from resolves: a package is excluded when it matches an exclusion rule
and no inclusion rule. A filter can be set globally via the `package_filter` setting, applied per
command with `--exclude` / `--include`, or attached to a package with `rez-pkg-ignore`. Because a
filtered package is simply invisible, the symptom is "it exists on disk but rez won't use it".

```bash
rez-config package_filter              # global rules
rez-search <pkg> --no-local            # check the released repo, not your local install
```

Also check timestamps: `rez-env -t <time>` ignores packages released after a time (epoch, or
relative like `-10d`), and a bad `-t` in a wrapper script makes current packages invisible.

### Cause 6 — package or version not found

`PackageFamilyNotFoundError` means no package of that name exists anywhere on the search path;
`PackageNotFoundError` means the family exists but not a version in the requested range.

```bash
rez-config packages_path               # the search path, in order
rez-config local_packages_path         # ~/packages, normally first
rez-search <pkg>                       # does rez see it at all?
rez-search <pkg> --paths <path>        # search one repository explicitly
rez-status                             # environment and repository sanity
```

Resolution order matters: the first repository on `packages_path` that has the family wins at the
family level, and `local_packages_path` is normally first, so a stale local package can mask a
released one. Confirm by searching without local packages (`rez-search <pkg> --no-local`).

## Step 3 — last resort: verbose, and caching

Only escalate to `-v` once the above is inconclusive, and always rule out the cache first.

```bash
rez-env <reqs> --no-cache              # bypass the resolve cache entirely
rez-env <reqs> -v                      # solver steps; -vv / -vvv for more
rez-env <reqs> --stats                 # advanced solver stats
```

Two caches are easy to blame wrongly. **Check whether caching is even on first**: `resolve_caching`
defaults to `True` but does nothing unless `memcached_uri` is configured, and that defaults to `[]`.
So on a stock install there is no resolve cache to be stale — confirm with
`rez-config memcached_uri` before chasing this cause.

- **Resolve caching** (`resolve_caching`, default `True`, backed by `memcached_uri`) — a cached
  resolve can be returned **stale**: its timestamp is the original one. Symptom: rez returns a
  version you know you released or deleted. `rez-env --no-cache` bypasses it; `rez-memcache` shows
  hit/miss stats and can reset it. Cache entries self-invalidate when a newer package changes the
  result, so a genuinely stale hit usually means a package was edited in place rather than released.
- **Package caching** (`default_cachable`, default `False`) — copies package payloads to
  `cache_packages_path`. When a package is retargeted, `REZ_<PKG>_ROOT` changes while
  `REZ_<PKG>_ORIG_ROOT` keeps the original. Disable per command with `--no-pkg-cache`.

If a resolve returns something impossible, **retry with `--no-cache` before reading any solver
output** — it is one flag and costs nothing, but only skip past this cause if `memcached_uri` is
actually set.

## Triage cheat sheet

```bash
# capture, then classify
rez-env <reqs> -o context.rxt                  # store even a failed resolve
rez-env <reqs> --no-cache -o context.rxt       # ...with the cache out of the way

# read it
rez-context context.rxt --so                   # request + source order
rez-context context.rxt --print-graph          # dot graph of the failed resolve
rez-env <reqs> --fail-graph                    # rendered failure graph
rez-env <reqs> --max-fails 5                   # more than the first failure

# rule causes in or out
rez-env <reqs> --ni                            # implicit packages?
rez-env <reqs> --nl                            # local packages?
rez-env <reqs> --no-filters                    # package filters?
rez-search <pkg>                              # what versions exist?
rez-depends <pkg>                              # who requires it?
rez-config packages_path                       # where is rez looking?

# escalate
rez-env <reqs> -v --stats                      # solver trace
rez-memcache                                   # cache hit/miss, reset
```

## Agent workflow

1. Reproduce with `-o context.rxt --no-cache`. Never debug inside an interactive subshell.
2. Read the failure reason **and** the `Resolve paths starting from initial requests` block. The path
   names the culprit package; the request you typed usually is not it.
3. Classify with the six-cause table and confirm with that cause's command before changing anything.
4. Rule out implicit packages, local packages and filters with `--ni`, `--nl` and `--no-filters`
   before reading solver output — each is one flag and each is a common cause.
5. Use `rez-depends` for reverse lookups instead of grepping `package.py` files.
6. Bisect the request to keep the reproducer minimal, fix the cause, then confirm with a fresh
   resolve — and re-confirm with `--no-cache` if the result looked stale.
