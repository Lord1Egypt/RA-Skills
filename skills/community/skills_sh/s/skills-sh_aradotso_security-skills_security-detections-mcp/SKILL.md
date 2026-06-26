---
name: security-detections-mcp
description: Query unified Sigma, Splunk, Elastic, KQL, Sublime, and CrowdStrike security detection rules via MCP server with MITRE ATT&CK mapping and coverage analysis
triggers:
  - search for security detections covering technique
  - analyze MITRE ATT&CK coverage for ransomware
  - find detection gaps in our security stack
  - query Sigma rules for process injection
  - generate ATT&CK Navigator layer showing coverage
  - compare detection coverage across threat actors
  - build detections for lateral movement techniques
  - show me Splunk rules for credential dumping
---

# security-detections-mcp

> Skill by [ara.so](https://ara.so) — Security Skills collection

An MCP (Model Context Protocol) server providing LLM access to 8,200+ security detection rules across Sigma, Splunk ESCU, Elastic, KQL, Sublime, and CrowdStrike CQL formats, with MITRE ATT&CK mapping, coverage analysis, and autonomous detection engineering.

## What It Does

- **Unified detection search** across 6 major security platforms (Sigma, Splunk, Elastic, KQL, Sublime, CrowdStrike)
- **MITRE ATT&CK integration** with 172 threat actors, 784 software, 4,362 actor-technique relationships
- **Coverage analysis** identifying gaps in detection by tactic/technique/actor
- **ATT&CK Navigator layers** exportable as JSON for visualization
- **Autonomous detection pipeline** from CTI ingestion to draft PR generation
- **81 MCP tools** for detection engineering (local) or ~25 tools (hosted)
- **11 expert prompts** for ransomware assessment, APT emulation, purple teaming

## Installation

### Local Installation (Full Power)

**Prerequisites:**
- Node.js 18+ 
- Detection rule repositories cloned locally

**Quick start with npx:**

```bash
npx -y security-detections-mcp
```

**Configure in Claude Desktop** (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "security-detections": {
      "command": "npx",
      "args": ["-y", "security-detections-mcp"],
      "env": {
        "SIGMA_PATHS": "/path/to/sigma/rules,/path/to/sigma/rules-threat-hunting",
        "SPLUNK_PATHS": "/path/to/security_content/detections",
        "STORY_PATHS": "/path/to/security_content/stories",
        "ELASTIC_PATHS": "/path/to/detection-rules/rules",
        "KQL_PATHS": "/path/to/kql-rules",
        "SUBLIME_PATHS": "/path/to/sublime-rules/detection-rules",
        "CQL_HUB_PATHS": "/path/to/cql-hub/queries",
        "ATTACK_STIX_PATH": "/path/to/enterprise-attack.json"
      }
    }
  }
}
```

**Configure in Cursor** (`.cursor/settings.json`):

```json
{
  "mcp": {
    "servers": {
      "security-detections": {
        "command": "npx",
        "args": ["-y", "security-detections-mcp"],
        "env": {
          "SIGMA_PATHS": "/Users/you/detections/sigma/rules",
          "SPLUNK_PATHS": "/Users/you/detections/security_content/detections"
        }
      }
    }
  }
}
```

**Configure in VS Code** (settings.json):

```json
{
  "mcp.servers": {
    "security-detections": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "security-detections-mcp"],
      "env": {
        "SIGMA_PATHS": "/home/you/detections/sigma/rules"
      }
    }
  }
}
```

### Hosted Installation (Zero Setup)

**Prerequisites:**
- API token from [detect.michaelhaag.org/account/tokens](https://detect.michaelhaag.org/account/tokens)
- Free tier: 200 calls/day, read-only tools

**Claude Desktop** (requires `mcp-remote`):

```json
{
  "mcpServers": {
    "security-detections": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://detect.michaelhaag.org/api/mcp/mcp",
        "--header",
        "Authorization: Bearer ${SDMCP_TOKEN}"
      ]
    }
  }
}
```

**VS Code / Cursor:**

```json
{
  "mcp.servers": {
    "security-detections": {
      "type": "http",
      "url": "https://detect.michaelhaag.org/api/mcp/mcp",
      "headers": {
        "Authorization": "Bearer ${SDMCP_TOKEN}"
      }
    }
  }
}
```

## Getting Detection Content

Download all detection sources with sparse checkout:

```bash
mkdir -p ~/detections && cd ~/detections

# Sigma rules
git clone --depth 1 --filter=blob:none --sparse https://github.com/SigmaHQ/sigma.git
cd sigma && git sparse-checkout set rules rules-threat-hunting && cd ..

# Splunk ESCU
git clone --depth 1 --filter=blob:none --sparse https://github.com/splunk/security_content.git
cd security_content && git sparse-checkout set detections stories && cd ..

# Elastic
git clone --depth 1 --filter=blob:none --sparse https://github.com/elastic/detection-rules.git
cd detection-rules && git sparse-checkout set rules && cd ..

# KQL
git clone --depth 1 https://github.com/Bert-JanP/Hunting-Queries-Detection-Rules.git kql-bertjanp
git clone --depth 1 https://github.com/jkerai1/KQL-Queries.git kql-jkerai1

# Sublime
git clone --depth 1 --filter=blob:none --sparse https://github.com/sublime-security/sublime-rules.git
cd sublime-rules && git sparse-checkout set detection-rules && cd ..

# CrowdStrike CQL
git clone --depth 1 https://github.com/ByteRay-Labs/Query-Hub.git cql-hub

# MITRE ATT&CK STIX
curl -o enterprise-attack.json https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json
```

Then update environment variables to point to these paths.

## Core MCP Tools

### Detection Search & Retrieval

```typescript
// Full-text search across all detections
{
  "name": "search",
  "arguments": {
    "query": "process injection",
    "limit": 10
  }
}

// Get specific detection by ID
{
  "name": "get_by_id",
  "arguments": {
    "id": "sigma_abc123"
  }
}

// List all detections with pagination
{
  "name": "list_all",
  "arguments": {
    "limit": 50,
    "offset": 0
  }
}

// Filter by source type
{
  "name": "list_by_source",
  "arguments": {
    "source_type": "sigma"  // sigma, splunk_escu, elastic, kql, sublime, crowdstrike_cql
  }
}

// Get index statistics
{
  "name": "get_stats",
  "arguments": {}
}
```

### MITRE ATT&CK Filtering

```typescript
// Find detections for specific technique
{
  "name": "list_by_mitre",
  "arguments": {
    "technique_id": "T1059.001"  // PowerShell
  }
}

// Filter by tactic
{
  "name": "list_by_mitre_tactic",
  "arguments": {
    "tactic": "execution"  // execution, persistence, privilege-escalation, etc.
  }
}

// Search by CVE
{
  "name": "list_by_cve",
  "arguments": {
    "cve_id": "CVE-2021-34527"  // PrintNightmare
  }
}

// Find by process name
{
  "name": "list_by_process_name",
  "arguments": {
    "process_name": "powershell.exe"
  }
}

// Filter by severity
{
  "name": "list_by_severity",
  "arguments": {
    "level": "critical"  // critical, high, medium, low
  }
}

// Filter by data source
{
  "name": "list_by_data_source",
  "arguments": {
    "data_source": "process_creation"
  }
}
```

### Coverage Analysis

```typescript
// Analyze overall coverage (~2KB response)
{
  "name": "analyze_coverage",
  "arguments": {
    "source_type": "sigma"  // optional: analyze specific source
  }
}

// Identify gaps for threat profile (~500B response)
{
  "name": "identify_gaps",
  "arguments": {
    "threat_profile": "ransomware"  // ransomware, apt, persistence, lateral_movement
  }
}

// Get detection suggestions for technique (~2KB)
{
  "name": "suggest_detections",
  "arguments": {
    "technique_id": "T1003.001"  // LSASS Memory
  }
}

// Coverage summary by tactic (~200B)
{
  "name": "get_coverage_summary",
  "arguments": {
    "source_type": "splunk_escu"
  }
}

// Analyze coverage against threat actor
{
  "name": "analyze_actor_coverage",
  "arguments": {
    "actor": "APT29"
  }
}

// Compare coverage across multiple actors
{
  "name": "compare_actor_coverage",
  "arguments": {
    "actors": ["APT29", "APT28", "Lazarus Group"]
  }
}

// Behavioral procedure breakdown for technique
{
  "name": "analyze_procedure_coverage",
  "arguments": {
    "technique_id": "T1055"
  }
}
```

### ATT&CK Navigator Layer Generation

```typescript
// Generate Navigator layer JSON
{
  "name": "generate_navigator_layer",
  "arguments": {
    "name": "Current Coverage",
    "description": "Detection coverage as of 2024-01",
    "filter": {
      "source": "sigma",
      "tactic": "defense-evasion",
      "min_severity": "medium"
    },
    "color_by": "coverage"  // coverage, severity, source
  }
}

// Export to file (local only)
{
  "name": "export_navigator_layer",
  "arguments": {
    "output_path": "./coverage-layer.json",
    "filter": {
      "actor": "APT29"
    }
  }
}
```

## Common Patterns

### Ransomware Readiness Assessment

Use the built-in prompt:

```
Use the ransomware-readiness-assessment prompt to evaluate our coverage
```

Or manually:

```typescript
// 1. Identify gaps
{
  "name": "identify_gaps",
  "arguments": {
    "threat_profile": "ransomware"
  }
}

// 2. Get detections for weak areas
{
  "name": "list_by_mitre",
  "arguments": {
    "technique_id": "T1486"  // Data Encrypted for Impact
  }
}

// 3. Generate coverage layer
{
  "name": "generate_navigator_layer",
  "arguments": {
    "name": "Ransomware Coverage",
    "filter": {
      "threat_profile": "ransomware"
    }
  }
}
```

### APT Threat Emulation

```typescript
// 1. Analyze actor coverage
{
  "name": "analyze_actor_coverage",
  "arguments": {
    "actor": "APT29"
  }
}

// 2. Get techniques used by actor
{
  "name": "get_actor_techniques",
  "arguments": {
    "actor": "APT29"
  }
}

// 3. Find detections for each technique
{
  "name": "list_by_mitre",
  "arguments": {
    "technique_id": "T1059.001"
  }
}

// 4. Compare with other actors
{
  "name": "compare_actor_coverage",
  "arguments": {
    "actors": ["APT29", "APT28"]
  }
}
```

### Detection Gap Analysis

```typescript
// 1. Get coverage summary
{
  "name": "get_coverage_summary",
  "arguments": {}
}

// 2. Analyze coverage by tactic
{
  "name": "analyze_coverage",
  "arguments": {}
}

// 3. Identify specific gaps
{
  "name": "identify_gaps",
  "arguments": {
    "threat_profile": "apt"
  }
}

// 4. Get suggestions for weak techniques
{
  "name": "suggest_detections",
  "arguments": {
    "technique_id": "T1078"  // Valid Accounts
  }
}
```

### Building Detection Content

```typescript
// 1. Search existing detections for pattern
{
  "name": "search",
  "arguments": {
    "query": "lateral movement SMB",
    "limit": 10
  }
}

// 2. Analyze procedure coverage
{
  "name": "analyze_procedure_coverage",
  "arguments": {
    "technique_id": "T1021.002"  // SMB/Windows Admin Shares
  }
}

// 3. Get detection template
{
  "name": "generate_detection_template",
  "arguments": {
    "technique_id": "T1021.002",
    "format": "sigma"
  }
}

// 4. Validate against existing detections
{
  "name": "list_by_mitre",
  "arguments": {
    "technique_id": "T1021.002"
  }
}
```

### Cross-Platform Detection Comparison

```typescript
// Compare Sigma vs Splunk for technique
// 1. Get Sigma detections
{
  "name": "list_by_mitre",
  "arguments": {
    "technique_id": "T1003.001"
  }
}

// Filter results by source_type: "sigma"

// 2. Get Splunk detections
{
  "name": "list_by_source",
  "arguments": {
    "source_type": "splunk_escu"
  }
}

// Filter by same technique

// 3. Compare coverage
{
  "name": "analyze_coverage",
  "arguments": {
    "source_type": "sigma"
  }
}

{
  "name": "analyze_coverage",
  "arguments": {
    "source_type": "splunk_escu"
  }
}
```

## Configuration Reference

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SIGMA_PATHS` | Comma-separated Sigma rule directories | `/path/to/sigma/rules,/path/to/sigma/rules-threat-hunting` |
| `SPLUNK_PATHS` | Splunk ESCU detection directories | `/path/to/security_content/detections` |
| `STORY_PATHS` | Splunk analytic story directories (optional) | `/path/to/security_content/stories` |
| `ELASTIC_PATHS` | Elastic detection rule directories | `/path/to/detection-rules/rules` |
| `KQL_PATHS` | KQL hunting query directories (comma-separated) | `/path/to/kql-bertjanp,/path/to/kql-jkerai1` |
| `SUBLIME_PATHS` | Sublime Security rule directories | `/path/to/sublime-rules/detection-rules` |
| `CQL_HUB_PATHS` | CQL Hub (CrowdStrike) query directories | `/path/to/cql-hub/queries` |
| `ATTACK_STIX_PATH` | Path to `enterprise-attack.json` STIX bundle | `/path/to/enterprise-attack.json` |

### Source Type Values

- `sigma` - Sigma rules (YAML)
- `splunk_escu` - Splunk Enterprise Security Content Update
- `elastic` - Elastic Security detection rules
- `kql` - Kusto Query Language hunting queries
- `sublime` - Sublime Security detection rules
- `crowdstrike_cql` - CrowdStrike Query Language (CQL)

### Tactic Values (MITRE ATT&CK)

- `reconnaissance`
- `resource-development`
- `initial-access`
- `execution`
- `persistence`
- `privilege-escalation`
- `defense-evasion`
- `credential-access`
- `discovery`
- `lateral-movement`
- `collection`
- `command-and-control`
- `exfiltration`
- `impact`

## Troubleshooting

### MCP Server Not Indexing Rules

**Problem:** `get_stats` shows 0 detections

**Solution:**
1. Verify paths exist: `ls -la /path/to/sigma/rules`
2. Check environment variables are set correctly in MCP config
3. Rebuild index manually:
   ```typescript
   {
     "name": "rebuild_index",
     "arguments": {}
   }
   ```
4. Check MCP server logs in Claude Desktop: `~/Library/Logs/Claude/mcp*.log`

### Permission Denied Errors

**Problem:** Cannot read detection files

**Solution:**
```bash
# Fix permissions on detection directories
chmod -R 755 ~/detections
```

### Hosted MCP 401 Unauthorized

**Problem:** Token authentication failing

**Solution:**
1. Verify token starts with `sdmcp_`
2. Check token is not expired at [detect.michaelhaag.org/account/tokens](https://detect.michaelhaag.org/account/tokens)
3. Ensure `Authorization: Bearer` header format is correct
4. Free tier rate limit: 200 calls/day

### Missing MITRE ATT&CK Data

**Problem:** Actor/technique queries return empty

**Solution:**
1. Download STIX bundle:
   ```bash
   curl -o ~/detections/enterprise-attack.json \
     https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json
   ```
2. Set `ATTACK_STIX_PATH` environment variable
3. Rebuild index

### Sigma Rules Not Parsing

**Problem:** Some Sigma rules show errors

**Solution:**
- Ensure you're using the official SigmaHQ repo
- Update to latest rules: `cd sigma && git pull`
- Some experimental rules may have schema issues - this is expected
- Check parsing errors in MCP logs

### Slow Initial Index Build

**Problem:** First startup takes 30+ seconds

**Solution:**
- Expected behavior with 8,200+ detections
- Subsequent startups use cached index (~2 seconds)
- Use hosted MCP for zero startup time
- Reduce `PATHS` to only needed sources

## Advanced Usage

### Custom Detection Repositories

Add your private detections:

```json
{
  "env": {
    "SIGMA_PATHS": "/path/to/sigma/rules,/path/to/my-custom-sigma",
    "SPLUNK_PATHS": "/path/to/security_content/detections,/path/to/internal-splunk"
  }
}
```

### Autonomous Detection Pipeline

Enable autonomous CTI → detection generation:

```typescript
// Configure autonomous settings (local only)
{
  "name": "configure_autonomous",
  "arguments": {
    "enabled": true,
    "cti_sources": ["misp", "otx"],
    "auto_pr": false  // Manual review before PR
  }
}

// Trigger gap analysis
{
  "name": "run_autonomous_analysis",
  "arguments": {
    "threat_actor": "APT29"
  }
}
```

See [Autonomous docs](https://github.com/MHaggis/Security-Detections-MCP/blob/main/docs/AUTONOMOUS.md) for full pipeline details.

### Exporting for SIEM

```typescript
// Export detections in native format
{
  "name": "export_detections",
  "arguments": {
    "technique_id": "T1055",
    "format": "sigma",  // or splunk, elastic, kql
    "output_path": "./exports/process_injection.yml"
  }
}
```

## Expert Prompts

Built-in workflows accessible by name:

- `ransomware-readiness-assessment` - Full kill-chain coverage analysis
- `apt-threat-emulation` - Actor-specific detection mapping
- `purple-team-exercise` - Combined offensive/defensive planning
- `executive-briefing` - High-level coverage summary
- `detection-sprint-planning` - Engineering backlog prioritization
- `insider-threat-detection` - Privilege abuse coverage
- `cloud-security-assessment` - Cloud-specific technique coverage
- `supply-chain-security` - Third-party risk detection
- `data-exfiltration-defense` - Exfiltration technique coverage
- `initial-access-hardening` - Entry point detection review
- `credential-theft-protection` - Credential access coverage

Usage:
```
Use the ransomware-readiness-assessment prompt
```

## Resources

- **GitHub:** https://github.com/MHaggis/Security-Detections-MCP
- **Web App:** https://detect.michaelhaag.org
- **Setup Guide:** https://github.com/MHaggis/Security-Detections-MCP/blob/main/SETUP.md
- **Hosted MCP Guide:** https://github.com/MHaggis/Security-Detections-MCP/blob/main/docs/HOSTED_MCP.md
- **Tools Reference:** https://github.com/MHaggis/Security-Detections-MCP/blob/main/docs/wiki/Tools-Reference.md
- **API Token:** https://detect.michaelhaag.org/account/tokens
