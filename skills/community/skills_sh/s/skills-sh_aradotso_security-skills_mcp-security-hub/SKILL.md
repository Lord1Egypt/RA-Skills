---
name: mcp-security-hub
description: Deploy and orchestrate 38 MCP servers for offensive security tools (Nmap, Nuclei, Ghidra, SQLMap, etc.) via Docker
triggers:
  - set up offensive security MCP servers
  - run nmap scan through Claude
  - configure nuclei vulnerability scanner
  - analyze binary with radare2 MCP
  - scan for secrets with gitleaks
  - perform web security assessment
  - deploy security tools as MCP servers
  - integrate offensive security tools with AI
---

# mcp-security-hub

> Skill by [ara.so](https://ara.so) — Security Skills collection.

## Overview

`mcp-security-hub` is a production-ready collection of 38 Dockerized MCP (Model Context Protocol) servers that expose 300+ offensive security tools to AI assistants like Claude. It enables natural language security assessments, vulnerability scanning, binary analysis, and penetration testing workflows.

**Key capabilities:**
- 8 reconnaissance servers (Nmap, Shodan, ProjectDiscovery tools, WhatWeb, Masscan, ZoomEye)
- 6 web security servers (Nuclei, SQLMap, Nikto, ffuf, Burp Suite)
- 6 binary analysis servers (radare2, Ghidra, Binwalk, YARA, Capa, IDA Pro)
- 3 blockchain security servers (DAML Viewer, Medusa, Solazy)
- 3 cloud security servers (Trivy, Prowler, RoadRecon)
- Plus: secrets detection, fuzzing, OSINT, threat intelligence, Active Directory, password cracking

## Installation

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Claude Desktop or MCP-compatible client

### Clone and Build

```bash
git clone https://github.com/FuzzingLabs/mcp-security-hub.git
cd mcp-security-hub

# Build all MCP servers
docker-compose build

# Or build specific servers
docker-compose build nmap-mcp nuclei-mcp gitleaks-mcp
```

### Verify Installation

```bash
# Check built images
docker images | grep mcp

# Start specific servers
docker-compose up nmap-mcp nuclei-mcp -d

# Verify health
docker-compose ps
```

## Configuration

### Claude Desktop Integration

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "nmap": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "--cap-add=NET_RAW", "nmap-mcp:latest"]
    },
    "nuclei": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "nuclei-mcp:latest"]
    },
    "gitleaks": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "${HOME}/repos:/app/target:ro",
        "gitleaks-mcp:latest"
      ]
    },
    "radare2": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "${HOME}/binaries:/samples:ro",
        "radare2-mcp:latest"
      ]
    },
    "sqlmap": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "sqlmap-mcp:latest"]
    },
    "trivy": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "/var/run/docker.sock:/var/run/docker.sock:ro",
        "trivy-mcp:latest"
      ]
    }
  }
}
```

### Project-Level Configuration

Create `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "nmap": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "--cap-add=NET_RAW", "nmap-mcp:latest"]
    },
    "nuclei": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "nuclei-mcp:latest"]
    }
  }
}
```

### Environment Variables

Many MCP servers require API keys for external services:

```bash
# Shodan
export SHODAN_API_KEY=your_key_here

# VirusTotal
export VT_API_KEY=your_key_here

# ZoomEye
export ZOOMEYE_API_KEY=your_key_here

# Burp Suite
export BURP_API_KEY=your_key_here
```

Pass environment variables to Docker containers:

```json
{
  "mcpServers": {
    "shodan": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "SHODAN_API_KEY=${SHODAN_API_KEY}",
        "shodan-mcp:latest"
      ]
    }
  }
}
```

## Key MCP Servers

### Nmap MCP (Network Scanning)

**Available tools (8):**
- `scan_hosts` - Basic host discovery
- `scan_ports` - Port scanning with service detection
- `scan_os` - OS fingerprinting
- `scan_vuln` - Vulnerability scanning with NSE scripts
- `scan_custom` - Custom nmap command execution
- `list_nse_scripts` - List available NSE scripts
- `get_nse_script_info` - Get NSE script details
- `scan_with_script` - Run specific NSE script

**Example prompts:**
- "Scan 192.168.1.0/24 for open ports"
- "Perform OS detection on 10.0.0.1"
- "Run vulnerability scan on example.com"

### Nuclei MCP (Vulnerability Scanning)

**Available tools (7):**
- `scan_target` - Scan with default templates
- `scan_with_severity` - Filter by severity (critical, high, medium, low)
- `scan_with_tags` - Use specific tags (cve, exposure, xss, sqli)
- `scan_with_templates` - Use custom template paths
- `list_templates` - Show available templates
- `update_templates` - Update template database
- `scan_multiple_targets` - Bulk scanning

**Example prompts:**
- "Scan https://example.com for critical vulnerabilities"
- "Check example.com for CVEs using nuclei"
- "Run nuclei with exposure and misconfiguration templates"

### Gitleaks MCP (Secrets Detection)

**Available tools (5):**
- `scan_repo` - Scan git repository
- `scan_file` - Scan individual file
- `scan_directory` - Scan directory tree
- `generate_baseline` - Create baseline for false positives
- `scan_commits` - Scan specific commit range

**Example prompts:**
- "Scan /app/target/myrepo for secrets"
- "Check this project for exposed API keys"
- "Find credentials in the last 10 commits"

**Volume mounting required:**
```json
{
  "gitleaks": {
    "command": "docker",
    "args": [
      "run", "-i", "--rm",
      "-v", "/path/to/repos:/app/target:ro",
      "gitleaks-mcp:latest"
    ]
  }
}
```

### Radare2 MCP (Binary Analysis)

**Available tools (32+):**
- `analyze_binary` - Load and analyze binary
- `disassemble` - Disassemble functions
- `decompile` - Decompile to C-like code
- `list_functions` - Show all functions
- `find_strings` - Extract strings
- `find_imports` - List imported functions
- `find_exports` - List exported functions
- `search_bytes` - Search byte patterns
- `analyze_entropy` - Detect packed sections

**Example prompts:**
- "Analyze /samples/malware.exe for suspicious functions"
- "Decompile main function in this binary"
- "Find strings in /samples/firmware.bin"

**Volume mounting required:**
```json
{
  "radare2": {
    "command": "docker",
    "args": [
      "run", "-i", "--rm",
      "-v", "/path/to/binaries:/samples:ro",
      "radare2-mcp:latest"
    ]
  }
}
```

### SQLMap MCP (SQL Injection)

**Available tools (8):**
- `test_url` - Test URL for SQL injection
- `dump_database` - Extract database contents
- `dump_table` - Extract specific table
- `list_databases` - Enumerate databases
- `list_tables` - Enumerate tables
- `get_dbs` - Get database names
- `get_current_user` - Get DB user
- `test_forms` - Test web forms for SQLi

**Example prompts:**
- "Test https://example.com/page?id=1 for SQL injection"
- "Dump database from vulnerable URL"
- "Check this form for SQL injection vulnerabilities"

### Trivy MCP (Container Security)

**Available tools (7):**
- `scan_image` - Scan Docker image
- `scan_filesystem` - Scan local filesystem
- `scan_config` - Scan IaC files (Terraform, K8s)
- `scan_repo` - Scan git repository
- `list_vulnerabilities` - Show known CVEs
- `get_sbom` - Generate SBOM
- `scan_kubernetes` - Scan K8s cluster

**Example prompts:**
- "Scan nginx:latest for vulnerabilities"
- "Check this Dockerfile for security issues"
- "Generate SBOM for python:3.11 image"

## Common Workflows

### Network Reconnaissance Workflow

```bash
# 1. Build reconnaissance servers
docker-compose build nmap-mcp whatweb-mcp masscan-mcp

# 2. Start services
docker-compose up nmap-mcp whatweb-mcp -d

# 3. Use in Claude
# "Scan 10.0.0.0/24 for web servers, then fingerprint each one"
```

### Web Application Security Assessment

```bash
# Build web security stack
docker-compose build nuclei-mcp sqlmap-mcp ffuf-mcp

# Start services
docker-compose up nuclei-mcp sqlmap-mcp ffuf-mcp -d

# In Claude:
# "Scan example.com with nuclei, test any forms for SQL injection,
#  and fuzz for hidden directories"
```

### Binary Analysis Pipeline

```bash
# Build binary analysis tools
docker-compose build radare2-mcp binwalk-mcp yara-mcp capa-mcp

# Mount binaries directory
docker-compose up radare2-mcp binwalk-mcp yara-mcp capa-mcp -d

# In Claude:
# "Analyze /samples/suspicious.exe - extract filesystem if packed,
#  scan for malware patterns, and identify capabilities"
```

### Secrets Scanning in CI/CD

```bash
# Build gitleaks
docker-compose build gitleaks-mcp

# Run as one-off scan
docker run -i --rm \
  -v "$(pwd):/app/target:ro" \
  gitleaks-mcp:latest <<EOF
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "scan_directory",
    "arguments": {
      "path": "/app/target"
    }
  },
  "id": 1
}
EOF
```

### Cloud Security Audit

```bash
# Build cloud security tools
docker-compose build trivy-mcp prowler-mcp

# Mount Docker socket for Trivy
docker-compose up trivy-mcp prowler-mcp -d

# In Claude:
# "Scan all running containers for CVEs, then audit AWS account
#  for security misconfigurations"
```

## Docker Compose Orchestration

### Start All Services

```bash
docker-compose up -d
```

### Start Specific Category

```bash
# Reconnaissance only
docker-compose up nmap-mcp whatweb-mcp masscan-mcp -d

# Web security only
docker-compose up nuclei-mcp sqlmap-mcp ffuf-mcp -d
```

### Resource Limits

Edit `docker-compose.yml` to adjust resource constraints:

```yaml
services:
  nmap-mcp:
    image: nmap-mcp:latest
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 256M
```

### Health Monitoring

```bash
# Check health status
docker-compose ps

# View logs
docker-compose logs -f nmap-mcp

# Restart unhealthy services
docker-compose restart nmap-mcp
```

## Development

### Building Individual Servers

```bash
cd reconnaissance/nmap-mcp
docker build -t nmap-mcp:latest .
```

### Testing MCP Server

```bash
# Run interactive test
docker run -it --rm nmap-mcp:latest

# Send JSON-RPC request
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | \
  docker run -i --rm nmap-mcp:latest
```

### Adding Custom MCP Server

```bash
mkdir -p custom-category/mytool-mcp
cd custom-category/mytool-mcp

# Create Dockerfile
cat > Dockerfile <<'EOF'
FROM python:3.11-slim
RUN useradd -m -u 1000 mcpuser
RUN pip install mcp mytool
USER mcpuser
WORKDIR /app
COPY server.py .
CMD ["python", "server.py"]
EOF

# Create server.py with MCP protocol implementation
# Add to docker-compose.yml
```

## Security Hardening

All MCP servers follow security best practices:

```dockerfile
# Example hardened Dockerfile pattern
FROM alpine:3.19
RUN adduser -D -u 1000 mcpuser
RUN apk add --no-cache tool-name
USER mcpuser
WORKDIR /app
# Drop all capabilities by default
# Add only required capabilities in docker-compose.yml
```

### Required Capabilities

Some tools need specific Linux capabilities:

```yaml
nmap-mcp:
  cap_drop:
    - ALL
  cap_add:
    - NET_RAW  # Required for SYN scanning

trivy-mcp:
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock:ro  # Docker scanning
```

### Read-Only Mounts

Always mount target directories read-only:

```yaml
gitleaks-mcp:
  volumes:
    - ./repos:/app/target:ro  # Read-only prevents modification
```

## Troubleshooting

### MCP Server Not Responding

```bash
# Check if container is running
docker ps | grep mcp

# View logs
docker logs nmap-mcp

# Restart service
docker-compose restart nmap-mcp

# Test JSON-RPC directly
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | \
  docker run -i --rm nmap-mcp:latest
```

### Permission Denied Errors

```bash
# Nmap requires NET_RAW capability
# Add to docker-compose.yml:
cap_add:
  - NET_RAW

# Or run with --cap-add
docker run --cap-add=NET_RAW nmap-mcp:latest
```

### Volume Mount Issues

```bash
# Ensure absolute paths
docker run -v /absolute/path:/app/target:ro gitleaks-mcp

# Check permissions (container runs as UID 1000)
chown -R 1000:1000 /path/to/repos

# Verify mount inside container
docker run -it --rm -v $(pwd):/app/target:ro gitleaks-mcp sh
ls -la /app/target
```

### Claude Desktop Not Finding MCP Servers

```bash
# Verify config location
# macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
# Windows: %APPDATA%\Claude\claude_desktop_config.json

# Check JSON syntax
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | jq .

# Restart Claude Desktop after config changes

# Verify image exists
docker images | grep nmap-mcp
```

### API Key Authentication Failures

```bash
# Verify environment variable is set
echo $SHODAN_API_KEY

# Pass to Docker container
docker run -e SHODAN_API_KEY=$SHODAN_API_KEY shodan-mcp

# For Claude Desktop, use full env var syntax
{
  "command": "docker",
  "args": ["-e", "SHODAN_API_KEY=${SHODAN_API_KEY}", ...]
}
```

### Network Connectivity Issues

```bash
# Some tools need host network access
docker run --network host nmap-mcp

# Or create custom network
docker network create security-net
docker run --network security-net nmap-mcp
```

### Container Build Failures

```bash
# Clear Docker build cache
docker builder prune -a

# Rebuild with no cache
docker-compose build --no-cache nmap-mcp

# Check base image availability
docker pull alpine:3.19
docker pull python:3.11-slim
```

## Advanced Usage

### Custom Nuclei Templates

```bash
# Mount custom template directory
docker run -i --rm \
  -v $(pwd)/custom-templates:/nuclei-templates:ro \
  nuclei-mcp:latest

# In Claude: "Use custom nuclei templates from /nuclei-templates"
```

### Multi-Stage Binary Analysis

```bash
# 1. Extract firmware
docker run -v $(pwd)/firmware:/samples:ro binwalk-mcp

# 2. Scan extracted files
docker run -v $(pwd)/firmware/_extracted:/samples:ro yara-mcp

# 3. Analyze suspicious binaries
docker run -v $(pwd)/firmware/_extracted:/samples:ro radare2-mcp
```

### Automated Scanning Pipeline

```bash
#!/bin/bash
# scan-pipeline.sh

TARGET=$1

# Network scan
docker run --rm --cap-add=NET_RAW nmap-mcp \
  -A $TARGET > nmap-results.txt

# Web fingerprinting
docker run --rm whatweb-mcp $TARGET > whatweb-results.txt

# Vulnerability scan
docker run --rm nuclei-mcp -u $TARGET -severity high,critical \
  > nuclei-results.txt
```

### Integration with Existing Tools

```bash
# Export Trivy results to JSON
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  trivy-mcp image nginx:latest -f json > trivy-report.json

# Parse and filter with jq
cat trivy-report.json | jq '.Results[] | select(.Vulnerabilities)'
```

## References

- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Official Documentation](https://fuzzinglabs.github.io/mcp-security-hub/)
- [GitHub Repository](https://github.com/FuzzingLabs/mcp-security-hub)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
