# Skill Registry Database Format

The skill registry is stored as JSON in `assets/skill-registry.json`.

## Schema

```json
{
  "version": "1.0.0",
  "skills": {
    "skill-name": {
      "name": "skill-name",
      "source": "clawhub|github|local",
      "source_url": "https://...",
      "description": "What this skill does",
      "trust_score": 85,
      "risk_flags": [],
      "current_version": "1.0.0",
      "latest_version": "1.1.0",
      "added_date": "2024-01-15T10:30:00",
      "last_updated": "2024-01-20T14:00:00",
      "update_available": true,
      "update_queued_date": "2024-01-20T14:00:00",
      "auto_update": true
    }
  }
}
```

## Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Skill identifier |
| `source` | enum | Where the skill came from |
| `source_url` | string | Link to source (GitHub repo, clawhub page, etc.) |
| `description` | string | Human-readable description |
| `trust_score` | int | 0-100 trust rating from vetting |
| `risk_flags` | array | Security warnings from skill-vetter |
| `current_version` | string | Installed version |
| `latest_version` | string | Available version |
| `added_date` | ISO date | When first added to registry |
| `last_updated` | ISO date | When last updated |
| `update_available` | bool | Is an update queued? |
| `update_queued_date` | ISO date | When update was detected |
| `auto_update` | bool | Allow automatic updates? |

## Trust Score Levels

- **90-100**: Core/Verified - No flags, well-maintained
- **70-89**: Trusted - Minor flags or new skill
- **50-69**: Caution - Some risk flags, review needed
- **0-49**: High Risk - Multiple flags, manual approval required
