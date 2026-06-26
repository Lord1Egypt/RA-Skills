# Azure Capacity Planning

Analyze resource capacity and plan for growth across compute, networking, containers, databases, and infrastructure services.

## Table of Contents

- [Compute Capacity](#compute-capacity)
- [Network Capacity](#network-capacity)
- [Container & Serverless Capacity](#container--serverless-capacity)
- [Database & Storage Capacity](#database--storage-capacity)
- [Infrastructure Capacity](#infrastructure-capacity)

## Compute Capacity

VM SKU distribution across regions:

```dql
smartscapeNodes "AZURE_MICROSOFT_COMPUTE_VIRTUALMACHINES"
| parse azure.object, "JSON:azjson"
| fieldsAdd vmSize = azjson[configuration][properties][hardwareProfile][vmSize],
            powerState = azjson[configuration][properties][extended][instanceView][powerState][displayStatus]
| summarize vm_count = count(), by: {vmSize, powerState, azure.location}
| sort vm_count desc
```

VMSS capacity analysis (current instance count vs configured SKU):

```dql
smartscapeNodes "AZURE_MICROSOFT_COMPUTE_VIRTUALMACHINESCALESETS"
| parse azure.object, "JSON:azjson"
| fieldsAdd vmSize = azjson[configuration][sku][name],
            tier = azjson[configuration][sku][tier],
            capacity = azjson[configuration][sku][capacity]
| fields name, vmSize, tier, capacity, azure.resource.group, azure.location
| sort capacity desc
```

## Network Capacity

Subnet count per virtual network:

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_VIRTUALNETWORKS_SUBNETS"
| traverse "*", "AZURE_MICROSOFT_NETWORK_VIRTUALNETWORKS"
| summarize subnet_count = count(), by: {name, azure.location}
| sort subnet_count desc
```

NIC usage across resource groups:

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_NETWORKINTERFACES"
| summarize nic_count = count(), by: {azure.resource.group, azure.location}
| sort nic_count desc
```

Public IP address counts by region:

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_PUBLICIPADDRESSES"
| summarize ip_count = count(), by: {azure.location, azure.resource.group}
| sort ip_count desc
```

Virtual network address space inventory:

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_VIRTUALNETWORKS"
| parse azure.object, "JSON:azjson"
| fieldsAdd addressPrefixes = toString(azjson[configuration][properties][addressSpace][addressPrefixes]),
            ddosProtection = azjson[configuration][properties][enableDdosProtection]
| fields name, addressPrefixes, ddosProtection, azure.location, azure.resource.group
```

## Container & Serverless Capacity

AKS cluster capacity overview:

```dql
smartscapeNodes "AZURE_MICROSOFT_CONTAINERSERVICE_MANAGEDCLUSTERS"
| parse azure.object, "JSON:azjson"
| fieldsAdd k8sVersion = azjson[configuration][properties][kubernetesVersion],
            currentVersion = azjson[configuration][properties][currentKubernetesVersion],
            powerState = azjson[configuration][properties][powerState][code],
            skuTier = azjson[configuration][sku][tier]
| fields name, k8sVersion, currentVersion, powerState, skuTier, azure.resource.group, azure.location
```

AKS agent pool sizing:

```dql
smartscapeNodes "AZURE_MICROSOFT_CONTAINERSERVICE_MANAGEDCLUSTERS_AGENTPOOLS"
| parse azure.object, "JSON:azjson"
| fieldsAdd vmSize = azjson[configuration][vmSize],
            nodeCount = azjson[configuration][count],
            minCount = azjson[configuration][minCount],
            maxCount = azjson[configuration][maxCount],
            enableAutoScaling = azjson[configuration][enableAutoScaling],
            mode = azjson[configuration][mode]
| fields name, vmSize, nodeCount, minCount, maxCount, enableAutoScaling, mode, azure.resource.group
| sort nodeCount desc
```

App Service Plan capacity and headroom:

```dql
smartscapeNodes "AZURE_MICROSOFT_WEB_SERVERFARMS"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][sku][name],
            skuTier = azjson[configuration][sku][tier],
            capacity = azjson[configuration][sku][capacity]
| fields name, skuName, skuTier, capacity, azure.resource.group, azure.location
| sort capacity desc
```

Container App scaling configuration:

```dql
smartscapeNodes "AZURE_MICROSOFT_APP_CONTAINERAPPS"
| parse azure.object, "JSON:azjson"
| fieldsAdd minReplicas = azjson[configuration][properties][template][scale][minReplicas],
            maxReplicas = azjson[configuration][properties][template][scale][maxReplicas],
            runningStatus = azjson[configuration][properties][runningStatus]
| fields name, minReplicas, maxReplicas, runningStatus, azure.resource.group, azure.location
```

## Database & Storage Capacity

SQL database sizing and tier distribution:

```dql
smartscapeNodes "AZURE_MICROSOFT_SQL_SERVERS_DATABASES"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][sku][name],
            skuTier = azjson[configuration][sku][tier],
            skuCapacity = azjson[configuration][sku][capacity],
            maxSizeBytes = azjson[configuration][properties][maxSizeBytes],
            zoneRedundant = azjson[configuration][properties][zoneRedundant]
| fields name, skuName, skuTier, skuCapacity, maxSizeBytes, zoneRedundant, azure.resource.group
| sort skuCapacity desc
```

Storage account distribution across regions:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][sku][name],
            kind = azjson[configuration][kind],
            accessTier = azjson[configuration][properties][accessTier]
| summarize account_count = count(), by: {skuName, kind, azure.location}
| sort account_count desc
```

Event Hub namespace throughput units:

```dql
smartscapeNodes "AZURE_MICROSOFT_EVENTHUB_NAMESPACES"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][sku][name],
            throughputUnits = azjson[configuration][sku][capacity],
            isAutoInflate = azjson[configuration][properties][isAutoInflateEnabled],
            maxThroughputUnits = azjson[configuration][properties][maximumThroughputUnits]
| fields name, skuName, throughputUnits, isAutoInflate, maxThroughputUnits, azure.location
```

## Infrastructure Capacity

VPN gateway inventory:

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_VIRTUALNETWORKGATEWAYS"
| parse azure.object, "JSON:azjson"
| fieldsAdd gatewaySku = azjson[configuration][properties][sku][name],
            gatewayType = azjson[configuration][properties][gatewayType]
| fields name, gatewaySku, gatewayType, azure.resource.group, azure.location
```

ExpressRoute circuit inventory:

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_EXPRESSROUTECIRCUITS"
| fields name, id, azure.resource.group, azure.location
```
