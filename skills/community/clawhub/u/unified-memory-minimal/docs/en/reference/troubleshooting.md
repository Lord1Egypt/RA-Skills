# Troubleshooting Guide

> Solutions for common issues with Unified Memory.

## 📚 Contents

1. [Installation Issues](#installation-issues)
2. [Startup Issues](#startup-issues)
3. [Storage Issues](#storage-issues)
4. [Search Issues](#search-issues)
5. [Vector Store Issues](#vector-store-issues)
6. [Plugin Issues](#plugin-issues)
7. [Performance Issues](#performance-issues)
8. [Data Recovery](#data-recovery)

## Installation Issues

### "command not found: unified-memory"

**Cause:** Installation not in PATH

**Solution:**
```bash
# Check installation
npm list -g unified-memory

# Reinstall
npm install -g unified-memory

# Or add to PATH
export PATH="$(npm root -g)/bin:$PATH"
```

### "Node.js version too old"

**Cause:** Node.js version < 18.0.0

**Solution:**
```bash
# Check version
node --version

# Update Node.js
# macOS/Linux
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo apt install -y nodejs

# Or use nvm
nvm install 18
nvm use 18
```

### "EACCES: permission denied"

**Cause:** npm global directory not writable

**Solution:**
```bash
# Create npm global directory
mkdir ~/.npm-global

# Configure npm
npm config set prefix '~/.npm-global'

# Add to PATH
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Install again
npm install -g unified-memory
```

## Startup Issues

### "Failed to initialize storage"

**Cause:** Cannot create/read storage directory

**Solution:**
```bash
# Create directory manually
mkdir -p ~/.unified-memory

# Fix permissions
chmod 755 ~/.unified-memory

# Reinitialize
unified-memory init
```

### "Port already in use"

**Cause:** Another process using port 3851

**Solution:**
```bash
# Find process
lsof -i :3851

# Kill process or use different port
unified-memory serve --port 3852
```

### "Configuration file invalid"

**Cause:** Invalid JSON in config

**Solution:**
```bash
# Validate JSON
cat ~/.unified-memory/config.json | python3 -m json.tool

# Reset to default
rm ~/.unified-memory/config.json
unified-memory init
```

## Storage Issues

### "Memory file corrupted"

**Cause:** JSON file is malformed

**Solution:**
```bash
# Check for backup
ls -la ~/.unified-memory/backups/

# Restore from backup
cp ~/.unified-memory/backups/memories-YYYY-MM-DD.json ~/.unified-memory/memories.json

# Or rebuild from WAL
unified-memory recover
```

### "Disk full"

**Cause:** Not enough disk space

**Solution:**
```bash
# Check disk space
df -h ~/.unified-memory

# Clean old backups
rm -rf ~/.unified-memory/backups/*

# Clean vector store (will rebuild)
rm -rf ~/.unified-memory/vector.lance
unified-memory init
```

### "Permission denied on memory file"

**Cause:** File permissions issue

**Solution:**
```bash
# Fix permissions
chmod 644 ~/.unified-memory/memories.json
chmod 755 ~/.unified-memory
```

## Search Issues

### "Search returns no results"

**Cause:** Empty index or wrong query

**Solution:**
```bash
# Check memories exist
unified-memory list

# Rebuild search index
unified-memory rebuild-index

# Try simpler query
unified-memory search "test"
```

### "Search very slow"

**Cause:** Large dataset, no caching

**Solution:**
```bash
# Enable caching (already default)
# Check config has cache.enable = true

# Rebuild BM25 index
unified-memory rebuild-bm25

# Check Ollama is running
ollama list
```

### "Vector search fails"

**Cause:** Ollama not running or no model

**Solution:**
```bash
# Start Ollama
ollama serve

# Pull embedding model
ollama pull nomic-embed-text

# Test Ollama
curl http://localhost:11434/api/generate -d '{"model":"nomic-embed-text","prompt":"test"}'
```

## Vector Store Issues

### "LanceDB initialization failed"

**Cause:** Corrupted vector store

**Solution:**
```bash
# Remove and rebuild
rm -rf ~/.unified-memory/vector.lance
unified-memory init
```

### "ChromaDB connection failed"

**Cause:** ChromaDB server not running

**Solution:**
```bash
# Start ChromaDB
docker run -d -p 8000:8000 chromadb/chroma

# Or switch to LanceDB
# Edit config.json:
# "vectorStore": { "backend": "lancedb", ... }
```

### "Embedding dimension mismatch"

**Cause:** Config dimension != model dimension

**Solution:**
```bash
# Check model dimension
ollama show nomic-embed-text

# Update config (e.g., for nomic-embed-text: 768)
# ~/.unified-memory/config.json
# "embedding": { "dimension": 768 }
```

## Plugin Issues

### "Plugin not loading"

**Cause:** Plugin has errors or missing dependencies

**Solution:**
```bash
# Check plugin directory
ls -la ~/.unified-memory/plugins/

# Enable debug logging
UNIFIED_MEMORY_DEBUG=1 unified-memory serve

# Check plugin syntax
node --check ~/.unified-memory/plugins/my-plugin/index.js
```

### "Plugin hot reload not working"

**Cause:** autoReload disabled

**Solution:**
```json
{
  "plugins": {
    "autoReload": true
  }
}
```

## Performance Issues

### "High memory usage"

**Cause:** Large dataset, no tier management

**Solution:**
```bash
# Run compression
unified-memory compress

# Migrate old memories to cold tier
unified-memory tier --action redistribute

# Reduce cache size
# Edit config:
# "cache": { "maxSize": 500 }
```

### "Slow startup"

**Cause:** Large memory file, rebuilding index

**Solution:**
```bash
# Compact memory file
unified-memory compact

# Use WAL recovery instead of full rebuild
# Config should have:
# "transaction": { "enable": true }
```

### "CPU usage high"

**Cause:** Too many background operations

**Solution:**
```bash
# Reduce BM25 rebuild frequency
# "search": { "bm25RebuildInterval": 86400 }

# Disable auto-compression
# "tier": { "autoCompress": false }
```

## Data Recovery

### "Recover from crash"

```bash
# Check WAL for uncommitted transactions
unified-memory wal --action list

# Recover data
unified-memory recover

# Verify
unified-memory stats
```

### "Restore from backup"

```bash
# List backups
ls -la ~/.unified-memory/backups/

# Restore specific backup
cp ~/.unified-memory/backups/memories-2026-04-15.json ~/.unified-memory/memories.json

# Restart server
unified-memory serve
```

### "Export/Import for migration"

```bash
# Export current data
unified-memory export --format json --output /tmp/memories.json

# Install on new system
npm install -g unified-memory

# Import data
unified-memory import --input /tmp/memories.json
```

## Getting Help

### Debug Mode

```bash
# Enable debug logging
UNIFIED_MEMORY_DEBUG=1 unified-memory serve

# Check logs
tail -f ~/.unified-memory/logs/app.log
```

### Health Check

```bash
# Run health check
unified-memory health

# Check specific components
unified-memory health --component storage
unified-memory health --component vector
unified-memory health --component wal
```

### Report Issues

When reporting issues, include:
- Unified Memory version: `unified-memory --version`
- Node.js version: `node --version`
- Operating system: `uname -a`
- Configuration: `cat ~/.unified-memory/config.json`
- Relevant logs: `~/.unified-memory/logs/`
