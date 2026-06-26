# Skill Rank Architecture

## System Overview

Skill Rank is a meta-skill that analyzes all available skills on ClawHub, computes quality metrics, and provides comprehensive rankings.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Skill Rank                              │
├─────────────────────────────────────────────────────────────┤
│  1. Fetch Skill List ← ClawHub Registry / GitHub API        │
│  2. Pull Documentation ← SKILL.md / README.md               │
│  3. Parse Metadata ← Extract description, version, deps     │
│  4. Compute Scores ← Multi-dimensional weighted scoring     │
│  5. Store & Cache ← SQLite database + doc cache             │
│  6. Query Interface ← CLI commands for user interaction     │
│  7. Periodic Update ← Cron task for refresh                 │
└─────────────────────────────────────────────────────────────┘
```

## Data Sources

### 1. ClawHub Registry

Primary source for skill discovery:

```
https://raw.githubusercontent.com/openclaw/skills-registry/main/index.json
```

Expected format:
```json
{
  "skills": [
    {
      "name": "skill-name",
      "repo_url": "https://github.com/owner/repo",
      "description": "Skill description"
    }
  ]
}
```

### 2. GitHub API

For each skill repository, fetch:
- Repository metadata (stars, forks, issues, license)
- Commit history (last commit date)
- File contents (SKILL.md, README.md)

### 3. Local Installed Skills

Scan `~/.openclaw/workspace/skills/` for locally installed skills.

## Scoring Algorithm

### Dimensions

| Dimension | Weight | Factors |
|-----------|--------|---------|
| Activity | 30% | Last commit recency, release frequency |
| Popularity | 25% | Stars, forks, watchers |
| Documentation | 20% | Length, structure, examples |
| Dependencies | 10% | Number, health, conflicts |
| Compatibility | 10% | Platform support, version support |
| Maintainer | 5% | Reputation, organization status |

### Score Calculation

```python
def compute_total_score(scores, weights):
    total = 0
    for dimension, score in scores.items():
        weight = weights.get(dimension, 0)
        total += score * weight
    return round(total, 2)
```

### Normalization

All dimension scores are normalized to 0-100:

- **Activity**: Based on days since last commit
  - < 7 days: 100
  - < 30 days: 90
  - < 90 days: 75
  - < 180 days: 60
  - < 365 days: 40
  - > 365 days: 20

- **Popularity**: Logarithmic scale
  ```python
  stars_score = min(log10(stars + 1) * 20, 50)
  forks_score = min(log10(forks + 1) * 25, 35)
  watchers_score = min(log10(watchers + 1) * 15, 15)
  ```

- **Documentation**: Content analysis
  - Length: up to 30 points
  - Structure (headers, code blocks, lists): up to 40 points
  - Quality indicators (examples, install instructions): up to 30 points

## Database Schema

### skills table

```sql
CREATE TABLE skills (
    name TEXT PRIMARY KEY,
    repo_url TEXT,
    description TEXT,
    stars INTEGER DEFAULT 0,
    forks INTEGER DEFAULT 0,
    watchers INTEGER DEFAULT 0,
    open_issues INTEGER DEFAULT 0,
    last_commit TIMESTAMP,
    created_at TIMESTAMP,
    license TEXT,
    doc_content TEXT,
    doc_quality_score REAL DEFAULT 0,
    activity_score REAL DEFAULT 50,
    popularity_score REAL DEFAULT 50,
    doc_score REAL DEFAULT 50,
    deps_score REAL DEFAULT 50,
    compat_score REAL DEFAULT 50,
    maintainer_score REAL DEFAULT 50,
    total_score REAL DEFAULT 0,
    rank INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT
);
```

### cache_meta table

```sql
CREATE TABLE cache_meta (
    url_hash TEXT PRIMARY KEY,
    url TEXT,
    cached_at TIMESTAMP,
    etag TEXT,
    status TEXT
);
```

## API Rate Limiting

GitHub API has rate limits:
- Unauthenticated: 60 requests/hour
- Authenticated: 5000 requests/hour

### Mitigation Strategies

1. **Caching**: Store results locally, refresh only when stale
2. **Conditional Requests**: Use `If-Modified-Since` header
3. **Token Authentication**: Recommend `GITHUB_TOKEN` env var
4. **Batch Processing**: Process skills in batches with delays

## Configuration

User configuration stored in `~/.openclaw/skill-rank/config.json`:

```json
{
  "weights": {
    "activity": 0.30,
    "popularity": 0.25,
    "documentation": 0.20,
    "dependencies": 0.10,
    "compatibility": 0.10,
    "maintainer": 0.05
  },
  "cache_ttl_hours": 24,
  "github_api_token": "",
  "clawhub_registry_url": "https://raw.githubusercontent.com/openclaw/skills-registry/main/index.json",
  "top_n_default": 10
}
```

## CLI Commands

### List Top Skills
```bash
python3 scripts/skill-rank.py --list [--top N]
```

### Search Skills
```bash
python3 scripts/skill-rank.py --search <keyword>
```

### Skill Details
```bash
python3 scripts/skill-rank.py --info <skill-name>
```

### Update Database
```bash
python3 scripts/skill-rank.py --update [--full]
```

### Configure
```bash
python3 scripts/skill-rank.py --config
```

## Integration Points

### With Auto-Updater

```bash
openclaw cron add \
  --name "Skill Rank Refresh" \
  --cron "0 3 * * 0" \
  --session isolated \
  --message "Run skill-rank --update"
```

### With ClawHub CLI

```bash
# After viewing rankings
clawhub install <skill-name>
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Database not found | First run | Run `--update` |
| Rate limit exceeded | Too many API calls | Wait or set GITHUB_TOKEN |
| Skill not found | Invalid name | Check spelling, run `--update` |
| Network error | Connection issue | Retry, check connectivity |

## Future Enhancements

1. **Web Dashboard**: HTML report generation
2. **Trend Analysis**: Track score changes over time
3. **Personalized Rankings**: Based on user's installed skills
4. **Skill Similarity**: Recommend similar skills
5. **Review Integration**: Incorporate user reviews/ratings
