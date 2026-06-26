---
name: securityclaw-autonomous-soc-agent
description: Deploy and operate SecurityClaw, an autonomous SOC agent with RAG-based threat detection, LLM-powered anomaly analysis, and skill-based security automation
triggers:
  - set up an autonomous security operations center agent
  - deploy SecurityClaw for threat detection and anomaly monitoring
  - configure RAG-based behavioral memory for security analytics
  - build a skill-based SOC automation framework
  - integrate LLM-powered threat analysis with OpenSearch
  - create an AI security agent with anomaly detection
  - implement automated threat hunting with LangGraph orchestration
  - set up continuous security monitoring with vector embeddings
---

# SecurityClaw Autonomous SOC Agent

> Skill by [ara.so](https://ara.so) — Security Skills collection.

SecurityClaw is a modular, skill-based autonomous Security Operations Center (SOC) agent that monitors OpenSearch/Elasticsearch data, builds RAG-based behavioral memory, and validates real-time anomalies using LLMs. It orchestrates security workflows through LangGraph, maintains conversation-based investigations, and provides both CLI and web interfaces for threat analysis.

## Core Capabilities

- **Skill-based architecture**: Each capability is an isolated module with Python logic + LLM instruction
- **RAG behavioral memory**: Vector embeddings of network baselines stored in OpenSearch
- **Anomaly detection**: Scheduled 1-minute watcher polls findings and escalates threats
- **LLM-powered analysis**: Threat analyst validates anomalies using retrieval-augmented context
- **LangGraph orchestration**: DECIDE→EXECUTE→EVALUATE supervisor loop with SQLite checkpointing
- **Web + CLI interfaces**: React UI for chat investigations, CLI for automation
- **Provider agnostic**: Swap OpenSearch↔Elasticsearch, Ollama↔other LLM providers

## Installation

### Prerequisites

```bash
# Python 3.11+ required
python --version

# Install Ollama for LLM provider
curl -fsSL https://ollama.com/install.sh | sh
ollama serve

# Pull recommended models
ollama pull qwen2.5:7b-instruct-q4_K_M
ollama pull nomic-embed-text:latest
```

### Setup

```bash
# Clone repository
git clone https://github.com/SecurityClaw/SecurityClaw.git
cd SecurityClaw

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run interactive onboarding wizard
python main.py onboard
```

The onboarding wizard configures:
- OpenSearch/Elasticsearch connection (host, port, SSL, auth)
- LLM provider (Ollama endpoint, model names)
- Optional external APIs (AbuseIPDB, VirusTotal, MaxMind GeoIP)
- Skill-specific environment variables

Outputs `config.yaml` and `.env` with validated configuration.

## Configuration

### config.yaml Structure

```yaml
# Database configuration
database:
  provider: opensearch  # or elasticsearch
  host: localhost
  port: 9200
  use_ssl: true
  verify_certs: false
  username: admin
  password_env: OPENSEARCH_PASSWORD  # Reads from .env

# LLM provider
llm:
  provider: ollama
  base_url: http://localhost:11434
  model: qwen2.5:7b-instruct-q4_K_M
  temperature: 0.7
  max_tokens: 16384

# RAG engine
rag:
  index_name: securityclaw_baselines
  embedding_model: nomic-embed-text:latest
  embedding_dimension: 768
  top_k: 5

# API server
api:
  host: 0.0.0.0
  port: 7799
  enable_cors: true
```

### Environment Variables (.env)

```bash
# Database credentials
OPENSEARCH_PASSWORD=your_password_here

# Optional external APIs
ABUSEIPDB_API_KEY=${ABUSEIPDB_API_KEY}
VIRUSTOTAL_API_KEY=${VIRUSTOTAL_API_KEY}
MAXMIND_LICENSE_KEY=${MAXMIND_LICENSE_KEY}

# Skill-specific variables (discovered by onboard command)
ANOMALY_TRIAGE_THRESHOLD=0.7
```

## CLI Commands

### Service Management

```bash
# Start full service (scheduler + web UI + API)
python main.py service
# Access web UI at http://localhost:5173
# API at http://localhost:7799

# Start API only (no background scheduler)
SECURITYCLAW_API_ONLY=1 python main.py service

# Start scheduler loop only (no web interface)
python main.py run

# Web development mode (frontend with hot reload)
python main.py web-dev
```

### Skill Operations

```bash
# List all loaded skills and their schedules
python main.py list-skills

# Manually dispatch a skill once
python main.py dispatch network_baseliner
python main.py dispatch threat_analyst

# Interactive chat interface (CLI)
python main.py chat

# View agent memory snapshot
python main.py status
```

### Configuration Management

```bash
# Re-run onboarding wizard
python main.py onboard

# Validate current configuration
python main.py validate-config
```

## Skill Development

### Creating a New Skill

Skills are directories in `skills/` with two required files:

**skills/my_skill/instruction.md** (LLM guidance + metadata):

```markdown
---
skill_id: my_skill
display_name: My Custom Skill
version: 1.0.0
schedule_interval_seconds: 3600  # Optional: for scheduled execution
capabilities:
  - custom_analysis
prerequisites:
  - network_data
required_entities:
  - ip_address
artifacts_produced:
  - analysis_report
---

# System Prompt for My Skill

You are a security analyst performing custom analysis.

## Task
Analyze network data and produce findings.

## Output Format
Return JSON with "findings" array.
```

**skills/my_skill/logic.py** (Python implementation):

```python
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def execute(
    db_connector,
    llm_provider,
    rag_engine,
    config: Dict[str, Any],
    memory: Dict[str, Any],
    **kwargs
) -> Dict[str, Any]:
    """
    Skill entrypoint.
    
    Args:
        db_connector: OpenSearch/ES client
        llm_provider: LLM client
        rag_engine: RAG context retrieval
        config: Skill-specific config from instruction.md
        memory: Shared agent memory (read/write)
        **kwargs: Additional context (user_query, conversation_id, etc.)
    
    Returns:
        Dict with success status and results
    """
    logger.info("Executing my_skill")
    
    # Query database
    query = {
        "size": 100,
        "query": {"match_all": {}},
        "sort": [{"@timestamp": "desc"}]
    }
    results = db_connector.search(index="network-*", body=query)
    
    # Retrieve RAG context
    context = rag_engine.retrieve("recent network behavior", top_k=3)
    
    # Call LLM with context
    prompt = f"""Analyze these network events:
{results['hits']['hits'][:5]}

Baseline context:
{context}

Identify anomalies."""
    
    response = llm_provider.chat([
        {"role": "system", "content": config.get("system_prompt", "")},
        {"role": "user", "content": prompt}
    ])
    
    # Update shared memory
    memory.setdefault("my_skill_runs", []).append({
        "timestamp": "2026-05-19T10:00:00Z",
        "findings_count": len(results['hits']['hits'])
    })
    
    return {
        "success": True,
        "findings": response["content"],
        "context_used": len(context)
    }
```

The skill is auto-discovered on next run. Set `schedule_interval_seconds` in `instruction.md` to enable automatic execution.

## Built-in Skills

### network_baseliner (6-hour schedule)

Builds behavioral baselines from network logs:

```python
# Triggered automatically every 6 hours
# Aggregates normal traffic patterns into RAG vectors
# Used by threat_analyst for context

# Manual dispatch:
python main.py dispatch network_baseliner
```

### anomaly_triage (Manual, convertible to scheduled)

Polls OpenSearch Anomaly Detection findings:

```python
# Currently manual dispatch:
python main.py dispatch anomaly_triage

# To enable 1-minute polling, add to skills/anomaly_triage/instruction.md:
# schedule_interval_seconds: 60
```

Escalates high-confidence anomalies to memory queue for analysis.

### threat_analyst (Manual, convertible to scheduled)

Analyzes escalated findings with RAG context:

```python
# Manual threat analysis:
python main.py dispatch threat_analyst

# Returns verdict with LLM reasoning:
# {
#   "verdict": "malicious",
#   "confidence": 0.85,
#   "reasoning": "Unusual port scan pattern...",
#   "context_sources": ["baseline_2026-05-15", ...]
# }
```

### opensearch_querier (Manual)

Executes raw database queries:

```python
# Via chat interface:
# "Query OpenSearch for failed logins in the last hour"

# Skill constructs and executes:
# GET /auth-logs-*/_search
# {
#   "query": {
#     "bool": {
#       "must": [
#         {"match": {"event.outcome": "failure"}},
#         {"range": {"@timestamp": {"gte": "now-1h"}}}
#       ]
#     }
#   }
# }
```

### geoip_lookup (Cron: Tue/Fri 2 AM UTC)

Maintains MaxMind GeoLite2 database:

```python
# Automatically updates GeoIP databases
# Requires MAXMIND_LICENSE_KEY in .env

# Manual update:
python main.py dispatch geoip_lookup
```

## API Usage

### Chat Endpoint (SSE Streaming)

```python
import requests
import json

url = "http://localhost:7799/chat"
payload = {
    "message": "Analyze recent anomalies and check if 192.168.1.100 is malicious",
    "conversation_id": "investigation_001"  # Optional: for multi-turn context
}

# Server-Sent Events stream
response = requests.post(url, json=payload, stream=True)
for line in response.iter_lines():
    if line.startswith(b"data: "):
        data = json.loads(line[6:])
        
        if data["type"] == "reasoning":
            print(f"[THINK] {data['content']}")
        elif data["type"] == "skill_call":
            print(f"[SKILL] {data['skill_name']}: {data['reasoning']}")
        elif data["type"] == "skill_result":
            print(f"[RESULT] {data['summary']}")
        elif data["type"] == "final":
            print(f"[ANSWER] {data['content']}")
```

### Dispatch Skill

```python
import requests

response = requests.post(
    "http://localhost:7799/dispatch",
    json={"skill_name": "threat_analyst"}
)

result = response.json()
# {
#   "success": true,
#   "skill": "threat_analyst",
#   "result": {...},
#   "execution_time": 2.34
# }
```

### Query Memory

```python
response = requests.get("http://localhost:7799/memory")
memory = response.json()

# {
#   "escalated_findings": [...],
#   "last_baseline_run": "2026-05-19T04:00:00Z",
#   "anomaly_triage_cursor": "1234567890",
#   "conversation_count": 5
# }
```

## LangGraph Orchestration

SecurityClaw uses LangGraph for chat routing with a supervisor pattern:

```python
# core/chat_router/graph.py structure
from langgraph.graph import StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver

class ChatState(TypedDict):
    messages: List[Dict]
    user_query: str
    plan: str
    skill_results: List[Dict]
    final_answer: str
    retry_count: int

def decide_node(state):
    """Supervisor plans which skills to invoke"""
    # Analyzes query against skill manifests
    # Returns plan with skill sequence
    pass

def execute_node(state):
    """Executes planned skills"""
    # Dispatches skills with context
    # Collects results
    pass

def evaluate_node(state):
    """Checks if answer is complete"""
    # Validates against user query
    # Triggers retry if insufficient
    pass

# Graph construction
workflow = StateGraph(ChatState)
workflow.add_node("decide", decide_node)
workflow.add_node("execute", execute_node)
workflow.add_node("evaluate", evaluate_node)

workflow.set_entry_point("decide")
workflow.add_edge("decide", "execute")
workflow.add_conditional_edges(
    "evaluate",
    should_continue,
    {"continue": "decide", "end": END}
)

# Checkpoint to SQLite
memory = SqliteSaver.from_conn_string("data/conversations.db")
app = workflow.compile(checkpointer=memory)
```

## Common Patterns

### Building Custom Threat Detection

```python
# skills/custom_detector/logic.py
def execute(db_connector, llm_provider, rag_engine, config, memory, **kwargs):
    # 1. Query recent events
    events = db_connector.search(
        index="network-*",
        body={
            "size": 1000,
            "query": {
                "range": {"@timestamp": {"gte": "now-1h"}}
            }
        }
    )
    
    # 2. Retrieve behavioral baseline
    baseline = rag_engine.retrieve(
        query="normal traffic patterns last 24h",
        top_k=5
    )
    
    # 3. LLM analysis with context
    threats = []
    for hit in events['hits']['hits']:
        event = hit['_source']
        
        prompt = f"""Event: {event}
Baseline: {baseline}

Is this anomalous? Respond JSON: {{"anomalous": bool, "reason": str}}"""
        
        response = llm_provider.chat([
            {"role": "user", "content": prompt}
        ])
        
        analysis = json.loads(response['content'])
        if analysis['anomalous']:
            threats.append({
                "event": event,
                "reason": analysis['reason']
            })
    
    # 4. Store findings in memory
    memory.setdefault("custom_threats", []).extend(threats)
    
    return {
        "success": True,
        "threats_found": len(threats),
        "details": threats
    }
```

### Enriching with External Threat Intel

```python
# skills/ip_enricher/logic.py
import os
import requests

def execute(db_connector, llm_provider, rag_engine, config, memory, **kwargs):
    suspicious_ips = kwargs.get("ip_addresses", [])
    
    enriched = []
    for ip in suspicious_ips:
        # AbuseIPDB lookup
        headers = {"Key": os.getenv("ABUSEIPDB_API_KEY")}
        response = requests.get(
            f"https://api.abuseipdb.com/api/v2/check",
            params={"ipAddress": ip, "maxAgeInDays": 90},
            headers=headers
        )
        
        data = response.json()
        enriched.append({
            "ip": ip,
            "abuse_score": data.get("data", {}).get("abuseConfidenceScore", 0),
            "reports": data.get("data", {}).get("totalReports", 0)
        })
    
    return {
        "success": True,
        "enriched_ips": enriched
    }
```

### Multi-Skill Investigation Workflow

```python
# Via chat interface or API:
# User: "Investigate source IP 10.0.0.50 - check logs, enrich with threat intel, analyze behavior"

# LangGraph supervisor plans:
# 1. opensearch_querier: fetch logs for 10.0.0.50
# 2. ip_enricher: check external reputation
# 3. baseline_querier: retrieve normal behavior for this IP
# 4. threat_analyst: final verdict with all context

# Automatic skill chaining based on manifests:
# - opensearch_querier provides "query_results" artifact
# - ip_enricher requires "ip_address" entity (extracted from results)
# - threat_analyst consumes all previous artifacts
```

## Troubleshooting

### Connection Issues

```bash
# Test OpenSearch connection
curl -k -u admin:password https://localhost:9200

# Test Ollama
curl http://localhost:11434/api/tags

# Validate config
python main.py validate-config
```

### Skill Not Loading

```bash
# Check skill discovery
python main.py list-skills

# Verify instruction.md has valid YAML frontmatter
# Required fields: skill_id, display_name, version

# Check logic.py has execute() function:
def execute(db_connector, llm_provider, rag_engine, config, memory, **kwargs):
    pass
```

### RAG Context Not Used

```python
# Verify embeddings index exists
from core.db_connector import get_db_connector
db = get_db_connector()
indices = db.cat_indices()
# Should show: securityclaw_baselines

# Rebuild baseline if empty
python main.py dispatch network_baseliner

# Check embedding model is running
ollama list  # Should show nomic-embed-text:latest
```

### Memory State Issues

```bash
# Reset conversation memory (keeps runtime memory)
rm data/conversations.db

# Reset all memory (caution: loses baselines)
rm data/conversations.db data/runtime_memory.db

# View memory structure
python -c "
from core.memory import AgentMemory
memory = AgentMemory()
print(memory.get_summary())
"
```

### LLM Response Truncation

```yaml
# Increase token budget in config.yaml
llm:
  max_tokens: 32768  # Default: 16384

# Reduce context injection in prompts
# Edit core/memory.py max_context_chars (default: 4000)
```

### Web UI Not Loading

```bash
# Build frontend if dist/ missing
cd web
npm install
npm run build

# Check API server logs
python main.py service
# Should show: "API server started on http://0.0.0.0:7799"

# Verify CORS enabled in config.yaml
api:
  enable_cors: true
```

## Testing

```bash
# Run test suite with mock providers
pytest tests/ -v

# Coverage report
pytest tests/ --cov=core --cov=skills --cov-report=html

# Test specific skill
pytest tests/test_threat_analyst.py -v

# Use mock OpenSearch (no real database needed)
# tests/conftest.py provides mock_db_connector fixture
```

## Production Considerations

- **Resource limits**: 8GB+ RAM recommended for production with multiple concurrent investigations
- **Checkpoint cleanup**: Prune old conversations in `data/conversations.db` periodically
- **RAG index maintenance**: Archive old baselines, rebuild quarterly for evolving network patterns
- **API authentication**: Add auth middleware to `web/api/server.py` before exposing publicly
- **Secrets management**: Rotate API keys in `.env`, use secret managers for production deployments
- **Monitoring**: Track skill execution times, LLM token usage, and anomaly escalation rates
