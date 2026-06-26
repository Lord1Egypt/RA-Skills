# Dokploy MCP Server — 449 Tools Reference

Official MCP server: `@sattva/dokploy-mcp` (repo: [sattva2020/dokploy-mcp](https://github.com/sattva2020/dokploy-mcp))

In Claude Code, tools are named `mcp__dokploy__<category>_<method>` (e.g., `mcp__dokploy__application_deploy`).

## Setup

### Claude Code (`~/.claude/mcp.json`)

```json
{
  "mcpServers": {
    "dokploy": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@sattva/dokploy-mcp"],
      "env": {
        "DOKPLOY_URL": "https://dokploy.example.com/api",
        "DOKPLOY_API_KEY": "<your-token>"
      }
    }
  }
}
```

**Windows:** use `"command": "cmd", "args": ["/c", "npx", "-y", "@sattva/dokploy-mcp"]`
**macOS/Linux:** use `"command": "npx", "args": ["-y", "@sattva/dokploy-mcp"]`
**Local dev:** use `"command": "node", "args": ["e:/My/MCP/dokploy-mcp/dist/index.js"]`

### Transport Modes

- **stdio** (default) — for CLI and desktop apps
- **HTTP** — Streamable HTTP (MCP 2025-03-26) + Legacy SSE (MCP 2024-11-05)

## Tool Annotations

All tools have semantic annotations:

| Annotation | Meaning |
|------------|---------|
| `readOnlyHint: true` | Safe read operation, no side effects |
| `destructiveHint: true` | Modifies or deletes resources |
| `destructiveHint: false` | Creates new resources |
| `idempotentHint: true` | Safe to repeat |
| `openWorldHint: true` | Calls external Dokploy API |

## When to Use MCP vs curl

| Scenario | Use MCP | Use curl/API |
|----------|---------|--------------|
| AI agent managing deployments | Yes | — |
| Claude Code interactive session | Yes | Fallback |
| CI/CD pipeline scripts | — | Yes |
| Automation without AI | — | Yes |
| Complex multi-step workflows | Yes | — |

**MCP advantages:** No need to construct tRPC URLs, handle URL encoding, or parse nested response wrappers. The MCP tools handle all of this internally.

---

## Admin (1 tool)

| Tool | Description |
|------|-------------|
| `admin_setupMonitoring` | Set up monitoring for the Dokploy instance |

## AI — Docker Compose Generator (9 tools)

| Tool | Description |
|------|-------------|
| `ai_create` | Create a new AI-generated Docker Compose configuration |
| `ai_delete` | Delete an AI compose configuration |
| `ai_deploy` | Deploy an AI-generated compose |
| `ai_get` | Get AI compose configuration |
| `ai_getAll` | List all AI compose configurations |
| `ai_getModels` | List available AI models |
| `ai_one` | Get a single AI compose by ID |
| `ai_suggest` | Get AI suggestions for compose configuration |
| `ai_update` | Update an AI compose configuration |

## Project Management (8 tools)

| Tool | Description |
|------|-------------|
| `project_all` | List all projects |
| `project_allForPermissions` | List projects with permission info |
| `project_create` | Create a new project |
| `project_duplicate` | Clone an existing project |
| `project_one` | Get project by ID |
| `project_remove` | Delete a project |
| `project_search` | Search projects by name |
| `project_update` | Update project details |

## Environment Management (7 tools)

| Tool | Description |
|------|-------------|
| `environment_byProjectId` | List environments for a project |
| `environment_create` | Create a new environment |
| `environment_duplicate` | Duplicate an environment |
| `environment_one` | Get environment by ID |
| `environment_remove` | Delete an environment |
| `environment_search` | Search environments |
| `environment_update` | Update an environment |

## Application Management (29 tools)

| Tool | Description |
|------|-------------|
| `application_cancelDeployment` | Cancel an active deployment |
| `application_cleanQueues` | Clear deployment queues |
| `application_clearDeployments` | Clear deployment history |
| `application_create` | Create a new application |
| `application_delete` | Delete an application |
| `application_deploy` | Trigger a deployment |
| `application_disconnectGitProvider` | Remove git provider connection |
| `application_killBuild` | Kill a running build |
| `application_markRunning` | Manually set app status to running |
| `application_move` | Move app to another project |
| `application_one` | Get application details and status |
| `application_readAppMonitoring` | Read application monitoring metrics |
| `application_readTraefikConfig` | Read Traefik routing config |
| `application_redeploy` | Force a redeployment |
| `application_refreshToken` | Regenerate webhook token |
| `application_reload` | Reload app configuration |
| `application_saveBitbucketProvider` | Connect Bitbucket as source |
| `application_saveBuildType` | Set build method (dockerfile, nixpacks, etc.) |
| `application_saveDockerProvider` | Set Docker image as source |
| `application_saveEnvironment` | Set environment variables |
| `application_saveGitProvider` | Connect generic git URL |
| `application_saveGiteaProvider` | Connect Gitea as source |
| `application_saveGithubProvider` | Connect GitHub as source |
| `application_saveGitlabProvider` | Connect GitLab as source |
| `application_search` | Search applications |
| `application_start` | Start a stopped application |
| `application_stop` | Stop a running application |
| `application_update` | Update application configuration |
| `application_updateTraefikConfig` | Modify Traefik routing rules |

## Docker Compose (28 tools)

| Tool | Description |
|------|-------------|
| `compose_cancelDeployment` | Cancel an active compose deployment |
| `compose_cleanQueues` | Clear compose deployment queues |
| `compose_clearDeployments` | Clear compose deployment history |
| `compose_create` | Create a new compose service |
| `compose_delete` | Delete a compose service |
| `compose_deploy` | Deploy a compose service |
| `compose_deployTemplate` | Deploy from a template |
| `compose_disconnectGitProvider` | Remove git provider from compose |
| `compose_fetchSourceType` | Get the source type of a compose |
| `compose_getConvertedCompose` | Get converted compose file |
| `compose_getDefaultCommand` | Get default docker compose command |
| `compose_getTags` | Get available tags |
| `compose_import` | Import a compose configuration |
| `compose_isolatedDeployment` | Deploy in isolated mode |
| `compose_killBuild` | Kill a running compose build |
| `compose_loadMountsByService` | List mounts for a compose service |
| `compose_loadServices` | List services in a compose |
| `compose_move` | Move compose to another project |
| `compose_one` | Get compose details by ID |
| `compose_processTemplate` | Process a compose template |
| `compose_randomizeCompose` | Randomize compose configuration |
| `compose_redeploy` | Force redeploy a compose |
| `compose_refreshToken` | Regenerate compose webhook token |
| `compose_search` | Search compose services |
| `compose_start` | Start a compose service |
| `compose_stop` | Stop a compose service |
| `compose_templates` | List available compose templates |
| `compose_update` | Update compose configuration |

## Deployment (8 tools)

| Tool | Description |
|------|-------------|
| `deployment_all` | List all deployments for an application |
| `deployment_allByCompose` | List deployments for a compose service |
| `deployment_allByServer` | List deployments for a server |
| `deployment_allByType` | List deployments filtered by type |
| `deployment_allCentralized` | List all deployments centralized |
| `deployment_killProcess` | Kill a running deployment process |
| `deployment_queueList` | List queued deployments |
| `deployment_removeDeployment` | Remove a deployment record |

## Preview Deployments (4 tools)

| Tool | Description |
|------|-------------|
| `previewDeployment_all` | List all preview deployments |
| `previewDeployment_delete` | Delete a preview deployment |
| `previewDeployment_one` | Get preview deployment details |
| `previewDeployment_redeploy` | Redeploy a preview deployment |

## Rollback (2 tools)

| Tool | Description |
|------|-------------|
| `rollback_delete` | Delete a rollback entry |
| `rollback_rollback` | Rollback to a previous deployment |

## Domain Management (9 tools)

| Tool | Description |
|------|-------------|
| `domain_byApplicationId` | List domains for an application |
| `domain_byComposeId` | List domains for a compose service |
| `domain_canGenerateTraefikMeDomains` | Check traefik.me domain support |
| `domain_create` | Create a new domain mapping |
| `domain_delete` | Remove a domain |
| `domain_generateDomain` | Auto-generate a subdomain |
| `domain_one` | Get domain details |
| `domain_update` | Update domain configuration |
| `domain_validateDomain` | Validate DNS for a domain |

## Port Management (4 tools)

| Tool | Description |
|------|-------------|
| `port_create` | Create a port mapping |
| `port_delete` | Delete a port mapping |
| `port_one` | Get port mapping details |
| `port_update` | Update a port mapping |

## Redirects (4 tools)

| Tool | Description |
|------|-------------|
| `redirects_create` | Create a redirect rule |
| `redirects_delete` | Delete a redirect rule |
| `redirects_one` | Get redirect details |
| `redirects_update` | Update a redirect rule |

## Security (4 tools)

| Tool | Description |
|------|-------------|
| `security_create` | Create a security rule (basic auth, etc.) |
| `security_delete` | Delete a security rule |
| `security_one` | Get security rule details |
| `security_update` | Update a security rule |

## Mounts (6 tools)

| Tool | Description |
|------|-------------|
| `mounts_allNamedByApplicationId` | List named mounts for an application |
| `mounts_create` | Create a mount/volume |
| `mounts_listByServiceId` | List mounts for a service |
| `mounts_one` | Get mount details |
| `mounts_remove` | Remove a mount |
| `mounts_update` | Update a mount |

---

## Databases (70 tools — 5 categories x 14 tools each)

All five database categories (PostgreSQL, MySQL, MariaDB, MongoDB, Redis) share the same 14-tool pattern. The tool prefix and ID parameter change per database type.

| Prefix | ID Parameter |
|--------|-------------|
| `postgres_` | `postgresId` |
| `mysql_` | `mysqlId` |
| `mariadb_` | `mariadbId` |
| `mongo_` | `mongoId` |
| `redis_` | `redisId` |

### Shared tool pattern (shown for `postgres_`, identical for all five)

| Tool | Description |
|------|-------------|
| `postgres_changeStatus` | Set database status |
| `postgres_create` | Create a new database instance |
| `postgres_deploy` | Deploy the database |
| `postgres_move` | Move to another project |
| `postgres_one` | Get database details |
| `postgres_rebuild` | Rebuild the database container |
| `postgres_reload` | Reload database configuration |
| `postgres_remove` | Delete the database |
| `postgres_saveEnvironment` | Set environment variables |
| `postgres_saveExternalPort` | Set external port |
| `postgres_search` | Search databases |
| `postgres_start` | Start the database |
| `postgres_stop` | Stop the database |
| `postgres_update` | Update database configuration |

---

## Backup (11 tools)

| Tool | Description |
|------|-------------|
| `backup_create` | Create a backup configuration |
| `backup_listBackupFiles` | List available backup files |
| `backup_manualBackupCompose` | Manually backup a compose service |
| `backup_manualBackupMariadb` | Manually backup MariaDB |
| `backup_manualBackupMongo` | Manually backup MongoDB |
| `backup_manualBackupMySql` | Manually backup MySQL |
| `backup_manualBackupPostgres` | Manually backup PostgreSQL |
| `backup_manualBackupWebServer` | Manually backup a web server |
| `backup_one` | Get backup details |
| `backup_remove` | Delete a backup configuration |
| `backup_update` | Update a backup configuration |

## Volume Backups (6 tools)

| Tool | Description |
|------|-------------|
| `volumeBackups_create` | Create a volume backup configuration |
| `volumeBackups_delete` | Delete a volume backup |
| `volumeBackups_list` | List volume backups |
| `volumeBackups_one` | Get volume backup details |
| `volumeBackups_runManually` | Trigger a manual volume backup |
| `volumeBackups_update` | Update volume backup configuration |

## Scheduled Tasks (6 tools)

| Tool | Description |
|------|-------------|
| `schedule_create` | Create a scheduled task |
| `schedule_delete` | Delete a scheduled task |
| `schedule_list` | List scheduled tasks |
| `schedule_one` | Get scheduled task details |
| `schedule_runManually` | Trigger a scheduled task manually |
| `schedule_update` | Update a scheduled task |

## Destination (S3/Storage) (6 tools)

| Tool | Description |
|------|-------------|
| `destination_all` | List all backup destinations |
| `destination_create` | Create a new destination |
| `destination_one` | Get destination details |
| `destination_remove` | Delete a destination |
| `destination_testConnection` | Test destination connectivity |
| `destination_update` | Update a destination |

---

## Git Providers (30 tools)

### General (2 tools)

| Tool | Description |
|------|-------------|
| `gitProvider_getAll` | List all configured git providers |
| `gitProvider_remove` | Remove a git provider |

### GitHub (6 tools)

| Tool | Description |
|------|-------------|
| `github_getGithubBranches` | List branches for a GitHub repo |
| `github_getGithubRepositories` | List GitHub repositories |
| `github_githubProviders` | List GitHub provider configurations |
| `github_one` | Get GitHub provider details |
| `github_testConnection` | Test GitHub connection |
| `github_update` | Update GitHub provider |

### GitLab (7 tools)

| Tool | Description |
|------|-------------|
| `gitlab_create` | Create a GitLab provider |
| `gitlab_getGitlabBranches` | List branches for a GitLab repo |
| `gitlab_getGitlabRepositories` | List GitLab repositories |
| `gitlab_gitlabProviders` | List GitLab provider configurations |
| `gitlab_one` | Get GitLab provider details |
| `gitlab_testConnection` | Test GitLab connection |
| `gitlab_update` | Update GitLab provider |

### Bitbucket (7 tools)

| Tool | Description |
|------|-------------|
| `bitbucket_bitbucketProviders` | List Bitbucket provider configurations |
| `bitbucket_create` | Create a Bitbucket provider |
| `bitbucket_getBitbucketBranches` | List branches for a Bitbucket repo |
| `bitbucket_getBitbucketRepositories` | List Bitbucket repositories |
| `bitbucket_one` | Get Bitbucket provider details |
| `bitbucket_testConnection` | Test Bitbucket connection |
| `bitbucket_update` | Update Bitbucket provider |

### Gitea (8 tools)

| Tool | Description |
|------|-------------|
| `gitea_create` | Create a Gitea provider |
| `gitea_getGiteaBranches` | List branches for a Gitea repo |
| `gitea_getGiteaRepositories` | List Gitea repositories |
| `gitea_getGiteaUrl` | Get configured Gitea URL |
| `gitea_giteaProviders` | List Gitea provider configurations |
| `gitea_one` | Get Gitea provider details |
| `gitea_testConnection` | Test Gitea connection |
| `gitea_update` | Update Gitea provider |

---

## Docker (7 tools)

| Tool | Description |
|------|-------------|
| `docker_getConfig` | Get Docker daemon configuration |
| `docker_getContainers` | List all Docker containers |
| `docker_getContainersByAppLabel` | Get containers by application label |
| `docker_getContainersByAppNameMatch` | Get containers matching app name |
| `docker_getServiceContainersByAppName` | Get service containers by app name |
| `docker_getStackContainersByAppName` | Get stack containers by app name |
| `docker_restartContainer` | Restart a Docker container |

## Registry (7 tools)

| Tool | Description |
|------|-------------|
| `registry_all` | List all registries |
| `registry_create` | Add a Docker registry |
| `registry_one` | Get registry details |
| `registry_remove` | Remove a registry |
| `registry_testRegistry` | Test registry connection |
| `registry_testRegistryById` | Test registry by ID |
| `registry_update` | Update registry configuration |

## Certificates (4 tools)

| Tool | Description |
|------|-------------|
| `certificates_all` | List all SSL certificates |
| `certificates_create` | Create/import a certificate |
| `certificates_one` | Get certificate details |
| `certificates_remove` | Remove a certificate |

---

## Server Management (16 tools)

| Tool | Description |
|------|-------------|
| `server_all` | List all servers |
| `server_buildServers` | List servers available for builds |
| `server_count` | Get server count |
| `server_create` | Register a new server |
| `server_getDefaultCommand` | Get default server setup command |
| `server_getServerMetrics` | Get server resource metrics |
| `server_getServerTime` | Get server time |
| `server_one` | Get server details |
| `server_publicIp` | Get server public IP |
| `server_remove` | Remove a server |
| `server_security` | Get server security info |
| `server_setup` | Run server setup |
| `server_setupMonitoring` | Set up server monitoring |
| `server_update` | Update server configuration |
| `server_validate` | Validate server connection |
| `server_withSSHKey` | Get server with SSH key |

## Cluster & Swarm (7 tools)

### Cluster (4 tools)

| Tool | Description |
|------|-------------|
| `cluster_addManager` | Add a manager node |
| `cluster_addWorker` | Add a worker node |
| `cluster_getNodes` | List cluster nodes |
| `cluster_removeWorker` | Remove a worker node |

### Swarm (3 tools)

| Tool | Description |
|------|-------------|
| `swarm_getNodeApps` | List applications on a swarm node |
| `swarm_getNodeInfo` | Get swarm node information |
| `swarm_getNodes` | List swarm nodes |

## SSH Keys (6 tools)

| Tool | Description |
|------|-------------|
| `sshKey_all` | List all SSH keys |
| `sshKey_create` | Create/import an SSH key |
| `sshKey_generate` | Generate a new SSH key pair |
| `sshKey_one` | Get SSH key details |
| `sshKey_remove` | Remove an SSH key |
| `sshKey_update` | Update SSH key configuration |

---

## Notification (38 tools)

Supports 11 notification providers: Custom, Discord, Email, Gotify, Lark, Ntfy, Pushover, Resend, Slack, Teams, Telegram.

Each provider has `create`, `update`, and `testConnection` tools.

| Tool | Description |
|------|-------------|
| `notification_all` | List all notification configurations |
| `notification_one` | Get notification details |
| `notification_receiveNotification` | Handle incoming notification |
| `notification_remove` | Remove a notification configuration |
| `notification_getEmailProviders` | List available email providers |
| `notification_createCustom` | Create custom webhook notification |
| `notification_createDiscord` | Create Discord notification |
| `notification_createEmail` | Create email notification |
| `notification_createGotify` | Create Gotify notification |
| `notification_createLark` | Create Lark notification |
| `notification_createNtfy` | Create Ntfy notification |
| `notification_createPushover` | Create Pushover notification |
| `notification_createResend` | Create Resend notification |
| `notification_createSlack` | Create Slack notification |
| `notification_createTeams` | Create Microsoft Teams notification |
| `notification_createTelegram` | Create Telegram notification |
| `notification_updateCustom` | Update custom webhook notification |
| `notification_updateDiscord` | Update Discord notification |
| `notification_updateEmail` | Update email notification |
| `notification_updateGotify` | Update Gotify notification |
| `notification_updateLark` | Update Lark notification |
| `notification_updateNtfy` | Update Ntfy notification |
| `notification_updatePushover` | Update Pushover notification |
| `notification_updateResend` | Update Resend notification |
| `notification_updateSlack` | Update Slack notification |
| `notification_updateTeams` | Update Microsoft Teams notification |
| `notification_updateTelegram` | Update Telegram notification |
| `notification_testCustomConnection` | Test custom webhook connection |
| `notification_testDiscordConnection` | Test Discord connection |
| `notification_testEmailConnection` | Test email connection |
| `notification_testGotifyConnection` | Test Gotify connection |
| `notification_testLarkConnection` | Test Lark connection |
| `notification_testNtfyConnection` | Test Ntfy connection |
| `notification_testPushoverConnection` | Test Pushover connection |
| `notification_testResendConnection` | Test Resend connection |
| `notification_testSlackConnection` | Test Slack connection |
| `notification_testTeamsConnection` | Test Teams connection |
| `notification_testTelegramConnection` | Test Telegram connection |

---

## Patch Management (12 tools)

| Tool | Description |
|------|-------------|
| `patch_byEntityId` | List patches for an entity |
| `patch_cleanPatchRepos` | Clean up patch repositories |
| `patch_create` | Create a new patch |
| `patch_delete` | Delete a patch |
| `patch_ensureRepo` | Ensure patch repo exists |
| `patch_markFileForDeletion` | Mark a file for deletion in patch |
| `patch_one` | Get patch details |
| `patch_readRepoDirectories` | List directories in patch repo |
| `patch_readRepoFile` | Read a file from patch repo |
| `patch_saveFileAsPatch` | Save a file as a patch |
| `patch_toggleEnabled` | Enable/disable a patch |
| `patch_update` | Update a patch |

---

## Organization (10 tools)

| Tool | Description |
|------|-------------|
| `organization_active` | Get the active organization |
| `organization_all` | List all organizations |
| `organization_allInvitations` | List all invitations |
| `organization_create` | Create a new organization |
| `organization_delete` | Delete an organization |
| `organization_one` | Get organization details |
| `organization_removeInvitation` | Remove an invitation |
| `organization_setDefault` | Set default organization |
| `organization_update` | Update organization details |
| `organization_updateMemberRole` | Update a member's role |

## User Management (18 tools)

| Tool | Description |
|------|-------------|
| `user_all` | List all users |
| `user_assignPermissions` | Assign permissions to a user |
| `user_checkUserOrganizations` | Check user organization membership |
| `user_createApiKey` | Create an API key |
| `user_deleteApiKey` | Delete an API key |
| `user_generateToken` | Generate an auth token |
| `user_get` | Get current user info |
| `user_getBackups` | Get user backups |
| `user_getContainerMetrics` | Get container metrics for user |
| `user_getInvitations` | Get user invitations |
| `user_getMetricsToken` | Get metrics access token |
| `user_getServerMetrics` | Get server metrics for user |
| `user_getUserByToken` | Look up user by token |
| `user_haveRootAccess` | Check if user has root access |
| `user_one` | Get user by ID |
| `user_remove` | Remove a user |
| `user_sendInvitation` | Send an invitation |
| `user_update` | Update user details |

## SSO (10 tools)

| Tool | Description |
|------|-------------|
| `sso_addTrustedOrigin` | Add a trusted origin |
| `sso_deleteProvider` | Delete an SSO provider |
| `sso_getTrustedOrigins` | List trusted origins |
| `sso_listProviders` | List SSO providers |
| `sso_one` | Get SSO provider details |
| `sso_register` | Register a new SSO provider |
| `sso_removeTrustedOrigin` | Remove a trusted origin |
| `sso_showSignInWithSSO` | Check if SSO sign-in is available |
| `sso_update` | Update SSO provider |
| `sso_updateTrustedOrigin` | Update a trusted origin |

## License Key (6 tools)

| Tool | Description |
|------|-------------|
| `licenseKey_activate` | Activate a license key |
| `licenseKey_deactivate` | Deactivate a license key |
| `licenseKey_getEnterpriseSettings` | Get enterprise settings |
| `licenseKey_haveValidLicenseKey` | Check if license is valid |
| `licenseKey_updateEnterpriseSettings` | Update enterprise settings |
| `licenseKey_validate` | Validate a license key |

## Stripe / Billing (7 tools)

| Tool | Description |
|------|-------------|
| `stripe_canCreateMoreServers` | Check server creation limit |
| `stripe_createCheckoutSession` | Create a payment checkout session |
| `stripe_createCustomerPortalSession` | Open customer billing portal |
| `stripe_getCurrentPlan` | Get current subscription plan |
| `stripe_getInvoices` | List invoices |
| `stripe_getProducts` | List available products/plans |
| `stripe_upgradeSubscription` | Upgrade the subscription |

---

## Settings (49 tools)

### System Info

| Tool | Description |
|------|-------------|
| `settings_getDokployVersion` | Get Dokploy version |
| `settings_getReleaseTag` | Get current release tag |
| `settings_getUpdateData` | Get update availability info |
| `settings_getIp` | Get server IP address |
| `settings_getDokployCloudIps` | Get Dokploy Cloud IP addresses |
| `settings_health` | Health check |
| `settings_isCloud` | Check if running on Dokploy Cloud |
| `settings_isUserSubscribed` | Check user subscription status |
| `settings_getOpenApiDocument` | Get OpenAPI specification |

### Server & Traefik Configuration

| Tool | Description |
|------|-------------|
| `settings_assignDomainServer` | Assign a domain to a server |
| `settings_getTraefikPorts` | Get Traefik port configuration |
| `settings_getWebServerSettings` | Get web server settings |
| `settings_haveTraefikDashboardPortEnabled` | Check Traefik dashboard status |
| `settings_readDirectories` | List server directories |
| `settings_readMiddlewareTraefikConfig` | Read Traefik middleware config |
| `settings_readTraefikConfig` | Read main Traefik config |
| `settings_readTraefikEnv` | Read Traefik environment variables |
| `settings_readTraefikFile` | Read a Traefik config file |
| `settings_readWebServerTraefikConfig` | Read web server Traefik config |
| `settings_reloadServer` | Reload server |
| `settings_reloadTraefik` | Reload Traefik |
| `settings_saveSSHPrivateKey` | Save SSH private key |
| `settings_toggleDashboard` | Toggle Traefik dashboard |
| `settings_toggleRequests` | Toggle request handling |
| `settings_updateMiddlewareTraefikConfig` | Update Traefik middleware |
| `settings_updateServer` | Update server settings |
| `settings_updateServerIp` | Update server IP address |
| `settings_updateTraefikConfig` | Update main Traefik config |
| `settings_updateTraefikFile` | Update a Traefik config file |
| `settings_updateTraefikPorts` | Update Traefik ports |
| `settings_updateWebServerTraefikConfig` | Update web server Traefik config |
| `settings_writeTraefikEnv` | Write Traefik environment variables |
| `settings_haveActivateRequests` | Check for pending activation requests |

### Cleanup & Maintenance

| Tool | Description |
|------|-------------|
| `settings_cleanAll` | Run all cleanup tasks |
| `settings_cleanAllDeploymentQueue` | Clear all deployment queues |
| `settings_cleanDockerBuilder` | Clean Docker builder cache |
| `settings_cleanDockerPrune` | Run Docker system prune |
| `settings_cleanMonitoring` | Clean monitoring data |
| `settings_cleanRedis` | Clean Redis cache |
| `settings_cleanSSHPrivateKey` | Remove stored SSH key |
| `settings_cleanStoppedContainers` | Remove stopped containers |
| `settings_cleanUnusedImages` | Remove unused Docker images |
| `settings_cleanUnusedVolumes` | Remove unused Docker volumes |
| `settings_reloadRedis` | Reload Redis |
| `settings_updateDockerCleanup` | Configure Docker auto-cleanup |
| `settings_updateLogCleanup` | Configure log auto-cleanup |
| `settings_getLogCleanupStatus` | Get log cleanup configuration |

### GPU

| Tool | Description |
|------|-------------|
| `settings_checkGPUStatus` | Check GPU availability |
| `settings_setupGPU` | Set up GPU support |

---

## MCP Limitations

Operations the MCP server **cannot** perform (use Dashboard or direct access instead):

| Operation | Reason | Alternative |
|-----------|--------|-------------|
| Read build/container logs | WebSocket streaming only | Dashboard UI |
| Docker exec into container | No API endpoint | SSH to VPS |
