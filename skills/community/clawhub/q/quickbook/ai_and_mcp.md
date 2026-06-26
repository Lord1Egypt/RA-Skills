# QuickBooks Online AI & MCP Server Integration Reference

## Model Context Protocol (MCP) Server

The Model Context Protocol (MCP) enables LLMs to securely access external tools and data sources. Intuit maintains an official, open-source **QuickBooks Online MCP Server** that exposes standard accounting tools to compatible AI clients (e.g., Claude Code, Cursor, LangChain).

### Deployment & Configuration
1.  **Clone & Install:**
    ```bash
    git clone https://github.com/intuit/quickbooks-online-mcp-server.git
    cd quickbooks-online-mcp-server
    npm install
    ```
2.  **Configuration (`mcp-config.json`):**
    ```json
    {
      "mcpServers": {
        "quickbooks": {
          "command": "node",
          "args": ["dist/index.js"],
          "env": {
            "QUICKBOOKS_CLIENT_ID": "YOUR_CLIENT_ID",
            "QUICKBOOKS_CLIENT_SECRET": "YOUR_CLIENT_SECRET",
            "QUICKBOOKS_REDIRECT_URI": "https://localhost:8000/callback",
            "QUICKBOOKS_ENVIRONMENT": "sandbox"
          }
        }
      }
    }
    ```

### Exposed Tools Schema
The MCP server exposes a rich set of tools to the LLM. Each tool includes a descriptive JSON schema defining required parameters:
*   `create_customer`: Arguments include `DisplayName`, `CompanyName`, `PrimaryEmailAddr`.
*   `get_profit_and_loss`: Arguments include `start_date`, `end_date`, `accounting_method`.
*   `create_invoice`: Arguments include `CustomerRef`, `Line` items array.

---

## AI Agentic Accounting Workflows (LangGraph)

When designing AI agents to automate bookkeeping or reconciliation, use state machines to model task flows safely. Below is a LangGraph state workflow for matching incoming bank transactions to pending bills:

```
                   [State: Start]
                         |
                         v
             [Action: Fetch Webhook]
                         |
                         v
           [Action: Query Pending Bills]
                         |
                         v
         [Decision: Match Found? (LLM)]
                    /         \
                  YES          NO
                  /             \
                 v               v
     [Action: Pay Bill]     [Action: Flag for Review]
                 \               /
                  \             /
                   v           v
                    [State: End]
```
