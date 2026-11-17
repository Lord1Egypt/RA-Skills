---
name: rez-package-commands
description: "Writing the Rez commands() section and rex environment API — env object, setenv/appendenv/prependenv/unsetenv/alias/source/error, string expansion, literal/expandable/expandvars, execution order and build-time branching. Use when a package must set, append or prepend environment variables, expose tools, source scripts, or behave differently during a build. Covers Rez 3.4.0."
---

# Rez package commands and the rex API

> **One-sentence summary**: `commands()` is Python that configures the *environment*; it is
> translated into shell code, not executed as Python at runtime.

Skill scope: the `commands()` body. For the surrounding `package.py` see `rez-package-definition`.

## How it runs

`commands()` is **not** plain Python at run time. Rez *interprets* it and emits target-shell code
(bash, zsh, csh, tcsh, sh, pwsh). Consequences:

- Only the documented rex API has meaning — arbitrary Python side effects do not survive.
- `print()` inside `commands()` does not write to the user's terminal in the way you expect;
  use `info()` / `error()`.
- Imports must be **inside** the function body.

## The `env` object

The `env` object is the common case and reads naturally:

```python
def commands():
    env.PATH.append("{root}/bin")
    env.PYTHONPATH.append("{root}/python")
    env.FOO_LIC = "{this.root}/lic"          # plain assignment == setenv
    env.MAYA_PLUG_IN_PATH.prepend("{root}/maya")
    env.SOME_VAR.unset()
```

Equivalent function-style API:

| `env` form | rex function | Effect |
|---|---|---|
| `env.X = v` | `setenv("X", v)` | set (overwrite) |
| `env.X.append(v)` | `appendenv("X", v)` | append to path-like var |
| `env.X.prepend(v)` | `prependenv("X", v)` | prepend to path-like var |
| `env.X.unset()` | `unsetenv("X")` | unset |
| — | `alias("name", "value")` | create a shell alias |
| — | `source("path")` | source a script |
| — | `error("msg")` | raise a user-visible error |
| — | `info("msg")` | print a message |
| — | `defined("VAR")` | `True` if the env var is set |
| — | `expandvars("{root}/bin")` | expand immediately |

### The first append overwrites

The **first** `append`/`prepend` on a given variable actually **overwrites** it. This is
deliberate: otherwise a system `PyQt` already on `PYTHONPATH` would still win over the version you
just resolved.

`PATH` is special-cased — it is not clobbered, because you would lose `ls`/`cd`. The system paths
(from a non-interactive shell's default `PATH`) are appended back after all commands are
interpreted.

## String expansion

Three flavors, and the difference matters:

| Package command | Equivalent bash |
|---|---|
| `env.FOO = literal("${USER}")` | `export FOO='${USER}'` |
| `env.FOO = expandable("${USER}")` | `export FOO="${USER}"` |
| `env.FOO = expandvars("${USER}")` | `export FOO="jbloggs"` |

- Object expansion (`{root}`, `{this.root}`, `{this.version.major}`) and env-var expansion
  (`$FOO`, `${FOO}`) normally happen automatically when a string reaches a rex call or `env`.
- A bare `var = "{root}/bin"` does **not** expand — wrap it: `var = expandvars("{root}/bin")`.
- `literal()` inhibits expansion; chain with `.expandable()` for mixed content:

```python
env.DESC = literal("the value of {root} is").expandable("{root}")
```

## Filepaths — always POSIX, even on Windows

```python
def commands():
    env.PATH.append("{root}/bin")   # forward slash, even on Windows
```

Rez normalizes to the target shell. It knows which variables are paths via the `pathed_env_vars`
config setting — by default any variable ending in `PATH`.

**Never** use `os.pathsep` or hardcoded `a:b` lists. On Git-for-Windows (git-bash) the shell's path
separator differs from the underlying system's, so these break portability.

## Order of execution

Two rules, in this precedence:

1. If package `A` was requested before `B`, `A`'s commands run before `B`'s.
2. **Unless** `A` requires `B` — then `B` runs first.

So for `rez-env maya_anim_tool-1.3+ PyYAML-3.10 maya-2015`, where `maya_anim_tool` requires `maya`
and `PyYAML` requires `python`:

```
maya → maya_anim_tool → python → PyYAML
```

This is why a Maya plugin can safely `append` to `MAYA_PLUG_IN_PATH` — Maya initialized it first.

## Branching on context

Objects available in `commands()`:

| Object | Use |
|---|---|
| `root` / `this.root` | install path of current variant |
| `base` / `this.base` | parent of the variant dirs |
| `this.version` | version, with `.major` / `.minor` / `.patch` |
| `building` | `True` during a build |
| `resolve` | mapping of resolved packages; `"maya" in resolve` |
| `ephemerals` | mapping of ephemeral packages |
| `in_context()` | `True` when part of a resolved context |
| `defined(name)` | env var presence |

A realistic example:

```python
def commands():
    import os.path                      # imports MUST be inline

    env.PYTHONPATH.append("{this.root}/python")
    env.PATH.append("{this.root}/bin")

    if building:                        # expose headers only to builds
        env.FOO_INCLUDE_PATH = "{this.root}/include"

    if defined("DEBUG_FOO"):
        conf_file = os.path.expanduser("~/.foo/config")
    else:
        conf_file = "{this.root}/config"
    env.FOO_CONFIG_FILE = conf_file

    if "maya" in resolve:               # only wire up maya bits when maya is present
        env.MAYA_PLUG_IN_PATH.append("{this.root}/maya/plugins")
        if resolve.maya.version.minor == "sp3":
            error("known issue with GL renderer in service pack 3, beware")

    env.FOO_LIC = "/lic/foo_{this.version.major}.lic"
```

## Build-time communication via `building`

Dependency packages use `building` to expose build-only information:

```python
# in boost's package.py
def commands():
    if building:
        env.CMAKE_MODULE_PATH.append("{root}/cmake")   # ships FindBoost.cmake
```

> **`commands()` is never executed for the package actually being built.** Use
> `pre_build_commands()` when you need code to run for the package under construction.

## Pre and post commands

- `pre_build_commands()` — runs for the package being built, before the build.
- `pre_test_commands()` — runs before the package's tests.

Both take the same rex API as `commands()`.

## Review checklist

- [ ] Imports are inside the function body.
- [ ] Forward slashes everywhere; no `os.pathsep`, no hardcoded `:`-joined paths.
- [ ] Guards use `building` / `in_context()` / `"pkg" in resolve` rather than assuming.
- [ ] The first `append` on a variable is understood to overwrite.
- [ ] `literal()` used where a `$VAR` must survive into the shell unresolved.

## Debug a commands section

```bash
rez-env mypkg --verbose            # more solver/command detail
rez-context --interpret            # show interpreted shell code
rez-test mypkg                     # run the package's own tests
rez-env mypkg -- printenv MY_VAR   # one-shot check without a subshell
```
