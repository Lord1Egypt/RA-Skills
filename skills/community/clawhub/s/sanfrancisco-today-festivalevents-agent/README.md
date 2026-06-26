# San Francisco Today Festival & Events Harvester Agent

An autonomous agent specialized in harvesting and indexing live event data occurring today in San Francisco. Optimized for execution on high-performance edge hardware like NVIDIA DGX Spark and Jetson Orin NX.

## Capabilities
- **Real-Time Pulse**: Direct scraping of today's events from curated SF sources.
- **Autonomous RAG**: Native ChromaDB integration provides LLMs with updated local context.
- **Cost Detection**: Automatically parses event descriptions to flag "Free" vs "Paid" activities.
- **Skill Integration**: Optimized for ClawHub with JSON and CLI search capabilities.

## Installation

```bash
# Clone the skill
git clone [https://github.com/assix/sf-event-agent.git](https://github.com/assix/sf-event-agent.git)
cd sf-event-agent

# Install dependencies
pip install requests beautifulsoup4 chromadb
```

## CLI Usage

### List Today's Top Events
```bash
python SanFrancisco-Today-FestivalEvents-Harvester-Agent.py --action list --scope top
```

### Update Vector Database (Ingest)
```bash
python SanFrancisco-Today-FestivalEvents-Harvester-Agent.py --action ingest --scope full
```

### Semantic Search
```bash
python SanFrancisco-Today-FestivalEvents-Harvester-Agent.py --action search --query "free comedy shows"
```

## Agent Manifest
- **Source**: `SanFrancisco-Today-FestivalEvents-Harvester-Agent.py`
- **Owner**: [assix](https://clawhub.ai/u/assix)
- **Environment**: Python 3.10
- **Persistence**: ChromaDB (Path: `./rag_db`)