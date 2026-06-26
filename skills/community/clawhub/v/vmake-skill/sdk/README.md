# Vmake AI SDK

Set **MT_AK** and **MT_SK** (or use `--ak` / `--sk` on the CLI). Keys: [Vmake Developers — API Key](https://vmake.ai/developers#api-key).

## CLI

From the repo root, run the script **`sdk/cli.py`** (not `python -m sdk.cli`):

```bash
export MT_AK="..." MT_SK="..."
python3 sdk/cli.py run-task --task eraser_watermark --input /path/to/file.jpg
python3 sdk/cli.py query-task --task-id "<id>"
python3 sdk/cli.py list-tasks
```

Optional JSON for the algorithm: `--params '{"parameter":{"rsp_media_type":"url"}}'`. Exit **0** = success, **1** = error or not finished.

Agents using OpenClaw should use **`scripts/vmake_ai.py`** instead (see root `README.md`).

## Python

Use **`SkillClient`**: one call runs upload → quota → job → poll; use **`poll_task_status`** only if you already have a **task id** and need to poll again.

```python
from sdk import SkillClient

client = SkillClient()  # uses MT_AK / MT_SK, or SkillClient(ak="...", sk="...")

result = client.run_task(
    task_name="eraser_watermark",
    image_path="/path/to/file.jpg",  # or "https://..."
    params={"parameter": {"rsp_media_type": "url"}},  # optional
)

# Optional: poll an existing job by id (from a previous run_task response)
result = client.poll_task_status(task_id="<task_id>")
```

`result` is a **dict** (same information the CLI prints as JSON). For quota or permission failures, `run_task` may raise **`ConsumeDeniedError`**.
