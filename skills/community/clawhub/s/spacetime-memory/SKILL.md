---
name: spacetime-memory
description: High-performance SpacetimeDB memory integration for OpenClaw. Replaces static file memory with a lightning-fast WebAssembly-powered mind-vault running on a local SpacetimeDB instance. Now includes full CRUD support, legacy file imports, and consolidation tools.
acceptLicenseTerms: true
metadata: {"openclaw":{"emoji":"🧠","tools":["tools/stdb_search.json","tools/stdb_store.json","tools/stdb_edit.json","tools/stdb_forget.json"],"install":[{"id":"npm-deps","kind":"script","sh":"npm install","label":"Install npm dependencies"}],"env":{"SPACETIMEDB_URL":{"description":"URL of the SpacetimeDB instance (default: http://127.0.0.1:3001)","optional":true},"SPACETIMEDB_NAME":{"description":"Name of the database (default: stdb-memory-1vgys)","optional":true}}}}
---

# SpacetimeDB Memory Integration

This skill provides a low-latency, WebAssembly-powered memory system for OpenClaw using [SpacetimeDB](https://spacetimedb.com/).
It connects directly to a locally running instance of SpacetimeDB to store, query, update, and delete long-term memories.

## Available Tools
* **stdb_store**: Stores a new memory string and optional tags.
* **stdb_search**: Queries local memory by tags or text.
* **stdb_edit**: Updates an existing memory's content and tags by its ID.
* **stdb_forget**: Deletes a specific memory entirely by its ID.

## Environment Variables
The tools support the following optional environment variables to customize connection settings:
- `SPACETIMEDB_URL` - Endpoint for the database (default: `http://127.0.0.1:3001`)
- `SPACETIMEDB_NAME` - Database identity/name (default: `stdb-memory-1vgys`)

## Legacy Import
A legacy import script is included to help migrate old flat-file memories (like `MEMORY.md`, `IDENTITY.md`, etc.).

**⚠️ CRITICAL INSTRUCTION:** The legacy import script is destructive. It modifies core user files in the workspace, creates `.bak` copies, and overwrites the originals with migration notices. 
To prevent accidental or unauthorized destruction of user data, the script enforces a strict run-time safeguard. It will not run unless you explicitly provide the `--confirm` flag and the direct target path. You **MUST** obtain explicit approval from the user before executing it.

Run it via:
`node ~/.openclaw/workspace/skills/spacetime-memory/legacy-import.js --confirm ~/.openclaw/workspace`
