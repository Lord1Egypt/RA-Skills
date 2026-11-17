# How a Strix scan works

Strix is a host-side Python CLI that drives a team of LLM agents. The agents validate weaknesses on targets the operator named. A finding is written only after the agent has a concrete proof, or, for a dependency advisory, a version match plus a contextual rating. The product of a run is the directory under `strix_runs/`, not the scrolling log.

Two trees of "skills" exist. `skills/` at the repo root (this file's parent) is for coding agents that operate Strix. `strix/skills/` is loaded by the pentest agents during a scan: vulnerability playbooks, framework notes, scan-mode behavior, and tool usage. Loading this consumer skill does not load those playbooks into your context.

## Processes

```
checkout (uv run strix)
  ├─ settings: environment, then ~/.strix/cli-config.json
  ├─ Docker: ensure STRIX_IMAGE exists, else pull it
  ├─ one sandbox container per run (Kali, STRIX_IMAGE)
  │    terminal, Python, browser, Caido proxy, scanners
  └─ LLM API (STRIX_LLM) for the root agent and every child
```

The host process coordinates. Tool execution that touches the target happens in the container. A local directory passed with `-t` is bind-mounted into that container writable, `.git` excepted, so the agents can read and edit the real tree. A git repository URL is cloned under the run directory and mounted from there. A URL, domain, or IP is reached over the network from the container.

`localhost` and `127.0.0.1` in a target are rewritten to `host.docker.internal` before the scan, so a dev server on the host is reachable from the container.

Startup order that matters when a run never begins:

1. `STRIX_LLM` missing → exit 1, no run directory.
2. Docker CLI missing or the daemon unreachable → exit 1.
3. `STRIX_IMAGE` not present locally → pull that name. A locally built `strix-sandbox:dev` is used only when `STRIX_IMAGE` names it.
4. LLM preflight fails → `LLM CONNECTION FAILED`, exit 1. The preflight wait is `LLM_PREFLIGHT_TIMEOUT` (default 30 seconds), separate from `LLM_TIMEOUT`.

## Who does the testing

The root agent orchestrates. It decomposes scope, writes a threat model, spawns specialists, and writes the executive report. It does not run scanners or send exploit payloads itself. Children do reconnaissance, vulnerability testing, and proof-of-concept work, then report back.

Children share a threat model (`get_threat_model` / `save_threat_model` / `amend_threat_model`) and a coverage ledger. On a repository target the root derives the threat model from source before hunters start. On a black-box target, reconnaissance runs first and the model is written from what answered.

Each agent gets a slice of `strix/skills/` chosen for its task, plus the scan-mode skill (`quick`, `standard`, or `deep`). Those files tell the agent which attacks to try. They are not findings.

Agent tools on the host side of the loop include creating and messaging agents, notes, todos, the coverage ledger, the threat model, web search (when Exa or Perplexity is configured), MCP servers from `~/.strix/mcp-servers.json`, and the reporting tools below. Shell, browser, and proxy tools run inside the sandbox.

## What "validated" means

Dynamic findings go through `create_vulnerability_report`. The tool requires a title, description, impact, target, technical analysis, PoC description, PoC script, remediation, evidence, assumptions, counterevidence, confidence, severity-change conditions, fix effort, and a CVSS v3.1 breakdown. Severity is computed from that breakdown. The agent is instructed to file only when a proof demonstrates an unauthorized security consequence, and to record the strongest case that the issue is not exploitable.

A duplicate of an existing finding is rejected. The agent is told to amend the original with `update_vulnerability_report` instead of filing again.

Known-CVE dependency and supply-chain matches that cannot be executed as a live proof go through `create_dependency_report`. Those records use `finding_class: dependency_cve` and carry package metadata. They are still listed under `vulnerabilities/`. Read them as "this pinned version matches an advisory, rated in this codebase," which is a different evidence bar from a dynamic PoC. The distinction is in [reports.md](reports.md).

Observations without a proof — a version banner, a reachable port, a missing header with no demonstrated impact — are not supposed to become vulnerability files. When one does, the PoC, evidence, and CVSS sections are how you judge it.

## Scope and depth

| Input | Effect |
| --- | --- |
| `-m quick` | Short high-impact playbook, shallow enumeration. Docs describe it as minutes. Nothing in the CLI kills the process on a clock. |
| `-m standard` | Source-aware mapping, then dynamic validation of the top candidates. Docs describe about 30–60 minutes. |
| `-m deep` | CLI default. Broader static triage, then systematic validation. Docs describe hours. |
| `--scope-mode auto` | Headless and CI runs over a git checkout limit white-box work to the diff against the default branch. |
| `--scope-mode diff` | Force that diff scope. `--diff-base` picks the base ref. |
| `--scope-mode full` | Whole tree. |
| `--instruction` | Credentials, roles, and focus. This is how a grey-box test is authenticated. |
| API spec as `-t` | OpenAPI/Swagger or a Postman collection is copied into the workspace. Base URLs declared by the spec are in scope. Pair the spec with the live base URL. |
| `--max-budget` | USD cap for the whole scan, root plus children. Checked after each model response, so in-flight calls can overshoot slightly. |
| `--max-turns` | Per agent, default 500. Hitting it force-stops that agent. |

In headless mode the budget hard-stop ends the scan with `status: stopped` and tears down the sandbox. Children are stopped at 90% of the budget so the root can finish the report. Wrap-up warnings fire earlier (root around 70/85/95 percent; children around 75/80/85 percent). A warning does not by itself set `stopped`: an agent that calls `finish_scan` after a warning still records `completed`. Compare `llm_usage.cost` with the budget either way.

Cost is token usage times pricing. A model LiteLLM cannot price under-counts until `STRIX_LLM_INPUT_COST_PER_MTOK` and `STRIX_LLM_OUTPUT_COST_PER_MTOK` are set. A `chatgpt/` subscription run records tokens with zero cost.

## Sandbox image

`containers/Dockerfile` builds a Kali image. `bash scripts/docker.sh` tags it `strix-sandbox:dev`. The published default Strix pulls when `STRIX_IMAGE` is unset is the string on `RuntimeSettings.image` in `strix/config/settings.py` (the installer repeats it in `scripts/install.sh`).

The image is the agent's toolkit: recon (subfinder, naabu, httpx, katana, ffuf, nmap), web testing (arjun, dirsearch, wafw00f), scanners (nuclei, sqlmap, wapiti, ZAP), JavaScript analysis, SAST (semgrep, ast-grep, tree-sitter, bandit), secrets (trufflehog, gitleaks), JWT and interactsh, Trivy, the Caido proxy, and Playwright. The maintained inventory is `docs/tools/sandbox.mdx` in the checkout. When that page and this paragraph disagree, the checkout wins.

Caido is the HTTP interception proxy inside the container. Sandbox Python can script it. The host is shown a Caido URL while a scan runs. Proxy capture ids stay inside the run; finding prose is written to omit them.

## Where time and money go

Most of a scan is LLM turns plus sandbox tool calls. `quick` with a budget is the shape for an unattended agent. `deep` without `--max-budget` runs until the root agent decides to finish or hits 500 turns per agent.

Artifacts are rewritten during the run, so a `running` directory already contains partial `vulnerabilities.json` and `run.json`. The executive report appears when the root calls `finish_scan`. A budget stop or a crash can leave findings on disk and no `penetration_test_report.md`.

## Layout of the checkout

| Path | Role |
| --- | --- |
| `strix/interface/` | CLI, headless startup, TUI, local viewer |
| `strix/agents/` | Agent graph and system prompt |
| `strix/tools/` | Proxy, browser, terminal, reporting, coverage, threat model |
| `strix/runtime/` | Docker sandbox session |
| `strix/report/` | `run.json`, Markdown, CSV, JSON, SARIF, coverage |
| `strix/skills/` | Playbooks the pentest agents load |
| `strix/config/settings.py` | Environment variable names and defaults |
| `containers/Dockerfile` | Sandbox image |
| `scripts/docker.sh` | Build `strix-sandbox:<tag>` |
| `skills/` | Consumer skills for coding agents, including this one |
