---
name: venn
description: Safely connects Gmail, Calendar, Drive, Atlassian (Jira/Confluence), Notion, GitHub, Salesforce, and dozens of other enterprise tools via a single MCP endpoint. Free, register @ https://venn.ai
version: 1.0.4
metadata:
  openclaw:
    emoji: "🦉"
    # 1. LIFECYCLE GATING
    # Prevents execution if the URL is missing or vennporter isn't installed.
    requires:
      env:
        - VENN_UNIVERSAL_URL
      bins:
        - vennporter

    # 2. AUTOMATED SETUP PROTOCOLS
    # This handles the "Discovery & Fix" flow if the skill is blocked.
    setup:
      on_missing:
        - message: "I need your Venn Universal URL to begin. You can find this in your Venn.ai settings under 'Integrations'."
          variable: VENN_UNIVERSAL_URL
          store: "openclaw.json"
      on_ready:
        - command: "bash ~/.openclaw/workspace/skills/venn/scripts/install-vennporter.sh"
          help: "Install/build vennporter (device_code-capable fork)"

        - command: "~/.local/bin/vennporter config add venn \"$VENN_UNIVERSAL_URL\" --deviceCodeGrant"
          help: "Register the Venn MCP server using vennporter"

        - command: "~/.local/bin/vennporter auth venn"
          help: "Authenticate Venn via device code (headless-safe)"

        - command: "~/.local/bin/vennporter list --output json"
          help: "Verify Venn is healthy"

    # 3. UI DASHBOARD CONFIGURATION
    # Maps the environment variable to a visible text field in the Web UI.
    fields:
      - name: VENN_UNIVERSAL_URL
        label: "Venn Universal URL"
        type: string
        ui: "config"
        placeholder: "https://app.venn.ai/mcp"
        help: "Your Venn Universal URL from https://app.venn.ai/assistants/openclaw"

    # 4. EXAMPLE PROMPTS TO GET STARTED
    examples:
      - prompt: "@venn which services do I have connected?"
        label: "Check connected services"
      - prompt: "@venn check my recent emails and summarize any action items"
        label: "Check recent emails"
      - prompt: "@venn find jira tickets assigned to me that need attention"
        label: "Check for work in Jira"
      - prompt: "@venn summarize this figma figjam session. The URL was [FIGJAM_SESSION_URL_HERE]"
        label: "Review figma figjam session"

    primaryEnv: VENN_UNIVERSAL_URL
    auth:
      method: oauth
      provider: venn
---

# Venn Your Universal MCP Server

## Overview
You are the architectural bridge between the user and their enterprise SaaS stack. You operate via the Venn MCP gateway to coordinate tasks across Atlassian, Google Workspace, Notion, Box, and other enterprise software tools.

## ⚡️ Quick Start Prompts
Copy and paste these to get started:

* **First Time Setup:** `@venn setup. Here is my URL: [PASTE_UNIVERSAL_URL_HERE]`
* **Reauthenticate:** `@venn auth`
* **Discovery:** `@venn Show me all my connected services`

## Core Activation Loop
When `@venn` is mentioned, or the user asks for data from a Venn-connected SaaS service (Gmail, Jira, Notion, etc.):

1. **Verify Environment:** Check if `VENN_UNIVERSAL_URL` is set. If not, follow the **Setup Flow**.
2. **The Discovery Loop:** Since Venn is a "Server of Servers," you must discover tools dynamically:
    - **Search:** Use `~/.local/bin/vennporter call venn.search_tools --args '{"query":"..."}'` for every new request.
    - **Describe:** Use `~/.local/bin/vennporter call venn.describe_tools` to validate JSON schemas before execution.
    - **Governance:** Check for `write_operation: "audit"`. If present, you MUST pause for user confirmation.

## Setup Request with Venn Universal URL & Bootstrap
If the user provides a URL in response to a setup request:
1. **Save & Sync:** Confirm you have saved the URL as an environment variable `VENN_UNIVERSAL_URL`
2. **Register:** Immediately run `~/.local/bin/vennporter config add venn --url <URL> --auth oauth --deviceCodeGrant`.
3. **Authenticate:** Follow Venn Authentication.
4. **Verify Health:** Run `~/.local/bin/vennporter list` and confirm the `venn` status is "ok" before proceeding.

## Setup Request with Missing Venn Universal URL
If `VENN_UNIVERSAL_URL` is missing or the connection is broken:
1. **Request URL:** Prompt the user for their Venn Universal URL from Venn.ai.
2. **Register Server:** Once provided, run:
   `~/.local/bin/vennporter config add venn --url "$VENN_UNIVERSAL_URL" --auth oauth --deviceCodeGrant`
3. **Initiate OAuth:** Check browser availability (see above).
   - **Browser available:** Run `~/.local/bin/vennporter auth venn` to launch the browser authorization.
   - **No browser:** Follow **Headless Authentication** below.
4. **Verify Health:** Run `~/.local/bin/vennporter  list` and confirm the `venn` status is "ok" before proceeding.

## Venn Authentication

### Step 1 — Build vennporter (once)
Check if the build already exists. If `~/.local/share/vennporter/dist/cli.js` is missing, run:
```
bash ~/.openclaw/workspace/skills/venn/scripts/install-vennporter.sh"
```

### Step 2 — Authenticate
In a sub-process, run the following command:
```bash
~/.local/bin/vennporter auth venn
```

#### Polling sub-process for outcome (timeout is 3 minutes)
1. Every 5 seconds, poll sub-process for output.
2. If `Authorization complete for 'venn'` is received, then the sub-process is complete.
3. If `To authorize, visit [[auth_url]]` is received, inform user to visit auth_url to authenticate Venn.
4. If `Failed to authorize 'venn'` is received DO NOT automatically retry authenticating. Inform user it did not complete.
5. Go back to step 1 until success or timeout.


## Execution Protocols

### 1. High-Efficiency Workflows
**Always** prefer `execute_workflow` for multi-step tasks to reduce latency.
- **Context Guardrail:** Extract only necessary keys (e.g., `id`, `subject`, `summary`). Do not return full raw API payloads to the user.
- **Timeout Management:** Enterprise SaaS calls can be slow. If using a `run` tool, set a 30s timeout for Venn workflows.

### 2. Single Tool Calls via `venn.execute_tool`
For individual operations, use this syntax:
```bash
~/.local/bin/vennporter call venn.execute_tool --args '{"server_id":"atlassian","tool_name":"atlassian_user_info","tool_args":{}}'
```

### 3. Discover which services are connected to Venn via `venn.help` tool
To list all services that user has connected to their Venn account, use this syntax:
```bash
~/.local/bin/vennporter call venn.help --args '{"action":"LIST_SERVERS"}'
```
