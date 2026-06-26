---
name: zettabrain-rag
description: Query documents on your NFS shares, SMB servers, or local drive using local AI. No cloud, no Docker, no API keys — the only RAG skill that reads from enterprise storage directly. Runs on your own machine with Ollama + ChromaDB.
version: 1.0.2
emoji: "🧠"
homepage: https://zettabrain.io
metadata:
  openclaw:
    requires:
      anyBins: [zettabrain-chat, zettabrain-ingest]
    install:
      - kind: brew
        formula: pipx
        bins: [pipx]
    envVars:
      - name: ZETTABRAIN_DOCS
        required: false
        description: Path to your documents folder (e.g. ~/Documents/ZettaBrain). Overrides the value set during zettabrain-setup.
      - name: ZETTABRAIN_LLM_MODEL
        required: false
        description: Ollama model name to use (e.g. llama3.1:8b, qwen2.5:14b). Defaults to the model selected during setup.
      - name: OLLAMA_HOST
        required: false
        description: "Ollama API URL. Default: http://localhost:11434 (local). WARNING: setting this to a remote host sends document queries off-machine."
---

# ZettaBrain RAG Skill

Chat with your own documents using a local AI. Document data stays on your machine **when you use local storage and a local Ollama endpoint** (the default). Remote storage (S3, NFS, SMB) and a remote `OLLAMA_HOST` are optional and will move data off-device — see the [Privacy](#privacy) section.

Supports **PDF, DOCX, TXT, Markdown**. Works on Linux, macOS (including EC2 Mac Apple Silicon), and Windows.

- **Source code**: https://github.com/zettabrain/zettabrain-rag (MIT)
- **Installer scripts**: https://github.com/zettabrain/zettabrain-rag/blob/main/install.sh | [install.ps1](https://github.com/zettabrain/zettabrain-rag/blob/main/install.ps1)
- **PyPI**: https://pypi.org/project/zettabrain-rag/

## Install

### Recommended — pipx (no elevated privileges, fully inspectable)
```bash
pipx install zettabrain-rag
sudo zettabrain-setup
```

### One-line installer (review source before running)
The installer scripts are open source and auditable at the links above before execution.

```bash
# Linux — review first: https://github.com/zettabrain/zettabrain-rag/blob/main/install.sh
curl -fsSL https://zettabrain.app/install.sh | sudo bash

# macOS — review first: https://github.com/zettabrain/zettabrain-rag/blob/main/install.sh
curl -fsSL https://zettabrain.app/install.sh | bash

# Windows — review first: https://github.com/zettabrain/zettabrain-rag/blob/main/install.ps1
irm https://zettabrain.app/install.ps1 | iex
```

The Linux installer requires `sudo` to install Ollama system-wide and register a systemd service. The macOS installer does not require `sudo` for the package install step.

## Setup

Run the interactive setup wizard once after install:
```bash
sudo zettabrain-setup
```

This will:
1. Configure your document storage (local, NFS, SMB, or S3)
2. Install and start Ollama locally
3. Pull the recommended AI model for your hardware
4. Generate a self-signed TLS certificate (stays on-device)
5. Register ZettaBrain as a background service (see [Service Management](#service-management) to stop or remove it)

## Commands

| Command | Description |
|---|---|
| `zettabrain-chat` | Interactive CLI chat with your documents |
| `zettabrain-server` | Start the web GUI server (HTTPS on port 7860) |
| `zettabrain-ingest` | Index documents into the vector store |
| `zettabrain-ingest --rebuild` | Wipe and re-index all documents |
| `zettabrain-status` | Show Ollama, vector store, and storage status |
| `zettabrain-storage add` | Add an additional storage source |
| `zettabrain-setup` | Re-run the setup wizard |

## Usage Examples

**Chat via CLI:**
```bash
zettabrain-chat
# > What does our Q3 report say about cloud costs?
```

**Start the web GUI (https://localhost:7860):**
```bash
zettabrain-server
```

**Ingest a specific folder:**
```bash
ZETTABRAIN_DOCS=/path/to/docs zettabrain-ingest
```

## Vector Store — Location, Retention & Deletion

The vector index (document embeddings) is stored **only on your local machine**:

| Item | Location |
|---|---|
| Vector database | `/opt/zettabrain/src/zettabrain_vectorstore/` |
| Ingestion log (MD5 hashes) | `/opt/zettabrain/src/ingested_files.json` |
| Configuration | `/opt/zettabrain/src/zettabrain.env` |

Embeddings are **never transmitted** to any remote service. They are derived from your documents and stored locally in ChromaDB.

**Delete the vector index:**
```bash
# Via CLI
zettabrain-server &
curl -X DELETE http://localhost:7860/api/vectorstore

# Or directly
rm -rf /opt/zettabrain/src/zettabrain_vectorstore
rm -f  /opt/zettabrain/src/ingested_files.json
```

**Rebuild from scratch:**
```bash
zettabrain-ingest --rebuild
```

**Exclude files or folders** by not including them in `ZETTABRAIN_DOCS` — only files under that path are indexed.

## Service Management

ZettaBrain registers a background service so the web GUI auto-starts on boot. Here is how to control or fully remove it:

### Linux (systemd)
```bash
# Stop the service
sudo systemctl stop zettabrain

# Disable auto-start on boot
sudo systemctl disable zettabrain

# Check status
sudo systemctl status zettabrain

# View logs
journalctl -u zettabrain -f

# Remove service completely
sudo systemctl stop zettabrain
sudo systemctl disable zettabrain
sudo rm /etc/systemd/system/zettabrain.service
sudo systemctl daemon-reload
```

### macOS (launchd)
```bash
# Stop the service
sudo launchctl unload /Library/LaunchDaemons/io.zettabrain.server.plist

# Remove auto-start on boot
sudo rm /Library/LaunchDaemons/io.zettabrain.server.plist

# View logs
tail -f /opt/zettabrain/logs/server.log
```

### Uninstall completely
```bash
# Remove the package
pipx uninstall zettabrain-rag

# Stop and remove service (Linux)
sudo systemctl stop zettabrain && sudo systemctl disable zettabrain
sudo rm -f /etc/systemd/system/zettabrain.service && sudo systemctl daemon-reload

# Stop and remove service (macOS)
sudo launchctl unload /Library/LaunchDaemons/io.zettabrain.server.plist
sudo rm -f /Library/LaunchDaemons/io.zettabrain.server.plist

# Remove all data, config, and vector index
sudo rm -rf /opt/zettabrain
```

## Privacy

Privacy depends on your configuration:

| Configuration | Data stays local? |
|---|---|
| Local storage + `OLLAMA_HOST=http://localhost:11434` (default) | ✅ Yes — fully on-device |
| NFS or SMB network storage | ⚠️ Documents fetched over your LAN |
| S3 / object storage | ⚠️ Documents streamed from cloud storage |
| Remote `OLLAMA_HOST` | ⚠️ Queries and retrieved document chunks sent to remote Ollama |

**Default setup is fully local.** The setup wizard defaults to local storage and a localhost Ollama endpoint. Remote options are opt-in and clearly labelled during setup.

Document embeddings (vector index) are always stored locally regardless of storage configuration.

## Configuration

Settings file: `/opt/zettabrain/src/zettabrain.env`

| Variable | Default | Description |
|---|---|---|
| `ZETTABRAIN_DOCS` | set during setup | Path to documents folder |
| `ZETTABRAIN_LLM_MODEL` | set during setup | Ollama model name |
| `ZETTABRAIN_EMBED_MODEL` | `nomic-embed-text` | Embedding model |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama API endpoint (keep local for full privacy) |
| `ZETTABRAIN_CHUNK_SIZE` | `1000` | Document chunk size |
| `ZETTABRAIN_CHUNK_OVERLAP` | `200` | Chunk overlap |

## Supported Platforms

| Platform | Notes |
|---|---|
| Ubuntu 22.04 / 24.04 | Full GPU support (NVIDIA auto-installed) |
| Amazon Linux 2 / 2023 | Full support |
| RHEL / Rocky / AlmaLinux 8/9 | Full support |
| macOS 12+ Apple Silicon | Metal GPU via Ollama (`mac2.metal`, `mac2-m2.metal`) |
| macOS 12+ Intel | CPU inference (`mac1.metal`) |
| Windows 10/11 | Via PowerShell installer |

## Links

- **GitHub** (source + installer scripts): https://github.com/zettabrain/zettabrain-rag
- **PyPI**: https://pypi.org/project/zettabrain-rag/
- **Website**: https://zettabrain.io
- **Issues**: https://github.com/zettabrain/zettabrain-rag/issues
