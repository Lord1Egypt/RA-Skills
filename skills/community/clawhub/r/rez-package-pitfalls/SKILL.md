---
name: rez-package-pitfalls
description: "The package.py execution model and the errors it produces — why a top-level `from x import SomeClass` makes the installed package.py unparseable, why module-scope values are frozen on the build machine, why `env`/`this`/`root` look undefined to linters, and why a failed rez-build can leave a broken install behind. Use when a package resolves or builds with a confusing error, when reviewing a package.py for module-scope mistakes, or before releasing one. Covers Rez 3.4.0."
---

# Rez `package.py` pitfalls

> **One-sentence summary**: rez `exec`s `package.py` once at build time and writes every surviving
> module-level name back out as Python source, so anything at module scope that is not a plain
> value, a function or a module lands in the installed `package.py` as text that no longer parses.

Skill scope: **what rez does to `package.py` and when**. For the attribute reference and the
`@early`/`@late` mechanics see `rez-package-definition`; for the `commands()` body and the rex API
see `rez-package-commands`; for the version/variant/range decisions and the rest of the
anti-pattern list see `rez-package-authoring`.

Every pitfall below was reproduced against Rez 3.4.0, and the error text is copied from a real
run with only the host, user and timestamp replaced by placeholders.

## The three phases

| Phase | When it runs | What it does to `package.py` |
|---|---|---|
| **Load** | every time rez reads a package, including during `rez-build` | `exec`s the file; every module-level name is collected as a candidate attribute |
| **Serialize** | on `rez-build` / `rez-release` | writes the surviving attributes back out as a new `package.py` into the install |
| **Interpret** | on `rez-env` and every other resolve | runs `commands()` through rex and emits shell code; **does not** run the module body |

Two consequences drive every pitfall here: the module body is **Python** evaluated **on the build
machine**, and `commands()` is **not** Python at resolve time.

## Pitfall 1 — a top-level `from x import SomeClass` breaks the installed package

### Symptom

`rez-build --install` fails while *resolving the build environment*, before your build command ever
runs. The named file is a temporary copy, not your source.

### Trigger

Any module-level name bound to something that is not a plain value, a function, a module or a
`__`-leading name. The most common shape is importing a **class** at the top of the file:

```python
from pathlib import Path          # Path is a class, so it survives serialization

documents_path = Path.home().as_posix() + "/Documents/.p4config"

name = "foo"
version = "1.0.0"
```

### Actual error

```text
Resolving build environment:
resolved by builder@BUILD-HOST, on Fri Oct 02 01:05:17 2026, using Rez v3.4.0

requested packages:
~platform==windows           (implicit)
~arch==AMD64                 (implicit)
~os==windows-10.0.26100.SP0  (implicit)

resolved packages:
01:05:17 ERROR    ResourceError: Problem loading C:\Users\<user>\AppData\Local\Temp\rez_write__epzwl2x\package.py: invalid syntax (package.py, line 12)

Invoking custom build system...
```

The `rez_write_<random>` directory is rez's own temp copy of the definition
(`rez/serialise.py`, `prefix="rez_write_"`), so the path in the message never points at the file you
edited. The offending line is what rez wrote, not what you wrote — here line 12 of the generated
file is:

```python
Path = <class 'pathlib.Path'>
```

`package.py` attributes are dumped with `pformat()`, and the `repr` of a class object is not valid
Python source.

### Correct form

Import inside `commands()`, and keep the value out of the module scope entirely:

```python
name = "foo"
version = "1.0.0"


def commands():
    # Import inside commands() so the module is not captured as a package
    # attribute: rez serializes module-level names into the installed
    # package.py, and a class object renders as invalid syntax.
    from pathlib import Path

    documents_path = Path.home().as_posix() + "/Documents/.p4config"
    env.P4CONFIG.set(documents_path)
```

The installed `package.py` then carries `name`, `version`, `commands`, `timestamp` and
`format_version` — and nothing else. The last two are rez's, not yours: `timestamp` defaults to the
install time and `format_version` is always written by the filesystem package repository
(`rezplugins/package_repository/filesystem.py`), so expect both after every `rez-build --install`.

## Pitfall 2 — module-scope values are frozen on the build machine

### Symptom

A package works on the machine that released it and is wrong everywhere else: a per-user path, a
hostname, a `sys.prefix` or a `os.getcwd()` result points at the *builder's* machine.

### Trigger

Computing anything environment-dependent at module scope:

```python
import sys
from pathlib import Path

sys_path = sys.prefix                                    # frozen at build time
documents_path = Path.home().as_posix() + "/Documents/.p4config"
```

### Why

The module body runs once, during `rez-build`, and its **results** are written into the install.
This is what lands in the installed `package.py`:

```python
sys_path = 'C:\\Users\\<user>\\AppData\\Local\\Programs\\Python\\Python312'

documents_path = 'C:/Users/<user>/Documents/.p4config'
```

Note that `sys_path` survived even though `sys` itself did not — the module was stripped, the string
it produced was not.

### Correct form

Move anything that depends on *who* or *where* the resolve runs into `commands()`, which is
interpreted on the consumer's machine at resolve time:

```python
def commands():
    from pathlib import Path

    env.P4CONFIG.set(Path.home().as_posix() + "/Documents/.p4config")
```

Use `@early()` only for values that are genuinely a property of the build — see
`rez-package-definition`.

## Pitfall 3 — `env`, `this` and `root` are undefined names to your linter

### Symptom

Your editor or CI linter flags `package.py` even though it works perfectly in rez.

### Trigger

Any use of a name that rez injects. Rez binds `this`, `version`, `root` and `base` only while it
interprets `commands()` (`resolved_context.py`), and `env` is the rex environment object. None of
them exists when the file is read as ordinary Python.

### Actual error

```text
F821 Undefined name `env`
 --> package.py:6:5
  |
5 | def commands():
6 |     env.PYTHONPATH.prepend("{this.root}/site-packages")
  |     ^^^
```

### Correct form

Silence it at the point of use, which documents the intent for the next reader:

```python
env.PYTHONPATH.prepend("{this.root}/site-packages")  # noqa: F821
env.RESOURCE_PATH.prepend("{this.root}/resource")    # noqa: F821
```

Do not "fix" it by defining `env` or `root` yourself at module scope — that shadows rez's binding and
creates a real package attribute that then gets serialized (pitfall 1 and 2).

## Pitfall 4 — a failed build can leave a broken install on the package path

### Symptom

You fix `package.py`, rebuild, and the *same* error comes back — now naming the installed copy
instead of a temp file.

### Trigger

A failed `rez-build --install` leaves a package behind whenever the run got as far as writing the
install. Whether it did depends on where the build stopped: the failure in pitfall 1 happens while
resolving the build environment, before the build system is invoked, so that run installs nothing —
but a failure during or after the install step does leave the payload in place. When an install is
left behind, every later resolve and every later build of that package fails while reading it,
whatever your source now says.

### Correct form

Check whether the failed run left an install behind before deleting anything — the answer is not
always yes:

```bash
rez-search foo                 # is foo visible, and at which version?
```

If it is, remove that version and rebuild:

```bash
rm -rf <packages_path>/foo/1.0.0
rez-build --install
```

Then verify in a fresh resolve, not in the build shell:

```bash
rez-env foo
rez-context --so
```

## What survives at module scope

Reproduced on 3.4.0 by loading each snippet and dumping the installed form:

| Module-level statement | Survives? | Written as |
|---|---|---|
| `import sys` | no — module stripped | — |
| `sys_path = sys.prefix` | **yes** | `'C:\\Users\\<user>\\...\\Python312'` (build machine) |
| `from os.path import join` | no — function stripped | — |
| `def _helper(): ...` | no — plain function stripped | — |
| `from pathlib import Path` | **yes** | `Path = <class 'pathlib.Path'>` — unparseable |
| `class Helper: ...` | **yes** | `Helper = <class 'Helper'>` — unparseable |
| `my_re = re.compile(r'foo-\d+')` | **yes** | `my_re = re.compile('foo-\\d+')` — parses, then `NameError: name 're' is not defined` |
| `my_const = 'hello'` | **yes** | `'hello'` — a normal attribute, this is the intended use |

The rule rez applies is narrow: it strips **modules**, **functions** (except `commands`,
`pre_commands`, `post_commands`, `pre_build_commands`, `pre_test_commands`, `preprocess`, `@early`
and `@late`) and `__`-leading names. Everything else stays.

Surviving values fail in two different ways, and which one you get tells you where to look. A
`repr` that is not valid Python (`Path = <class 'pathlib.Path'>`) fails while **parsing**, with
`invalid syntax`. A `repr` that *is* valid Python but names a stripped module
(`my_re = re.compile(...)`) parses cleanly and fails while **executing**, with `NameError`. Both
reach you as `ResourceError: Problem loading <path>: <reason>`, so read the reason, not just the
exception type.

## Review checklist

- [ ] No class, instance or other non-plain object is bound at module scope — imports live inside
      `commands()` or inside `@late()`.
- [ ] Nothing environment-dependent (`Path.home()`, `os.getcwd()`, `sys.prefix`, `os.environ`) is
      computed at module scope.
- [ ] Every `env` / `this` / `root` use in `commands()` carries `# noqa: F821` if the repo lints
      `package.py`.
- [ ] No `env`, `this` or `root` is defined at module scope to "satisfy" a linter.
- [ ] `rez-build --install` exits 0 **and** `rez-env <pkg>` resolves — a non-zero build may still
      have written an install.
- [ ] After a serialization failure, `rez-search <pkg>` was used to check for a broken install, and
      any that was found was removed before rebuilding.

## Agent workflow

1. Read the error's file path first: a `rez_write_*` temp path means the generated package, a
   `packages_path` path means an already-installed one.
2. Grep the module scope of `package.py` for `import`, `class`, and anything that is not a literal
   before suspecting the solver.
3. Move imports into `commands()`; move environment-dependent values into `commands()` too.
4. Check for a broken install left by the previous attempt (`rez-search <pkg>`), remove it if
   present, then `rez-build --install`.
5. Confirm with `rez-env <pkg>` in a separate shell — a green build proves the file parses, not that
   it resolves.
