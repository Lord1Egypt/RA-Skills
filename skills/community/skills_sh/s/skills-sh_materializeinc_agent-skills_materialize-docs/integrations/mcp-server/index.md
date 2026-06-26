# MCP Servers and agent skills

This section contains guides for installing Materialize Agent skills and integrating with Materialize's built-in MCP servers.

## Agent skills

Materialize provides the following open-source [agent
skills](https://github.com/MaterializeInc/agent-skills) to help developers build
with Materialize.

| Skill | What it provides | When to use |
|-------|------------------|-------------|
| `mcp-developer-analysis` | Exact catalog schemas, diagnostic workflows, remediation runbooks, and guardrails for known pitfalls (cluster-scoped queries, uint8 ID mismatches, etc.). | Operational introspection and troubleshooting via the `materialize-developer` server. Examples: *"why is my materialized view stale?"*, *"what can I optimize to save costs?"*, *"is my source healthy?"* |
| `materialize-docs` | Comprehensive Materialize documentation, including SQL syntax, idiomatic patterns, data ingestion, concepts, and best practices (400+ reference files). | Authoring view definitions, learning concepts, looking up patterns. Useful with either MCP server. Examples: *"show me how to deduplicate a stream"*, *"what's the idiomatic top-K pattern?"*, *"how do I create a Kafka source?"* |

## MCP servers

Materialize provides built-in Model Context Protocol (MCP) servers that AI
agents can use. The MCP interface is served directly by the database; no sidecar
process or external server is required. These endpoints use [JSON-RPC
 2.0](https://www.jsonrpc.org/specification) over HTTP POST (default port 6876)
and support the MCP `initialize`, `tools/list`, and `tools/call` methods.

| Endpoint | Path | Description |
|----------|------|-------------|
| **Agent** | `/api/mcp/agent` | Discover and query your real-time data products over HTTP. <br>For details, see [MCP Server for agents](/integrations/mcp-server/mcp-agent/).<br>*Available starting in v26.24*|
| **Developer** | `/api/mcp/developer` | Read `mz_*` system catalog tables for troubleshooting and observability. <br>For details, see [MCP Server for developer](/integrations/mcp-server/mcp-developer/).|

## See also

- [MCP Server
  Troubleshooting](/integrations/mcp-server/mcp-server-troubleshooting/)
- [Appendix: MCP Server (Python)](/integrations/mcp-server/llm) for locally-run,
  separate MCP Server.

---

## Agent endpoint configuration

## Available configuration parameters

The following configurations are available for the `/api/mcp/agent` endpoint:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `enable_mcp_agent` | `true` | Enable or disable the `/api/mcp/agent` endpoint. When disabled, requests return `HTTP 503 (Service Unavailable)`.|
| `enable_mcp_agent_query_tool` <a name="enable_mcp_agent_query_tool"></a> | `true` | Enable or disable the [`query` tool](/integrations/mcp-server/mcp-agent-tools/#query), which allows for queries with joins. Enabling the `query` tool can impact performance, leak information via query
execution errors, and, by default, allow catalog-level discovery of operational
metadata through system catalog access.  To prevent catalog-level discovery of operational metadata through system catalog access, you can [restrict `query` tool access to user objects only](/integrations/mcp-server/mcp-agent-tools/#restrict-to-user-objects). |
| `mcp_max_response_size` | `1000000` | Maximum response size in bytes. Queries exceeding this limit return an error. |

## Disabling the endpoint

The `materialize-agent` endpoint is enabled by default. To disable it:

**Cloud:**

Contact [Materialize support](https://materialize.com/docs/support/) to
enable/disable the MCP agent endpoint for your environment.

**Self-Managed:**

Disable the endpoint using one of these methods:

**Option 1: Configuration file**

Set the parameter in your
[system parameters configuration file](/self-managed-deployments/configuration-system-parameters/):

```yaml
system_parameters:
  enable_mcp_agent: "false"
```

**Option 2: Terraform**

Set the parameter via the [Materialize Terraform module](https://github.com/MaterializeInc/materialize-terraform-self-managed):

```hcl
system_parameters = {
  enable_mcp_agent = "false"
}
```

**Option 3: SQL**

Connect as `mz_system` and run:

```mzsql
ALTER SYSTEM SET enable_mcp_agent = false;
```

> **Note:** These parameters are only accessible to the `mz_system` and `mz_support`
> roles. Regular database users cannot view or modify them.

---

## Agent MCP server tools

## Tools

### `get_data_products`

Returns the list of data products discoverable by the tool. Materialized views
and indexed views are discoverable by `get_data_products`. Regular views must
have an index to be discoverable.

**Parameters:** None.

**Example response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "[\n  [\n    \"\\\"materialize\\\".\\\"mcp_schema\\\".\\\"payment_status\\\"\",\n    \"mcp_cluster\",\n    \"Given an order ID, return the current payment status.\"\n  ]\n]"
      }
    ],
    "isError": false
  }
}
```

### `get_data_product_details`

Returns the full details for a specific data product, including its JSON schema
with column names, types, and descriptions.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Exact name from the `get_data_products` list. |

**Example response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "[\n  [\n    \"\\\"materialize\\\".\\\"mcp_schema\\\".\\\"payment_status\\\"\",\n    \"mcp_cluster\",\n    \"Given an order ID, return the current payment status.\",\n    \"{\\\"order_id\\\": {\\\"type\\\": \\\"integer\\\", \\\"position\\\": 1}, \\\"status\\\": {\\\"type\\\": \\\"text\\\", \\\"position\\\": 3}}\"\n  ]\n]"
      }
    ],
    "isError": false
  }
}
```

### `read_data_product`

Reads rows from a data product.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Fully-qualified name, e.g. `"materialize"."public"."payment_status"`. |
| `limit` | integer | No | Maximum rows to return. Default: 500, max: 1000. |
| `cluster` | string | No | Cluster override. If omitted, uses the cluster from the catalog. |

**Example response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "[\n  [\n    1001,\n    42,\n    \"shipped\",\n    \"2026-03-26T10:30:00Z\"\n  ]\n]"
      }
    ],
    "isError": false
  }
}
```

### `query`

> **Warning:** Enabling the `query` tool can impact performance, leak information via query
> execution errors, and, by default, allow catalog-level discovery of operational
> metadata through system catalog access.

Allows the agent to run arbitrary `SELECT` statements (including joins) against
**any** object for which the agent has the appropriate privileges (`SELECT` on
the object, `USAGE` on the object's schema), not just the objects
discoverable by `get_data_products`. Starting in v26.27, it is enabled by
default.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `cluster` | string | Yes | Exact cluster name from the data product details. |
| `sql_query` | string | Yes | PostgreSQL-compatible `SELECT` statement. |

**Example response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "[\n  [\n    \"42\",\n    \"shipped\"\n  ]\n]"
      }
    ],
    "isError": false
  }
}
```

> **Note:** - *Recommended*. To prevent an agent from querying the system catalog objects
>   (`mz_catalog.*`, `mz_internal.*`, `pg_catalog.*`, and `information_schema.*`),
>   see [Restrict `query` tool access to user objects
>   only](#restrict-to-user-objects).
> - To disable the tool, set the [`enable_mcp_agent_query_tool`
>   configuration](/integrations/mcp-server/mcp-agent-config/#enable_mcp_agent_query_tool)
>   system parameter to `false`. Once disabled, you can only query data products
>   that are discoverable by [`get_data_products`](#get_data_products).

#### Restricting `query` tool access to user objects only {#restrict-to-user-objects}

When the [`query` tool](/integrations/mcp-server/mcp-agent-tools/#query) is
enabled, a role can, by default, query any object for which it has appropriate
privileges, including system catalog objects (`mz_catalog.*`, `mz_internal.*`,
`pg_catalog.*`, and `information_schema.*`).

To prevent an agent role from reading system catalog objects, a **superuser**
can set the `restrict_to_user_objects` parameter to `true` on both the
functional role and each individual agent role. Setting the parameter on the
functional role is recommended as a precaution in case the role is ever used
directly to run queries. Because role configuration in Materialize is not
inherited, the parameter must be set explicitly on each individual agent role:

```mzsql
ALTER ROLE mcp_agent SET restrict_to_user_objects = true;
ALTER ROLE my_agent SET restrict_to_user_objects = true;
```

This setting takes effect on the next connection. Once active:

- Queries referencing system catalog objects are rejected with a permission
  error.
- Data product discovery (`get_data_products`, `get_data_product_details`,
  `read_data_product`) continues to work normally.
- The restriction cannot be bypassed by the role itself; only a superuser can
  change or remove it.

To remove the restriction for an agent, a superuser can reset the parameter (or
set it to `false`):

```mzsql
ALTER ROLE my_agent RESET restrict_to_user_objects;
```

---

## Appendix: MCP Server (Python)

> **Disambiguation:** This page provides information on the locally-run, separate MCP Server. For documentation on using the new built-in MCP Server endpoints, see: - [MCP Server for Developer](/integrations/mcp-server/mcp-developer/) 

The [Model Context Protocol (MCP) Server for Materialize](https://materialize.com/blog/materialize-turns-views-into-tools-for-agents/) lets large language models (LLMs) call your indexed views as real-time tools.
The MCP Server automatically turns any indexed view with a comment into a callable, typed interface that LLMs can use to fetch structured, up-to-date answers—directly from the database.

These tools behave like stable APIs.
They're governed by your SQL privileges, kept fresh by Materialize's incremental view maintenance, and ready to power applications that rely on live context instead of static embeddings or unpredictable prompt chains.

## Get Started

We recommend using [uv](https://docs.astral.sh/uv/) to install and run the server.
It provides fast, reliable Python environments with dependency resolution that matches pip.

If you don't have uv installed, you can install it first:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

To install and launch the MCP Server for Materialize:

```bash
uv venv
uv pip install mcp-materialize-agents
uv run mcp_materialize_agents
```

You can configure it using CLI flags or environment variables:

| Flag              | Env Var             | Default                                               | Description                                   |
| ----------------- | ------------------- | ----------------------------------------------------- | --------------------------------------------- |
| `--mz-dsn`        | `MZ_DSN`            | `postgres://materialize@localhost:6875/materialize`   | Materialize connection string                 |
| `--transport`     | `MCP_TRANSPORT`     | `stdio`                                               | Communication mode (`stdio`, `sse`, or `http`) |
| `--host`          | `MCP_HOST`          | `0.0.0.0`                                             | Host for `sse` and `http` modes               |
| `--port`          | `MCP_PORT`          | `3001` (sse), `8001` (http)                           | Port for `sse` and `http` modes               |
| `--pool-min-size` | `MCP_POOL_MIN_SIZE` | `1`                                                   | Minimum DB pool size                          |
| `--pool-max-size` | `MCP_POOL_MAX_SIZE` | `10`                                                  | Maximum DB pool size                          |
| `--log-level`     | `MCP_LOG_LEVEL`     | `INFO`                                                | Logging verbosity                             |

## Define Tools

Any view in Materialize can become a callable tool as long as it meets a few requirements to ensure that the tool is fast to query, safe to expose, and easy for language models to use correctly.

- [The view is indexed.](#1-define-and-index)
- [The view includes a top level comment.](#2-comment)
- [The role used to run the MCP Server must have required privileges.](#3-set-rbac-permissions)

### 1. Define and Index

You must create at least one [index](/concepts/indexes/) on the view. The columns in the index define the required input fields for the tool.

You can index a single column:

```mzsql
CREATE INDEX ON payment_status_summary (order_id);
```

Or multiple columns:

```mzsql
CREATE INDEX ON payment_status_summary (user_id, order_id);
```

Every indexed column becomes part of the tool's input schema.

### 2. Comment

The view must include a top-level comment that is used as the tool's description.
Comments should be descriptive as they help the model reason about what the tool does and when to use it.
You can optionally add a comment on any of the indexed columns to improve the tool's schema with descriptions for each field.

```mzsql
COMMENT ON VIEW payment_status_summary IS
  'Given a user ID and order ID, return the current payment status and last update time.
   Use this tool to drive user-facing payment tracking.';

COMMENT ON COLUMN payment_status_summary.user_id IS
  'The ID of the user who placed the order';

COMMENT ON COLUMN payment_status_summary.order_id IS
  'The unique identifier for the order';
```

### 3. Set RBAC Permissions

The database role used to run the MCP Server must:

* Have `USAGE` privileges on the database and schema the view is in.
* Have `SELECT` privileges on the view.
* Have `USAGE` privileges on the cluster where the index is installed.

```mzsql
GRANT USAGE on DATABASE materialize TO mcp_server_role;
GRANT USAGE on SCHEMA materialize.public TO mcp_server_role;
GRANT SELECT ON payment_status_summary TO mcp_server_role;
GRANT USAGE ON CLUSTER mcp_cluster TO mcp_server_role;
```

## Related Pages

* [Coding Agent Skills](/integrations/coding-agent-skills/)
* [CREATE VIEW](/sql/create-view)
* [CREATE INDEX](/sql/create-index)
* [COMMENT ON](/sql/comment-on)
* [CREATE ROLE](/sql/create-role)
* [GRANT PRIVILEGE](/sql/grant-privilege)

---

## Developer endpoint configuration

## Available configuration parameters

The following configurations are available for the `/api/mcp/developer`
endpoint:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `enable_mcp_developer` | `true` | Enable or disable the `/api/mcp/developer` endpoint. When the endpoint is disabled, requests return HTTP 503 (Service Unavailable). |
| `mcp_max_response_size` | `1000000` | Maximum response size in bytes. Queries exceeding this limit return an error. |

## Disabling the endpoint

The developer endpoint is enabled by default. To disable it:

**Cloud:**

Contact [Materialize support](https://materialize.com/docs/support/) to
disable the MCP developer endpoint for your environment.

**Self-Managed:**

Disable the endpoint using one of these methods:

**Option 1: Configuration file**

Set the parameter in your
[system parameters configuration file](/self-managed-deployments/configuration-system-parameters/):

```yaml
system_parameters:
  enable_mcp_developer: "false"
```

**Option 2: Terraform**

Set the parameter via the [Materialize Terraform module](https://github.com/MaterializeInc/materialize-terraform-self-managed):

```hcl
system_parameters = {
  enable_mcp_developer = "false"
}
```

**Option 3: SQL**

Connect as `mz_system` and run:

```mzsql
ALTER SYSTEM SET enable_mcp_developer = false;
```

> **Note:** These parameters are only accessible to the `mz_system` and `mz_support`
> roles. Regular database users cannot view or modify them.

---

## Developer MCP server tools

## Tools

### `query_system_catalog`

Execute a read-only SQL query restricted to system catalog tables (`mz_*`,
`pg_catalog`, `information_schema`).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sql_query` | string | Yes | `SELECT`, `SHOW`, or `EXPLAIN` query using only system catalog tables. |

Only one statement per call is allowed. Write operations (`INSERT`, `UPDATE`,
`CREATE`, etc.) are rejected.

**Example response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "[\n  [\n    \"quickstart\",\n    \"ready\"\n  ],\n  [\n    \"mcp_cluster\",\n    \"ready\"\n  ]\n]"
      }
    ],
    "isError": false
  }
}
```

### Key system catalog tables

| Scenario | Tables |
|----------|--------|
| Freshness / lag | `mz_internal.mz_materialization_lag`, `mz_internal.mz_wallclock_global_lag_recent_history`, `mz_internal.mz_hydration_statuses` |
| Memory / resources | `mz_internal.mz_cluster_replica_utilization`, `mz_internal.mz_cluster_replica_metrics` |
| Cluster health | `mz_internal.mz_cluster_replica_statuses`, `mz_catalog.mz_cluster_replicas` |
| Source / Sink health | `mz_internal.mz_source_statuses`, `mz_internal.mz_sink_statuses`, `mz_internal.mz_source_statistics` |
| Object inventory | `mz_catalog.mz_materialized_views`, `mz_catalog.mz_sources`, `mz_catalog.mz_sinks`, `mz_catalog.mz_indexes` |
| Optimization | `mz_internal.mz_index_advice`, `mz_catalog.mz_cluster_replica_sizes` |

Use `SHOW TABLES FROM mz_internal` or `SHOW TABLES FROM mz_catalog` to
discover more tables.

## See also

- [System catalog](/reference/system-catalog/)

---

## MCP Server for Agents

> **Public Preview:** This feature is in public preview.

Starting in v26.24, Materialize provides a built-in `materialize-agent` Model
Context Protocol (MCP) server (`/api/mcp/agent`, port 6876) for querying data
products. The server is provided directly by Materialize; no sidecar process or
external server is required.

## Overview

The `materialize-agent` MCP server lets AI agents query business-facing data
products over HTTP. You can connect an MCP-compatible client (such as Claude
Code, Claude Desktop, or Cursor) to the MCP server and ask the agent to discover
and query your data products using either natural language or SQL:

- *Via `materialize-agent`: What data products can I query?*
- *SELECT * FROM mcp_product_performance LIMIT 5;*
- *What's the `total_revenue` for product 42?*
- *Perform a Pareto analysis on my products.*

## Set up the agent query environment and data products

> **Note:** Starting in v26.27, the [`query`
> tool](/integrations/mcp-server/mcp-agent-tools/#query) is **enabled by default**
> and can execute arbitrary `SELECT` queries (including joins) on **all** objects
> the agent can access (including system catalog objects), not just those
> discoverable by the [`get_data_products`
> tool](/integrations/mcp-server/mcp-agent-tools/#get_data_products).
> To prevent agents from reading system catalog objects, set
> `restrict_to_user_objects` on each agent role.

In Materialize, querying data products (i.e., running [`SELECT`](/sql/select/))
requires:

- `SELECT` privileges on each directly referenced data product.
- `USAGE` privileges on the schemas that contain the data products.
- `USAGE` privileges on the cluster where the query runs.

To use the `materialize-agent` MCP server, we recommend:

1. Creating a dedicated query environment for agents.
1. Defining curated data products within that environment.

> **Note:** The examples below use the default `materialize` database.

### Create an agent query environment

In general, AI agents that access the `materialize-agent` MCP server should be
isolated to:

| Query environment | Granted privileges |
|---|---|
| Serving cluster dedicated to agents | `USAGE` on this cluster only |
| Schema dedicated to agents | `USAGE` on this schema only |

1. Create a dedicated cluster and schema:

   ```mzsql
   CREATE CLUSTER mcp_cluster SIZE '25cc';
   CREATE SCHEMA materialize.mcp_schema;
   ```

1. Create a functional role `mcp_agent` that can be assigned to individual
   agents:

   ```mzsql
   CREATE ROLE mcp_agent;
   ```

1. Grant privileges to the functional role:

   ```mzsql
   GRANT USAGE ON CLUSTER mcp_cluster TO mcp_agent;
   GRANT USAGE ON SCHEMA materialize.mcp_schema TO mcp_agent;
   ```

1. Set the default cluster and schema for `mcp_agent` to `mcp_cluster` and
   `mcp_schema`:

   ```mzsql
   ALTER ROLE mcp_agent SET cluster TO mcp_cluster;
   ALTER ROLE mcp_agent SET search_path TO mcp_schema;
   ```

   Later on, you will also set these role configurations on the specific agent
   roles since role configurations are **not** inherited; only privileges are
   inherited.

1. Recommended. Restrict the role to user objects only so that the [`query`
   tool](/integrations/mcp-server/mcp-agent-tools/#query) cannot read system
   catalog objects. You must run the following as a **superuser**:

   ```mzsql
   ALTER ROLE mcp_agent SET restrict_to_user_objects = true;
   ```

   As mentioned before, role configurations are **not** inherited; you must also
   set it on each specific agent role. Setting the parameter on the functional
   role is recommended as a precaution in case the role is ever used directly to
   run queries.

   See also [Restrict `query` tool access to user objects
   only](/integrations/mcp-server/mcp-agent-tools/#restrict-to-user-objects).

### Define data products and grant access

Once a dedicated agent environment is set up, create the curated data products
in the dedicated cluster and schema rather than granting access to existing
objects in other schemas; this allows you to:

- Project, mask, or filter their contents before exposing them to the agent.

- Restrict the agent's `USAGE` to the dedicated schema.

> **Tip:** - To expose an existing object (such as a table, view, or materialized view) to
>   the agent, create a view in `mcp_schema` that selects from it, then add an
>   index on that view `IN CLUSTER mcp_cluster`. If the existing object is a
>   materialized view, the index reuses the already-maintained result instead of
>   recomputing it.
> - When a view (regular view or materialized view) is indexed, the indexed
>   columns are surfaced in the tool input schema as preferred lookup keys,
>   enabling [index point-lookups](/concepts/indexes/#point-lookups) instead of
>   index scans.
> - Adding [comments](/sql/comment-on/) to the data product and its columns is
>   **optional but recommended**. Comments are surfaced to the agent to help it
>   better understand **when** and **how** to use the data products:
>   - Object-level comments: When a data product is indexed, if the index also has
>     a comment, the index's comment is surfaced to the agent. Otherwise, the view
>     or materialized view's comment is surfaced.
>   - Column comments: Column comments are made on the view or materialized view.
>     Indexes do not support comments on columns.

#### Define data products

The following example assumes a materialized view `sales.product_performance`
exists.

1. Create a view in the dedicated schema that selects from the existing
   materialized view:

   ```mzsql
   CREATE VIEW materialize.mcp_schema.mcp_product_performance AS
   SELECT * FROM sales.product_performance;
   ```

1. Index the view `IN CLUSTER mcp_cluster`. The indexed columns are surfaced to
   the agent as preferred lookup keys:

   ```mzsql
   CREATE INDEX mcp_product_performance_idx
   IN CLUSTER mcp_cluster
   ON materialize.mcp_schema.mcp_product_performance (product_id);
   ```

1. Optional but recommended. Add comments to the view and column(s):

   ```mzsql
   COMMENT ON VIEW materialize.mcp_schema.mcp_product_performance IS
   'Per-product performance metrics including stock status. Use this to answer
   questions about a specific product''s sales performance or inventory.';

   COMMENT ON COLUMN materialize.mcp_schema.mcp_product_performance.total_revenue IS
   'Lifetime gross revenue for this product, computed as SUM(quantity *
   unit_price) across all order_items. Returns 0 for products that have
   not been ordered yet.';

   COMMENT ON COLUMN materialize.mcp_schema.mcp_product_performance.stock_status IS
   'Derived inventory state: ''out_of_stock'' (stock_quantity = 0),
   ''low_stock'' (< 20), or ''in_stock'' (>= 20).';
   ```

   Comments are surfaced to the agent to help the agent better understand
   **when** and **how** to use the data products.

#### Grant access

1. Grant `SELECT` privilege on the data products. For each existing data
   product, grant `SELECT` to the `mcp_agent` functional role:

   ```mzsql
   GRANT SELECT ON materialize.mcp_schema.mcp_product_performance TO mcp_agent;
   ```

1. Optionally, set a [default privilege](/sql/alter-default-privileges/) to
   automatically grant `SELECT` to the `mcp_agent` functional role for future
   data products created in the `mcp_schema`:

   ```mzsql
   ALTER DEFAULT PRIVILEGES
     FOR ROLE <creator_role> -- creator of the object
     IN SCHEMA materialize.mcp_schema
     GRANT SELECT ON TABLES TO mcp_agent;
   ```

   - The `FOR ROLE <creator_role>` clause scopes the default privilege to those
     objects created by that role. Specify the role that will actually create
     your data products.

   - `TABLES` includes views and materialized views also.

   - [`ALTER DEFAULT PRIVILEGES`](/sql/alter-default-privileges/) only applies
     to objects created **after** the `ALTER DEFAULT PRIVILEGES` statement runs.
     For objects that already exist, use [`GRANT SELECT ON <object> TO
     mcp_agent`](/sql/grant-privilege/).

## Create the specific agent role

For your specific agent, create the role with which the agent will connect.

**Cloud:**

1. Log in to the [Materialize Console](https://console.materialize.com/).

1. Create a dedicated
   [service account](/security/cloud/users-service-accounts/create-service-accounts/)
   for your specific AI agent (only an Org admin can create service
   accounts).[^1]

   For example, to create a new `my_agent` service account:

   1. Click **+ Create New** and select **App Password** to open the **New app
      password** modal.

   1. In the **New app password** modal, specify:

      | Field      | Value        |
      | ---------- | -------------|
      | **Type**   | **Service**  |
      | **Name**   | **MCP**      |
      | **User**   | **my_agent** |
      | **Roles**  | **Organization Member** |

   1. Click **Create Password**. The **Password** and the **MCP Token** are
      created.

   1. Save the **MCP Token** in a secure place. Once you navigate away, the
      password and the MCP token will not display again. You will use the **MCP
      Token** to connect.

      ![Image of Create new service app
      flow](/images/console/console-create-new/create-app-password-mcp-token.png
      "Materialize Console Create New Service App Password Flow")

1. Ensure the corresponding database role has been created, either by:

   - Manually issuing the following commands in the SQL Shell:

     ```mzsql
     CREATE ROLE my_agent;
     ```

   - Or, connecting to Materialize (not the MCP server) using the new account.
     On first connection, Materialize automatically creates the corresponding
     database role if it does not exist.

1. Grant `mcp_agent` role to your agent:

   ```mzsql
   GRANT mcp_agent TO my_agent;
   ```

1. Set the default cluster and schema for `my_agent` to `mcp_cluster` and
   `mcp_schema`:

   ```mzsql
   ALTER ROLE my_agent SET cluster TO mcp_cluster;
   ALTER ROLE my_agent SET search_path TO mcp_schema;
   ```

   You set these role configurations on the individual roles as configurations are not inherited.

1. Recommended. Restrict the role to user objects only so that the [`query`
   tool](/integrations/mcp-server/mcp-agent-tools/#query) cannot read system
   catalog objects. You must run the following as a **superuser** (an
   Organization Admin):

   ```mzsql
   ALTER ROLE my_agent SET restrict_to_user_objects = true;
   ```

[^1]: Avoid using a personal app account instead of a service account as a
    personal app account would include all your roles and privileges as well.

**Self-Managed:**

1. Create a login role for your specific AI agent, replacing
   `<your_app_password>` with an actual password:

   ```mzsql
   CREATE ROLE my_agent LOGIN PASSWORD '<your_app_password>';
   ```

1. Grant `mcp_agent` role to your agent:

   ```mzsql
   GRANT mcp_agent TO my_agent;
   ```

1. Set the default cluster and schema for `my_agent` to `mcp_cluster` and
   `mcp_schema`:

   ```mzsql
   ALTER ROLE my_agent SET cluster TO mcp_cluster;
   ALTER ROLE my_agent SET search_path TO mcp_schema;
   ```

   You set these role configurations on the individual roles as configurations
   are not inherited.

1. Recommended. Restrict the role to user objects only so that the [`query`
   tool](/integrations/mcp-server/mcp-agent-tools/#query) cannot read system
   catalog objects. You must run the following as a **superuser**:

   ```mzsql
   ALTER ROLE my_agent SET restrict_to_user_objects = true;
   ```

**Emulator:**

1. Create a role for your specific AI agent (the Emulator does not support the
   `LOGIN PASSWORD` option):

   ```mzsql
   CREATE ROLE my_agent;
   ```

1. Grant `mcp_agent` role to your agent:

   ```mzsql
   GRANT mcp_agent TO my_agent;
   ```

1. Set the default cluster and schema for `my_agent` to `mcp_cluster` and
   `mcp_schema`:

   ```mzsql
   ALTER ROLE my_agent SET cluster TO mcp_cluster;
   ALTER ROLE my_agent SET search_path TO mcp_schema;
   ```

   You set these role configurations on the individual roles as configurations
   are not inherited.

1. Recommended. Restrict the role to user objects only so that the [`query`
   tool](/integrations/mcp-server/mcp-agent-tools/#query) cannot read system
   catalog objects. You must run the following as a **superuser**:

   ```mzsql
   ALTER ROLE my_agent SET restrict_to_user_objects = true;
   ```

## Connect to the MCP server

### Step 1. Get connection details

When connecting to the MCP server, the MCP-compatible client needs:

- The Base64-encoded `user:password` credentials (i.e., the MCP token) of your
  [agent](#create-the-specific-agent-role).

- The `materialize-agent` MCP server URL: `<baseURL>/api/mcp/agent`.

**Cloud:**

1. Log in to the Materialize Console.

1. Go to **App Passwords** and for the [service account created
   `my_agent`](#create-the-specific-agent-role), click
   **Connect**.

1. Click on the **MCP Server** tab.

1. In the **Get your MCP token** section[^1],
   - If using [`my_agent`](#create-the-specific-agent-role), use the **MCP
     Token** that was returned when you created the service account. You can
     skip to the next step.

   - Otherwise, you can:
     - [Create a different service account](#create-the-specific-agent-role) and
       use the generated MCP token; or

     - Use an existing service account, Base64 encoding the `role:password` to
       generate the MCP token. Ensure the existing account does not have more
       privileges than necessary.

1. In the **Connect your client** section, click on the **Agent** tab.

   You can find your `materialize-agent` MCP server URL
   `<baseURL>/api/mcp/agent` as part of the code block.

   If using Claude Code as your MCP-compatible client, you can copy the code
   block wholesale for the next step.

[^1]: Avoid using a personal app account instead of a service account as a
    personal app account would include all your roles and privileges as well.

**Self-Managed:**

1. Encode your agent role's credentials `<role>:<password>` in Base64 to create
   the MCP token, replacing `<your_app_password>` with the actual password:

   ```bash
   printf 'my_agent:<your_app_password>' | base64
   ```

1. Find your deployment's host name to determine your `materialize-agent` MCP
   URL:

   ```
   http://<host>:6876/api/mcp/agent
   ```

   - For your Self-Managed Materialize deployment in AWS/GCP/Azure, the `<host>`
     is the load balancer address. If [deployed via
     Terraform](/self-managed-deployments/installation/#install-using-terraform-modules),
     run the Terraform output command for your cloud provider:

     ```bash
     # AWS
     terraform output -raw nlb_dns_name

     # GCP
     terraform output -raw balancerd_load_balancer_ip

     # Azure
     terraform output -raw balancerd_load_balancer_ip
     ```

   - For local
     [kind](/self-managed-deployments/installation/install-on-local-kind/)
     clusters, use port forwarding and use `localhost` for `<host>`:

     ```bash
     kubectl port-forward svc/<instance-name>-balancerd 6876:6876 -n materialize-environment
     ```

**Emulator:**

1. Encode your agent role's credentials `<role>:<password>` in Base64 to create
   the MCP token (the Emulator does not support passwords):

   ```bash
   printf 'my_agent:' | base64
   ```

1. For the Emulator, you will use `http://localhost:6876` as the `<baseURL>`
   portion of the MCP URL:

   ```
   <baseURL>/api/mcp/agent
   ```

### Step 2. Configure your MCP client

> **Warning:** When saving your credentials or other sensitive information in a config file, do
> **not** commit these files to version control or share them publicly.

**Claude Code:**

1. Add the `materialize-agent` MCP server as [local-scoped
   server](https://code.claude.com/docs/en/mcp#local-scope) (i.e., the
   configurations are stored in `~/.claude.json`):

   ```sh
   claude mcp add --transport http "materialize-agent" \
     "<baseURL>/api/mcp/agent" \
     --header "Authorization: Basic <mcp-token>"
   ```

   Update the `<baseURL>` and `<mcp-token>` placeholders with your values:

   | Deployment   |  `<baseURL>`                                                     |  `<mcp-token>`              |
   |--------------| ------------------------------------------------------------------| -------------------------------|
   | **Cloud**        | Replace with your value (format: `https://<region-id>.materialize.cloud`)  | Replace with your value       |
   | **Self-Managed** | Replace with your value (format: `http://<host>:6876`) | Replace with your value       |
   | **Emulator**     | `http://localhost:6876` | Replace with your value |

   > **Tip:** For **Cloud**, you can get the full MCP URL directly from the Console's
   > **Connect** modal.

1. Restart Claude Code to pick up the new setting.

**Claude Desktop:**

1. Add the `materialize-agent` MCP server entry to your Claude Desktop
   configuration (`claude_desktop_config.json`).
   - When merging into an existing `mcpServers` object, remember to add commas
     between entries.
   - If the `mcpServers` field does not already exist, add it as well.
   - For older Claude Desktop versions, you may need to include the transport
     `"type": "http",` as well as part of the `materialize-agent` entry.

   ```json {hl_lines="3-8"}
   {
     "mcpServers": {
       "materialize-agent": {
         "url": "<baseURL>/api/mcp/agent",
         "headers": {
           "Authorization": "Basic <mcp-token>"
         }
       }
     }
   }
   ```

   Update the `<baseURL>` and `<mcp-token>` placeholders with your values:

   | Deployment   |  `<baseURL>`                                                     |  `<mcp-token>`              |
   |--------------| ------------------------------------------------------------------| -------------------------------|
   | **Cloud**        | Replace with your value (format: `https://<region-id>.materialize.cloud`)  | Replace with your value       |
   | **Self-Managed** | Replace with your value (format: `http://<host>:6876`) | Replace with your value       |
   | **Emulator**     | `http://localhost:6876` | Replace with your value |

   > **Tip:** For **Cloud**, you can get the full MCP URL directly from the Console's
   > **Connect** modal.

1. Restart Claude Desktop to pick up the new setting.

**Cursor:**

1. Add the `materialize-agent` MCP server entry to your local MCP settings
   file (`~/.cursor/mcp.json`).
   - When merging into an existing `mcpServers` object, remember to add commas
     between entries.
   - If the `mcpServers` field does not already exist, add it as well.

   ```json {hl_lines="3-8"}
   {
     "mcpServers": {
       "materialize-agent": {
         "url": "<baseURL>/api/mcp/agent",
         "headers": {
           "Authorization": "Basic <mcp-token>"
         }
       }
     }
   }
   ```

   Update the `<baseURL>` and `<mcp-token>` placeholders with your values:

   | Deployment   |  `<baseURL>`                                                     |  `<mcp-token>`              |
   |--------------| ------------------------------------------------------------------| -------------------------------|
   | **Cloud**        | Replace with your value (format: `https://<region-id>.materialize.cloud`)  | Replace with your value       |
   | **Self-Managed** | Replace with your value (format: `http://<host>:6876`) | Replace with your value       |
   | **Emulator**     | `http://localhost:6876` | Replace with your value |

   > **Tip:** For **Cloud**, you can get the full MCP URL directly from the Console's
   > **Connect** modal.

1. Restart Cursor to pick up the new setting.

**Generic HTTP:**

Any MCP-compatible client can connect by sending JSON-RPC 2.0 requests; update
the `<baseURL>` and `<mcp-token>` placeholders with your values:

```bash
curl -X POST <baseURL>/api/mcp/agent \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic <mcp-token>" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list"
  }'
```

## Start querying

Once connected to the MCP server, you can query your curated data products using
either natural language or SQL:

- *Via `materialize-agent`: What data products can I query?*
- *SELECT * FROM mcp_product_performance LIMIT 5;*
- *What's the `total_revenue` for product 42?*
- *Perform a Pareto analysis on my products.*

> **Warning:** By default, the [`query` tool](/integrations/mcp-server/mcp-agent-tools/#query)
> is **enabled**. This tool allows arbitrary `SELECT` queries (including joins) on
> **all** objects for which the agent has the appropriate privileges (`SELECT` on
> the object, `USAGE` on the object's schema).
> To disable it, set
> [`enable_mcp_agent_query_tool`](/integrations/mcp-server/mcp-agent-config/#enable_mcp_agent_query_tool)
> to `false`. See [Agent endpoint
> configuration](/integrations/mcp-server/mcp-agent-config/).

## Related pages

- [`materialize-agent` MCP Server available
  tools](/integrations/mcp-server/mcp-agent-tools/)
- [`materialize-agent` MCP Server
  configuration](/integrations/mcp-server/mcp-agent-config/)
- [Agent Skills](/integrations/coding-agent-skills/)
- [CREATE INDEX](/sql/create-index)
- [COMMENT ON](/sql/comment-on)
- [CREATE ROLE](/sql/create-role)
- [GRANT PRIVILEGE](/sql/grant-privilege)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)

---

## MCP Server for Developers

> **Public Preview:** This feature is in public preview.

Materialize provides a built-in `materialize-developer` Model Context Protocol
(MCP) server (`/api/mcp/developer`, port 6876) for troubleshooting and
observability. The server is provided directly by Materialize; no sidecar
process or external server is required.

## Overview

The `materialize-developer` MCP server provides read-only access to the system
catalog (`mz_*` tables). You can connect an MCP-compatible client (such as
Claude Code, Claude Desktop, or Cursor) to the MCP server and ask natural
language questions like:

- *Why is my materialized view stale?*
- *How much memory is my cluster using?*

## Connect to the MCP server

### Step 1. Get connection details

When connecting to the MCP server, the MCP-compatible client needs:

- The Base64-encoded `user:password` credentials (i.e., the MCP token).

- The `materialize-developer` MCP server URL: `<baseURL>/api/mcp/developer`.

**Cloud:**

1. Log in to the [Materialize Console](https://console.materialize.com/).
1. Click the **Connect** link (lower-left corner) to open the **Connect** modal
   and click on the **MCP Server** tab.

   ![Image of MCP tab in the Console's Connect
   modal](/images/console/console-connect-mcp.png "Materialize Connect modal,
   MCP Server tab")

1. To get your base64-encoded token:
   - If you want to create a new personal app password to use, click on the
     **Generate personal MCP token** to generate a new personal app token for
     the MCP Server. **Copy the token** as you will use the token to connect.
     Once you navigate away, the token will not display again.

   - If using an existing personal app password, manually generate the
     base64-encoded token.

     ```bash
     printf '<user>:<app_password>' | base64 -w0
     ```

1. In the **Connect your client** section, click on the **Developer** tab.

   You can find your `materialize-developer` MCP server URL
   `<baseURL>/api/mcp/developer` as part of the code block.

   If using Claude Code as your MCP-compatible client, you can copy the code
   block wholesale for the next step.

**Self-Managed:**

1. You can connect using either an existing or new login role with password.

   - To use an existing login role with password, go to the next step.
   - To create a new login role with password:

     ```mzsql
     CREATE ROLE my_dev_agent LOGIN PASSWORD '<your_app_password>';
     ```

1. Encode your role's credentials `<role>:<password>` in Base64 to create the
   MCP token, replacing `<your_app_password>` with the actual password:

   ```bash
   printf 'my_dev_agent:<your_app_password>' | base64
   ```

1. Find your deployment's host name to determine your `materialize-developer`
   MCP URL:

   ```
   http://<host>:6876/api/mcp/developer
   ```

   - For your Self-Managed Materialize deployment in AWS/GCP/Azure, the `<host>`
     is the load balancer address. If [deployed
     viaTerraform](/self-managed-deployments/installation/#install-using-terraform-modules),run
     the Terraform output command for your cloud provider:

     ```bash
     # AWS
     terraform output -raw nlb_dns_name

     # GCP
     terraform output -raw balancerd_load_balancer_ip

     # Azure
     terraform output -raw balancerd_load_balancer_ip
     ```

   - For local
     [kind](/self-managed-deployments/installation/install-on-local-kind/)
     clusters, use port forwarding and use `localhost` for `<host>`:

     ```bash
     kubectl port-forward svc/<instance-name>-balancerd 6876:6876 -n materialize-environment
     ```

**Emulator:**

To connect to the MCP server for your Emulator, you can create a role for your
specific AI agent or use the default `materialize` user:

1. You can create a role for your specific AI agent (the Emulator does not
   support the `LOGIN PASSWORD` option):

   ```mzsql
   CREATE ROLE my_dev_agent;
   ```

1. Encode your agent role's credentials `<role>:<password>` in Base64 to create
   the MCP token (the Emulator does not support passwords):

   ```bash
   printf 'my_dev_agent:' | base64
   ```

1. For the Emulator, you will use `http://localhost:6876` as the `<baseURL>`
   portion of the MCP URL:

   ```
   <baseURL>/api/mcp/developer
   ```

### Step 2. Configure your MCP client

> **Warning:** When saving your credentials or other sensitive information in a config file, do
> **not** commit these files to version control or share them publicly.

**Claude Code:**

1. Add the `materialize-developer` MCP server as [local-scoped
   server](https://code.claude.com/docs/en/mcp#local-scope) (i.e., the
   configurations are stored in `~/.claude.json`):

   ```sh
   claude mcp add --transport http materialize-developer \
     <baseURL>/api/mcp/developer \
     --header "Authorization: Basic <mcp-token>"
   ```

   Update the `<baseURL>` and `<mcp-token>` placeholders with your values:

   | Deployment   |  `<baseURL>`                                                     |  `<mcp-token>`              |
   |--------------| ------------------------------------------------------------------| -------------------------------|
   | **Cloud**        | Replace with your value (format: `https://<region-id>.materialize.cloud`)  | Replace with your value       |
   | **Self-Managed** | Replace with your value (format: `http://<host>:6876`) | Replace with your value       |
   | **Emulator**     | `http://localhost:6876` | Replace with your value |

   > **Tip:** For **Cloud**, you can get the full MCP URL directly from the Console's
   > **Connect** modal.

1. Restart Claude Code to pick up the new setting.

**Claude Desktop:**

1. Add the `materialize-developer` MCP server entry to your Claude Desktop
   configuration (`claude_desktop_config.json`).
   - When merging into an existing `mcpServers` object, remember to add commas
     between entries.
   - If the `mcpServers` field does not already exist, add it as well.
   - For older Claude Desktop versions, you may need to include the transport
     `"type": "http",` as well as part of the `materialize-developer` entry.

   ```json {hl_lines="3-8"}
   {
     "mcpServers": {
       "materialize-developer": {
         "url": "<baseURL>/api/mcp/developer",
         "headers": {
           "Authorization": "Basic <mcp-token>"
         }
       }
     }
   }
   ```

   Update the `<baseURL>` and `<mcp-token>` placeholders with your values:

   | Deployment   |  `<baseURL>`                                                     |  `<mcp-token>`              |
   |--------------| ------------------------------------------------------------------| -------------------------------|
   | **Cloud**        | Replace with your value (format: `https://<region-id>.materialize.cloud`)  | Replace with your value       |
   | **Self-Managed** | Replace with your value (format: `http://<host>:6876`) | Replace with your value       |
   | **Emulator**     | `http://localhost:6876` | Replace with your value |

   > **Tip:** For **Cloud**, you can get the full MCP URL directly from the Console's
   > **Connect** modal.

1. Restart Claude Desktop to pick up the new setting.

**Cursor:**

1. Add the `materialize-developer` MCP server entry to your local MCP settings
   file (`~/.cursor/mcp.json`).
   - When merging into an existing `mcpServers` object, remember to add commas
     between entries.
   - If the `mcpServers` field does not already exist, add it as well.

   ```json {hl_lines="3-8"}
   {
     "mcpServers": {
       "materialize-developer": {
         "url": "<baseURL>/api/mcp/developer",
         "headers": {
           "Authorization": "Basic <mcp-token>"
         }
       }
     }
   }
   ```

   Update the `<baseURL>` and `<mcp-token>` placeholders with your values:

   | Deployment   |  `<baseURL>`                                                     |  `<mcp-token>`              |
   |--------------| ------------------------------------------------------------------| -------------------------------|
   | **Cloud**        | Replace with your value (format: `https://<region-id>.materialize.cloud`)  | Replace with your value       |
   | **Self-Managed** | Replace with your value (format: `http://<host>:6876`) | Replace with your value       |
   | **Emulator**     | `http://localhost:6876` | Replace with your value |

   > **Tip:** For **Cloud**, you can get the full MCP URL directly from the Console's
   > **Connect** modal.

1. Restart Cursor to pick up the new setting.

**Generic HTTP:**

Any MCP-compatible client can connect by sending JSON-RPC 2.0 requests; update
the `<baseURL>` and `<mcp-token>` placeholders with your values:

```bash
curl -X POST <baseURL>/api/mcp/developer \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic <mcp-token>" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list"
  }'
```

## Start asking questions

Once connected to the MCP server, you can ask natural language questions like:

| Question | What the agent does |
|----------|---------------------|
| **Why is my materialized view stale?** | Checks materialization lag, hydration status, replica health, and source errors. |
| **Why is my cluster running out of memory?** | Checks replica utilization, identifies the largest dataflows, and finds optimization opportunities via the built-in index advisor. |
| **Has my source finished snapshotting yet?** | Checks source statistics and status. |
| **How much memory is my cluster using?** | Checks replica utilization metrics across all clusters. |
| **What's the health of my environment?** | Checks replica statuses, source and sink health, and resource utilization. |
| **What can I optimize to save costs?** | Queries the index advisor for materialized views that can be dematerialized and indexes that can be dropped. |

The agent translates natural language questions into the appropriate system
catalog queries, uses the [`query_system_catalog`
tool](/integrations/mcp-server/mcp-developer-tools/#query_system_catalog) to run
those queries, and synthesizes the results.

## Privileges

The privileges required to use the `materialize-developer` MCP server are:

* `USAGE` on system catalog schemas and `SELECT` on system catalog objects.
  These privileges are granted by default.

* If agents also need access to replica-specific metrics from
  `mz_introspection`, `USAGE` privileges on the corresponding cluster.

## Related pages

- [`materialize-developer` MCP Server available
  tools](/integrations/mcp-server/mcp-developer-tools/)
- [`materialize-developer` MCP Server
  configuration](/integrations/mcp-server/mcp-developer-config/)
- [Troubleshooting](/integrations/mcp-server/mcp-server-troubleshooting/)
- [Agent Skills](/integrations/coding-agent-skills/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)

---

## MCP Server Troubleshooting

## `unable to verify the first certificate`

**Symptom:** Your MCP client (Claude Code, Cursor, etc.) returns an error like:

```
Error: SDK auth failed: unable to verify the first certificate
```

**Cause:** This error has two common causes:

1. **Wrong protocol:** You're using `http://` but your deployment has TLS
   enabled. Switch to `https://` in your MCP configuration.
2. **Self-signed certificate:** Your Materialize deployment uses a self-signed
   TLS certificate, which is the default for
   [self-managed installations](/self-managed-deployments/). MCP clients built
   on Node.js (including Claude Code) reject self-signed certificates by
   default.

**First, check your URL** — if you're using `http://`, try changing to
`https://`. If that resolves the error, update your MCP configuration.

**Fix:**

For **Claude Code**, start with TLS verification disabled:

```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 claude
```

For **Cursor** or other Node.js-based clients, set the same environment variable
before launching:

```bash
export NODE_TLS_REJECT_UNAUTHORIZED=0
```

Alternatively, configure your deployment with a certificate from a trusted CA
(e.g., [Let's Encrypt](https://letsencrypt.org/)) to avoid this issue entirely.

## `HTTP 503 Service Unavailable`

**Symptom:** Requests to the MCP endpoint return HTTP 503.

**Cause:** The MCP endpoint is disabled.

**Fix:** Enable the endpoint. See
- [Developer endpoint
  configuration](/integrations/mcp-server/mcp-developer-config/)
- [Agents endpoint
  configuration](/integrations/mcp-server/mcp-developer-config/)

## `HTTP 401 Unauthorized`

**Symptom:** Requests return HTTP 401.

**Cause:** Invalid or missing credentials. The Base64 token may be incorrectly
encoded, or the user/password may be wrong.

**Fix:** Re-encode your credentials and verify:

```bash
# Encode
printf '<user>:<password>' | base64

# Verify by decoding
echo '<your-base64-token>' | base64 --decode
```

Make sure the decoded output matches `user:password` exactly.

