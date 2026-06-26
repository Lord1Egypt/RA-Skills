# SkillNet API & CLI Reference

## REST API (Public, No Auth)

**Base URL**: `https://api-skillnet.openkg.cn/v1`

> **Data handling**: The search API only sends your query string to return matching skills. No local files, credentials, or personal data are transmitted during search or download operations.

### `GET /search`

| Parameter   | Type   | Default      | Description                            |
| ----------- | ------ | ------------ | -------------------------------------- |
| `q`         | string | **required** | Search query                           |
| `mode`      | string | `"keyword"`  | `"keyword"` or `"vector"`              |
| `category`  | string | —            | Filter by category                     |
| `limit`     | int    | 20           | Max results                            |
| `page`      | int    | 1            | Page number (keyword only)             |
| `min_stars` | int    | 0            | Minimum stars (keyword only)           |
| `sort_by`   | string | `"stars"`    | `"stars"` or `"recent"` (keyword only) |
| `threshold` | float  | 0.8          | Similarity 0.0–1.0 (vector only)       |

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "skill_name": "pdf-parser",
      "skill_description": "Parse and extract text from PDF files...",
      "author": "...",
      "stars": 5,
      "skill_url": "https://github.com/...",
      "category": "data-science-visualization",
      "evaluation": {
        "safety": { "level": "Good", "reason": "..." },
        "completeness": { "level": "Average", "reason": "..." },
        "executability": { "level": "Good", "reason": "..." },
        "maintainability": { "level": "Average", "reason": "..." },
        "cost_awareness": { "level": "Good", "reason": "..." }
      }
    }
  ],
  "meta": {
    "query": "pdf",
    "mode": "keyword",
    "total": 42,
    "page": 1,
    "limit": 20
  }
}
```

---

## CLI Commands

Install: `pip install skillnet-ai` or `pipx install skillnet-ai` (provides `skillnet` command)

### `skillnet search`

```
skillnet search QUERY [OPTIONS]

Arguments:
  QUERY                         Search query (required)

Options:
  --mode TEXT                   "keyword" or "vector"  [default: keyword]
  --category TEXT               Filter by category
  --limit INTEGER               Max results  [default: 20]
  --page INTEGER                Page number (keyword)  [default: 1]
  --min-stars INTEGER           Minimum star rating  [default: 0]
  --sort-by TEXT                "stars" or "recent"  [default: stars]
  --threshold FLOAT             Similarity 0.0-1.0 (vector)  [default: 0.8]
```

### `skillnet download`

```
skillnet download URL [OPTIONS]

Arguments:
  URL                           GitHub URL of the skill folder (required)

Options:
  -d, --target-dir TEXT         Local install directory  [default: .]
  -t, --token TEXT              GitHub token override
  -m, --mirror TEXT             Mirror URL for faster downloads in restricted networks
                                (e.g. https://ghfast.top/). Also reads GITHUB_MIRROR env var.
```

### `skillnet create`

```
skillnet create [OPTIONS]

Options:
  --github TEXT                 GitHub repository URL
  --office TEXT                 Path to PDF/PPT/DOCX
  --prompt TEXT                 Natural-language description
  TRAJECTORY                    Path to trajectory/log file (positional)
  --output-dir TEXT             Output directory  [default: ./generated_skills]
  --model TEXT                  LLM model  [default: gpt-4o]
                                Also reads SKILLNET_MODEL env var.
  --max-files INTEGER           Max files for GitHub mode  [default: 50]
```

Model priority: `--model` flag > `SKILLNET_MODEL` env var > `gpt-4o`.

Input types (auto-detected):

- `github` — analyses repo structure, README, key source files
- `trajectory` — extracts patterns from execution logs
- `office` — extracts knowledge from documents
- `prompt` — generates from description

### `skillnet evaluate`

```
skillnet evaluate TARGET [OPTIONS]

Arguments:
  TARGET                        Local path or GitHub URL (required)

Options:
  --name TEXT                   Override skill name
  --category TEXT               Override category
  --description TEXT            Override description
  --model TEXT                  LLM model  [default: gpt-4o]
                                Also reads SKILLNET_MODEL env var.
  --max-workers INTEGER         Concurrency  [default: 5]
```

Output: Five dimensions — Safety, Completeness, Executability, Maintainability, Cost-Awareness. Each rated Good / Average / Poor with a textual reason.

### `skillnet analyze`

```
skillnet analyze SKILLS_DIR [OPTIONS]

Arguments:
  SKILLS_DIR                    Directory containing skill folders (required)

Options:
  --no-save                     Don't write relationships.json
  --model TEXT                  LLM model  [default: gpt-4o]
                                Also reads SKILLNET_MODEL env var.
```

Output: `relationships.json` with edges:

```json
[
  {
    "source": "skill-a",
    "target": "skill-b",
    "type": "similar_to",
    "reason": "Both handle PDF parsing but with different approaches"
  }
]
```

Relationship types: `similar_to`, `belong_to`, `compose_with`, `depend_on`.

---

## Python SDK

```python
from skillnet_ai import SkillNetClient

client = SkillNetClient(
    api_key="sk-...",          # env: API_KEY (required for create/evaluate/analyze)
    base_url="https://...",    # env: BASE_URL (optional)
    github_token="ghp_..."    # env: GITHUB_TOKEN (optional)
)
```

### `client.search(q, mode, category, limit, page, min_stars, sort_by, threshold)`

Returns `List[SkillModel]`. Each object has:

- `.skill_name` (str)
- `.skill_description` (str)
- `.author` (str)
- `.stars` (int)
- `.skill_url` (str)
- `.category` (str)
- `.evaluation` (dict or None)

### `client.download(url, target_dir, token, mirror_url)`

Returns `str` — absolute path to installed skill directory.

- `mirror_url` — Mirror URL for faster downloads in restricted networks. Also reads `GITHUB_MIRROR` env var.

### `client.create(input_type, trajectory_content, github_url, office_file, prompt, output_dir, model, max_files)`

Returns `List[str]` — paths to generated skill directories.

### `client.evaluate(target, name, category, description, model, max_workers, cache_dir)`

Returns `Dict[str, Any]` — evaluation report with five dimension keys.

### `client.analyze(skills_dir, save_to_file, model)`

Returns `List[Dict[str, Any]]` — relationship edges.

---

## Environment Variables

| Variable         | Purpose                                  | Required                      |
| ---------------- | ---------------------------------------- | ----------------------------- |
| `API_KEY`        | LLM API key (OpenAI-compatible)          | For create, evaluate, analyze |
| `BASE_URL`       | Custom LLM endpoint                      | No (defaults to OpenAI)       |
| `GITHUB_TOKEN`   | GitHub PAT for private repos             | No                            |
| `SKILLNET_MODEL` | Default LLM model for all commands       | No (defaults to `gpt-4o`)     |
| `GITHUB_MIRROR`  | Mirror URL for faster downloads          | No                            |

## Security & Privacy

For credential scope, network endpoints, data flow details, and user confirmation policy, see `security-privacy.md`.

---

## Credential Strategy

### Just-in-Time Credential Pattern

Credentials follow a **"transparent — always inform the user which credentials are being used"** pattern:

1. **If already configured** (via `openclaw.json`, environment, or earlier in the session) → use the configured credentials and briefly inform the user (e.g., "Using your configured API_KEY").
2. **If missing and the command needs it** → ask the user **once** using the standard ask templates below.
3. **If the user declines** → acknowledge and continue the main task. Never block.

**Execution convention** — inject credentials for the current invocation only:

```bash
# One-shot injection (does not pollute the global environment)
API_KEY="..." BASE_URL="..." skillnet create --prompt "..." --output-dir ~/.openclaw/workspace/skills

# Or export for the session if multiple commands follow
export API_KEY="<value>"
export BASE_URL="<value>"   # only if user provided
export GITHUB_TOKEN="<value>"  # only if needed
```

### Command ↔ Variable Requirement

| Command             | `API_KEY`    | `BASE_URL` | `GITHUB_TOKEN`                | `SKILLNET_MODEL` | `GITHUB_MIRROR` |
| ------------------- | ------------ | ---------- | ----------------------------- | ----------------- | --------------- |
| `skillnet search`   | —            | —          | —                             | —                 | —               |
| `skillnet download` | —            | —          | Private repos only            | —                 | Optional        |
| `skillnet create`   | **Required** | Optional   | `--github` private repos only | Optional          | —               |
| `skillnet evaluate` | **Required** | Optional   | —                             | Optional          | —               |
| `skillnet analyze`  | **Required** | Optional   | —                             | Optional          | —               |

**No env vars are required for install, search, or download (public repos).**

### Standard Ask Templates

**API_KEY** — triggered before `create`/`evaluate`/`analyze` when not configured:

> I need an OpenAI-compatible API_KEY (used only for create/evaluate/analyze in this run). Optionally provide BASE_URL and model name (default gpt-4o). May I proceed with your key?

**GITHUB_TOKEN** — triggered only on private repo access or rate-limit (403):

> We hit GitHub rate limits or need private repo access. Can you share a read-only Personal Access Token (`repo:read` scope)?

**BASE_URL** — triggered only if user explicitly wants a custom endpoint but hasn't provided one:

> Would you like to use a custom LLM BASE_URL? (default `https://api.openai.com/v1`)

### OpenClaw Pre-Configuration (Silent Use)

If credentials are provided in `openclaw.json`, they are injected automatically — no prompts, no interruptions:

```json
{
  "skills": {
    "entries": {
      "skillnet": {
        "enabled": true,
        "apiKey": "sk-xxxx",
        "env": {
          "BASE_URL": "https://api.openai.com/v1",
          "GITHUB_TOKEN": "ghp_xxx"
        }
      }
    }
  }
}
```

- `apiKey` → injected as `API_KEY` (bound via `primaryEnv` in metadata).
- `env.BASE_URL` / `env.GITHUB_TOKEN` → injected as environment variables.
- Once configured, commands use these credentials automatically. The agent will still inform the user before executing security-sensitive operations.

### Terminology Note

The evaluation dimension **Maintainability** is sometimes referred to as **Modifiability** in older documentation. Both terms describe the same dimension: how easy a skill is to update, extend, or customize. The canonical name in the SDK and API is `maintainability`.
