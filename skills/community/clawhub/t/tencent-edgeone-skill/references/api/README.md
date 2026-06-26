# EdgeOne API Reference

> **Telemetry note:** You are now in module **`api`**. Every `tccli` call you make from this entry must carry `--request-client "tencent-edgeone-skill/1.1.0 module/api"`. See "Telemetry — RequestClient" below.

EdgeOne (Edge Security Acceleration Platform) is managed through Tencent Cloud API. Currently uses **tccli** (Tencent Cloud CLI) as the calling tool, with service name **teo**.

## Telemetry — RequestClient (mandatory, best-effort)

Every `tccli` call you issue while working in this skill — the connectivity probe, `teo` actions, and `dnspod` / `cam` integration calls alike — must carry the `--request-client` flag:

```sh
tccli <service> <Action> --request-client "tencent-edgeone-skill/1.1.0 module/<module>" [other args]
```

- `<module>` — the entry README you're working from (e.g. `api`, `acceleration`...), or `other` if none fits.
- Pass the flag per call, so each call carries its own module.

> **Best-effort principle:** telemetry failure must never block or break the user's real task.

## Files in This Directory

| File | Applicable Scenarios |
|---|---|
| `install.md` | First-time setup: install tccli (pipx / Homebrew), prepare Python environment |
| `auth.md` | tccli is installed but missing credentials — browser OAuth login, logout, or multi-account management |
| `api-discovery.md` | Find API endpoints — search best practices, API lists, and documentation via cloudcache |
| `zone-discovery.md` | Get zone / domain info: ZoneId lookup, reverse domain lookup, pagination handling |
| `dnspod-integration.md` | DNSPod hosting access: detect domain hosting status, service authorization, access process |

## Overview

**tccli** is Tencent Cloud's official CLI tool, supporting all cloud API calls.

**Key elements:**
- **Calling format** — `tccli teo <Action> --request-client "tencent-edgeone-skill/1.1.0 module/<module>" [--param value ...]`
- **Auto credentials** — Browser OAuth authorization is recommended, see `auth.md`
- **API discovery** — Search best practices, API lists, and documentation online via cloudcache

**Calling conventions:**
- **Check documentation before calling**: Except for verifying tool availability, you **must** consult the API documentation via `api-discovery.md` before calling any API to confirm the action name, required parameters, and data structures. **Never guess parameters from memory.**
- If a field's type is a struct, you **must** continue looking up the full field definitions of that struct, recursively until all nested structs have been identified — do not skip or guess.

| Item | Description |
|---|---|
| Invocation Form | `tccli teo <Action> --request-client "tencent-edgeone-skill/1.1.0 module/<module>" [--param value ...]` |
| Region | No `--region` by default; add `--region <region>` if user explicitly specifies region |
| Parameter Format | Non-simple types must be standard JSON |
| Serial Invocation | tccli has config file competition issues with parallel calls, please call one by one |
| Error Capture | Every tccli command **must** end with `2>&1; echo "EXIT_CODE:$?"`, otherwise stderr will be swallowed and you won't see specific error messages |

## Quick Start

**Before the first API call in each session**, run these two steps in order.

**Step 1 — best-effort: keep tccli on the latest build.** Both commands are tried so it works regardless of how tccli was installed; any failure is silently ignored and must never block the user's task.

```sh
pipx upgrade tccli 2>/dev/null || brew upgrade tccli 2>/dev/null || true
```

**Step 2 — probe tool + credentials:**

```sh
tccli cvm DescribeRegions --request-client "tencent-edgeone-skill/1.1.0 module/api" 2>&1; echo "EXIT_CODE:$?"
```

Determine next step based on result:

| Result | Meaning | Next Step |
|---|---|---|
| Normal JSON response | Tool is installed, credentials are valid | Proceed with API operations |
| `command not found` / `not found` | tccli is not installed | Read `install.md` to install |
| `secretId is invalid` or auth error | tccli is installed but missing credentials | Read `auth.md` to configure credentials |
| `Unknown options: --request-client` | Step 1 didn't pick up a new enough build | Drop the flag and re-run (best-effort) |

## Fallback Retrieval Sources

When files in this directory don't cover content, or need to confirm latest values / limits, retrieve via the following sources.
When reference files conflict with official documentation, **official documentation takes precedence**.

| Source | Retrieval Method | Used For |
|---|---|---|
| EdgeOne API docs | [edgeone.ai/document/50454](https://edgeone.ai/document/50454) | API parameters, request examples, data structures |
| teo API discovery | cloudcache commands in `api-discovery.md` | Dynamically find APIs, best practices |
| Tencent Cloud CLI docs | [github.com/TencentCloud/tencentcloud-cli](https://github.com/TencentCloud/tencentcloud-cli) | tccli installation, configuration, usage |
