---
name: vcf-sustainability-mcp
description: An MCP server that interfaces with VMware Aria Operations to extract Green IT metrics, carbon footprint data, and the organizational Green Score for ESG reporting.
version: 1.0.1
homepage: https://github.com/kasture-rohit/vcf-openclaw-skills
metadata:
  openclaw:
    requires:
      env:
        - ARIA_OPS_HOST
        - ARIA_OPS_API_TOKEN
    emoji: ""
---

# VCF Sustainability & Carbon Footprint Analyzer

This skill uses the Model Context Protocol (MCP) to provide the AI agent with a native `get_vcf_carbon_footprint` tool. It queries VMware Aria Operations to generate executive-level ESG and Green IT reports.

### Setup Instructions for OpenClaw
To use this skill, the OpenClaw agent must run the attached Python MCP server. 

1. Install dependencies: `pip install -r requirements.txt`
2. Configure your OpenClaw settings to launch this MCP server. Add the following to your agent's MCP configuration:

```json
{
  "mcpServers": {
    "vcf-sustainability": {
      "command": "python",
      "args": ["server.py"],
      "env": {
        "ARIA_OPS_HOST": "your-aria-ops-fqdn",
        "ARIA_OPS_API_TOKEN": "your-api-token"
      }
    }
  }
}