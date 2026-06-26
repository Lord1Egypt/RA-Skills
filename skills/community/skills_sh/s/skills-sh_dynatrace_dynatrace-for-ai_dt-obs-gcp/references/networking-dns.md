# GCP Networking & DNS

Monitor VPC networks, subnets, routes, and Cloud DNS record sets across GCP projects.

## Table of Contents

- [Networking Entity Types](#networking-entity-types)
- [VPC Network Configuration](#vpc-network-configuration)
- [Subnet Management](#subnet-management)
- [Route Analysis](#route-analysis)
- [DNS Records](#dns-records)
- [Network Topology](#network-topology)

## Networking Entity Types

All these types support the standard discovery pattern: `smartscapeNodes "<TYPE>" | fields name, gcp.project.id, gcp.region`

| Entity type | Description |
|---|---|
| `GCP_COMPUTE_GOOGLEAPIS_COM_NETWORK` | VPC networks |
| `GCP_COMPUTE_GOOGLEAPIS_COM_SUBNETWORK` | VPC subnets |
| `GCP_COMPUTE_GOOGLEAPIS_COM_ROUTE` | Network routes |
| `GCP_DNS_GOOGLEAPIS_COM_RESOURCERECORDSET` | Cloud DNS resource record sets |

## VPC Network Configuration

List VPC networks with auto-subnet mode and routing configuration:

```dql
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_NETWORK"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd autoCreateSubnetworks = gcpjson[configuration][resource][autoCreateSubnetworks],
            routingMode = gcpjson[configuration][resource][routingConfig][routingMode]
| fields name, gcp.project.id, autoCreateSubnetworks, routingMode
```

Find VPC networks in a specific project:

```dql-template
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_NETWORK"
| filter gcp.project.id == "<GCP_PROJECT_ID>"
| fields name, autoCreateSubnetworks
```

## Subnet Management

List all subnets with CIDR ranges and purpose:

```dql
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_SUBNETWORK"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd ipCidrRange = gcpjson[configuration][resource][ipCidrRange],
            purpose = gcpjson[configuration][resource][purpose]
| fields name, gcp.project.id, gcp.region, ipCidrRange, purpose
```

Count subnets by project and region:

```dql
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_SUBNETWORK"
| summarize count(), by: {gcp.project.id, gcp.region}
```

Find subnets in a specific project:

```dql-template
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_SUBNETWORK"
| filter gcp.project.id == "<GCP_PROJECT_ID>"
| fields name, gcp.region, ipCidrRange, purpose
```

## Route Analysis

List routes with destination ranges and next-hop gateways:

```dql
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_ROUTE"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd destRange = gcpjson[configuration][resource][destRange],
            nextHopGateway = gcpjson[configuration][resource][nextHopGateway]
| fields name, gcp.project.id, destRange, nextHopGateway
```

Find routes targeting the default internet gateway:

```dql
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_ROUTE"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd destRange = gcpjson[configuration][resource][destRange],
            nextHopGateway = gcpjson[configuration][resource][nextHopGateway]
| filter contains(toString(nextHopGateway), "default-internet-gateway")
| fields name, gcp.project.id, destRange
```

## DNS Records

List all Cloud DNS resource record sets:

```dql
smartscapeNodes "GCP_DNS_GOOGLEAPIS_COM_RESOURCERECORDSET"
| fields name, gcp.project.id
```

Count DNS records by project:

```dql
smartscapeNodes "GCP_DNS_GOOGLEAPIS_COM_RESOURCERECORDSET"
| summarize count(), by: {gcp.project.id}
```

## Network Topology

Count all networking resources by type and project:

```dql
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_NETWORK", "GCP_COMPUTE_GOOGLEAPIS_COM_SUBNETWORK", "GCP_COMPUTE_GOOGLEAPIS_COM_ROUTE", "GCP_DNS_GOOGLEAPIS_COM_RESOURCERECORDSET"
| summarize count(), by: {type, gcp.project.id}
```
