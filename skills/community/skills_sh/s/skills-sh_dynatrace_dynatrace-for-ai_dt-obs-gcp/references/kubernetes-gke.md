# GCP Kubernetes / GKE

Monitor GKE clusters, workloads, nodes, RBAC, and storage via Dynatrace Smartscape.

## Table of Contents

- [Kubernetes Entity Types](#kubernetes-entity-types)
- [Pod Discovery and Status](#pod-discovery-and-status)
- [Deployment and StatefulSet Management](#deployment-and-statefulset-management)
- [Node and Node Pool Configuration](#node-and-node-pool-configuration)
- [Service Discovery](#service-discovery)
- [RBAC Analysis](#rbac-analysis)
- [Storage](#storage)
- [Cross-Resource Summarization](#cross-resource-summarization)

## Kubernetes Entity Types

All these types support the standard discovery pattern: `smartscapeNodes "<TYPE>" | fields name, gcp.project.id, gcp.region, ...`

Config parsing pattern: `parse gcp.object, "JSON:gcpjson"` then access `gcpjson[configuration][resource][...]`

| Entity type | Description |
|---|---|
| `GCP_K8S_IO_POD` | Kubernetes pods |
| `GCP_K8S_IO_NODE` | Kubernetes nodes |
| `GCP_K8S_IO_SERVICE` | Kubernetes services |
| `GCP_K8S_IO_SERVICEACCOUNT` | Kubernetes service accounts |
| `GCP_K8S_IO_PERSISTENTVOLUMECLAIM` | Persistent volume claims |
| `GCP_APPS_K8S_IO_DEPLOYMENT` | Kubernetes deployments |
| `GCP_APPS_K8S_IO_STATEFULSET` | Kubernetes stateful sets |
| `GCP_CONTAINER_GOOGLEAPIS_COM_NODEPOOL` | GKE node pools |
| `GCP_RBAC_AUTHORIZATION_K8S_IO_CLUSTERROLEBINDING` | Cluster-wide role bindings |
| `GCP_RBAC_AUTHORIZATION_K8S_IO_ROLEBINDING` | Namespace-scoped role bindings |

## Pod Discovery and Status

List all pods with project and region:

```dql
smartscapeNodes "GCP_K8S_IO_POD"
| fields name, gcp.project.id, gcp.region
```

Extract pod phase and assigned node from the GCP object configuration:

```dql
smartscapeNodes "GCP_K8S_IO_POD"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd phase = gcpjson[configuration][resource][status][phase],
            nodeName = gcpjson[configuration][resource][spec][nodeName]
| fields name, gcp.project.id, phase, nodeName
```

Find all pods scheduled on a specific node:

```dql-template
smartscapeNodes "GCP_K8S_IO_POD"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd nodeName = gcpjson[configuration][resource][spec][nodeName]
| filter nodeName == "<NODE_NAME>"
| fields name, gcp.project.id, nodeName
```

## Deployment and StatefulSet Management

List all deployments:

```dql
smartscapeNodes "GCP_APPS_K8S_IO_DEPLOYMENT"
| fields name, gcp.project.id, gcp.region
```

List all stateful sets:

```dql
smartscapeNodes "GCP_APPS_K8S_IO_STATEFULSET"
| fields name, gcp.project.id, gcp.region
```

## Node and Node Pool Configuration

List all Kubernetes nodes:

```dql
smartscapeNodes "GCP_K8S_IO_NODE"
| fields name, gcp.project.id, gcp.region
```

Inspect GKE node pool sizing and machine types — use for capacity planning and cost analysis:

```dql
smartscapeNodes "GCP_CONTAINER_GOOGLEAPIS_COM_NODEPOOL"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd initialNodeCount = gcpjson[configuration][resource][initialNodeCount],
            diskSizeGb = gcpjson[configuration][resource][config][diskSizeGb],
            machineType = gcpjson[configuration][resource][config][machineType]
| fields name, gcp.project.id, gcp.region, initialNodeCount, diskSizeGb, machineType
```

List node pool configurations for a specific project:

```dql-template
smartscapeNodes "GCP_CONTAINER_GOOGLEAPIS_COM_NODEPOOL"
| filter gcp.project.id == "<GCP_PROJECT_ID>"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd initialNodeCount = gcpjson[configuration][resource][initialNodeCount],
            diskSizeGb = gcpjson[configuration][resource][config][diskSizeGb],
            machineType = gcpjson[configuration][resource][config][machineType]
| fields name, gcp.region, initialNodeCount, diskSizeGb, machineType
```

## Service Discovery

List all Kubernetes services:

```dql
smartscapeNodes "GCP_K8S_IO_SERVICE"
| fields name, gcp.project.id, gcp.region
```

List all service accounts:

```dql
smartscapeNodes "GCP_K8S_IO_SERVICEACCOUNT"
| fields name, gcp.project.id, gcp.region
```

## RBAC Analysis

List cluster-wide role bindings — use for auditing cluster-level permissions:

```dql
smartscapeNodes "GCP_RBAC_AUTHORIZATION_K8S_IO_CLUSTERROLEBINDING"
| fields name, gcp.project.id, gcp.region
```

List namespace-scoped role bindings:

```dql
smartscapeNodes "GCP_RBAC_AUTHORIZATION_K8S_IO_ROLEBINDING"
| fields name, gcp.project.id, gcp.region
```

## Storage

List all persistent volume claims:

```dql
smartscapeNodes "GCP_K8S_IO_PERSISTENTVOLUMECLAIM"
| fields name, gcp.project.id, gcp.region
```

## Cross-Resource Summarization

Count pods by GCP project:

```dql
smartscapeNodes "GCP_K8S_IO_POD"
| summarize count(), by: {gcp.project.id}
```
