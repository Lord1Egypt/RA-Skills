---
name: rez-cli
description: "Rez command-line reference — rez-env, rez-build, rez-release, rez-context, rez-search, rez-depends, rez-test, rez-config, rez-bind, rez-pip and the rest, with the flags that matter. Use when the user needs the right rez command or flag, or when running a build/release/test loop. Covers Rez 3.4.0."
---

# Rez CLI reference

> **One-sentence summary**: every subcommand is available both as `rez <cmd>` and `rez-<cmd>`;
> resolve with `rez-env`, build with `rez-build`, ship with `rez-release`, inspect with `rez-context`.

Skill scope: commands and flags. For concepts see `rez-core-concepts`; for resolve failures see
`rez-resolve-troubleshooting`.

## Full command list

| Command | Purpose |
|---|---|
| `rez-env` | Open a configured shell, possibly interactive |
| `rez-build` | Build a package from source |
| `rez-release` | Build a package from source and deploy it |
| `rez-context` | Print info about the current context or a `.rxt` file |
| `rez-search` | Search for packages |
| `rez-depends` | Reverse package dependency lookup |
| `rez-diff` | Compare the source of two packages |
| `rez-view` | View the contents of a package |
| `rez-config` | Print current rez settings |
| `rez-status` | Report status of the environment, a tool or a package |
| `rez-test` | Run tests listed in a package definition file |
| `rez-selftest` | Run rez's own unit tests (pytest if available) |
| `rez-bind` | Create a rez package for existing software |
| `rez-pip` | Install a pip package and its deps as rez packages |
| `rez-cp` / `rez-mv` / `rez-rm` | Copy / move / remove packages between repositories |
| `rez-pkg-cache` | Manipulate a package cache |
| `rez-pkg-ignore` | Disable a package so it is hidden from resolves |
| `rez-suite` | Manage suites |
| `rez-bundle` | Bundle a context and its packages into a relocatable dir |
| `rez-python` | Start python or run a script within rez's own context |
| `rez-interpret` | Execute some Rex code and print the result |
| `rez-help` | Display help for a given package |
| `rez-plugins` | List a package's plugins |
| `rez-memcache` | Manage and query memcache server(s) |
| `rez-benchmark` | Benchmark runtime resolves |
| `rez-yaml2py` | Print a `package.yaml` in `package.py` format |
| `rez-gui` | Run the Rez GUI application |
| `rez-complete` | Print package completion strings (hidden) |
| `rez-forward` | See `util.create_forwarding_script()` (hidden) |

Common flags on every subcommand: `-v/--verbose` (repeatable), `--debug`, `--profile FILE`.

## rez-env — resolve and enter

```bash
rez-env foo bah                      # interactive subshell
rez-env foo bah -- echo '$REZ_FOO_ROOT'   # one-shot, no subshell
rez-env 'python-2.6+' 'utils-1.1+<2'      # quote requests
rez-env foo -o context.rxt            # write context, don't enter
rez-env foo -i context.rxt            # load a saved context
```

Key flags:

| Flag | Effect |
|---|---|
| `-c, --command CMD` | run a command instead of opening a shell |
| `-s, --stdin` | read commands from stdin |
| `-o, --output FILE` | write the context (`.rxt`) and exit |
| `-i, --input FILE` | load a saved context |
| `--shell SHELL` | target shell (`bash`, `zsh`, `sh`, `csh`, `tcsh`, `pwsh`) |
| `--ni, --no-implicit` | drop implicit packages |
| `--nl, --no-local` | exclude locally installed packages |
| `-b, --build` | build environment instead of runtime |
| `--paths PATH` | override the package search path |
| `-p, --patch` | patch the resolve |
| `--patch-rank N` | apply additional patches |
| `--max-fails N` | report more failures (default first only) |
| `--fail-graph` | render the failure graph |
| `--no-cache` | bypass resolve caching |
| `--strict` | treat patch conflicts as errors |
| `--exclude/--include RULE` | filter packages in/out |
| `--no-filters` | ignore configured filters |
| `-q, --quiet` | suppress the banner |
| `-t, --time` / `--time-limit` | timestamp / limit for the resolve |
| `--rcfile` / `--norc` | shell rc handling |

## rez-build — build from source

```bash
rez-build                            # build only
rez-build --install                  # build + install to ~/packages
rez-build --clean                    # clean the build dir
rez-build -- -DMYVAR=YES             # pass args to the build system
```

Key flags:

| Flag | Effect |
|---|---|
| `-i, --install` | install to the local packages path |
| `-c, --clean` | clean before building |
| `-p, --prefix PATH` | install prefix |
| `--process local\|remote` | where the build runs |
| `-b, --build-system NAME` | force a build system |
| `--variants INDEX [INDEX…]` | build only specific variants |
| `--ba, --build-args ARGS` | args for the build system |
| `--cba, --child-build-args ARGS` | args for child builds |
| `-s, --scripts` | show shell scripts instead of running |
| `--view-pre` | view the pre-build resolved environment |
| `--fail-graph` | render the resolution failure graph |

Build system is auto-detected (`CMakeLists.txt` → cmake, etc.). A package can override it with the
`build_command` attribute. Build systems add their own flags to `rez-build -h` (e.g.
`--build-target` for cmake), and a `parse_build_args.py` in the package root lets you add custom
flags — they arrive as `__PARSE_ARG_<NAME>` env vars.

The build environment is assembled from `requires` → `build_requires` (transitive) →
`private_build_requires` → the current variant's requirements. CWD during the build is the **build
path**, not the package root — use `{root}` to reach scripts in the package root.

Local install loop:

```bash
# edit code
rez-build --install
rez-env mypackage        # in a separate shell; picks up the local install
```

You do not need a fresh `rez-env` after every install if requirements did not change.

## rez-release — build and deploy

```bash
rez-release -m "release message"
```

| Flag | Effect |
|---|---|
| `-m, --message MSG` | release message |
| `--vcs VCS` | version control system (`git`, `hg`, `svn`, `stub`) |
| `--no-latest` | do not set the package as latest |
| `--ignore-existing-tag` | proceed even if the VCS tag exists |
| `--skip-repo-errors` | continue past repository errors |
| `--no-message` | release without a message |

Releases to `release_packages_path` (default `~/.rez/packages/int`). Release hooks
(`amqp`, `command`, `emailer`) run around it; a `ReleaseHookCancellingError` from a hook cancels
the release.

## rez-context — inspect a resolve

```bash
rez-context                          # info about the current environment
rez-context context.rxt              # info about a saved context
```

| Flag | Effect |
|---|---|
| `--req, --print-request` | print the request |
| `--res, --print-resolve` | print the resolve |
| `--so, --source-order` | command execution order |
| `--su, --show-uris` | show package URIs |
| `-t, --tools` | list tools exposed by the resolve |
| `--which CMD` | which package provides a command |
| `-g, --graph` / `-d, --dependency-graph` | dot graphs |
| `--pg, --print-graph` / `--wg, --write-graph FILE` | compact / written graph |
| `--pp, --prune-package PKG` | prune the displayed graph down to `PKG` (graph output only, no re-resolve) |
| `-i, --interpret` | show the interpreted shell code |
| `-f, --format FMT` | output in a given shell format |
| `--diff RXT` | diff against another context |
| `--no-env` | interpret the context in an empty environment |
| `--fetch` | fetch missing packages |

`rez-context --so` and `rez-context --which` are the two cheapest answers to "what did I actually
get" and "where did this binary come from".

## rez-search / rez-depends / rez-test

```bash
rez-search maya                      # find packages
rez-search --validate mypackage      # validate a package definition
rez-depends python                   # who depends on python?
rez-test mypackage                   # run the package's tests
```

`rez-search` flags: `-t, --type`, `--nl, --no-local`, `--validate`, `--paths`, `-f, --format`.
`rez-depends` is the reverse-dependency lookup — reach for it before grepping `package.py` files.

## rez-config / rez-status / rez-bind / rez-pip

```bash
rez-config                           # all settings
rez-config packages_path             # one setting
rez-status                           # environment sanity
rez-bind python                      # wrap existing software as a rez package
rez-pip install requests             # pip package as rez packages
```

## Other useful ones

```bash
rez-pkg-ignore foo-1.0.0             # hide a bad package from resolves
rez-cp / rez-mv                      # move packages between repositories
rez-bundle context.rxt out_dir       # relocatable bundle
rez-interpret '"{root}"'             # test a rex expression
```

## Agent workflow

1. Prefer non-interactive forms — `-c`, `--output`, `rez-context` — over opening a subshell.
2. Scope output: `rez-context --so`, `rez-config <setting>`, `rez-search <pkg> -f <template>`.
3. `rez-status` first when something looks broken about the environment itself.
4. Use `rez-depends` for reverse lookups instead of broad greps.
5. Build → install → test in that order: `rez-build --install`, `rez-env <pkg>`, `rez-test <pkg>`.
