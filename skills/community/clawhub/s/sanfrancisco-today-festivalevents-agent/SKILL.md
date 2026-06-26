---
name: sf-today-events-harvester
description: Harvests, indexes, and searches today's festivals and events in San Francisco.
homepage: https://clawhub.ai/u/assix
metadata:
  clawdbot:
    emoji: "🌉"
    requires:
      env: []
    files: ["SanFrancisco-Today-FestivalEvents-Harvester-Agent.py"]
---

# San Francisco Today Events Harvester

This skill provides the ability to scrape live event data from SF Funcheap and interact with a local RAG database (ChromaDB) to find specific activities.

## Agent Instructions
When the user asks about events in San Francisco today:
1. Use the script `SanFrancisco-Today-FestivalEvents-Harvester-Agent.py`.
2. To see live listings, run: `python3 SanFrancisco-Today-FestivalEvents-Harvester-Agent.py --action list --scope top`
3. To search previous harvests, run: `python3 SanFrancisco-Today-FestivalEvents-Harvester-Agent.py --action search --query "<user query>"`
4. To update the local database with full listings, run: `python3 SanFrancisco-Today-FestivalEvents-Harvester-Agent.py --action ingest --scope full`