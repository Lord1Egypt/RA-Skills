# GCP Compute Engine Instances

Monitor and analyze GCP Compute Engine virtual machine instances, configurations, and static IP addresses.

## Table of Contents

- [Compute Entity Types](#compute-entity-types)
- [Instance Discovery and Inventory](#instance-discovery-and-inventory)
- [Instance Configuration Analysis](#instance-configuration-analysis)
- [Security Analysis](#security-analysis)
- [Relationship Traversal](#relationship-traversal)
- [IP Address Management](#ip-address-management)

## Compute Entity Types

All these types support the standard discovery pattern: `smartscapeNodes "<TYPE>" | fields name, gcp.project.id, gcp.region, gcp.zone, gcp.resource.name`

| Entity type | Description |
|---|---|
| `GCP_COMPUTE_GOOGLEAPIS_COM_INSTANCE` | Compute Engine VM instances |
| `GCP_COMPUTE_GOOGLEAPIS_COM_ADDRESS` | Static IP addresses |

## Instance Discovery and Inventory

List all Compute Engine instances:

```dql
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_INSTANCE"
| fields name, gcp.project.id, gcp.region, gcp.zone, gcp.resource.name
```

Count instances by project:

```dql
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_INSTANCE"
| summarize count(), by: {gcp.project.id}
```

Find instances in a specific project:

```dql-template
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_INSTANCE"
| filter gcp.project.id == "<GCP_PROJECT_ID>"
| fields name, gcp.region, gcp.zone
```

## Instance Configuration Analysis

Get machine type and status for all instances:

```dql
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_INSTANCE"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd machineType = gcpjson[configuration][additionalAttributes][machineType],
            status = gcpjson[configuration][resource][status]
| fields name, gcp.project.id, machineType, status
```

Retrieve instance labels:

```dql
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_INSTANCE"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd labels = gcpjson[configuration][resource][labels]
| fields name, labels
```

## Security Analysis

Check deletion protection and external IP exposure:

```dql
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_INSTANCE"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd deletionProtection = gcpjson[configuration][additionalAttributes][deletionProtection],
            externalIPs = gcpjson[configuration][additionalAttributes][externalIPs]
| fields name, deletionProtection, externalIPs
```

Audit network interface details — internal and external IPs with machine type:

```dql
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_INSTANCE"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd internalIPs = gcpjson[configuration][additionalAttributes][internalIPs],
            externalIPs = gcpjson[configuration][additionalAttributes][externalIPs],
            machineType = gcpjson[configuration][additionalAttributes][machineType]
| fields name, gcp.project.id, machineType, internalIPs, externalIPs
```

## Relationship Traversal

Traverse from instances to their subnetworks:

```dql
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_INSTANCE"
| traverse "*", "GCP_COMPUTE_GOOGLEAPIS_COM_SUBNETWORK"
| fields name, gcp.project.id
```

## IP Address Management

List all static IP addresses:

```dql
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_ADDRESS"
| fields name, gcp.project.id, gcp.region
```
