---
name: snowflake-data
description: Execute SQL queries, inspect Snowflake databases, schemas, tables, views, warehouses, and data pipeline resources. Use this skill when users want to query data, explore database structure, manage warehouses, or run analytics workflows in Snowflake.
---

# Snowflake

![Snowflake](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/snowflake.svg?v=2)

Execute SQL queries and explore Snowflake data resources — databases, schemas, tables, views, warehouses, and pipelines — directly from chat.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=snowflake-data) for hosted connection flows and credentials so you do not need to configure Snowflake API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Snowflake |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Snowflake |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Snowflake      │
│   (User Chat)   │     │   (OAuth)    │     │   REST API       │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Snowflake │                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ Snowflake│
   │  File    │           │ Auth     │           │ Account  │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Snowflake again."

## Quick Start

```bash
# List databases
clawlink_call_tool --tool "snowflake_list_databases" --params '{}'

# Execute a SELECT query
clawlink_call_tool --tool "snowflake_execute_query" --params '{"sql": "SELECT * FROM MY_DB.MY_SCHEMA.MY_TABLE LIMIT 10"}'

# List tables in a schema
clawlink_call_tool --tool "snowflake_list_tables" --params '{"database": "MY_DB", "schema": "MY_SCHEMA"}'
```

## Authentication

All Snowflake tool calls are authenticated automatically by ClawLink using the user's connected Snowflake account credentials.

**No credentials are required in chat.** ClawLink stores the connection credentials securely and injects them into every Snowflake API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=snowflake and connect Snowflake.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `snowflake` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration snowflake
```

**Response:** Returns the live tool catalog for Snowflake.

### Reconnect

If Snowflake tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=snowflake
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration snowflake`

## Security & Permissions

- Access is scoped to the Snowflake account and databases authorized during connection setup.
- **All write operations and DDL/DML queries require explicit user confirmation.** Never execute ALTER, DROP, DELETE, or TRUNCATE without explicit approval.
- SELECT queries should use explicit LIMIT clauses to avoid returning extremely large result sets.
- Confirm the target database, schema, and table before any write or delete operation.
- Raw SQL execution via `snowflake_execute_query` carries full risk — always confirm the SQL before running.

## Tool Reference

### Databases & Schemas

| Tool | Description | Mode |
|------|-------------|------|
| `snowflake_list_databases` | List all databases accessible to the account | Read |
| `snowflake_get_database` | Get metadata for a specific database | Read |
| `snowflake_list_schemas` | List all schemas in a database | Read |
| `snowflake_get_schema` | Get metadata for a specific schema | Read |

### Tables & Views

| Tool | Description | Mode |
|------|-------------|------|
| `snowflake_list_tables` | List all tables in a database and schema | Read |
| `snowflake_get_table` | Get metadata for a specific table | Read |
| `snowflake_list_views` | List all views in a database and schema | Read |
| `snowflake_get_view` | Get the SQL definition of a view | Read |
| `snowflake_list_columns` | List all columns in a table or view | Read |
| `snowflake_describe_table` | Describe the structure of a table | Read |

### Query Execution

| Tool | Description | Mode |
|------|-------------|------|
| `snowflake_execute_query` | Execute a raw SQL query and return results | Write |
| `snowflake_execute_statement` | Execute a DDL or DML statement | Write |

### Warehouses

| Tool | Description | Mode |
|------|-------------|------|
| `snowflake_list_warehouses` | List all warehouses | Read |
| `snowflake_get_warehouse` | Get warehouse properties and status | Read |
| `snowflake_create_warehouse` | Create a new warehouse | Write |
| `snowflake_suspend_warehouse` | Suspend a warehouse | Write |
| `snowflake_resume_warehouse` | Resume a suspended warehouse | Write |

### Users & Roles

| Tool | Description | Mode |
|------|-------------|------|
| `snowflake_list_users` | List all users in the account | Read |
| `snowflake_get_user` | Get user properties and grants | Read |
| `snowflake_list_roles` | List all roles | Read |
| `snowflake_get_role_grants` | List grants for a role | Read |

### Stages & Files

| Tool | Description | Mode |
|------|-------------|------|
| `snowflake_list_stages` | List stages in a schema | Read |
| `snowflake_list_files_in_stage` | List files in a named stage | Read |
| `snowflake_put_file` | Upload a file to an internal stage | Write |

## Code Examples

### List all tables in a schema

```bash
clawlink_call_tool --tool "snowflake_list_tables" \
  --params '{
    "database": "ANALYTICS_DB",
    "schema": "PUBLIC"
  }'
```

### Execute a SELECT query with a LIMIT

```bash
clawlink_call_tool --tool "snowflake_execute_query" \
  --params '{
    "sql": "SELECT customer_id, SUM(amount) as total FROM TRANSACTIONS GROUP BY customer_id ORDER BY total DESC LIMIT 20"
  }'
```

### Get table column details

```bash
clawlink_call_tool --tool "snowflake_list_columns" \
  --params '{
    "database": "SALES_DB",
    "schema": "ORDERS",
    "table": "CUSTOMERS"
  }'
```

### Check warehouse status

```bash
clawlink_call_tool --tool "snowflake_get_warehouse" \
  --params '{
    "warehouse_name": "COMPUTE_WH"
  }'
```

### Suspend a warehouse

```bash
clawlink_call_tool --tool "snowflake_suspend_warehouse" \
  --params '{
    "warehouse_name": "COMPUTE_WH"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Snowflake is connected.
2. Call `clawlink_list_tools --integration snowflake` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `snowflake`.
5. If no Snowflake tools appear, direct the user to https://claw-link.dev/dashboard?add=snowflake.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → describe → execute SELECT                    │
│                                                             │
│  Example: List schemas → List tables → Describe table     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → execute DDL/DML             │
│                                                             │
│  Example: Preview DDL → User approves → Run CREATE TABLE   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, describe, and SELECT operations before any write or DDL.
4. For writes or DDL/DML queries, call `clawlink_preview_tool` first and confirm the exact SQL.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Always use explicit LIMIT clauses on SELECT queries to avoid returning extremely large datasets.
- DDL and DML operations (CREATE, DROP, DELETE, UPDATE, TRUNCATE) require explicit user confirmation.
- Table and column names may be case-sensitive depending on how they were created — use double quotes if needed.
- Warehouses must be running before queries can execute — they may auto-suspend after periods of inactivity.
- The account parameter for some operations is the Snowflake account identifier (not the account name).

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration snowflake`. |
| Missing connection | Snowflake is not connected. Direct the user to https://claw-link.dev/dashboard?add=snowflake. |
| `Database not found` | The specified database does not exist or is not accessible. |
| `Schema not found` | The specified schema does not exist in the database. |
| `Table not found` | The specified table does not exist. |
| `Warehouse not found` | The warehouse name is incorrect or not accessible. |
| `Insufficient privileges` | The connected account lacks the required role/privilege for this operation. |
| `Warehouse is suspended` | Cannot execute queries on a suspended warehouse. Resume it first. |
| `SQL compilation error` | Syntax error in the SQL query. Review and fix the SQL. |
| Write rejected | User did not confirm a write action or DDL/DML. Always confirm before executing. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Query Returns Empty

1. Verify the database, schema, and table names are spelled correctly — use `snowflake_list_tables` to confirm the table exists.
2. Check that the warehouse is running — suspended warehouses return no data.
3. Confirm the connected account has SELECT privilege on the target table.

### Troubleshooting: DDL/DML Fails

1. Verify the connected account has the required role/grants for the operation.
2. Some operations require the ACCOUNTADMIN role or specific object privileges.
3. Dropping tables or schemas may be blocked by referential integrity constraints.

## Resources

- [Snowflake Documentation](https://docs.snowflake.com/en/)
- [Snowflake SQL Reference](https://docs.snowflake.com/en/sql-reference)
- [Snowflake REST API](https://docs.snowflake.com/en/developer-guide/sql-api/index)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=snowflake-data
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=snowflake-data)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)