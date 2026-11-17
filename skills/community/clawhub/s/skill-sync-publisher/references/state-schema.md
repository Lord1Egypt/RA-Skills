# State schema

The default state path is `~/.codex/skill-sync/state.json`. It is user-owned,
outside the source repository, and must never contain credentials.

```json
{
  "version": 1,
  "skills": {
    "github.com/org/repo#skills/example": {
      "source": {"repo": "github.com/org/repo", "path": "skills/example"},
      "platforms": {
        "clawhub": {
          "choice": "enabled",
          "status": "published",
          "sourceHash": "sha256:...",
          "sourceCommit": "abc123",
          "remoteId": "example",
          "remoteUrl": "https://clawhub.ai/...",
          "publishedVersion": "0.1.0",
          "lastAttemptAt": "2026-07-28T00:00:00Z",
          "lastSuccessAt": "2026-07-28T00:00:00Z",
          "error": null
        }
      }
    }
  }
}
```

Allowed choices are `enabled`, `disabled`, and `deferred`. Runtime statuses
are `planned`, `skipped`, `blocked`, `indexed`, `published`, and `failed`.
