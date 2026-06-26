---
name: proxy
description: Local-first proxy inventory, routing planner, and health tracking engine. Use whenever the user needs to organize proxy assets, compare providers, track regions, protocols, auth methods, manage expiry, assign sessions, or decide which proxy best fits a task. Stores all data locally only.
---

# Proxy

Know what you have. Route with intention.

## Core Philosophy
1. Treat proxies as infrastructure assets, not throwaway strings.
2. Recommendation quality matters more than raw inventory size.
3. Track health, expiry, and fit-for-purpose before choosing a proxy.
4. Keep all proxy metadata local-only.

## Runtime Requirements
- Python 3 must be available as `python3`
- No external packages required

## Storage
All data is stored locally only under:
- `~/.openclaw/workspace/memory/proxy/proxies.json`
- `~/.openclaw/workspace/memory/proxy/sessions.json`
- `~/.openclaw/workspace/memory/proxy/stats.json`

No external sync. No cloud storage. No third-party proxy APIs required.

## What This Skill Manages
- provider
- host and port
- protocol
- region / country / city
- auth type
- sticky or rotating behavior
- session labels
- status and health notes
- expiry date
- cost and quality metadata

## Key Workflows
- **Add Proxy**: `add_proxy.py` to record a proxy and its metadata
- **List Inventory**: `list_proxies.py` to view and filter available proxies
- **Pick Best Fit**: `pick_proxy.py` to recommend the best proxy for a given use case
- **Score Quality**: `score_proxy.py` to update health, reliability, and fit
- **Update Metadata**: `update_proxy.py` to change status, expiry, notes, or tags

## Scripts
| Script | Purpose |
|---|---|
| `init_storage.py` | Initialize local storage files |
| `add_proxy.py` | Add a proxy asset |
| `list_proxies.py` | List and filter proxies |
| `score_proxy.py` | Score reliability and quality |
| `pick_proxy.py` | Recommend the best proxy for a task |
| `update_proxy.py` | Update status, expiry, notes, or tags |
