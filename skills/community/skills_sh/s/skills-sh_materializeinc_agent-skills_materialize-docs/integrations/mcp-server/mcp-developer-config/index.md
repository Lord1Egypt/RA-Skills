# Developer endpoint configuration
Configuration for /api/mcp/developer endpoint.
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

