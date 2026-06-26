---
name: vcf-compliance-mcp
description: An MCP server that interfaces with VMware Aria Operations to run regulatory compliance checks (ISO 27001, PCI DSS, CIS, etc.) against the VCF environment.
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

# VCF Regulatory Compliance Scanner

This skill uses the Model Context Protocol (MCP) to provide the AI agent with a native `get_vcf_compliance_status` tool. It queries VMware Aria Operations to generate instant audit reports for standard security frameworks.

### Setup Instructions for OpenClaw
To use this skill, the OpenClaw agent must run the attached Python MCP server. 

1. Install dependencies: `pip install -r requirements.txt`
2. Configure your OpenClaw settings to launch this MCP server. Add the following to your agent's MCP configuration:

```json
{
  "mcpServers": {
    "vcf-compliance": {
      "command": "python",
      "args": ["server.py"],
      "env": {
        "ARIA_OPS_HOST": "your-aria-ops-fqdn",
        "ARIA_OPS_API_TOKEN": "your-api-token"
      }
    }
  }
}