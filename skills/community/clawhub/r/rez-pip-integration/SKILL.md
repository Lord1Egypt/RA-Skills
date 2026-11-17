---
name: rez-pip-integration
description: "Converting pip packages into rez packages — rez-pip usage, install vs release vs custom prefix, choosing and pinning the python version, how rez-pip picks which pip to run, the python-MAJOR.MINOR dependency it writes, extra pip arguments, the pip_install_package API and InstallMode, and the failures that account for most broken conversions. Use when the user wants a PyPI package available as a rez package, or asks why a converted package will not resolve. Covers Rez 3.4.0."
---

# Rez pip integration

> **One-sentence summary**: `rez-pip` runs `pip install` inside a rezified python and converts the
> result — plus the dependencies it had to install — into rez packages, and it only goes one way:
> pip to rez, never rez to pip.

Skill scope: getting PyPI packages into rez. For authoring a `package.py` by hand see
`rez-package-authoring`; for the resolve that consumes the result see `rez-resolve`; for driving the
conversion from Python see `rez-python-api`.

## What rez-pip does

Rez is language agnostic, but python is everywhere, so rez knows how to translate a pip package into
a rez package. The conversion:

- downloads and installs the package with pip, inside a **rez** python package;
- writes a rez package for it, plus a rez package for each dependency pip had to install;
- gives each generated package a dependency on `python-MAJOR.MINOR`.

It does **not** do the reverse. There is no rez-to-pip converter, and upstream documents a
rewrite of `rez-pip` as a plugin to address most of its current limitations.

## Choosing the python version

This is the decision everything else follows from, so make it first and make it explicit:

```bash
rez-pip --install requests --python-version 3.11
```

`--python-version` names a **rez** `python` package version. rez resolves it, runs that
interpreter's pip, and the generated packages depend on `python-3.11`. Leave it out and you get the
latest `python` rez package, which is rarely what a studio wants.

If a package is not pure python — it ships a `.so` or a `.pyd` — it is built against one interpreter,
so **run rez-pip once per python version you need**. One conversion does not serve several pythons.

## Install, release, or a custom prefix

```bash
rez-pip --install foo                 # local_packages_path
rez-pip --install --release foo       # release_packages_path
rez-pip --install --prefix /studio/packages/int foo
```

Check where those actually point before you predict where a package will land:

```bash
rez-config local_packages_path
rez-config release_packages_path
```

`--install` is **required**; `rez-pip` without it errors out with `Expected one of: --install`. That
is deliberate — a conversion you did not ask to persist should not write into a package repository.

## Which pip runs

pip is too tightly coupled to the interpreter it ships with for rez to treat it as a normal
dependency, so rez-pip walks a fallback chain and prints what it picked:

1. pip inside the rezified `python` package named by `--python-version` (or the latest);
2. if that has none, pip inside a rezified `pip` package (backwards compatibility);
3. otherwise, the pip in rez's own virtualenv.

Whichever it lands on, pip must be **19.0 or newer** — that is a hard requirement.

Two consequences worth internalising:

- `--pip-version` does not exist. It was removed, because a pip version decoupled from an
  interpreter cannot be honoured.
- Install pip *into your python packages* rather than as its own rez package. Build python 2 with
  `--with-ensurepip` and upgrade it; python 3 already ships one, but check the version. Add `wheel`
  and refresh `setuptools` while you are there.

When installing into an interpreter by hand, make sure it lands in *that* interpreter:

```bash
/path/to/python -E -s -m pip install foo
```

`-E` ignores `PYTHON*` environment variables and `-s` takes your user site out of the equation.

## Flags

| Flag | Effect |
|---|---|
| `--python-version VERSION` | the rez `python` package to install with; becomes `python-MAJOR.MINOR` |
| `-i, --install` | actually install (required) |
| `-r, --release` | install into `release_packages_path` instead of local |
| `-p, --prefix PATH` | install into a custom package repository path |
| `-e, --extra ...` | pass the rest of the line through to `pip install` |
| `-v, --verbose` | verbose mode, repeatable |

`-e` / `--extra` takes everything after it, so it must be last. Anything you put there replaces
rez's pre-configured pip arguments rather than adding to them.

## Verifying a conversion

```bash
rez-search foo
rez-env foo -o context.rxt
rez-context context.rxt --so
```

`rez-search` proves the packages exist in a repository on your search path; the `rez-env` /
`rez-context` pair proves they actually resolve and shows you which `python` came along. Do both —
a conversion that wrote a package nobody can resolve is the common failure, not the rare one.

## The API

```python
from rez.pip import pip_install_package, InstallMode

installed, skipped = pip_install_package(
    "foo",
    python_version="3.11",
    release=False,
    prefix=None,
    extra_args=None,
    mode=InstallMode.min_deps,
)
```

It returns a 2-tuple of `Variant` lists: what was installed, and what was skipped because an
existing rez package already satisfied it. `InstallMode` has two members:

| Mode | Behaviour |
|---|---|
| `min_deps` | install only the dependencies that must be installed — reuse an existing rez package when it satisfies one. The default, and what the CLI uses |
| `no_deps` | install no dependencies. Fine for pure python; a package that must compile against a dependency will fail |

The signature also still carries `pip_version`, but the CLI no longer passes it and `--pip-version`
was removed — treat it as legacy.

## Troubleshooting

| Symptom | Cause |
|---|---|
| `Expected one of: --install` | `--install` is mandatory |
| Installed into the wrong repository | `-i` is local, `-r` is release, `-p PATH` overrides both |
| Package resolves on my machine only | it went to `local_packages_path`, which is per user |
| Import fails on another python | built against one interpreter; rerun per python version |
| pip is too old | pip must be >= 19.0; upgrade the pip inside the python package |
| Wrong wheel for the platform | rez-pip resolved a different `python` package than you think; pass `--python-version` |
| A dependency did not arrive | `min_deps` reuses an existing rez package when one satisfies it |
| Compile fails | the package needs a dependency rez did not install; try `InstallMode.min_deps` explicitly, or author the package by hand |

## Agent workflow

1. Decide the target python version first, and always pass `--python-version`.
2. Confirm the destination with `rez-config local_packages_path` and `rez-config release_packages_path`
   before you convert.
3. Convert with `--install`, adding `--release` or `--prefix` only when you mean it.
4. Verify with `rez-search` and a real `rez-env` resolve — existence is not resolvability.
5. For a non-pure package, repeat the conversion for every python version that needs it.
6. Reserve `-e` for a one-off pip workaround; a conversion that needs custom pip flags is a
   candidate for a hand-written `package.py` instead.
