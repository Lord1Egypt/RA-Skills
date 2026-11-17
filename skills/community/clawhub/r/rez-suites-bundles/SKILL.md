---
name: rez-suites-bundles
description: "Rez suites and context bundles — rez-suite to expose tools from several contexts behind one PATH entry, suite tool aliasing, prefixing, hiding, bumping and control arguments (++help, ++about, ++patch, ++peek), and rez-bundle / bundle_context() to package a resolve with its packages into a relocatable directory. Use when the user wants to ship a resolved environment to artists, a render farm, a container or another machine. Covers Rez 3.4.0."
---

# Rez suites and context bundles

> **One-sentence summary**: a **suite** is a directory of contexts plus wrapper scripts that makes
> tools from different resolves look like one `PATH` entry; a **context bundle** is a directory that
> carries the context *and its packages*, so the whole thing can be moved somewhere else.

Skill scope: delivering a resolve to somewhere other than your own shell. For the resolve itself see
`rez-resolve`; for the objects these commands are built on see `rez-python-api`; for the command
reference see `rez-cli`.

## Which one do I want?

| | Suite | Context bundle |
|---|---|---|
| Holds | contexts + wrapper scripts | one context + its packages |
| Packages stay where they are | yes — absolute refs to shared repos | no — copied into the bundle, refs become relative |
| Relocatable | no | yes |
| Typical use | artist workstations, `PATH` entry | farm, container, server, air-gapped copy |
| Built by | `rez-suite` | `rez-bundle` |

## Suites

A suite is a directory containing a set of contexts and wrapper scripts that run tools within those
contexts. Put its `bin` directory on `PATH` and `foo` resolves to the wrapper, which resolves to the
right context — the artist never has to know.

### Building one

```bash
rez-env foo -o foo.rxt
rez-suite --create mysuite
rez-suite --add foo.rxt --context fooCtx mysuite
export PATH=$PWD/mysuite/bin:$PATH
```

`--add` copies the context into `mysuite/contexts/<name>.rxt`, and `--context` is the label it gets
inside the suite. The label is what every other context-scoped option refers to, so name it after
what the context is for, not after the file you happened to save it as.

### rez-suite flags

| Flag | Effect |
|---|---|
| `--create` | create an empty suite at `DIR` |
| `-a, --add RXT` | add a context to the suite (needs `--context`) |
| `-c, --context NAME` | which context a context-scoped option applies to |
| `-r, --remove NAME` | remove a context |
| `-d, --description DESC` | set a context's description |
| `-p, --prefix PREFIX` / `-s, --suffix SUFFIX` | prefix/suffix every tool in the context |
| `--hide TOOL` / `--unhide TOOL` | hide or expose one tool |
| `--alias TOOL ALIAS` / `--unalias TOOL` | give one tool a different name |
| `-b, --bump NAME` | raise a context's priority so its tools win |
| `-P, --prefix-char CHAR` | change the control-argument prefix (default `+`; `""` disables) |
| `-t, --tools` | list the tools the suite exposes |
| `--which TOOL` | print the path of a suite wrapper |
| `-l, --list` | list visible suites |
| `--validate` | check the suite is internally consistent |
| `--find-request PKG` / `--find-resolve PKG` | which contexts contain `PKG` in the request / the resolve |
| `-i, --interactive` | open a shell in a suite context (needs `--context`) |

### Which tools get exposed

A suite exposes the `tools` attribute of the packages in a context's **requests**. Three rules
follow from that, and they explain most "my tool is missing" reports:

- Packages pulled in as dependencies do **not** expose their tools.
- Weak references (`~foo-1`) and conflict requests (`!foo`) do **not** expose their tools.
- If two contexts expose the same tool name, one is a conflict; `--bump`, aliasing or prefixing
  resolves it.

Prefixing and suffixing are the cheap way to offer the same tool from two contexts at once:

```bash
rez-suite --add foo2017.rxt --context foo2017 mysuite
rez-suite --suffix _beta --context foo2017 mysuite
rez-suite --tools mysuite
```

That gives you `foo` from the stable context and `foo_beta` from the new one.

### Control arguments

Suite wrappers pass their arguments through to the real tool, except for rez's own *control*
arguments, which use `+` instead of `-`:

```bash
foo ++help
foo ++about
foo ++versions
foo +i
foo +p bar-2
foo ++peek
foo ++command 'printenv FOO_VERSION'
foo ++no-rez-args --not-a-rez-flag
```

| Control arg | Meaning |
|---|---|
| `+h, ++help` | wrapper usage |
| `+a, ++about` | which suite, context and package the wrapper comes from |
| `++versions` | versions of the package providing the tool |
| `+i, ++interactive` | interactive shell in the tool's environment |
| `+p, ++patch PKG...` | run the tool in a patched environment |
| `++strict` | strict patching (ignored without `++patch`) |
| `++nl, ++no-local` | do not load local packages when patching |
| `++command`, `++stdin` | run commands instead of the tool |
| `++peek` | diff the tool's context against a re-resolve — how stale it is |
| `++verbose`, `++quiet` | output control |
| `++no-rez-args` | pass everything through, even `+` args |

If a target tool uses `+` for its own arguments, change rez's prefix with `--prefix-char`.

### The Suite object

```python
from rez.suite import Suite
from rez.resolved_context import ResolvedContext

suite = Suite()
suite.add_context(name="fooCtx", context=ResolvedContext.load("foo.rxt"))
suite.save("mysuite")

reloaded = Suite.load("mysuite")
reloaded.context_names                 # ['fooCtx']
reloaded.set_context_suffix("fooCtx", "_beta")
reloaded.validate()                    # raises rez.exceptions.SuiteError when broken
```

`context_names` lists the labels, `tools_path` is the `bin` directory to put on `PATH`,
`get_tools()` is the alias-to-tool mapping, and `Suite.print_info()` dumps the whole thing.

## Context bundles

A context bundle is a directory holding a context and a package repository containing every package
the context uses. Package references in the `.rxt` become **relative**, which is what makes the
bundle relocatable — copy it to a server, a container or a USB stick and nothing points back at
your shared storage.

```bash
rez-env foo -o foo.rxt
rez-bundle foo.rxt ./mybundle
```

The result:

```text
.../mybundle/
   ./context.rxt
   ./packages/
      <standard package repository layout>
```

Run something out of it by pointing `rez-env` at the bundled context:

```bash
rez-env -i ./mybundle/context.rxt -- foo-tool
```

### rez-bundle flags

| Flag | Effect |
|---|---|
| `-s, --skip-non-relocatable` | leave non-relocatable packages where they are instead of failing |
| `-f, --force` | bundle anyway, even when a package says it cannot be relocated |
| `-n, --no-lib-patch` | skip the library-patching step |
| `-v, --verbose` | verbose mode |

`-s`, `-f` and `-n` all sit in one mutually exclusive group: pass at most one of them.

### Library patching

A compiled library inside a package can carry an absolute `rpath`/`runpath` to a library in another
package, which would silently resolve *outside* the bundle. Bundling rewrites those references to
`$ORIGIN`-relative paths pointing at the copy inside the bundle, and the step is platform-specific
(linux rewrites ELF headers with `patchelf`). References that have no equivalent inside the bundle —
a system library, say — are left alone, which is why a bundle is rarely *completely* hermetic.

### The bundle API

```python
from rez.bundle_context import bundle_context
from rez.resolved_context import ResolvedContext

context = ResolvedContext(["foo-1"])
bundle_context(context, "./mybundle", force=True)
```

`bundle_context(context, dest_dir, force=False, skip_non_relocatable=False, quiet=False,
patch_libs=False, verbose=False)` is the same operation as `rez-bundle`; note that the CLI passes
`patch_libs=True` unless you give it `--no-lib-patch`, while the API default is off.

## Troubleshooting

| Symptom | Check |
|---|---|
| A tool is missing from the suite | was it in the *request*? dependencies and weak refs expose nothing |
| Two tools fight | `rez-suite --tools`; fix with `--bump`, `--alias` or `--prefix`/`--suffix` |
| Wrappers ignore your suite after an edit | re-run `rez-suite --validate`; wrappers are regenerated on save |
| The tool uses `+` itself | `rez-suite --prefix-char` |
| `rez-bundle` refuses a package | relocatable is off; decide between `-s` (skip it) and `-f` (force it) |
| A bundled tool loads a library from outside | library patching; check the platform and drop `-n` |
| Bundle works here, not there | the bundle is only as portable as its payloads; check `--validate` and `--peek` |

## Agent workflow

1. Decide first: shared disk and many tools means a suite; anywhere-but-here means a bundle.
2. For a suite, build the contexts with `rez-env ... -o`, then add them one at a time with
   `rez-suite --add ... --context <name>`.
3. Confirm exposure with `rez-suite --tools` before telling anyone to put `bin` on `PATH`.
4. For a bundle, resolve, bundle, then *run the bundled context* — a bundle you have not executed is
   a guess.
5. Re-check both with `rez-suite --validate` and `rez-context context.rxt --so` after a package
   changes.
