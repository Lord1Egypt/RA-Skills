# X List Digest

Collect authorized X lists, skip archived posts, and turn observed market viewpoints into one daily writing digest. Use a host agent for authenticated browsing and analysis; use deterministic scripts for fixed windows, limits, deduplication, Markdown and SQLite.

Version 2.0.0 replaces the former standalone HTTP/CLI wrappers with a host-native workflow. No private list, credentials, Feishu destination or enabled job ships in this repository.

## Features

- Incremental collection across days and lists with auditable frozen history.
- Fixed 24-hour windows and conservative 500-post / 45-minute / 300-step ceilings.
- Separate list/detail traversal; unknown ordering and incomplete threads remain partial.
- Top-five topic and writing-direction tables, category statistics and author-normalized ticker comparisons.
- Same-day deduplicated daily archive; Sunday weekly off-topic statistics with sample limitations.
- Optional native Feishu CLI archive with revisions, checkpoints and complete readback.

## Install

Use a trusted Agent Skills installer or place this directory in your host's skill discovery path. Review files before enabling execution. See [host adapters](references/agent-adapters.md).

After authorizing Python dependencies, create a package-local virtualenv:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/doctor.py
```

Python 3.11+ is required. Configure your own list aliases in `config.yaml`; see [example configuration](assets/config.example.yaml). The optional macOS Hermes browser preflight uses Hermes' existing Python, psutil, Chrome and previously authorized `~/.hermes/chrome-debug` profile at port 9234; it does not install these dependencies or log into X.

## Use

Ask your agent: "Run x-list-digest for list primary over 24 hours, output both." `both` means chat plus local files; `feishu` additionally requires a configured native CLI user profile and authorized root folder. Follow [SKILL.md](SKILL.md) for the complete collection, analysis, finish and readback sequence.

User data defaults to `~/.local/share/x-list-digest`, outside this package. Failed runs and source evidence are preserved. Scheduling is opt-in; `cron_runner.py` only previews parameters and does not install a scheduler. Provider, time and tool availability must be checked in the real host.

## Validation and limits

```sh
.venv/bin/python -m unittest discover -s tests
```

The local macOS Codex/Hermes adaptation has real incremental collection and native Feishu readback evidence. Public packaging tests cover the portable scripts; they do not establish every host's browser compatibility. The next natural scheduled run remains unverified. A protective stop or `window_boundary_unverified` is not complete 24-hour coverage. X DOM changes, incomplete text/media/thread evidence, sleeping hosts and expired authentication may block or reduce coverage.

## License and source

MIT-0. Maintained at [0xcjl/x-list-digest](https://github.com/0xcjl/x-list-digest). This release continues the same repository's original skill and its locally tested adaptations. No third-party skill is redistributed.
