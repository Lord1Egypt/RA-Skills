# Vmake (OpenClaw skill)

Use the **Vmake** commercial media API inside [OpenClaw](https://github.com/openclaw/openclaw) to process images and videos (watermark removal and quality restoration). Agents use a single CLI entrypoint: `scripts/vmake_ai.py`.

Calls consume **quota / credits** for the tenant tied to **MT_AK**. Do not tell end users the service is free or guess pricing — see *Billing and user-facing claims* in [SKILL.md](SKILL.md).

## What this skill does

| task_name | Capability |
|-----------|------------|
| `eraser_watermark` | Image watermark removal |
| `videoscreenclear` | Video watermark removal |
| `image_restoration` | Image quality restoration |
| `hdvideoallinone` | Video quality restoration |

## Installing for OpenClaw

1. Add this repository (or the skill folder) as an OpenClaw skill per **your host’s documentation** (e.g. copy into the skills directory, or install from a marketplace / URL).
2. Ensure **`python3`** is available and the skill can read **`MT_AK`** and **`MT_SK`** (same as `metadata.openclaw.requires` in [SKILL.md](SKILL.md)).
3. Agent behavior and async video flow (e.g. `spawn-run-task` + `sessions_spawn`) are defined in [SKILL.md](SKILL.md); this README does not repeat them.

## API keys (AK / SK)

Get your Access Key and Secret Key from **[Vmake Developers — API Key](https://vmake.ai/developers#api-key)**.

Put them in `scripts/.env` (see `scripts/.env.example`) or export them in the environment:

```bash
export MT_AK="..."
export MT_SK="..."
```

Check connectivity and install Python dependencies:

```bash
python3 scripts/vmake_ai.py preflight   # should print ok
python3 scripts/vmake_ai.py install-deps
```

## Upgrading from older builds

If you previously used `openclaw-kaipai-ai` / `scripts/kaipai_ai.py`: state and history now live under **`~/.openclaw/workspace/openclaw-vmake-ai/`**, and local GID cache under **`~/.cache/vmake/`**. Nothing is migrated automatically from the old paths.

## Further reading

- [SKILL.md](SKILL.md) — Full agent workflow and mandatory rules  
- [docs/multi-platform.md](docs/multi-platform.md) — Delivery (Feishu, Telegram, Discord, …)  
- [docs/errors-and-polling.md](docs/errors-and-polling.md) — Polling, timeouts, failure codes  
- [docs/im-attachments.md](docs/im-attachments.md) — IM attachments and `resolve-input`  
- [docs/feishu-send-video.md](docs/feishu-send-video.md) — Feishu native video send  

## License

MIT (see repository root if present).
