# Azure Cost Optimization

Identify cost savings opportunities and optimize Azure spending across compute, storage, networking, and managed services.

## Table of Contents

- [Compute Costs](#compute-costs)
- [Storage Costs](#storage-costs)
- [Network Costs](#network-costs)
- [Database Costs](#database-costs)
- [Serverless Costs](#serverless-costs)
- [Infrastructure Management Costs](#infrastructure-management-costs)

## Compute Costs

Analyze VM SKU distribution for right-sizing opportunities:

```dql
smartscapeNodes "AZURE_MICROSOFT_COMPUTE_VIRTUALMACHINES"
| parse azure.object, "JSON:azjson"
| fieldsAdd vmSize = azjson[configuration][properties][hardwareProfile][vmSize],
            powerState = azjson[configuration][properties][extended][instanceView][powerState][displayStatus]
| summarize vm_count = count(), by: {vmSize, azure.location}
| sort vm_count desc
```

Find deallocated VMs (still incurring disk costs):

```dql
smartscapeNodes "AZURE_MICROSOFT_COMPUTE_VIRTUALMACHINES"
| parse azure.object, "JSON:azjson"
| fieldsAdd powerState = azjson[configuration][properties][extended][instanceView][powerState][displayStatus]
| filter powerState != "VM running"
| fields name, id, powerState, azure.resource.group, azure.location
```

Analyze VMSS instance sizing and capacity:

```dql
smartscapeNodes "AZURE_MICROSOFT_COMPUTE_VIRTUALMACHINESCALESETS"
| parse azure.object, "JSON:azjson"
| fieldsAdd vmSize = azjson[configuration][sku][name],
            capacity = azjson[configuration][sku][capacity]
| summarize vmss_count = count(), total_instances = sum(capacity), by: {vmSize}
| sort total_instances desc
```

## Storage Costs

Find unattached managed disks by SKU and size (wasted spend):

```dql
smartscapeNodes "AZURE_MICROSOFT_COMPUTE_DISKS"
| parse azure.object, "JSON:azjson"
| fieldsAdd diskState = azjson[configuration][properties][diskState],
            diskSizeGB = azjson[configuration][properties][diskSizeGB],
            skuName = azjson[configuration][sku][name]
| filter diskState == "Unattached"
| fields name, skuName, diskSizeGB, azure.resource.group, azure.location
| sort diskSizeGB desc
```

Analyze storage account access tier distribution:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd accessTier = azjson[configuration][properties][accessTier],
            kind = azjson[configuration][kind]
| summarize account_count = count(), by: {accessTier, kind}
| sort account_count desc
```

Analyze storage account redundancy for cost reduction:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][sku][name],
            skuTier = azjson[configuration][sku][tier]
| summarize account_count = count(), by: {skuName, skuTier}
| sort account_count desc
```

## Network Costs

Count public IP addresses (each incurs cost):

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_PUBLICIPADDRESSES"
| parse azure.object, "JSON:azjson"
| fieldsAdd ipConfig = azjson[configuration][properties][ipConfiguration]
| fieldsAdd is_associated = if(isNotNull(ipConfig), "associated", else: "unassociated")
| summarize ip_count = count(), by: {is_associated, azure.location}
| sort ip_count desc
```

Analyze VPN gateway SKUs:

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_VIRTUALNETWORKGATEWAYS"
| parse azure.object, "JSON:azjson"
| fieldsAdd gatewaySku = azjson[configuration][properties][sku][name],
            gatewayType = azjson[configuration][properties][gatewayType]
| fields name, gatewaySku, gatewayType, azure.resource.group, azure.location
```

Review load balancer SKUs:

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_LOADBALANCERS"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][sku][name]
| summarize lb_count = count(), by: {skuName, azure.location}
| sort lb_count desc
```

## Database Costs

Analyze SQL database tier and DTU allocation:

```dql
smartscapeNodes "AZURE_MICROSOFT_SQL_SERVERS_DATABASES"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][sku][name],
            skuTier = azjson[configuration][sku][tier],
            skuCapacity = azjson[configuration][sku][capacity],
            serviceObjective = azjson[configuration][properties][currentServiceObjectiveName]
| fields name, skuName, skuTier, skuCapacity, serviceObjective, azure.resource.group
| sort skuCapacity desc
```

Summarize SQL database costs by tier:

```dql
smartscapeNodes "AZURE_MICROSOFT_SQL_SERVERS_DATABASES"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuTier = azjson[configuration][sku][tier],
            skuCapacity = azjson[configuration][sku][capacity]
| summarize db_count = count(), total_capacity = sum(skuCapacity), by: {skuTier}
| sort total_capacity desc
```

Review Redis cache SKU distribution:

```dql
smartscapeNodes "AZURE_MICROSOFT_CACHE_REDIS"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][properties][sku][name],
            skuFamily = azjson[configuration][properties][sku][family],
            skuCapacity = azjson[configuration][properties][sku][capacity]
| fields name, skuName, skuFamily, skuCapacity, azure.resource.group, azure.location
```

## Serverless Costs

Analyze Azure Functions runtime distribution:

```dql
smartscapeNodes "AZURE_MICROSOFT_WEB_SITES"
| parse azure.object, "JSON:azjson"
| fieldsAdd kind = azjson[configuration][kind],
            runtime = azjson[configuration][properties][siteConfig][linuxFxVersion],
            sku = azjson[configuration][properties][sku]
| filter contains(toString(kind), "functionapp")
| summarize function_count = count(), by: {runtime, sku}
| sort function_count desc
```

Analyze App Service Plan SKU distribution:

```dql
smartscapeNodes "AZURE_MICROSOFT_WEB_SERVERFARMS"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][sku][name],
            skuTier = azjson[configuration][sku][tier],
            skuCapacity = azjson[configuration][sku][capacity]
| summarize plan_count = count(), total_instances = sum(skuCapacity), by: {skuName, skuTier}
| sort plan_count desc
```

## Infrastructure Management Costs

List Key Vaults and their configuration:

```dql
smartscapeNodes "AZURE_MICROSOFT_KEYVAULT_VAULTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd rbacAuth = azjson[configuration][properties][enableRbacAuthorization],
            softDelete = azjson[configuration][properties][enableSoftDelete]
| fields name, rbacAuth, softDelete, azure.resource.group, azure.location
```

Review monitoring resource counts (Log Analytics workspaces, Application Insights):

```dql
smartscapeNodes "AZURE_MICROSOFT_OPERATIONALINSIGHTS_WORKSPACES",
    "AZURE_MICROSOFT_INSIGHTS_COMPONENTS"
| summarize count = count(), by: {type, azure.location}
| sort count desc
```
