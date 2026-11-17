---
name: rez-package-definition
description: "Authoring Rez package.py files — standard attributes, early/late binding functions, requires/variants/build_requires, string expansion and package overrides. Use when writing, reviewing or debugging a package definition file, or when the user asks how to declare dependencies, variants, tools or build-time requirements. Covers Rez 3.4.0."
---

# Rez package definition (`package.py`)

> **One-sentence summary**: every variable in `package.py` becomes an attribute of the package;
> `requires` declares dependencies and `commands()` configures the runtime environment.

Skill scope: the definition file itself. For the `commands()` body see `rez-package-commands`;
for requests/version syntax see `rez-core-concepts`; for builds see `rez-cli`. For the decisions behind
versions, variants, range width and the build/release loop see `rez-package-authoring`.

## Minimal package

```python
name = "sequence"

version = "2.1.2"

description = "Sequence detection library."

authors = ["ajohns"]

tools = ["lsq", "cpq"]

requires = ["python-2.6+<3", "argparse"]

def commands():
    env.PATH.append("{root}/bin")
    env.PYTHONPATH.append("{root}/python")

uuid = "6c43d533-92bb-4f8b-b812-7020bf54d3f1"
```

The file lives at the root of each package install:
`/packages/inhouse/foo/1.0.0/package.py`.

## What becomes a package attribute

Every module-level variable becomes an attribute — including custom ones. These do **not**:

- Python modules (`import sys` does not create a `sys` attribute);
- plain functions (except `commands`, `@early` and `@late` functions);
- names with a leading double underscore;
- any build-only attribute.

That list is exactly as wide as it reads, and no wider. A **class** is not a module and not a
function, so `from pathlib import Path` at module scope does create a `Path` attribute — and it is
serialized into the installed `package.py` as `Path = <class 'pathlib.Path'>`, which no longer
parses. Same for a class defined in the file and for any object instance. Values *derived* from a
stripped module survive too: `sys_path = sys.prefix` is kept, frozen on the build machine. See
`rez-package-pitfalls` for the errors and the correct form.

## Standard attributes

| Attribute | Type | Purpose |
|---|---|---|
| `name` | `str` | package name (required) |
| `version` | `str` | version (required) |
| `description` | `str` | general description, no version details |
| `authors` | `list[str]` | ordered, major contributor first |
| `requires` | `list[str]` | runtime dependencies |
| `build_requires` | `list[str]` | build-time deps, **transitive** |
| `private_build_requires` | `list[str]` | build-time deps, **not** transitive |
| `tools` | `list[str]` | entry points exposed into the environment |
| `variants` | `list[list[str]]` | variant definitions (see `rez-core-concepts`) |
| `hashed_variants` | `bool` | install variants under a hash |
| `commands()` | function | runtime environment configuration |
| `uuid` | `str` | stable identity across renames |
| `has_plugins` / `plugin_for` | `bool` / `str` | plugin discovery via `rez-plugins` |
| `cachable` | `bool` | allow package caching |
| `config` | `dict` | override rez settings during build/release |

Arbitrary custom attributes are allowed and are often the cleanest way to pass
build-computed data to `commands()`.

## `requires` vs `build_requires` vs `private_build_requires`

The build environment requirement list is assembled in this order:

1. `requires`
2. `build_requires` — **transitive**: build requirements of all packages in the env are included
3. `private_build_requires` — **not** transitive
4. the current variant's requirements

Use `private_build_requires` for doc generators (`doxygen`, `sphinx`), build utilities and
statically linked libraries. Use `build_requires` for header-only C++ libraries, where consumers
of your headers also need the header at build time.

## Early binding functions (`@early`)

Evaluated at **build time**; the returned value is baked into the installed `package.py`.

```python
@early()
def authors():
    import subprocess
    p = subprocess.Popen("git shortlog -sn | cut -f2",
                         shell=True, stdout=subprocess.PIPE)
    out, _ = p.communicate()
    return out.strip().split("\n")
```

Rules and gotchas:

- Only package attributes are visible — the implicit `this` object exposes package attributes only.
- **No** rez environment variables are accessible.
- **Do not** reference other `@early` or `@late` attributes — an error is raised.
- CWD during evaluation is the directory containing your `package.py`.
- `@early` functions are evaluated **multiple times**: once pre-build and once per variant.
  The **pre-build** value (with `building == False`) is what lands in the installed package.
- Therefore: make sure the function returns the runtime value when `building` is `False`.

```python
@early()
def requires():
    if building:
        return ["python-2"]
    else:
        return ["runtimeonly-1.2", "python-2"]
```

Objects available during early evaluation: `this`, `building`, `build_variant_index`,
`build_variant_requires`.

## Late binding functions (`@late`)

Remain as functions in the installed package; evaluated lazily on first access and then cached.
Allowed for: `requires`, `build_requires`, `private_build_requires`, `tools`, `help`, and any
arbitrary attribute.

```python
@late()
def tools():
    import os                      # imports MUST be inside the function
    result = this._tools
    if os.getenv("_USER_ROLE") != "superuser":
        result = set(result) - set(["delete-all", "mod-things"])
    return list(result)

@early()
def _tools():
    import os
    return os.listdir("./bin")     # relative: not installed yet at build time
```

- Split the work: compute what you can at build time into an `@early` custom attribute, then do
  only the runtime-dependent part in `@late`. This keeps resolves cheap.
- `in_context()` returns `True` when the package is part of a resolved context (e.g. iterating a
  `ResolvedContext`) and `False` when merely iterating packages (e.g. `rez-search`). Guard
  context-dependent logic with it.

> `commands()` is late bound but is **never** decorated with `@early`/`@late`.

## String expansion

`{root}` expands to the install location of the package; `{this.root}` is equivalent.
Available in `commands()` and in rex calls. See `rez-package-commands` for `literal()`,
`expandable()` and `expandvars()`.

## Package config overrides

A package can override rez settings during its own build/release:

```python
with scope("config") as c:
    c.release_packages_path = "/software/packages/apps"
```

Overrides only apply while the package is being built or released, so only these are useful:
`packages_path`, `local_packages_path`, `release_packages_path`, the `build_system` /
`release_hook` / `release_vcs` plugin settings, `package_definition_python_path`,
and `package_filter`.

Useful for routing internally- and externally-developed packages to different release paths.

## Preprocessing

`package.py` can be preprocessed before evaluation — for example to add a version timestamp or
to generate attributes from an external source. See the "Package Preprocessing" section of the
Rez package-definition docs: the `package_preprocess_function` setting installs a global
preprocessor, and `rez-build --view-pre` prints the preprocessed result.
Prefer the simplest thing that works: an `@early()` function usually covers the same ground with
far less machinery.

## Review checklist for a `package.py`

- [ ] `requires` uses ranges (`python-2.7+<3`) rather than unpinned names when pinning matters.
- [ ] Build-only deps are in `private_build_requires`, not `requires`.
- [ ] `@early()` returns the correct value when `building` is `False`.
- [ ] `@late()` performs imports **inside** the function body.
- [ ] `variants` entries that must be discriminated are pinned in the request, not left ambiguous.
- [ ] `commands()` uses POSIX forward slashes, even on Windows.
- [ ] No `os.pathsep` or hardcoded `a:b` path lists.

## Validate before release

```bash
rez-build --install          # build + install locally
rez-env mypackage            # resolve in a fresh shell
rez-search --validate mypackage
```

Narrow the output — read the specific resolve, not the whole build log:

```bash
rez-context --so             # source order of the resolve
```
