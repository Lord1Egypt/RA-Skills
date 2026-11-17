---
name: rez-core-concepts
description: "Rez core concepts — packages, versions, requests, repositories, the package search path, implicit packages and variants. Use when the user asks what Rez is, how package versions or requests work, where Rez finds packages, why a resolve picked a certain version, or when a project contains package.py files. Covers Rez 3.4.0."
---

# Rez core concepts

> **One-sentence summary**: Rez takes a *request* (a list of package requests), runs a
> **solver** over packages found on a **search path**, and produces a *resolve* — a
> conflict-free list of concrete package versions.

Reference: [Rez](https://github.com/AcademySoftwareFoundation/rez) 3.4.0.
Skill scope: concepts only. For `package.py` authoring see `rez-package-definition`,
for `commands()` see `rez-package-commands`, for resolve mechanics see `rez-resolve`,
for resolve failures see `rez-resolve-troubleshooting`.

## Mental model

```
request ──► solver ──► resolve ──► package commands concatenated ──► shell code ──► subshell
```

- A **package** is a versioned piece of software with a single definition file (`package.py`).
- A **variant** is a build flavor of one package version (e.g. one per Maya/Python version).
- A **resolve** never contains two versions of the same package — that is a *conflict*.
- Rez never mutates your current shell; `rez-env` puts you in a **subshell**.

## Versions

Version numbers are alphanumeric token lists separated by `.` or `-`.
Examples: `1`, `1.0.0`, `3.2.build_13`, `4.rc1`, `10a-5`.

Ordering rules (tokens compared left to right):

| Order | Rule |
|---|---|
| 1 | letters before numbers (`a` < `1`) |
| 2 | among letters: `A`–`Z` < `_` < `a`–`z` (`A` < `a`, and `_` sits **between** them) |
| 3 | zero-padded numbers before less-padded (`02` < `2`, `002` < `02`) |
| 4 | mixed tokens split into letter/number groups and compared with the same rules |

Alpha sub-tokens are compared with Python's native string comparison, so ordering follows ASCII
code points: `A`–`Z` (65–90) < `_` (95) < `a`–`z` (97–122). That makes the full ordering:

```text
sorted(['_', 'A', 'Z', 'a', 'z', '0', '9'], key=Version)
-> ['A', 'Z', '_', 'a', 'z', '0', '9']
```

`_` is **not** before everything — it comes after uppercase but before lowercase, so
`1.0.rc_1 > 1.0.RC1` while `1.0.rc_1 < 1.0.rca`.

Gotchas that matter in practice:

- The delimiter is **ignored** for comparison: `1.0.0` == `1-0.0`.
- Longer shared-prefix wins: `1.0.0` > `1.0`.
- **No special meaning** for `alpha`/`beta`/`rc`. Semver is *encouraged but not enforced*, and
  semver ordering does **not** apply: `foo-1.0.0 < foo-1.0.0-beta.1` in Rez.

> **Trust the code over the docs here.** The ordering table in Rez's own `basic_concepts.rst` has
> **one** error: it claims `a` < `A`, but `A` < `a` in reality. Its other twelve rows — including
> `13` < `043` — are correct. The same mistake appears in the `AlphanumericVersionToken` docstring
> in `src/rez/version/_version.py`, which states alphas compare "`_`, then A-Z, then a-z". Since a
> **source docstring** gets this wrong too, treat the class itself as the only reliable benchmark
> and verify any ordering question that matters:
>
> ```bash
> python -c "from rez.version._version import Version; print(sorted(['_','A','a'], key=Version))"
> ```

## Package requests

A request is a string matching a range of versions. Used in `requires`, `variants` and on the CLI.

| Request | Meaning |
|---|---|
| `foo` | any version |
| `foo-1` | any `foo-1[.x.x…]` |
| `foo-1+` | `foo-1` or greater |
| `foo-1.2+<2` | `>=1.2, <2` |
| `foo<2` | any version less than 2 |
| `foo==2.0.0` | exactly `2.0.0` |
| `foo-1.3\|5+` | OR'd requests |

Two operators deserve special attention:

- **Conflict `!`** — `!maya-2015.6` means *no* `maya` within `2015.6` (includes `2015.6.1`).
- **Weak reference `~`** — constrains the version *if* the package is present, but does not
  require it. Maya's `package.py` uses `~python-2.7.3` so that any python-using package picks
  the python compatible with Maya, without Maya actually depending on python.

Quote requests on the shell — `<`, `>`, `|` and `!` are shell metacharacters:

```bash
rez-env 'python-2.6+' 'my_py_utils-5.4+<6'
```

## Repositories and the search path

Packages live in **package repositories**; Rez finds them via `packages_path` (a search path,
like `PYTHONPATH`). Inspect it with:

```bash
rez-config packages_path
```

Typical layout of the `filesystem` repository plugin:

```
/packages/inhouse/foo/1.1/package.py
                       /python/<FILES>
                       /bin/<EXECUTABLES>
/packages/inhouse/foo/1.2/
/packages/inhouse/foo/1.3/
```

Only the definition file location is fixed (root of the version dir); the rest is up to the build.

Shadowing rules — these cause most "wrong version" surprises:

- Earlier paths on `packages_path` win, **at version level**: local `foo-1.0.0` hides released
  `foo-1.0.0`, but not `foo-1.2.0`.
- Rez does **not** merge variants of the same package version across repositories.
- Rez does **not** fall back to a later repository when the earlier package has no compatible
  variant — a local Linux-only `foo-1.0.0` hides a released Windows variant even on Windows.
- Use `rez-env --no-local` to exclude locally installed packages from a resolve.

Typical setup: `local_packages_path` (`~/packages`) first so developers can test before release,
then central released repositories later in the path.

## Implicit packages

Every request automatically gets `implicit_packages` appended. The default:

```python
implicit_packages = [
    "~platform=={system.platform}",
    "~arch=={system.arch}",
    "~os=={system.os}",
]
```

Rez models platform/arch/OS as packages. These are **weak** requirements, so a
platform-dependent package is constrained to the current system without forcing those packages in.
`rez-env` and `rez-context` print the implicits that were used.

## Variants

A variant is a sub-build of one package version that differs by dependencies.
Each variant entry's requirements are **appended to** `requires`:

```python
name = "my_maya_plugin"
version = "1.0.0"
requires = ["openexr-2.2"]
variants = [["maya-2016.sp2"], ["maya-2017"]]
```

On disk, variants are subdirectories of the package version:

```
/rez/packages/my_maya_plugin/1.0.0/maya-2016.sp2/<PAYLOAD>
                                   /maya-2017/<PAYLOAD>
```

- `root` = root of the **current** variant; `base` = the directory containing variants.
  For a package without variants, `root == base`.
- `hashed_variants = True` installs variants under a hash instead, avoiding long paths and
  escaping problems with `!`/`<`. `use_variant_shortlinks` adds symlinks under `_v/`.
- **Only one variant of a package is ever used in a given environment.**

### Variant selection

Default `variant_select_mode = "version_priority"`:

1. Priority to packages that appear in the **request** list.
2. Then priority to packages listed **earlier** in the variant.
3. Prefer the higher version.

The other mode, `intersection_priority`, prefers the variant with the most packages present in
the request, with version priority secondary.

**Undefined behavior**: if variants are *not* mutually exclusive (e.g. `[["maya-2016"], ["houdini-14"]]`)
and the discriminating package is not in the request, Rez gives **no guarantee** which variant is
chosen. It is deterministic, just not predictable. Add the discriminator to the request to make it
predictable.

You cannot add variants to a package that has none without bumping the version — so adding a
single variant now is a common future-proofing move.

## Ephemeral packages

Names starting with `.` are **ephemerals**: requests for packages that do not exist. They
participate in the solve (their ranges intersect, conflicts occur) but contribute no payload and
no `commands()`. Useful for passing resolved intent through an environment.

```bash
rez-env python .foo-1 .bah-2
echo $REZ_EPH_FOO_REQUEST   # 1
echo $REZ_USED_EPH_RESOLVE  # .foo-1 .bah-2
```

## Environment variables set by Rez

| Variable | Meaning |
|---|---|
| `REZ_USED_RESOLVE` | full resolved package list |
| `REZ_USED_REQUEST` | the original request |
| `REZ_USED_LOCAL_RESOLVE` | subset resolved from the local repository |
| `REZ_USED_EPH_RESOLVE` | ephemerals in the resolve |
| `REZ_USED_IMPLICIT_PACKAGES` | implicits used |
| `REZ_USED_VERSION` / `REZ_USED_TIMESTAMP` | rez version / resolve time |
| `REZ_<PKG>_ROOT` | root of the current variant of `<PKG>` |
| `REZ_<PKG>_BASE` | base of `<PKG>` (parent of its variants) |
| `REZ_<PKG>_VERSION` | version of `<PKG>` |
| `REZ_RXT_FILE` | path to the context (`.rxt`) file when one was saved |

Package names are upper-cased and non-alphanumerics become `_`: `my_utils` → `REZ_MY_UTILS_ROOT`.

## Reading a resolve

```bash
rez-env foo bah
```

Output lists `requested packages` (with `(implicit)` and `(ephemeral)` labels) and
`resolved packages` (with `(local)` for local installs). The `>` prompt prefix is the visual cue
that you are inside a Rez-configured environment.

Use `rez-context` for non-interactive inspection — see the `rez-cli` skill.

## Agent workflow

1. Inspect before guessing: `rez-config packages_path`, `rez-search <pkg>`, `rez-status`.
2. Narrow the read — `rez-context --so`, `rez-search <pkg> --latest` — instead of dumping everything.
3. Reproduce a resolve without entering a shell: `rez-env <reqs> --output context.rxt`.
4. If a resolve fails, go to the `rez-resolve` skill; do not guess at the cause.
