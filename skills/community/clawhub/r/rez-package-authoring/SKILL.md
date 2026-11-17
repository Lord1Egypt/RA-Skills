---
name: rez-package-authoring
description: "Rules and decision-making for authoring Rez packages — how to split versions and variants, how to write requires/variants/build_requires/commands, how wide to make dependency ranges, the rez-build and rez-release workflow and conventions, and the recurring pitfalls and anti-patterns. Use when writing, reviewing or restructuring a package.py, or when deciding whether a change needs a new version or a new variant. Covers Rez 3.4.0."
---

# Rez package authoring rules

> **One-sentence summary**: `package.py` is a *declaration* of what a package needs and provides —
> decide the version/variant split first, then keep requirement ranges as wide as the truth allows
> and as narrow as reality demands.

Skill scope: **how to decide and structure a package**. For the attribute reference and
`@early`/`@late` mechanics see `rez-package-definition`; for the `commands()` body and rex API see
`rez-package-commands`; for build/release command flags see `rez-cli`; for what rez does to the
module scope of `package.py` — serialization, build-time freezing and the errors that follow — see
`rez-package-pitfalls`.

## The three decisions, in order

Get these right and the file writes itself.

1. **Is this a new version or a new variant?** — something about the package changed vs. something
   about its *dependencies* changed.
2. **How wide is each dependency range?** — what the package genuinely works with, not what it
   happened to be built against.
3. **What is build-time vs. runtime?** — which requirements survive into the installed package.

## Decision 1 — new version or new variant?

| The change | Do this |
|---|---|
| Your own source code changed | **new version** |
| A dependency version it must build against changed (maya 2016 → 2017, python 2 → 3) | **new variant** |
| Need to support a second platform/arch/os | **new variant** |
| Fixing a bug in the payload | **new version** |

The rule that catches people out: **variants cannot be added to a package that has none without
bumping the version.** A package released with no `variants` at all can never gain them. So if a
compiled package plausibly needs variants later — a second python, a second DCC — declare the single
variant now:

```python
name = "my_utils"

variants = [
    ["python-2.7"],
]
```

This is the "future proofing" reason for single-variant packages. The second common reason is
cosmetic but real: variant requirements appear in the install path, so
`my_utils/1.0.0/python-2.7/<payload>` tells a user what they are getting, where
`my_utils/1.0.0/<payload>` does not.

**Variants are per-version, not per-package.** Adding a variant means re-releasing that version; it
does not retroactively change already-released versions.

## Decision 2 — how wide should a range be?

Start from the truth about compatibility, then express it with the narrowest syntax that still says
it.

| You mean | Write |
|---|---|
| any version | `foo` |
| any `1.x` | `foo-1` |
| `1.0.0` or newer | `foo-1+` |
| at least `1.2`, below `2` | `foo-1.2+<2` |
| exactly `2.0.0`, nothing else | `foo==2.0.0` |
| `1.3` or `5+`, but not between | `foo-1.3\|5+` |
| if present it must be in range, but don't require it | `~foo-2.7.3` |
| this version is unacceptable | `!foo-2015.6` |

Three rules for sound ranges:

- **Do not pin what you do not have to pin.** `python==2.7.11` forces every environment that uses
  your package onto that exact build; `python-2.7` lets rez co-exist with everything else. Pin only
  when there is a concrete incompatibility.
- **Do not widen past what you tested.** A range is a promise. `foo-1+` claims you work with every
  future `foo-1`.
- **Build time can be wider than runtime.** This is what requirements expansion is for. A C++ package
  may build against any `boost-1` but must link at runtime against the minor version it was built
  with. Write the loose range and let rez expand it:

  ```python
  requires = [
      "boost-1.*",      # expands to the version actually built against, e.g. boost-1.55
  ]
  ```

  `**` expands to the full version (`boost-1.**` → `boost-1.55.1`). The equivalent done by hand:

  ```python
  @early()
  def requires():
      from rez.package_py_utils import expand_requires
      return expand_requires(["boost-1.*"])
  ```

- **Use `~` (weak reference) when you constrain but do not require.** DCCs that ship an embedded
  python should declare `requires = ["~python-2.7.3"]`: python is not pulled into the environment,
  but if something else brings python in, it has to be the compatible one. This is how a studio keeps
  python libraries usable both inside and outside the DCC.

## Decision 3 — runtime vs. build time

| Attribute | Puts into the environment at | Transitive? |
|---|---|---|
| `requires` | runtime **and** build | yes |
| `build_requires` | build only | **yes** — collects from every package in the build env |
| `private_build_requires` | build only | no — only from the package being built |
| `variants` | build (one variant at a time) **and** runtime (the selected variant) | n/a |

Choose `build_requires` when other packages also need the dependency to build against *your* headers
— a header-only C++ library is the canonical case: if your public headers include its headers, anyone
compiling against you needs it too. Choose `private_build_requires` for things nobody downstream
needs: doc generators (`doxygen`, `sphinx`), build utilities, statically linked libraries.

The build environment is assembled in a fixed order — `requires`, then transitive `build_requires`,
then `private_build_requires`, then the current variant's requirements.

**A subtle trap with `building`:** early-bound functions are evaluated more than once per build —
once pre-build, and once per variant — and the **pre-build** value (where `building` is `False`) is
the one baked into the installed package. So to add a requirement at runtime only:

```python
@early()
def requires():
    if building:
        return ["python-2"]
    else:
        return ["runtimeonly-1.2", "python-2"]
```

Always check the function returns what you want when `building` is `False`.

## Writing `commands()`

Rez is not a build system and does not know how your package is consumed. `commands()` is where you
say it. Keep it declarative — remember it is **interpreted into shell code**, not executed as Python.

```python
def commands():
    env.PATH.append("{root}/bin")
    env.PYTHONPATH.append("{root}/python")

    if building:
        env.CMAKE_MODULE_PATH.append("{root}/cmake")
```

Rules:

- **Put build information behind `if building:`** so consumers find headers and CMake config at build
  time without polluting the runtime environment.
- **`commands()` never runs for the package being built.** Use `pre_build_commands()` for that.
- **Expose tools with `tools`**, not by hand-managing `PATH`, so `rez-context --tools` and the tool
  conflict detection work.
- **Keep it cheap.** Anything that can be computed once should be an `@early()` attribute; use
  `@late()` only for values that genuinely depend on runtime state (env vars, user role).

## The build/release loop

```bash
rez-build --install                    # build all variants, install to ~/packages
rez-env mypackage                      # resolve and test in a separate shell
rez-test mypackage                     # run the package's tests
rez-release                            # build + release_hooks + VCS plugins + tag
```

Conventions worth following:

- **Local first, release when ready.** `rez-build --install` goes to `local_packages_path`
  (typically `~/packages`), which sits at the front of `packages_path`, so your local package shadows
  the released one. That is the intended test loop — and also the reason `--no-local` exists when a
  local build is masking a released one.
- **Use `--prefix` to install somewhere else**, for example
  `rez-build -i --prefix /path/to/repo`. `rez-release` is the managed alternative: it targets
  `release_packages_path`, runs `release_hooks`, runs tests, does sanity checks and VCS tagging, and
  adds the release package attributes automatically.
- **Inspect before you build.** `rez-build --view-pre` prints the preprocessed package and exits —
  the fastest way to see what `preprocess()` and `@early()` actually produced.
- **Build one variant while iterating**: `rez-build --variants 0`.
- **Pass build-system args after `--`**: `rez-build -- -DMYVAR=YES`.
- **Do not re-resolve a test shell unnecessarily** — if requirements have not changed, the existing
  environment is still valid.

## Pitfalls and anti-patterns

| Anti-pattern | Why it breaks | Do instead |
|---|---|---|
| `foo==1.2.3` on every dependency | over-constrains every downstream resolve | range it: `foo-1.2+<2`, pin only real incompatibilities |
| No `variants` on a package that will need them | variants cannot be added later without a version bump | declare one variant now |
| Non-mutually-exclusive variants, relying on the pick | rez cannot compare versions across packages; the choice is a preference, and a transitive dep can overrule it | put the discriminator in the request, e.g. `rez-env pkg maya` |
| Heavy work in `@late()` | runs at resolve/runtime, on every use | compute at build time in `@early()`, keep `@late()` for genuine runtime state |
| Imports at the top of `package.py` for `@late()` | late functions must import inside the function | import inside the function body |
| Referencing other `@early()`/`@late()` attributes from an `@early()` function | raises an error | reference plain attributes only, via `this` |
| Expecting `commands()` to run during your own build | it never runs for the package being built | use `pre_build_commands()` |
| Referencing files by relative path in `commands()` | cwd during a build is the *build path*, not the package root | use `{root}` |
| Editing a released package in place | breaks timestamped resolves and returns stale cached resolves | release a new version |
| Setting env vars for build consumers unconditionally | pollutes runtime | guard with `if building:` |
| Skipping `tools` and appending to `PATH` by hand | loses tool tracking and conflict detection | use the `tools` attribute |

For the ones that produce a rez error rather than a bad decision — top-level imports that make the
installed `package.py` unparseable, values frozen on the build machine — see
`rez-package-pitfalls`, which carries the verbatim error text.

## Review checklist

Before releasing, check in this order:

1. Does every range say what the package *actually* supports — not wider, not narrower?
2. Does the package need variants now, so it can gain more later without a version bump?
3. Are build-only dependencies in `build_requires` / `private_build_requires`, and is the transitive
   one the right choice?
4. Does every `@early()` function return the right value when `building` is `False`?
5. Is build information in `commands()` guarded by `if building:`?
6. Does `rez-build --view-pre` show the package you intended?
7. Did `rez-test` pass before `rez-release`?

## Agent workflow

1. Read the existing `package.py` and `rez-build --view-pre` output before editing anything.
2. Classify the requested change against decision 1 — version or variant — before touching
   `requires`.
3. Widen or narrow each range deliberately; never copy a range from another package without checking
   it means the same thing.
4. Prefer `~` and `!` over hard requirements when you are constraining rather than requiring.
5. Validate with `rez-build --view-pre`, then `rez-build --install`, then `rez-env` in a separate
   shell — cheapest check first.
6. Run `rez-test` before `rez-release`.
