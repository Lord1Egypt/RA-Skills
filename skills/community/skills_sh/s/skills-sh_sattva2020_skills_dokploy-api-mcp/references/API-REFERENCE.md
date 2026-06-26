# Dokploy API Reference

Source: OpenAPI 3.1.0 spec from `settings.getOpenApiDocument` — **449 endpoints** (Dokploy v0.28.4).

## Authentication

All requests require the `x-api-key` header:

```
x-api-key: <your-api-token>
```

Generate token: Dashboard -> Settings -> Profile -> API/CLI -> Generate.
Tokens never expire by default.

## Retrieving the OpenAPI Spec

```bash
curl -s "${DOKPLOY_URL}/api/settings.getOpenApiDocument" \
  -H "x-api-key: ${DOKPLOY_API_KEY}"
```

Returns the full OpenAPI 3.1.0 JSON document with all 449 endpoints.

## Request Formats

Dokploy uses tRPC. Two formats depending on operation type.

### Queries (GET) — Read operations

```bash
curl -s -X GET \
  "${DOKPLOY_URL}/api/trpc/<router>.<procedure>?input=$(python3 -c "
import urllib.parse, json
print(urllib.parse.quote(json.dumps({'json': {<params>}})))
")" \
  -H "x-api-key: ${DOKPLOY_API_KEY}"
```

The `input` query parameter must be URL-encoded JSON with a `{"json": {...}}` wrapper.

### Mutations (POST) — Write operations

```bash
curl -s -X POST "${DOKPLOY_URL}/api/<router>.<procedure>" \
  -H "x-api-key: ${DOKPLOY_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"json": {<params>}}'
```

### Response Format

```json
{
  "result": {
    "data": {
      "json": { ... }
    }
  }
}
```

Extract data: `response.result.data.json`

## Project (8 endpoints)

| Endpoint | Method | Required Params | Optional Params |
|----------|--------|-----------------|-----------------|
| `project.all` | GET | — | — |
| `project.one` | GET | `projectId` | — |
| `project.create` | POST | `name` | `description`, `env` |
| `project.remove` | POST | `projectId` | — |
| `project.update` | POST | `projectId`, fields | — |
| `project.duplicate` | POST | `projectId` | — |
| `project.search` | GET | search params | — |
| `project.allForPermissions` | GET | — | — |

## Application (29 endpoints)

### Core Operations

| Endpoint | Method | Required | Optional |
|----------|--------|----------|----------|
| `application.one` | GET | `applicationId` | — |
| `application.create` | POST | `name`, `environmentId` | `appName`, `description`, `serverId` |
| `application.deploy` | POST | `applicationId` | `title`, `description` |
| `application.redeploy` | POST | `applicationId` | — |
| `application.stop` | POST | `applicationId` | — |
| `application.start` | POST | `applicationId` | — |
| `application.delete` | POST | `applicationId` | — |
| `application.reload` | POST | `applicationId` | — |
| `application.cancelDeployment` | POST | `applicationId` | — |
| `application.killBuild` | POST | `applicationId` | — |
| `application.search` | GET | search params | — |
| `application.move` | POST | `applicationId`, target | — |
| `application.refreshToken` | POST | `applicationId` | — |
| `application.markRunning` | POST | `applicationId` | — |
| `application.cleanQueues` | POST | `applicationId` | — |
| `application.clearDeployments` | POST | `applicationId` | — |
| `application.readAppMonitoring` | GET | `applicationId` | — |

### Configuration

| Endpoint | Method | Required | Optional |
|----------|--------|----------|----------|
| `application.update` | POST | `applicationId` | 80+ fields (see below) |
| `application.saveBuildType` | POST | `applicationId`, `buildType`, `dockerContextPath`, `dockerBuildStage` | `dockerfile`, `herokuVersion`, `publishDirectory`, `isStaticSpa`, `railpackVersion` |
| `application.saveEnvironment` | POST | `applicationId` | `env`, `buildArgs`, `buildSecrets`, `createEnvFile` |
| `application.readTraefikConfig` | GET | `applicationId` | — |
| `application.updateTraefikConfig` | POST | `applicationId`, config | — |

### Git Provider Connections

| Endpoint | Method | Required |
|----------|--------|----------|
| `application.saveGithubProvider` | POST | `applicationId`, provider config |
| `application.saveGitlabProvider` | POST | `applicationId`, provider config |
| `application.saveGiteaProvider` | POST | `applicationId`, provider config |
| `application.saveBitbucketProvider` | POST | `applicationId`, provider config |
| `application.saveGitProvider` | POST | `applicationId`, provider config |
| `application.saveDockerProvider` | POST | `applicationId`, provider config |
| `application.disconnectGitProvider` | POST | `applicationId` |

### Build Types (`buildType` enum)

```
dockerfile | heroku_buildpacks | paketo_buildpacks | nixpacks | static | railpack
```

### Application Statuses (`applicationStatus` enum)

```
idle | running | done | error
```

### Key `application.update` Fields

Resource limits:
- `memoryReservation`, `memoryLimit`, `cpuReservation`, `cpuLimit`

Git settings:
- `sourceType`: `github|docker|git|gitlab|bitbucket|gitea|drop`
- `repository`, `owner`, `branch`, `buildPath`
- `autoDeploy`: boolean
- `triggerType`: `push|tag`
- `enableSubmodules`: boolean

Docker settings:
- `dockerfile`, `dockerContextPath`, `dockerBuildStage`
- `dockerImage`, `registryUrl`

Build:
- `buildArgs`, `buildSecrets`, `cleanCache`
- `createEnvFile`: boolean

Preview deployments:
- `isPreviewDeploymentsActive`, `previewEnv`, `previewPort`, `previewHttps`, `previewLimit`

Swarm mode:
- `healthCheckSwarm`, `restartPolicySwarm`, `placementSwarm`, `replicas`

## Deployment (8 endpoints)

| Endpoint | Method | Required |
|----------|--------|----------|
| `deployment.all` | GET | `applicationId` |
| `deployment.allByCompose` | GET | `composeId` |
| `deployment.allByServer` | GET | `serverId` |
| `deployment.allByType` | GET | type params |
| `deployment.allCentralized` | GET | params |
| `deployment.queueList` | GET | — |
| `deployment.removeDeployment` | POST | `deploymentId` |
| `deployment.killProcess` | POST | `deploymentId` |

**IMPORTANT:** Build logs and container logs are **WebSocket only**.
No REST endpoint exists for reading logs. Use the Dashboard UI.

## Domain (9 endpoints)

| Endpoint | Method | Required | Optional |
|----------|--------|----------|----------|
| `domain.byApplicationId` | GET | `applicationId` | — |
| `domain.byComposeId` | GET | `composeId` | — |
| `domain.one` | GET | `domainId` | — |
| `domain.create` | POST | `host` | `path`, `port`, `https`, `applicationId`, `composeId`, `certificateType`, `serviceName`, `domainType`, `stripPath`, `internalPath` |
| `domain.update` | POST | `domainId`, fields | — |
| `domain.delete` | POST | `domainId` | — |
| `domain.generateDomain` | POST | params | — |
| `domain.validateDomain` | POST | params | — |
| `domain.canGenerateTraefikMeDomains` | GET | — | — |

### Certificate Types

```
letsencrypt | none | custom
```

### Domain Types

```
compose | application | preview
```

## PostgreSQL (14 endpoints)

| Endpoint | Method | Required | Optional |
|----------|--------|----------|----------|
| `postgres.one` | GET | `postgresId` | — |
| `postgres.create` | POST | `name`, `databaseName`, `databaseUser`, `databasePassword`, `environmentId` | `appName`, `dockerImage`, `description`, `serverId` |
| `postgres.update` | POST | `postgresId`, fields | — |
| `postgres.remove` | POST | `postgresId` | — |
| `postgres.deploy` | POST | `postgresId` | — |
| `postgres.start` | POST | `postgresId` | — |
| `postgres.stop` | POST | `postgresId` | — |
| `postgres.reload` | POST | `postgresId` | — |
| `postgres.rebuild` | POST | `postgresId` | — |
| `postgres.saveExternalPort` | POST | `postgresId`, `externalPort` (nullable) | — |
| `postgres.saveEnvironment` | POST | `postgresId`, env | — |
| `postgres.changeStatus` | POST | `postgresId`, status | — |
| `postgres.move` | POST | `postgresId`, target | — |
| `postgres.search` | GET | search params | — |

## Redis (14 endpoints)

| Endpoint | Method | Required | Optional |
|----------|--------|----------|----------|
| `redis.one` | GET | `redisId` | — |
| `redis.create` | POST | `name`, `databasePassword`, `environmentId` | `appName`, `dockerImage`, `description`, `serverId` |
| `redis.update` | POST | `redisId`, fields | — |
| `redis.remove` | POST | `redisId` | — |
| `redis.deploy` | POST | `redisId` | — |
| `redis.start` | POST | `redisId` | — |
| `redis.stop` | POST | `redisId` | — |
| `redis.reload` | POST | `redisId` | — |
| `redis.rebuild` | POST | `redisId` | — |
| `redis.saveExternalPort` | POST | `redisId`, `externalPort` | — |
| `redis.saveEnvironment` | POST | `redisId`, env | — |
| `redis.changeStatus` | POST | `redisId`, status | — |
| `redis.move` | POST | `redisId`, target | — |
| `redis.search` | GET | search params | — |

## Docker (7 endpoints)

| Endpoint | Method | Required |
|----------|--------|----------|
| `docker.getContainers` | GET | — |
| `docker.getContainersByAppLabel` | GET | `appLabel` |
| `docker.getContainersByAppNameMatch` | GET | `appName` |
| `docker.getServiceContainersByAppName` | GET | `appName` |
| `docker.getStackContainersByAppName` | GET | `appName` |
| `docker.getConfig` | GET | — |
| `docker.restartContainer` | POST | `containerId` |

**No Docker exec endpoint exists.**

## Docker Compose (28 endpoints)

| Endpoint | Method | Required |
|----------|--------|----------|
| `compose.one` | GET | `composeId` |
| `compose.create` | POST | `name`, `environmentId` |
| `compose.deploy` | POST | `composeId` |
| `compose.stop` | POST | `composeId` |
| `compose.start` | POST | `composeId` |
| `compose.delete` | POST | `composeId` |
| `compose.update` | POST | `composeId`, fields |
| `compose.redeploy` | POST | `composeId` |
| `compose.loadServices` | GET | `composeId` |
| `compose.templates` | GET | — |
| `compose.cancelDeployment` | POST | `composeId` |
| `compose.cleanQueues` | POST | `composeId` |
| `compose.clearDeployments` | POST | `composeId` |
| `compose.deployTemplate` | POST | template params |
| `compose.disconnectGitProvider` | POST | `composeId` |
| `compose.fetchSourceType` | GET | `composeId` |
| `compose.getConvertedCompose` | GET | `composeId` |
| `compose.getDefaultCommand` | GET | `composeId` |
| `compose.getTags` | GET | `composeId` |
| `compose.import` | POST | import params |
| `compose.isolatedDeployment` | POST | `composeId` |
| `compose.killBuild` | POST | `composeId` |
| `compose.loadMountsByService` | GET | `composeId`, `serviceName` |
| `compose.move` | POST | `composeId`, target |
| `compose.processTemplate` | POST | template params |
| `compose.randomizeCompose` | POST | `composeId` |
| `compose.refreshToken` | POST | `composeId` |
| `compose.search` | GET | search params |

## Settings (49 endpoints)

Covers server settings, Traefik configuration, cleanup operations, GPU, logging, and more.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `settings.health` | GET | Server health check |
| `settings.getOpenApiDocument` | GET | Full OpenAPI spec |
| `settings.getDokployVersion` | GET | Dokploy version |
| `settings.getIp` | GET | Server IP |
| `settings.reloadServer` | POST | Reload server |
| `settings.reloadTraefik` | POST | Reload Traefik |
| `settings.reloadRedis` | POST | Reload Redis |
| `settings.cleanDockerPrune` | POST | Docker system prune |
| `settings.cleanUnusedImages` | POST | Remove unused images |
| `settings.cleanStoppedContainers` | POST | Remove stopped containers |
| `settings.cleanUnusedVolumes` | POST | Remove unused volumes |
| `settings.cleanDockerBuilder` | POST | Clean Docker builder cache |
| `settings.cleanAll` | POST | Run all cleanup operations |
| `settings.cleanAllDeploymentQueue` | POST | Clear deployment queue |
| `settings.cleanMonitoring` | POST | Clean monitoring data |
| `settings.cleanRedis` | POST | Clean Redis data |
| `settings.cleanSSHPrivateKey` | POST | Clean SSH private key |
| `settings.readTraefikConfig` | GET | Read Traefik config |
| `settings.updateTraefikConfig` | POST | Update Traefik config |
| `settings.readMiddlewareTraefikConfig` | GET | Read middleware config |
| `settings.updateMiddlewareTraefikConfig` | POST | Update middleware config |
| `settings.readWebServerTraefikConfig` | GET | Read web server Traefik config |
| `settings.updateWebServerTraefikConfig` | POST | Update web server Traefik config |
| `settings.readTraefikEnv` | GET | Read Traefik environment |
| `settings.writeTraefikEnv` | POST | Write Traefik environment |
| `settings.readTraefikFile` | GET | Read Traefik file |
| `settings.updateTraefikFile` | POST | Update Traefik file |
| `settings.getTraefikPorts` | GET | Get Traefik ports |
| `settings.updateTraefikPorts` | POST | Update Traefik ports |
| `settings.getWebServerSettings` | GET | Web server settings |
| `settings.updateServer` | POST | Update server settings |
| `settings.updateServerIp` | POST | Update server IP |
| `settings.assignDomainServer` | POST | Assign domain to server |
| `settings.getReleaseTag` | GET | Get release tag |
| `settings.getUpdateData` | GET | Get update data |
| `settings.readDirectories` | GET | Read server directories |
| `settings.saveSSHPrivateKey` | POST | Save SSH private key |
| `settings.getDokployCloudIps` | GET | Get Dokploy Cloud IPs |
| `settings.isCloud` | GET | Check if cloud instance |
| `settings.isUserSubscribed` | GET | Check user subscription |
| `settings.haveActivateRequests` | GET | Check activate requests |
| `settings.toggleRequests` | POST | Toggle requests |
| `settings.haveTraefikDashboardPortEnabled` | GET | Check Traefik dashboard port |
| `settings.toggleDashboard` | POST | Toggle Traefik dashboard |
| `settings.checkGPUStatus` | GET | Check GPU status |
| `settings.setupGPU` | POST | Setup GPU support |
| `settings.getLogCleanupStatus` | GET | Get log cleanup status |
| `settings.updateLogCleanup` | POST | Update log cleanup settings |
| `settings.updateDockerCleanup` | POST | Update Docker cleanup settings |

## Notification (38 endpoints)

Supports Slack, Telegram, Discord, Email, Custom webhooks, Gotify, Ntfy, Pushover, Lark, Teams, and Resend.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `notification.all` | GET | List all notifications |
| `notification.one` | GET | Get one notification |
| `notification.remove` | POST | Remove notification |
| `notification.receiveNotification` | POST | Receive/trigger notification |
| `notification.getEmailProviders` | GET | List email providers |
| `notification.createSlack` | POST | Create Slack notification |
| `notification.updateSlack` | POST | Update Slack notification |
| `notification.testSlackConnection` | POST | Test Slack connection |
| `notification.createTelegram` | POST | Create Telegram notification |
| `notification.updateTelegram` | POST | Update Telegram notification |
| `notification.testTelegramConnection` | POST | Test Telegram connection |
| `notification.createDiscord` | POST | Create Discord notification |
| `notification.updateDiscord` | POST | Update Discord notification |
| `notification.testDiscordConnection` | POST | Test Discord connection |
| `notification.createEmail` | POST | Create Email notification |
| `notification.updateEmail` | POST | Update Email notification |
| `notification.testEmailConnection` | POST | Test Email connection |
| `notification.createCustom` | POST | Create custom webhook |
| `notification.updateCustom` | POST | Update custom webhook |
| `notification.testCustomConnection` | POST | Test custom webhook |
| `notification.createGotify` | POST | Create Gotify notification |
| `notification.updateGotify` | POST | Update Gotify notification |
| `notification.testGotifyConnection` | POST | Test Gotify connection |
| `notification.createNtfy` | POST | Create Ntfy notification |
| `notification.updateNtfy` | POST | Update Ntfy notification |
| `notification.testNtfyConnection` | POST | Test Ntfy connection |
| `notification.createPushover` | POST | Create Pushover notification |
| `notification.updatePushover` | POST | Update Pushover notification |
| `notification.testPushoverConnection` | POST | Test Pushover connection |
| `notification.createLark` | POST | Create Lark notification |
| `notification.updateLark` | POST | Update Lark notification |
| `notification.testLarkConnection` | POST | Test Lark connection |
| `notification.createTeams` | POST | Create Teams notification |
| `notification.updateTeams` | POST | Update Teams notification |
| `notification.testTeamsConnection` | POST | Test Teams connection |
| `notification.createResend` | POST | Create Resend notification |
| `notification.updateResend` | POST | Update Resend notification |
| `notification.testResendConnection` | POST | Test Resend connection |

## Backup (11 endpoints)

| Endpoint | Method | Required |
|----------|--------|----------|
| `backup.one` | GET | `backupId` |
| `backup.create` | POST | backup config |
| `backup.update` | POST | `backupId`, fields |
| `backup.remove` | POST | `backupId` |
| `backup.listBackupFiles` | GET | `backupId` |
| `backup.manualBackupPostgres` | POST | `backupId` |
| `backup.manualBackupMySql` | POST | `backupId` |
| `backup.manualBackupMariadb` | POST | `backupId` |
| `backup.manualBackupMongo` | POST | `backupId` |
| `backup.manualBackupCompose` | POST | `backupId` |
| `backup.manualBackupWebServer` | POST | `backupId` |

## Server (16 endpoints)

| Endpoint | Method | Required |
|----------|--------|----------|
| `server.all` | GET | — |
| `server.one` | GET | `serverId` |
| `server.create` | POST | server config |
| `server.update` | POST | `serverId`, fields |
| `server.remove` | POST | `serverId` |
| `server.setup` | POST | `serverId` |
| `server.validate` | POST | `serverId` |
| `server.publicIp` | GET | `serverId` |
| `server.count` | GET | — |
| `server.buildServers` | GET | — |
| `server.withSSHKey` | GET | `serverId` |
| `server.getServerMetrics` | GET | `serverId` |
| `server.getServerTime` | GET | `serverId` |
| `server.getDefaultCommand` | GET | `serverId` |
| `server.security` | GET | `serverId` |
| `server.setupMonitoring` | POST | `serverId` |

## User (18 endpoints)

| Endpoint | Method | Required |
|----------|--------|----------|
| `user.all` | GET | — |
| `user.one` | GET | `userId` |
| `user.get` | GET | — |
| `user.update` | POST | `userId`, fields |
| `user.remove` | POST | `userId` |
| `user.createApiKey` | POST | api key config |
| `user.deleteApiKey` | POST | `apiKeyId` |
| `user.generateToken` | POST | token params |
| `user.getUserByToken` | GET | `token` |
| `user.assignPermissions` | POST | `userId`, permissions |
| `user.sendInvitation` | POST | invitation config |
| `user.getInvitations` | GET | — |
| `user.checkUserOrganizations` | GET | — |
| `user.haveRootAccess` | GET | — |
| `user.getBackups` | GET | — |
| `user.getContainerMetrics` | GET | params |
| `user.getServerMetrics` | GET | params |
| `user.getMetricsToken` | GET | — |

## Other Database Services

Same pattern as PostgreSQL/Redis (14 endpoints each):

- `mysql.*` — MySQL
- `mariadb.*` — MariaDB
- `mongo.*` — MongoDB

## Environment (7 endpoints)

| Endpoint | Method | Required |
|----------|--------|----------|
| `environment.byProjectId` | GET | `projectId` |
| `environment.one` | GET | `environmentId` |
| `environment.create` | POST | `name`, `projectId` |
| `environment.duplicate` | POST | `environmentId` |
| `environment.remove` | POST | `environmentId` |
| `environment.search` | GET | search params |
| `environment.update` | POST | `environmentId`, fields |

## Patch (12 endpoints)

| Endpoint | Method | Required |
|----------|--------|----------|
| `patch.byEntityId` | GET | entity ID |
| `patch.one` | GET | `patchId` |
| `patch.create` | POST | patch config |
| `patch.update` | POST | `patchId`, fields |
| `patch.delete` | POST | `patchId` |
| `patch.ensureRepo` | POST | repo params |
| `patch.cleanPatchRepos` | POST | — |
| `patch.readRepoDirectories` | GET | repo params |
| `patch.readRepoFile` | GET | repo/file params |
| `patch.saveFileAsPatch` | POST | file/patch params |
| `patch.markFileForDeletion` | POST | file params |
| `patch.toggleEnabled` | POST | `patchId` |

## SSO (10 endpoints)

| Endpoint | Method | Required |
|----------|--------|----------|
| `sso.listProviders` | GET | — |
| `sso.one` | GET | `ssoId` |
| `sso.register` | POST | SSO config |
| `sso.update` | POST | `ssoId`, fields |
| `sso.deleteProvider` | POST | `ssoId` |
| `sso.showSignInWithSSO` | GET | — |
| `sso.getTrustedOrigins` | GET | — |
| `sso.addTrustedOrigin` | POST | origin config |
| `sso.updateTrustedOrigin` | POST | origin ID, fields |
| `sso.removeTrustedOrigin` | POST | origin ID |

## Organization (10 endpoints)

| Endpoint | Method | Required |
|----------|--------|----------|
| `organization.all` | GET | — |
| `organization.one` | GET | `organizationId` |
| `organization.active` | GET | — |
| `organization.create` | POST | org config |
| `organization.update` | POST | `organizationId`, fields |
| `organization.delete` | POST | `organizationId` |
| `organization.setDefault` | POST | `organizationId` |
| `organization.allInvitations` | GET | — |
| `organization.removeInvitation` | POST | invitation ID |
| `organization.updateMemberRole` | POST | member ID, role |

## AI (9 endpoints)

| Endpoint | Method | Required |
|----------|--------|----------|
| `ai.getAll` | GET | — |
| `ai.one` | GET | `aiId` |
| `ai.get` | GET | params |
| `ai.create` | POST | AI config |
| `ai.update` | POST | `aiId`, fields |
| `ai.delete` | POST | `aiId` |
| `ai.deploy` | POST | `aiId` |
| `ai.suggest` | POST | suggestion params |
| `ai.getModels` | GET | — |

## License Key (6 endpoints)

| Endpoint | Method | Required |
|----------|--------|----------|
| `licenseKey.activate` | POST | license key |
| `licenseKey.deactivate` | POST | — |
| `licenseKey.validate` | GET | — |
| `licenseKey.haveValidLicenseKey` | GET | — |
| `licenseKey.getEnterpriseSettings` | GET | — |
| `licenseKey.updateEnterpriseSettings` | POST | settings |

## Preview Deployment (4 endpoints)

| Endpoint | Method | Required |
|----------|--------|----------|
| `previewDeployment.all` | GET | `applicationId` |
| `previewDeployment.one` | GET | `previewDeploymentId` |
| `previewDeployment.delete` | POST | `previewDeploymentId` |
| `previewDeployment.redeploy` | POST | `previewDeploymentId` |

## Rollback (2 endpoints)

| Endpoint | Method | Required |
|----------|--------|----------|
| `rollback.rollback` | POST | rollback params |
| `rollback.delete` | POST | rollback ID |

## Schedule (6 endpoints)

| Endpoint | Method | Required |
|----------|--------|----------|
| `schedule.list` | GET | params |
| `schedule.one` | GET | `scheduleId` |
| `schedule.create` | POST | schedule config |
| `schedule.update` | POST | `scheduleId`, fields |
| `schedule.delete` | POST | `scheduleId` |
| `schedule.runManually` | POST | `scheduleId` |

## Volume Backups (6 endpoints)

| Endpoint | Method | Required |
|----------|--------|----------|
| `volumeBackups.list` | GET | params |
| `volumeBackups.one` | GET | `volumeBackupId` |
| `volumeBackups.create` | POST | backup config |
| `volumeBackups.update` | POST | `volumeBackupId`, fields |
| `volumeBackups.delete` | POST | `volumeBackupId` |
| `volumeBackups.runManually` | POST | `volumeBackupId` |

## Stripe (7 endpoints)

| Endpoint | Method | Required |
|----------|--------|----------|
| `stripe.getProducts` | GET | — |
| `stripe.getCurrentPlan` | GET | — |
| `stripe.getInvoices` | GET | — |
| `stripe.canCreateMoreServers` | GET | — |
| `stripe.createCheckoutSession` | POST | session params |
| `stripe.createCustomerPortalSession` | POST | — |
| `stripe.upgradeSubscription` | POST | subscription params |

## Swarm (3 endpoints)

| Endpoint | Method | Required |
|----------|--------|----------|
| `swarm.getNodes` | GET | — |
| `swarm.getNodeInfo` | GET | node params |
| `swarm.getNodeApps` | GET | node params |

## Redirects (4 endpoints)

| Endpoint | Method | Required |
|----------|--------|----------|
| `redirects.one` | GET | `redirectId` |
| `redirects.create` | POST | redirect config |
| `redirects.update` | POST | `redirectId`, fields |
| `redirects.delete` | POST | `redirectId` |

## All 449 Endpoint Categories

| Category | Count | Description |
|----------|-------|-------------|
| `settings.*` | 49 | Server settings, Traefik, cleanup, GPU, logging |
| `notification.*` | 38 | Slack/Telegram/Discord/Email/Gotify/Ntfy/Pushover/Lark/Teams/Resend/Custom |
| `application.*` | 29 | Application management |
| `compose.*` | 28 | Docker Compose services |
| `user.*` | 18 | User management, API keys |
| `server.*` | 16 | Remote server management |
| `postgres.*` | 14 | PostgreSQL management |
| `redis.*` | 14 | Redis management |
| `mysql.*` | 14 | MySQL management |
| `mariadb.*` | 14 | MariaDB management |
| `mongo.*` | 14 | MongoDB management |
| `patch.*` | 12 | File patching and repo management |
| `backup.*` | 11 | Database and service backups |
| `organization.*` | 10 | Organization management |
| `sso.*` | 10 | Single Sign-On |
| `domain.*` | 9 | Domain/SSL management |
| `ai.*` | 9 | AI features |
| `deployment.*` | 8 | Deployment history and queue |
| `project.*` | 8 | Project management |
| `gitea.*` | 8 | Gitea provider |
| `docker.*` | 7 | Container operations |
| `bitbucket.*` | 7 | Bitbucket provider |
| `registry.*` | 7 | Docker registries |
| `gitlab.*` | 7 | GitLab provider |
| `stripe.*` | 7 | Billing (cloud) |
| `environment.*` | 7 | Environment management |
| `github.*` | 6 | GitHub provider |
| `licenseKey.*` | 6 | Enterprise licensing |
| `sshKey.*` | 6 | SSH key management |
| `mounts.*` | 6 | Volume mounts |
| `destination.*` | 6 | S3 backup destinations |
| `schedule.*` | 6 | Scheduled jobs |
| `volumeBackups.*` | 6 | Volume backup management |
| `certificates.*` | 4 | SSL certificates |
| `cluster.*` | 4 | Docker Swarm cluster |
| `port.*` | 4 | Port management |
| `redirects.*` | 4 | URL redirects |
| `security.*` | 4 | Security settings |
| `previewDeployment.*` | 4 | Preview deployments |
| `swarm.*` | 3 | Swarm node management |
| `gitProvider.*` | 2 | Git provider generic |
| `rollback.*` | 2 | Deployment rollbacks |
| `admin.*` | 1 | Admin setup |

## Practical Examples

### Deploy and poll until done

```bash
DOKPLOY_URL="https://dokploy.example.com"
DOKPLOY_API_KEY="your-key"
APP_ID="your-app-id"

# Trigger deploy
curl -s -X POST "${DOKPLOY_URL}/api/application.deploy" \
  -H "x-api-key: ${DOKPLOY_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"json\":{\"applicationId\":\"${APP_ID}\"}}"

# Poll status every 15 seconds
while true; do
  STATUS=$(curl -s -X GET "${DOKPLOY_URL}/api/trpc/application.one?input=$(python3 -c "
import urllib.parse, json
print(urllib.parse.quote(json.dumps({'json':{'applicationId':'${APP_ID}'}})))
")" -H "x-api-key: ${DOKPLOY_API_KEY}" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d.get('result',{}).get('data',{}).get('json',{}).get('applicationStatus','unknown'))
")
  echo "Status: ${STATUS}"
  if [ "$STATUS" = "done" ] || [ "$STATUS" = "error" ]; then break; fi
  sleep 15
done
```

### Set environment variables

```bash
curl -s -X POST "${DOKPLOY_URL}/api/application.saveEnvironment" \
  -H "x-api-key: ${DOKPLOY_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "json": {
      "applicationId": "APP_ID",
      "env": "DATABASE_URL=postgresql://user:pass@host:5432/db\nREDIS_URL=redis://:pass@host:6379\nNODE_ENV=production"
    }
  }'
```

### Create a domain with HTTPS

```bash
curl -s -X POST "${DOKPLOY_URL}/api/domain.create" \
  -H "x-api-key: ${DOKPLOY_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "json": {
      "applicationId": "APP_ID",
      "host": "app.example.com",
      "https": true,
      "port": 3000,
      "certificateType": "letsencrypt",
      "domainType": "application",
      "stripPath": false
    }
  }'
```

### Create PostgreSQL service

```bash
curl -s -X POST "${DOKPLOY_URL}/api/postgres.create" \
  -H "x-api-key: ${DOKPLOY_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "json": {
      "name": "my-postgres",
      "databaseName": "mydb",
      "databaseUser": "myuser",
      "databasePassword": "secure-password",
      "environmentId": "ENV_ID",
      "dockerImage": "postgres:16-alpine"
    }
  }'
```

### Get deployment history

```bash
curl -s -X GET "${DOKPLOY_URL}/api/trpc/deployment.all?input=$(python3 -c "
import urllib.parse, json
print(urllib.parse.quote(json.dumps({'json':{'applicationId':'APP_ID'}})))
")" -H "x-api-key: ${DOKPLOY_API_KEY}" | python3 -c "
import sys, json
d = json.load(sys.stdin)
for dep in d.get('result',{}).get('data',{}).get('json',[])[:5]:
    print(f\"{dep.get('status','?'):8} {dep.get('title','')[:50]:50} {dep.get('createdAt','')[:19]}\")
"
```

### List Docker containers

```bash
curl -s -X GET "${DOKPLOY_URL}/api/trpc/docker.getContainersByAppNameMatch?input=$(python3 -c "
import urllib.parse, json
print(urllib.parse.quote(json.dumps({'json':{'appName':'your-app-name'}})))
")" -H "x-api-key: ${DOKPLOY_API_KEY}"
```

### Set build type to Dockerfile

```bash
curl -s -X POST "${DOKPLOY_URL}/api/application.saveBuildType" \
  -H "x-api-key: ${DOKPLOY_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "json": {
      "applicationId": "APP_ID",
      "buildType": "dockerfile",
      "dockerfile": "./Dockerfile",
      "dockerContextPath": "./",
      "dockerBuildStage": ""
    }
  }'
```
