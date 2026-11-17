---
name: rez-caching
description: "Rez's two independent caches — the memcached-backed resolve cache and the on-disk package payload cache — the five settings that turn each one on, what invalidates an entry and what silently does not, rez-memcache and rez-pkg-cache for inspecting and flushing them, and the decision tree for 'I changed the package and nothing took effect'. Use when a resolve is slow, when a package change appears to be ignored, or when you need to prove a stale cache is or is not the cause. Covers Rez 3.4.0."
---

# Rez caching

> **One-sentence summary**: rez has two caches that share almost nothing — a memcached **resolve**
> cache that stores solves and package file reads, and a local-disk **package** cache that stores
> variant payloads — and the single most useful move when a change seems to be ignored is to
> disable one at a time and see which one was lying.

Skill scope: **what is cached, when it goes stale, and how to prove it**. For the solver internals
that a cached resolve short-circuits see `rez-resolve`; for the six causes of a failed resolve see
`rez-resolve-troubleshooting`; for a package that fails to load or was left half-installed see
`rez-package-pitfalls`; for the `cachable` attribute in a `package.py` see `rez-package-definition`.

## The two caches

They are configured separately, live in different places, and fail in different ways. Naming the
right one first is most of the work.

| | Resolve cache | Package cache |
|---|---|---|
| What it stores | solves, package file reads, directory listings, variant states | variant **payloads** — the package root directory |
| Where | a memcached server | local disk |
| Enabled by | `memcached_uri` (plus `resolve_caching`) | `cache_packages_path` |
| Default | off (`memcached_uri = []`) | off (`cache_packages_path = None`) |
| Speeds up | the solve | the *runtime* — loading files off shared storage |
| Inspect with | `rez-memcache` | `rez-pkg-cache` |
| Disable for one run | `rez-env --no-cache` | `rez-env --no-pkg-cache` |

Both are **off out of the box**, so a cache that is biting you is one somebody turned on. Check
before you theorise:

```bash
rez-config memcached_uri
rez-config cache_packages_path
```

An empty list and `None` respectively mean neither cache is active.

## Resolve caching

Backed by [memcached](https://memcached.org/). In a studio, a machine that performs a solve another
machine already performed gets the cached result instead of re-solving.

```python
# rezconfig.py
memcached_uri = ["127.0.0.1:11211"]
```

That one setting is all that is required. The related switches:

| Setting | Default | Effect |
|---|---|---|
| `memcached_uri` | `[]` | memcached servers; empty means no memcaching at all |
| `resolve_caching` | `True` | cache solves, but only when `memcached_uri` is non-empty |
| `cache_package_files` | `True` | cache `package.py` / `package.yaml` reads |
| `cache_listdir` | `True` | cache directory traversals |
| `resource_caching_maxsize` | `-1` | in-process resource cache size; `0` disables, `-1` is unlimited |

`resolve_caching = True` with `memcached_uri = []` is **not** caching. The setting is a permission
slip, not a switch — the URI list is what turns it on.

### What invalidation actually covers

Each cached solve stores solver state, the timestamps of the packages it saw, and the **variant
state** of every variant involved. For the filesystem repository the variant state is the last
modified time of the file backing the variant. Two consequences:

- Releasing a newer version that would change the result **does** invalidate the entry. A cached
  `foo-1+<2` pointing at `1.0.0` is discarded once `1.0.1` exists.
- Changing a variant's backing file **does** invalidate the entry, because its state changed.

The gap is the case upstream calls out: "hacking" a released package into production in a way that
does not produce a new version and does not move the file rez is watching. That entry is not
invalidated, and you get the old answer.

### rez-memcache

```bash
rez-memcache --stats             # hit/miss ratios and memory per server
rez-memcache --flush             # drop every cache entry
rez-memcache --reset-stats       # zero the counters, keep the entries
rez-memcache --warm              # pre-populate with visible packages
rez-memcache --poll              # continuously show get/sets per second
```

`--stats` is the one to reach for first — a high hit ratio on a studio server is the whole point of
the cache, and a ratio near zero means it is not doing anything.

With no servers configured — the default, since `memcached_uri` is empty — every `rez-memcache`
subcommand prints `memcaching is not enabled.` **to stderr and exits 1**. That is worth knowing
before you put it in a script: exit 1 here means "caching is off", which is the normal state, not a
fault. If you only care whether memcaching is configured, redirect stderr and treat 1 as
informational:

```bash
rez-memcache --stats 2>&1 || true
```

`--flush` is the blunt instrument. It is safe — the cache is a cache — but on a busy studio server
it pushes the cost of every subsequent solve back onto the machines that were sharing results.

To see memcached traffic per operation, set `REZ_DEBUG_MEMCACHE` (or `debug_memcache`) for
everything, or `debug_resolve_memcache` for the resolve cache alone.

## Package caching

Copies variant payloads from shared storage onto local disk so that running, say, a Python process
does not pull every source file across the network.

> Package caching does **not** cache package definitions — only payloads.

```python
# rezconfig.py
cache_packages_path = "/path/to/local/cache"
```

Individual packages opt in with the `cachable` attribute; when it is absent, rez falls back to
`default_cachable_per_repository`, then `default_cachable_per_package`, then `default_cachable`
(`False`).

| Setting | Default | Effect |
|---|---|---|
| `cache_packages_path` | `None` | cache root; `None` disables package caching entirely |
| `read_package_cache` | `True` | resolves use cached payloads when present |
| `write_package_cache` | `True` | creating or sourcing a context caches variants |
| `default_cachable` | `False` | fallback when a package does not set `cachable` |
| `package_cache_async` | `True` | copy in a background process instead of blocking the resolve |
| `package_cache_local` | `False` | allow caching of local packages — for testing only |
| `package_cache_same_device` | `False` | allow caching when source and cache share a disk |
| `package_cache_during_build` | `False` | cache during `rez-build` |
| `package_cache_max_variant_days` | `30` | `--clean` deletes variants unused for this long; `0` disables |
| `package_cache_clean_limit` | `0.5` | seconds of cleanup per cache update; `-1` disables |
| `package_cache_space_buffer` | `104857600` | bytes to keep free |
| `package_cache_used_threshold` | `80` | stop caching at this much of the disk in use |

### Cached variants are assumed immutable

This is the setting people get wrong. **No check is ever made** to see whether a variant's payload
changed and should replace an existing cache entry. Caching a repository whose packages get
overwritten in place will serve the old payload forever.

It is for exactly this reason that caching is off for local packages by default
(`package_cache_local`), and for a source on the same disk as the cache
(`package_cache_same_device`). Both are for testing only.

### Asynchronous, so the first resolve does not benefit

With `package_cache_async = True` (the default), variants are copied by a separate `rez-pkg-cache`
process *after* the resolve returns. A resolve will therefore often not use the cached copies it
should, the first time around. Package caching is cumulative by design: more cached variants get
used over time. That is a deliberate trade — it avoids blocking every resolve on a network copy.

To make a resolve wait, use `rez-pkg-cache --pkg-cache-mode sync`.

### rez-pkg-cache

```bash
rez-pkg-cache                            # table of every cached variant
rez-pkg-cache -c status package variant_uri
rez-pkg-cache --logs                     # what the cache daemon did
rez-pkg-cache --clean                    # delete stalled and unused variants
```

Each variant is one of three statuses, and the status tells you what to do next:

| Status | Meaning |
|---|---|
| `copying` | mid-copy, not yet usable |
| `cached` | ready for use |
| `stalled` | the copy went wrong; a partial, unused copy is on disk |

You can see which variants a resolve actually used — the `(cached)` label in the right-hand column:

```bash
rez-env foo
```

Cached packages also record where the payload really lives, in `REZ_<PKG>_ORIG_ROOT`, while
`REZ_<PKG>_ROOT` points at the cache. A package whose root is the cache is the fastest way to
confirm caching is in effect.

Removing a variant takes two steps, and people routinely do only the first:

```bash
rez-pkg-cache -r <variant_uri>     # uncache it — the files stay on disk
rez-pkg-cache --clean              # purge the now-unused files
```

A **stalled** variant will never be re-cached until a `--clean` removes it, and
`package_cache_clean_limit` deliberately will not clean stalled entries either — otherwise a
problematic variant could cycle cached → stalled → deleted → cached forever. `--clean` is the only
thing that removes a stalled variant.

Without `package_cache_clean_limit` (or a scheduled `rez-pkg-cache --clean`), the cache grows
indefinitely.

## "I changed the package and nothing took effect"

Walk this in order. Each step names the cache it rules out, so you stop at the one that was the
cause instead of flushing everything.

1. **Is the change even visible?** `rez-search foo`. If the version you edited is not there, this is
   not a caching problem — it is a build/release problem, or a failed build that left a broken
   install. See `rez-package-pitfalls`.
2. **Bypass the resolve cache.** `rez-env foo --no-cache`. If the change appears, the resolve cache
   served a stale entry. Flush it with `rez-memcache --flush` and re-check.
3. **Bypass the package cache.** `rez-env foo --no-pkg-cache`. If the change appears here but not in
   step 2, the payload cache is serving an old copy — most likely because the package was overwritten
   in place rather than released as a new version. Uncache and clean it:
   `rez-pkg-cache -r <variant_uri>` then `rez-pkg-cache --clean`.
4. **Confirm in a fresh process, not the build shell.** `rez-env foo -o context.rxt` then
   `rez-context --so`. A green build proves the file parses, not that a later resolve picks it up.

If the change appears with both caches bypassed but not without them, and neither flush helps, the
entry is being re-populated by something else — usually another machine, or a `rez-config` override
you did not expect. Check where the settings come from:

```bash
rez-config --source-list resolve_caching
```

## Measuring instead of guessing

`rez-benchmark` runs a fixed set of resolves and writes a results directory containing
`summary.json`. Use it before and after a cache change rather than trusting a stopwatch.

Run each benchmark on its own — `--compare` **replaces** the benchmark run rather than following it,
so a second `rez-benchmark --out after --compare before` never writes `after` at all. Two separate
runs, then the comparison as a third command:

```bash
rez-benchmark --out before
rez-benchmark --out after
rez-benchmark --out after --compare before
rez-benchmark --histogram --out after
```

`--compare` reports each statistic as a `[delta, percentage]` pair, and the sign is easy to read
backwards. The delta is always **the `--compare` directory minus the `--out` directory**:

```text
mean_delta = mean(--compare) - mean(--out)
```

So for the command above, where `--out` is `after` and `--compare` is `before`:

- **`mean_delta` is positive → `after` is faster** (the baseline was slower, so your change helped).
- **`mean_delta` is negative → `after` is slower** (your change made things worse).

Say which directory is which rather than relying on "the second one" — the two directories play
opposite roles, and the whole point of the run is one number's sign.

One caveat: the comparison divides by the `--out` summary's values, so a `--out` summary containing
a `0.0` (a `min` of zero is common on a fast machine) fails with `ZeroDivisionError`. Swapping the
two directories usually clears it, since the other run rarely has a zero in the same field.

For a per-solve breakdown, `rez-env --stats` prints solver counters (`num_solves`, `load_time`,
`solve_time`, reduction and intersection counts). It reports **solver** statistics, not cache hit
ratios — use `rez-memcache --stats` for those.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `memcaching is not enabled.` | `memcached_uri` is empty; `resolve_caching` alone does nothing |
| Change ignored, fixed by `--no-cache` | stale resolve cache entry; `rez-memcache --flush` |
| Change ignored, fixed by `--no-pkg-cache` | package was overwritten in place; cached payloads are immutable |
| Change ignored, neither flag helps | not a cache — check `rez-search`, then `rez-package-pitfalls` |
| A resolve uses the network copy it should have cached | `package_cache_async` means the first resolve does not benefit |
| `stalled` variant never recovers | only `rez-pkg-cache --clean` removes stalled entries |
| Cache grows without bound | no `package_cache_clean_limit` and no scheduled `--clean` |
| `rez-pkg-cache -r` freed nothing | removal uncaches but leaves files; run `--clean` |
| Resolves slower after enabling caching | `package_cache_async = False` is blocking each resolve on the copy |

## Agent workflow

1. Establish which caches are even on: `rez-config memcached_uri` and `rez-config cache_packages_path`.
2. For "my change did not take effect", first confirm the change is visible with `rez-search`.
3. Bypass one cache at a time — `--no-cache`, then `--no-pkg-cache` — and stop at the one that
   changes the answer.
4. Fix the specific cache (`rez-memcache --flush`, or `rez-pkg-cache -r` + `--clean`) rather than
   flushing both.
5. Verify in a fresh resolve (`rez-env -o` + `rez-context --so`), not in the shell that built it.
6. For slowness claims, measure with `rez-benchmark --compare` before and after the change.
