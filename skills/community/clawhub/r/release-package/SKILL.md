---
name: Storage Manager
description: Feishu Bitable Storage Manager - Integrated tool for item storage, retrieval, and location updates
read_when:
  - Need to record item storage locations
  - Need to find item locations
  - Need to update item locations
  - Need to manage personal item storage
metadata: {"clawdbot":{"emoji":"box","requires":{"bins":["python3"]}}}
allowed-tools: Bash(storage-manager:*)
---

# Storage Manager

Intelligent storage management tool based on Feishu Bitable.

## Core Features
1. Item Storage (add_storage_item)
2. Item Retrieval (search_storage_item)
3. Location Update (update_storage_location)

## Usage
- storage-manager add [item] [location]
- storage-manager search [item]
- storage-manager update [item] [new_location]

## Requirements
- Python 3.6+
- requests >= 2.25.0
- Feishu app credentials

