# YouTube Reporting access policy

An access policy limits which endpoints YouTube Reporting connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/youtube-reporting#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for YouTube Reporting: its 6 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create youtube-reporting --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v1/jobs"},
    {"method": "GET", "path": "v1/jobs/{id}"},
    {"method": "GET", "path": "v1/media/{id}"},
    {"method": "GET", "path": "v1/reportTypes"},
    {"method": "GET", "path": "v1/jobs/{id}/reports"},
    {"method": "GET", "path": "v1/jobs/{id}/reports/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The YouTube Reporting endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v1/jobs | read | jobs | Lists jobs. |
| POST | v1/jobs | write | jobs | Creates a job and returns it. |
| GET | v1/jobs/{id} | read | jobs | Gets a job. |
| DELETE | v1/jobs/{id} | write | jobs | Deletes a job. |
| GET | v1/media/{id} | read | media | Method for media download. |
| GET | v1/reportTypes | read | reportTypes | Lists report types. |
| GET | v1/jobs/{id}/reports | read | reports | Lists reports created by a specific job. |
| GET | v1/jobs/{id}/reports/{id} | read | reports | Gets the metadata of a specific report. |
