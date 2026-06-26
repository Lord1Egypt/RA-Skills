# TeamClaw install modes

## 1. Guided install

Use this when the user already has OpenClaw working and wants the shortest path:

```bash
npx -y @teamclaws/teamclaw install
```

What it helps with:

- installs or updates the TeamClaw plugin
- locates `openclaw.json`
- lets the user choose a topology
- reuses existing OpenClaw model definitions
- prompts for workspace placement

## 2. Manual plugin install

Use this when the user wants direct control over plugin installation:

```bash
openclaw plugins install @teamclaws/teamclaw
```

If the user explicitly wants the ClawHub source:

```bash
openclaw plugins install clawhub:@teamclaws/teamclaw
```

## 3. Recommended first topology: controller + localRoles

Minimal TeamClaw plugin block:

```json
{
  "mode": "controller",
  "port": 9527,
  "teamName": "my-team",
  "taskTimeoutMs": 1800000,
  "gitEnabled": true,
  "gitDefaultBranch": "main",
  "localRoles": ["architect", "developer", "qa"]
}
```

Use this first because it avoids multi-machine networking and still exercises the real controller, workers, UI, messages, clarifications, and git-backed workspace flow.

## 4. Worker-only topology

Use this only when a controller already exists elsewhere:

```json
{
  "mode": "worker",
  "port": 9528,
  "role": "developer",
  "controllerUrl": "http://controller-host:9527",
  "taskTimeoutMs": 1800000,
  "gitEnabled": true,
  "gitDefaultBranch": "main"
}
```

## 5. On-demand process workers

Use this when the controller should launch same-machine workers only as needed:

```json
{
  "mode": "controller",
  "port": 9527,
  "teamName": "my-team",
  "workerProvisioningType": "process",
  "workerProvisioningMinPerRole": 0,
  "workerProvisioningMaxPerRole": 2,
  "workerProvisioningIdleTtlMs": 120000,
  "workerProvisioningStartupTimeoutMs": 120000
}
```

## 6. On-demand Docker workers

Use this when the user already has Docker and wants containerized workers:

```json
{
  "mode": "controller",
  "port": 9527,
  "teamName": "my-team",
  "workerProvisioningType": "docker",
  "workerProvisioningControllerUrl": "http://host.docker.internal:9527",
  "workerProvisioningImage": "ghcr.io/topcheer/teamclaw-openclaw:latest",
  "workerProvisioningWorkspaceRoot": "/workspace-root",
  "workerProvisioningDockerWorkspaceVolume": "teamclaw-workspaces",
  "workerProvisioningMaxPerRole": 3
}
```

Important notes:

- `workerProvisioningControllerUrl` must be reachable from the worker container.
- If persistent workspaces matter, keep `workerProvisioningDockerWorkspaceVolume`.

## 7. On-demand Kubernetes workers

Use this only when the user already runs the controller in or behind a reachable cluster address:

```json
{
  "mode": "controller",
  "port": 9527,
  "teamName": "my-team",
  "workerProvisioningType": "kubernetes",
  "workerProvisioningControllerUrl": "http://teamclaw-controller.default.svc.cluster.local:9527",
  "workerProvisioningImage": "ghcr.io/topcheer/teamclaw-openclaw:latest",
  "workerProvisioningWorkspaceRoot": "/workspace-root",
  "workerProvisioningKubernetesWorkspacePersistentVolumeClaim": "teamclaw-workspace",
  "workerProvisioningMaxPerRole": 2
}
```

Important notes:

- `kubectl` must be available where the controller runs.
- The controller URL must be reachable from pods.
