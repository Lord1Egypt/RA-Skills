# Vmake AI (OpenClaw skill)

Process images and video with **Vmake AI**: watermark removal and quality restoration. Works inside [OpenClaw](https://github.com/openclaw/openclaw) with a single CLI entrypoint: `scripts/vmake_ai.py`.

## Capabilities

Calls go to the **Vmake commercial API** and **consume account quota** (credits) for the configured **MT_AK** tenant. Agents must not tell users the service is free or guess pricing — see [SKILL.md](SKILL.md) (*Billing and user-facing claims*).

Executable task IDs are server-driven. The skill supports image/video watermark removal and quality restoration, but callers must discover current IDs before naming or running a task.

## Install

Install the skill folder as your OpenClaw skill (path or marketplace URL your host documents), then restart the gateway if required.

## One-time setup

1. Put **MT_AK** and **MT_SK** in `scripts/.env` (or export them in the environment).
2. Run:

```bash
python3 scripts/vmake_ai.py preflight
```

Output must be `ok`.

## Dependencies

```bash
python3 scripts/vmake_ai.py install-deps
```

Uses `scripts/requirements.txt` (e.g. `requests`, OSS client as needed).

## Discover current tasks

```bash
python3 scripts/vmake_ai.py catalog
python3 scripts/vmake_ai.py catalog --media-type video
```

V2 output includes `material_id`, `name`, `description`, and `media_type`. Select by the display fields, then pass the exact returned `material_id` to `--task`; this avoids ambiguity when display names repeat. A legacy alias is valid only when the response is explicitly `config_mode: legacy` and returns that alias. Configuration failure stops the flow; no local task fallback is used. This command does not upload media, consume quota, or submit an algorithm job.

## URL inputs (`--input https://...`)

- **Shell:** Quote the full URL so `&` in query strings is not broken (e.g. signed storage URLs).
- **Limits:** Streamed download with **15s connect / 120s read** timeouts and **100MB** max by default (shared with `resolve-input --url`). Override: `MT_AI_URL_CONNECT_TIMEOUT`, `MT_AI_URL_READ_TIMEOUT`, `MT_AI_URL_MAX_BYTES`.
- **Large or slow media:** Use `resolve-input --url …` to save locally, then pass the returned `path` as `--input`.

## Quick examples

**Image watermark removal (blocking):**

```bash
python3 scripts/vmake_ai.py run-task \
  --task "<image_catalog_material_id_or_confirmed_legacy_alias>" \
  --input "https://example.com/photo.jpg"
```

**Video task (async worker payload):**

```bash
python3 scripts/vmake_ai.py spawn-run-task \
  --task "<video_catalog_material_id_or_confirmed_legacy_alias>" \
  --input "https://example.com/clip.mp4" \
  --deliver-to "oc_xxx_or_ou_xxx" \
  --deliver-channel feishu
```

Pass the printed `sessions_spawn_args` to OpenClaw `sessions_spawn`. Keep **`runTimeoutSeconds`** at the payload default (**3600**); do not reduce it without accepting timeout risk. Wall time varies. If a host **session/tool wait cap** cuts off before JSON finishes, recover with **`last-task`** / **`history`** / **`query-task`** (see [SKILL.md](SKILL.md) and [docs/errors-and-polling.md](docs/errors-and-polling.md)).

**Two-stage video** (watermark removal then restoration): select both video task entries from the remote catalog and use their `material_id` values, then run **`spawn-run-task` + `sessions_spawn` twice** — one embed per stage. After the first worker finishes, pass its **`primary_result_url`** as the second stage's **`--input`**.

**Resume polling by task id:**

```bash
python3 scripts/vmake_ai.py query-task --task-id "<full_task_id>"
```

**Last run / history (local state under `~/.openclaw/workspace/openclaw-vmake-ai/`):**

```bash
python3 scripts/vmake_ai.py last-task
python3 scripts/vmake_ai.py history
```

**IM attachment → local path for `--input`:**

```bash
python3 scripts/vmake_ai.py resolve-input --telegram-file-id "AgAC..." --output-dir /tmp
```

See [docs/im-attachments.md](docs/im-attachments.md) and [SKILL.md](SKILL.md) for agents.

## Operators

**One line:** Video tasks → **`spawn-run-task`** (not a blocking **`run-task`** in the main session); if a job was cut off or the user asks for status → **`last-task`** / **`query-task`** — never submit **`run-task`** again for the same **`task_id`**.

**New jobs:** Agents must submit only via **`vmake_ai.py run-task`** (or the same command inside **`spawn-run-task`**); do not call AIGC/wapi directly and skip **`/skill/consume.json`** — see [SKILL.md](SKILL.md) section **API submission path (MANDATORY)**.

## Docs

- [SKILL.md](SKILL.md) — agent instructions
- [docs/multi-platform.md](docs/multi-platform.md) — delivery (Feishu, Telegram, Discord, …)
- [docs/errors-and-polling.md](docs/errors-and-polling.md) — env vars, polling, failures
- [docs/feishu-send-video.md](docs/feishu-send-video.md) — Feishu native video send

## License

MIT (see repository root if present).
