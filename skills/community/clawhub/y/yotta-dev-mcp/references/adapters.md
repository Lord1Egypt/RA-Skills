# Optional external adapters

`run_adapter` probes and explicitly runs mature third-party tools that the user
already installed. The core engine stays Python-standard-library-only; adapters
are optional evidence sources, never a required dependency.

## Adapter matrix

| Adapter | License | What it adds | Required config |
|---|---|---|---|
| `import-linter` | BSD-2-Clause | Python import boundaries and layered contracts | `.importlinter`, `setup.cfg`, `tox.ini` or `pyproject.toml` |
| `dependency-cruiser` | MIT | JavaScript / TypeScript dependency rules | `.dependency-cruiser.js` / `.cjs` / `.mjs` / `.json` |
| `repomix` | MIT | Repository packing and context budget enforcement | optional `repomix.config.json` |

## Commands

`action=list` only inspects the project-local `node_modules/.bin`, project
virtualenv directories and `PATH`. It does not execute anything. Each adapter
entry reports `available`, `ready`, `executable`, `executable_source`, `config`
and a reason when it is not ready.

`action=run` requires `allow_execute=true` and exactly one adapter. The command
arguments are fixed by the adapter implementation:

```text
lint-imports --config <detected-config>
depcruise --config <detected-config> --output-type json --progress none --exclude node_modules <target>
repomix --stdout --style xml --quiet --no-git-sort-by-changes [--token-budget N] <target>
```

No adapter accepts arbitrary arguments, shell strings, remote repositories or
package installation. Repomix never receives `--remote` or
`--no-security-check`.

## Output

The run result contains:

- `status`: `PASS`, `FAIL` or `UNKNOWN`;
- `adapter`: detected executable, source, config and version;
- `command`: fixed argv, relative cwd, exit code, timeout flag and output hash;
- `findings`: normalized adapter violations with rule, severity, path and target;
- `content`: Repomix-only packed text metadata and bounded text;
- `next_step`: what to install, configure or rerun when the result is not PASS.

Missing tools, missing required config, invalid JSON output, timeouts and
non-whitelisted execution all degrade to `UNKNOWN`. Adapter findings are
reported separately; they do not silently change the status of
`system_model`, `architecture_review`, `impact_analysis` or `verify_change`.

## Safety boundary

Adapters are local-only and deterministic under the same repository state:

- executable discovery is limited to the project `node_modules/.bin`, project
  virtualenvs and `PATH`;
- execution uses a fixed argv with `shell=False`;
- the working directory and target must stay inside the repository;
- output is bounded, hashed and never contains wall-clock timestamps;
- no package is installed, downloaded or updated by this tool.

## Command line

```bash
python scripts/dev_engine.py adapter . --action list
python scripts/dev_engine.py adapter . --action run --adapter import-linter --allow-execute
python scripts/dev_engine.py adapter . --action run --adapter dependency-cruiser --allow-execute
python scripts/dev_engine.py adapter . --action run --adapter repomix --allow-execute --token-budget 50000
```
