# Zilliz Cloud CLI Skill

A skill that teaches AI agents how to operate [Zilliz Cloud](https://zilliz.com/) and Milvus vector databases through `zilliz-cli`. Instead of memorizing CLI commands, just describe what you want:

- "Create a serverless cluster in us-east-1 and set up a collection with 768-dimension vectors"
- "Search for similar items in my product collection with filter age > 20"
- "Show me the status of all my clusters and collections"
- "Set up a daily backup policy for my production cluster with 7-day retention"
- "Create a role with read-only access to the analytics collection"

## Skill Structure

```
zilliz/
├── SKILL.md                      # Main entry — prerequisites, workflows, safety rules
└── references/                   # Domain-specific command references (loaded on demand)
    ├── setup.md                  # Install, auth, context, config, troubleshooting
    ├── cluster.md                # Cluster create, list, describe, modify, suspend, delete
    ├── collection.md             # Collection CRUD, aliases, load/release
    ├── vector.md                 # Search, query, insert, hybrid search, filter syntax
    ├── index.md                  # Index types, create/drop
    ├── database.md               # Database CRUD (Dedicated clusters only)
    ├── partition.md              # Partition management
    ├── user-role.md              # RBAC: users, roles, privileges
    ├── backup.md                 # Backup/restore, policies
    ├── import.md                 # Bulk data import from cloud storage
    ├── billing.md                # Usage, invoices, payment
    ├── monitoring.md             # Status overview, collection stats
    └── project-region.md         # Projects, volumes, cloud providers
```

## Capabilities

| Area | What You Can Do |
|------|----------------|
| **Clusters** | Create, delete, suspend, resume, modify |
| **Collections** | Create with custom schema, load, release, rename, drop |
| **Vectors** | Search, query, insert, upsert, delete, hybrid search |
| **Indexes** | Create (AUTOINDEX), list, describe, drop |
| **Databases** | Create, list, describe, drop |
| **Users & Roles** | RBAC setup, privilege management |
| **Backups** | Create, restore, export, policy management |
| **Import** | Bulk data import from S3/GCS |
| **Partitions** | Create, load, release, manage |
| **Monitoring** | Cluster status, collection stats, load states |
| **Projects** | Project and region management |
| **Billing** | Usage queries, invoices |

## Installation

### Claude Code

```bash
claude skill add ./zilliz.skill
```

### Manual

Copy the `zilliz/` directory into your skill path and ensure SKILL.md is discoverable by your agent.

## Requirements

- Python 3.10+
- A [Zilliz Cloud](https://cloud.zilliz.com/) account
- `zilliz-cli` (the skill guides installation automatically)

## Origin

Extracted from the [zilliz-plugin](https://github.com/zilliztech/zilliz-plugin) Claude Code plugin. The 13 reference files correspond directly to the plugin's `skills/` directory.

## License

Apache License 2.0
