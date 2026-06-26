# Agent endpoint configuration
Configuration for /api/mcp/agent endpoint.
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

