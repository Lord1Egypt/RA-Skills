---
name: vcf-lcm-precheck-analyzer
description: An MCP server that interfaces with VCF SDDC Manager to retrieve and analyze LCM upgrade pre-check results, providing instant remediation steps for failures.
version: 1.0.1
homepage: https://github.com/kasture-rohit/vcf-openclaw-skills
metadata:
  openclaw:
    requires:
      env:
        - SDDCMANAGER_HOST
        - SDDCMANAGER_API_TOKEN
    emoji: ""
---

# VCF LCM Pre-check Analyzer (MCP)

This skill utilizes the Model Context Protocol (MCP) to provide the AI agent with a native `analyze_lcm_precheck` tool, connecting directly to the VMware Cloud Foundation SDDC Manager API.

### Setup Instructions for OpenClaw
To use this skill, the OpenClaw agent must run the attached Python MCP server locally.

1. Install dependencies: `pip install -r requirements.txt`
2. Configure your OpenClaw settings to launch this MCP server by adding the following to your agent's MCP configuration block:

```json
{
  "mcpServers": {
    "vcf-lcm-analyzer": {
      "command": "python",
      "args": ["server.py"],
      "env": {
        "SDDCMANAGER_HOST": "your-sddc-manager-fqdn",
        "SDDCMANAGER_API_TOKEN": "your-api-token"
      }
    }
  }
}