# Basic Usage Examples

## Initialize Memory on a Fresh VM

```bash
# Install the skill
openclaw skill install vm-memory-oracle

# Initialize directory structure
openclaw skill run vm-memory-oracle --action init

# Verify
ls -la /data/memory/
# Expected output:
# knowledge-graph/
# embeddings/
# daily/
# sessions/
# activation-metadata.json
# MEMORY.md
# health.json
```

## Store and Recall a Fact

```bash
# During a session, the agent stores a fact:
# (This happens automatically through the skill's ingestion pipeline)

# Fact stored in knowledge-graph/facts.jsonl:
# {"id":"fact-a1b2c3","subject":"project-alpha","predicate":"deadline","object":"2026-06-30","source":"user-stated","created":"2026-05-15T14:30:00Z","activation":1.0}

# Later, the agent recalls:
# Query: "When is the project alpha deadline?"
# Result: "2026-06-30" (activation boosted from recall)
```

## Run Manual Consolidation

```bash
# Summarize today's sessions
openclaw skill run vm-memory-oracle --action summarize

# Run full consolidation
openclaw skill run vm-memory-oracle --action consolidate

# Check results
cat /data/memory/health.json | jq '.status, .total_facts, .avg_activation'
# "healthy"
# 2847
# 0.42
```

## Check Memory Health

```bash
openclaw skill run vm-memory-oracle --action health-check
cat /data/memory/health.json | jq .

# Example healthy output:
# {
#   "status": "healthy",
#   "disk_usage_percent": 3.3,
#   "total_facts": 2847,
#   "active_facts": 2103,
#   "avg_activation": 0.42,
#   "warnings": []
# }

# Example with warnings:
# {
#   "status": "warning",
#   "disk_usage_percent": 85,
#   "total_facts": 9200,
#   "warnings": [
#     "Disk usage high",
#     "Approaching fact limit"
#   ]
# }
```

## Set Up Automated Maintenance

```bash
# Install cron jobs for automated lifecycle management
openclaw skill run vm-memory-oracle --action install-cron

# Verify cron jobs were created
cat /etc/cron.d/openclaw-vm-memory-oracle
# 0 23 * * * openclaw skill run vm-memory-oracle --action summarize
# 30 0 * * * openclaw skill run vm-memory-oracle --action consolidate
# 0 */6 * * * openclaw skill run vm-memory-oracle --action health-check
# 0 3 * * 0 openclaw skill run vm-memory-oracle --action quality-probe
```

## Run Quality Probe

```bash
# First, add canary facts for testing
cat > /data/memory/knowledge-graph/canary-facts.json << 'EOF'
[
  {
    "query": "When did the fleet deployment project start?",
    "expected_contains": "May 15, 2026"
  },
  {
    "query": "What VM size is recommended for medium workloads?",
    "expected_contains": "Standard_D4s_v5"
  },
  {
    "query": "What is the default memory decay half-life?",
    "expected_contains": "30 days"
  }
]
EOF

# Run the probe
openclaw skill run vm-memory-oracle --action quality-probe

# Check results in health.json
cat /data/memory/health.json | jq '.quality_probe'
# {
#   "last_run": "2026-05-18T03:00:00Z",
#   "passed": 3,
#   "total": 3,
#   "accuracy_percent": 100
# }
```

## Custom Configuration

```yaml
# Override defaults in your agent config
memory_oracle:
  data_path: /mnt/persistent/memory    # Custom mount point
  half_life_days: 14                    # Faster decay for high-volume agents
  max_facts: 5000                       # Lower cap for smaller VMs
  embedding_device: gpu                 # Use GPU if available
  session_retention_days: 7             # Aggressive session cleanup
```
