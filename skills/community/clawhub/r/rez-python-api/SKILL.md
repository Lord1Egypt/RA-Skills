---
name: rez-python-api
description: "Rez Python API — ResolvedContext construction and inspection, Package/Variant objects, programmatic resolves, .rxt context serialisation and deserialisation, running commands inside a context, and the module entry points (rez.resolved_context, rez.packages, rez.config, rez.pip, rez.suite, rez.bundle_context). Use when the user wants to drive rez from Python instead of the CLI, or asks what a context object actually holds. Covers Rez 3.4.0."
---

# Rez Python API

> **One-sentence summary**: `ResolvedContext` is the whole product — build one from a list of request
> strings, read the result off `success`, `resolved_packages` and `get_environ()`, persist it with
> `save()` / `load()`, and only open a shell through `execute_shell()` when you really need one.

Skill scope: embedding rez in Python. For the CLI equivalents see `rez-cli`; for solver internals see
`rez-resolve`; for a context used as a deliverable artifact see `rez-suites-bundles`.

## Before you embed rez

Two warnings straight from upstream `docs/source/api.rst`, and both change the design of a tool:

- **There are no compatibility guarantees between rez versions.** Pin the rez you import, the same
  way the CLI lanes in this repository pin `REZ_VERSION`.
- **Config is read once, at first import.** The Python API cannot reread configuration files or
  switch to a different `REZ_CONFIG_FILE` afterwards. A tool that has to change config mid-run must
  shell out to the CLI instead.

Confirm what you are actually about to import before you trust any of the code below:

```bash
rez-status
```

## Module entry points

| Module | What it holds |
|---|---|
| `rez.resolved_context` | `ResolvedContext` — a resolve, and everything you do with one |
| `rez.packages` | `Package`, `Variant`, `iter_packages`, `get_package`, `get_variant`, `get_latest_package_from_string` |
| `rez.config` | `config` — the merged, live settings object |
| `rez.resolver`, `rez.solver` | `Resolver`, `ResolverStatus`, the solver itself |
| `rez.suite` | `Suite` — see `rez-suites-bundles` |
| `rez.bundle_context` | `bundle_context` — see `rez-suites-bundles` |
| `rez.pip` | `pip_install_package` — see `rez-pip-integration` |
| `rez.developer_package` | build a package from source in-process |
| `rez.package_repository`, `rez.package_resources` | repositories and the resources they hand out |
| `rez.version` | `Version`, `VersionRange`, `Requirement`, `RequirementList`, `VersionError` |
| `rez.exceptions` | every rez error type; all of them derive from `RezError` |
| `rez.wrapper` | the module behind the main console script |

## Constructing a context

```python
from rez.resolved_context import ResolvedContext

# Requests are plain strings, exactly what you would pass to rez-env.
context = ResolvedContext(["foo-1", "bar"])

if not context.success:
    raise SystemExit(context.failure_description)
```

`ResolvedContext(requests, ...)` takes the request list positionally. The arguments worth knowing:

| Argument | Meaning |
|---|---|
| `verbosity` | 0, 1 or 2 — the same levels `rez-env -v` gives you |
| `timestamp` | epoch time; ignore packages released after it |
| `building` / `testing` | resolve as if for `rez-build` / `rez-test` |
| `caching` | `None` defers to the `resolve_caching` setting; `False` bypasses caches |
| `package_paths` | override `packages_path` for this resolve only |
| `package_filter` | a `PackageFilterList`; `rez.package_filter.no_filter` removes filtering |
| `add_implicit_packages` | append the `implicit_packages` (default `True`) |
| `max_fails` / `time_limit` | stop after N failures / after N seconds |

Set `verbosity=1` before reaching for a debugger: the solver trace is the same one `rez-env -v`
prints.

## Reading the result

```python
context.status                    # ResolverStatus.solved | .failed | .aborted | .pending
context.success                   # True when status is solved
context.failure_description       # why it failed, when it did
context.requested_packages()      # [Requirement, ...] — the request; implicits only if include_implicit=True
context.resolved_packages         # [Variant, ...] — what the solver picked
context.resolved_ephemerals       # resolved ephemeral (implicit-ish) packages
context.get_resolve_as_exact_requests()   # ['foo==1.1.0', ...] — pin the resolve down
context.get_environ()             # dict: the environment the context would produce
context.get_tools()               # {tool_name: (Variant, [alias, ...])}
context.which("foo")              # absolute path to a tool, or None
context.get_resolved_package("foo")       # the Variant, or None
context.print_info(source_order=True)     # the rez-context --so view, on stdout
```

`resolved_packages` yields `Variant` objects, not `Package` objects. A `Package` is a family; a
`Variant` is one resolved member of it, with `.name`, `.version`, `.qualified_name`, `.root`,
`.requires`, `.tools` and `.data` on it. Reach for `get_resolved_package(name)` when you want one
package out of a resolve, and `get_environ()` when you want the environment without running
anything.

## Context files (`.rxt`)

A context serialises to a `.rxt` file, which is how a resolve becomes something you can hand to
another process, another machine, or another day:

```python
context.save("context.rxt")                # write it
same = ResolvedContext.load("context.rxt") # read it back

# Or keep it in memory:
from io import StringIO
buf = StringIO()
context.write_to_buffer(buf)
buf.seek(0)
again = ResolvedContext.read_from_buffer(buf)

# Or move it through your own dict/JSON pipeline:
data = context.to_dict()
rebuilt = ResolvedContext.from_dict(data)
```

`save()` / `load()` and `write_to_buffer()` / `read_from_buffer()` round-trip the resolve, not the
environment — loading is cheap, and no package payload is re-read. `to_dict()` carries the metadata
(`status`, `package_requests`, `resolved_packages`, `failure_description`, `serialize_version`,
`rez_version`, ...) rather than a stable public schema; treat it as rez's own format, not as an API
you own.

`validate()` re-checks the context and raises `ResolvedContextError` when it no longer holds; call
it before trusting a context that has been sitting on disk.

## Running things inside a context

```python
# One command, non-interactive, with the context's environment:
proc = context.execute_command(["foo", "--version"])
print(proc.returncode)

# The environment as shell source, without starting a shell:
code = context.get_shell_code()

# An interactive shell — blocks, so only do this in a real terminal:
context.execute_shell(block=True)
```

Prefer `execute_command()` and `get_environ()` in automation. `execute_shell()` inherits the
terminal, so it is the wrong call in a service or a test; `get_shell_code()` takes a `style` of
`OutputStyle.file` (writable into a script) or `OutputStyle.eval` (sourceable in one shot).

## Packages and variants

```python
from rez.packages import iter_packages, get_package, get_latest_package_from_string

for package in iter_packages("foo"):          # every version of one family
    print(package.version)

package = get_package("foo", "1.1.0")         # one exact package, or None
latest = get_latest_package_from_string("foo")
```

`get_latest_package_from_string` accepts the same spellings a request does, so it is also the
cheapest way to turn a user-supplied string into a concrete package. `iter_packages` walks the
search path; both take `paths=` when you need to point them at a specific repository.

## Configuration

```python
from rez.config import config

config.packages_path
config.local_packages_path
```

`config` is the merged settings object, so an attribute read is the answer to "what took effect",
not "what is in the file". It is read at import — see the warning at the top.

## Errors

Every rez exception derives from `RezError` (`rez.exceptions`), so one `except RezError` catches
the library. The ones you are most likely to handle:

| Exception | Raised by |
|---|---|
| `ResolveError` | a resolve that cannot be performed |
| `PackageNotFoundError` / `PackageFamilyNotFoundError` | a package that is not there |
| `PackageRequestError` | a malformed request string |
| `ResolvedContextError` | `validate()` on a context that no longer holds |
| `SuiteError` | suite operations — see `rez-suites-bundles` |
| `ContextBundleError` | bundling — see `rez-suites-bundles` |

## Cross-check against the CLI

When an API result looks wrong, reproduce it with the CLI before you debug your own code — the CLI
is the reference implementation and it reads the config fresh:

```bash
rez-env foo -o context.rxt --no-cache   # ResolvedContext(..., caching=False)
rez-context context.rxt --so            # context.print_info(source_order=True)
```

`rez-context --so` prints exactly the `requested packages` / `resolved packages` split that
`context.print_info(source_order=True)` prints, and `-v` on `rez-env` is the same trace you get from
`verbosity=1`.

## Gotchas

| Symptom | Cause |
|---|---|
| Config changes ignored | rez was already imported; the API cannot reread config. Use the CLI |
| `resolved_packages` order surprises you | it is solver order; only `print_info()` sorts, and `source_order=True` skips that sort |
| Attribute missing after an upgrade | no cross-version API guarantees — pin rez |
| A resolve differs from `rez-env` | compare `package_paths`, `add_implicit_packages` and `caching` |
| `execute_shell()` hangs in CI | it wants a terminal; use `execute_command()` |

## Agent workflow

1. Import rez once, at the top of the process; never rely on rereading config afterwards.
2. Build one `ResolvedContext`, then read `success` and `failure_description` before anything else.
3. Inspect with `resolved_packages` / `get_environ()` / `get_tools()` instead of opening a shell.
4. Persist with `save()` when another process needs the resolve; `validate()` it before trusting it.
5. When the API and the CLI disagree, believe the CLI and diff the arguments above.
