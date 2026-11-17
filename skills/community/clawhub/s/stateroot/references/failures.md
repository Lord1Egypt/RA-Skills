# Bootstrap failures

Authoritative: https://stateroot.dev/docs/reference/faq

Quote CLI output. Do not hand-write `.stateroot/`, `~/.stateroot/`, or harness stubs.

| Symptom | Action |
| --- | --- |
| `version 'GLIBC_2.xx' not found` | Reinstall from the current GitHub latest (glibc 2.17+); the previous binary requires a newer glibc. |
| `stateroot --version` works, harnesses have no hooks | Run `stateroot setup` (this skill still applies). `stateroot install` is harness wiring only. |
| macOS Intel / unsupported architecture | Current macOS releases target Apple Silicon. Build from source (see install.md). |
| `doctor` non-zero | Broken local setup. Quote the output. Missing synthesis keys are not a failure. |
| Checksum mismatch / installer refuse | Fail closed. Re-download from the official latest release. Do not skip verification. |
| `not a stateroot project` | Project command on a tree with no `.stateroot/`. Run `stateroot init` from the repo root if the user wants this project on StateRoot — then expire this skill. |
| User hesitated to pipe `install.sh` | Stop. Give them the URL and the MSI/script to run themselves. |
| Setup already configured | Default is skip-unless-reconfigure. Do not pass `--blank-slate` unless they asked. |
| Public GitHub API quota exhausted | Current clients use public release metadata with checksum verification. Keep login optional; do not treat every `403` as a quota failure. |
| New supported agent missing from setup | Update the CLI, then rerun `stateroot install` to refresh integrations without resetting identity. |
| Want resume / checkpoint / memory | This skill has expired if setup ran. `stateroot skill show stateroot`. |
