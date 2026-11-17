# Upload Artifacts (Step 10)

Calls `scripts/upload_artifacts.py` to upload build artifacts and templates to OSS. This document covers invocation and key behaviors.

---

## Invocation

The stack template must carry the real artifact URLs, so the order is: upload artifacts → regenerate the template with those URLs → upload that template.

### 1. Upload build artifacts

```bash
python3 scripts/upload_artifacts.py --region "$REGION" \
  [--bucket "$BUCKET"] \
  --static-dir dist \
  --app-mode binary --app-dir app \
  > /tmp/qwencloud-artifacts.json
```

Output JSON contains `static_url` / `app_url` (reuse the same bucket later via `--bucket`).

### 2. Regenerate the template with the artifact URLs

Pass the artifacts-json to `generate_template.py` to produce the final template carrying the real artifact URLs (see step 7).

### 3. Upload the final template (obtain TemplateURL)

```bash
python3 scripts/upload_artifacts.py --region "$REGION" --bucket "$BUCKET" \
  --template-file /tmp/qwencloud-template.yaml
```

Output JSON contains `template_url` for stack creation in step 11.

---

## Output Format

```json
{
  "bucket": "qwencloud-deploy-tmp-a1b2c3",
  "static_url": "https://oss-...-internal.aliyuncs.com/static-20260729-143000.tar.gz?...",
  "app_url": "https://oss-...-internal.aliyuncs.com/app-20260729-143000.tar.gz?...",
  "template_url": "https://oss-...aliyuncs.com/template.yaml?..."
}
```

---

## Key Behaviors

| Behavior | Description |
|----------|-------------|
| Bucket name | `qwencloud-deploy-tmp-<6-char-random>`, created on first use, reused after (pass `--bucket`) |
| Auto-activate OSS | If OSS service not activated, auto-calls `OpenOssService` |
| Tag | New buckets auto-tagged `from=qwencloud` |
| Lifecycle | New buckets set to 7-day expiration (prevents forgotten resources) |
| Signed URL | Valid for 24 hours |
| Internal endpoint | Defaults to `oss-*-internal.aliyuncs.com` (free traffic within VPC) |
| Exclusions | `node_modules`, `.git`, `__pycache__`, `.venv`, `dist`, `build`, etc. |

---

## app-mode Options

| mode | Behavior |
|------|----------|
| `binary` | tar the app-dir |
| `docker-image` | `docker save` image then tar.gz |
| `docker-compose` | tar the entire directory |
| `skip` | Do not upload app |

---

## Notes

- Never manually copy-paste signed URLs — pipe via `--artifacts-json` to `generate_template.py`
- Template upload uses public endpoint (ROS needs a publicly-reachable URL)
- Artifact upload uses internal endpoint (ECS UserData pulls from within VPC)

---

## Tar Exclusion Rules

The script automatically excludes these directories and files during packaging:

**Excluded directory names** (matched at any path level):
`node_modules`, `.git`, `__pycache__`, `.venv`, `venv`, `.pytest_cache`, `.mypy_cache`, `.tox`, `.idea`, `.vscode`

**Excluded relative paths**:
`.next/cache`, `target/test-classes`, `build/test-results`

**Excluded file names**:
`.DS_Store`, `Thumbs.db`

> Rationale: macOS `node_modules` contains native extensions (sharp/bcrypt etc.) that won't run on Linux ECS; UserData reinstalls dependencies on ECS.

---

## OSS Service Auto-Activation

If OSS is not activated, the script auto-calls `aliyun ossadmin OpenOssService` (activation is free; charges are usage-based only).
On failure, prompts user to activate manually at https://oss.console.aliyun.com/.

---

## Internal Endpoint Conversion

By default replaces `oss-<region>.aliyuncs.com` with `oss-<region>-internal.aliyuncs.com`:
- Artifact URLs (ECS UserData pulls from within VPC) → internal, free traffic
- Template URLs (ROS needs public-reachable) → public (auto-handled in `--template-file` mode)
