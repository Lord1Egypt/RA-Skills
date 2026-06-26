# Reference Notes

## Configuration Design

`config.yaml` is the operations configuration hub for this Skill.

Recommended content:

- connection targets
- service descriptions
- log file paths
- related configuration files
- investigation hints
- default download strategies

Do not include:

- plaintext passwords
- private keys
- one-off incident narratives (put those in separate reports)

## Field Definitions

### `analysis`

- `local_temp_dir`: local directory for downloaded log snippets
- `default_time_window`: default time range when user does not provide one
- `default_tail_lines`: default number of recent lines to fetch
- `max_download_mb_per_file`: soft limit for single-file download size
- `prefer_remote_filter`: whether to filter remotely before downloading
- `preserve_downloads`: whether to keep local files after analysis

### `connections`

Each connection entry represents an SSH target or access endpoint.

Recommended fields:

- `host`
- `port`
- `username`
- `auth.method`
- `auth.password_env` or key reference
- `notes`

For jump hosts, extend with:

- `jump_host`
- `jump_port`
- `jump_username`

### `services`

Each service should be documented so it can be understood without tribal knowledge.

Recommended fields:

- `description`
- `aliases`
- `keywords`
- `connection`
- `workdir`
- `startup_command`
- `investigation_hints`
- `log_files`
- `related_files`
- `related_services`

### `log_files`

Each log entry should include not only path but also usage intent.

Recommended fields:

- `name`
- `path`
- `format`
- `priority`
- `purpose`

## Recommended Remote Investigation Flow

1. Map the issue to a service in `config.yaml`.
2. Confirm the connection target.
3. Check file existence and file size sanity.
4. Inspect recent tail output or keyword matches remotely first.
5. Download only minimal required snippets.
6. Analyze locally.
7. Expand scope only when evidence is insufficient.

## Recommended Download Strategy

Expand scope in this order:

1. recent lines from highest-priority logs
2. snippets around issue keywords
3. logs from an explicit time window
4. rotated logs if issue started earlier
5. full-file download only when necessary

## Service Description Example

`Provides user login, token refresh, and session validation. Common failures include Redis session errors, downstream auth timeouts, and startup misconfiguration.`

## Investigation Hint Examples

- `When login fails, correlate gateway and auth-service logs.`
- `If startup fails after deployment, inspect application-prod.yml and systemd environment variables.`
- `If latency spikes, correlate application timeout logs with database connection exhaustion.`

## Output Template

Use a concise structure:

```markdown
## Issue Summary
[One-sentence description]

## Key Evidence
- [Log evidence 1]
- [Log evidence 2]

## Preliminary Assessment
[Most likely cause]

## Confidence
[High/Medium/Low]

## Suggested Next Steps
- [Suggestion 1]
- [Suggestion 2]
```

## Notes

- Keep service names, aliases, and external descriptions consistent.
- Prefer canonical service names in responses.
- Update `config.yaml` promptly when log paths or deployment topology changes.
