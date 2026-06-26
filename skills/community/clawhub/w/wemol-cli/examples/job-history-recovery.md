# Job History Recovery Example

Use this example when the user asks about a previously run job but does not provide a `job_id`, or when the agent needs to reconnect to earlier results before checking status, logs, outputs, or downloads.

## Why This Example Matters

This is the normal recovery path for existing work:
- `job list` is good for recent history and status filtering
- `job search` is good when the user remembers a topic or module name
- once the `job_id` is recovered, the normal flow resumes with `status`, `tasks`, `logs`, `output`, or `download`

## Verified Recovery Patterns

List recent completed jobs:

```bash
wemol-cli job list --status Done --limit 5
```

In a verified run, this returned recent completed jobs from multiple modules.

Search by module or topic keyword:

```bash
wemol-cli job search ADMET --limit 5
wemol-cli job search Physico --limit 5
```

Observed behavior:
- exact or near-exact module keywords quickly recovered the matching jobs
- `job search` returned both recent and older matching runs when available

## Agent Rules From This Example

- Use `job list` when the user asks for recent jobs or jobs by status.
- Use `job search` when the user remembers a module name, keyword, or topic.
- Do not guess a `job_id` from memory if `job list` or `job search` can recover it.
- After recovering a `job_id`, continue with:
  - `job status <job_id>` for summary
  - `job tasks <job_id>` for task IDs
  - `job logs <job_id>` for diagnostics
  - `job download <job_id>` for artifact outputs

Download optimization pattern after recovery:

```bash
wemol-cli job download <job_id> --output ./downloads/<job_id> --retry 3 --concurrency 6
```

Resume and force-refresh variants:

```bash
wemol-cli job download <job_id> --output ./downloads/<job_id>
wemol-cli job download <job_id> --output ./downloads/<job_id> --no-resume
```
