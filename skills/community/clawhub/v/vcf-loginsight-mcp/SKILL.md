---
name: vcf-loginsight-mcp
description: An MCP server that provides native tools to dynamically search VMware Aria Operations for Logs (Log Insight).
version: 1.0.1
homepage: https://github.com/kasture-rohit/vcf-openclaw-skills
metadata:
  openclaw:
    requires:
      env:
        - LOGINSIGHT_HOST
        - LOGINSIGHT_API_TOKEN
    emoji: ""
---

# VCF Log Insight MCP Explorer

This skill uses the Model Context Protocol (MCP) to provide the AI agent with a native `query_vcf_logs` tool. 

### Setup Instructions for OpenClaw
To use this skill, the OpenClaw agent must run the attached Python MCP server. 

1. Install dependencies: `pip install -r requirements.txt`
2. Configure your OpenClaw settings to launch this MCP server. Add the following to your agent's MCP configuration:

```json
{
  "mcpServers": {
    "vcf-logs": {
      "command": "python",
      "args": ["server.py"],
      "env": {
        "LOGINSIGHT_HOST": "your-loginsight-fqdn",
        "LOGINSIGHT_API_TOKEN": "your-api-token"
      }
    }
  }
}