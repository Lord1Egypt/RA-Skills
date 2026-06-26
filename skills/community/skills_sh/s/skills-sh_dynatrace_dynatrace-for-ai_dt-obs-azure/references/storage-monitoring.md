# Azure Storage Monitoring

Monitor Azure Storage Accounts, blob containers, file shares, queues, tables, and managed disks.

## Table of Contents

- [Storage Entity Types](#storage-entity-types)
- [Storage Account Configuration](#storage-account-configuration)
- [Storage Services](#storage-services)
- [Managed Disks](#managed-disks)
- [Cross-Service Analysis](#cross-service-analysis)

## Storage Entity Types

All these types support the standard discovery pattern: `smartscapeNodes "<TYPE>" | fields name, id, azure.subscription, azure.resource.group, azure.location, ...`

| Entity Type | Description |
|---|---|
| `AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS` | Azure Storage Accounts |
| `AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_BLOBSERVICES_CONTAINERS` | Blob containers |
| `AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_FILESERVICES_SHARES` | File shares |
| `AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_QUEUESERVICES_QUEUES` | Storage queues |
| `AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_TABLESERVICES_TABLES` | Storage tables |
| `AZURE_MICROSOFT_COMPUTE_DISKS` | Managed disks |

## Storage Account Configuration

### Inventory and SKU Analysis

List all Storage Accounts with SKU and tier:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd accountKind = azjson[configuration][kind],
    skuName = azjson[configuration][sku][name],
    skuTier = azjson[configuration][sku][tier],
    accessTier = azjson[configuration][properties][accessTier]
| fields name, accountKind, skuName, skuTier, accessTier,
    azure.resource.group, azure.location
```

Summarize Storage Accounts by replication type (SKU):

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][sku][name]
| summarize account_count = count(), by: {skuName}
| sort account_count desc
```

Summarize Storage Accounts by access tier:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd accessTier = azjson[configuration][properties][accessTier]
| summarize account_count = count(), by: {accessTier}
| sort account_count desc
```

### HTTPS Enforcement and TLS

Find Storage Accounts and their HTTPS/TLS configuration:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd httpsOnly = azjson[configuration][properties][supportsHttpsTrafficOnly],
    minimumTlsVersion = azjson[configuration][properties][minimumTlsVersion]
| fields name, httpsOnly, minimumTlsVersion, azure.resource.group, azure.location
```

Find Storage Accounts not enforcing HTTPS:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd httpsOnly = azjson[configuration][properties][supportsHttpsTrafficOnly]
| filter httpsOnly == false
| fields name, azure.resource.group, azure.location
```

Find Storage Accounts with TLS version below 1.2:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd minimumTlsVersion = azjson[configuration][properties][minimumTlsVersion]
| filter minimumTlsVersion != "TLS1_2"
| fields name, minimumTlsVersion, azure.resource.group, azure.location
```

### Public Access and Network Rules

Find Storage Accounts allowing public blob access:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd allowBlobPublicAccess = azjson[configuration][properties][allowBlobPublicAccess],
    networkDefaultAction = azjson[configuration][properties][networkAcls][defaultAction]
| fields name, allowBlobPublicAccess, networkDefaultAction,
    azure.resource.group, azure.location
```

Find Storage Accounts with open network access (defaultAction = Allow):

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd networkDefaultAction = azjson[configuration][properties][networkAcls][defaultAction]
| filter networkDefaultAction == "Allow"
| fields name, azure.resource.group, azure.location
```

### Encryption Configuration

Check encryption key source for Storage Accounts:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd keySource = azjson[configuration][properties][encryption][keySource],
    blobEncryption = azjson[configuration][properties][encryption][services][blob][enabled]
| fields name, keySource, blobEncryption, azure.resource.group, azure.location
```

### Primary Region Status

Check primary region availability status:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd statusOfPrimary = azjson[configuration][properties][statusOfPrimary],
    primaryEndpoint = azjson[configuration][properties][primaryEndpoints][blob]
| fields name, statusOfPrimary, primaryEndpoint, azure.resource.group, azure.location
```

## Storage Services

### Blob Containers

List all blob containers:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_BLOBSERVICES_CONTAINERS"
| fields name, id, azure.resource.group, azure.location, azure.provisioning_state
```

Find blob containers belonging to a specific Storage Account (backward traversal):

```dql-template
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| filter name == "<STORAGE_ACCOUNT_NAME>"
| traverse "*", "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_BLOBSERVICES_CONTAINERS", direction:backward
| fields name, id, azure.resource.group
```

Count blob containers per Storage Account:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_BLOBSERVICES_CONTAINERS"
| traverse "*", "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| fieldsAdd accountName = name
| summarize container_count = count(), by: {accountName}
| sort container_count desc
```

### File Shares

List all file shares:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_FILESERVICES_SHARES"
| fields name, id, azure.resource.group, azure.location, azure.provisioning_state
```

Find file shares belonging to a specific Storage Account:

```dql-template
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| filter name == "<STORAGE_ACCOUNT_NAME>"
| traverse "*", "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_FILESERVICES_SHARES", direction:backward
| fields name, id, azure.resource.group
```

Count file shares per Storage Account:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_FILESERVICES_SHARES"
| traverse "*", "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| fieldsAdd accountName = name
| summarize share_count = count(), by: {accountName}
| sort share_count desc
```

### Queue Services

List all storage queues:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_QUEUESERVICES_QUEUES"
| fields name, id, azure.resource.group, azure.location, azure.provisioning_state
```

Find queues belonging to a specific Storage Account:

```dql-template
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| filter name == "<STORAGE_ACCOUNT_NAME>"
| traverse "*", "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_QUEUESERVICES_QUEUES", direction:backward
| fields name, id, azure.resource.group
```

### Table Services

List all storage tables:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_TABLESERVICES_TABLES"
| fields name, id, azure.resource.group, azure.location, azure.provisioning_state
```

Find tables belonging to a specific Storage Account:

```dql-template
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| filter name == "<STORAGE_ACCOUNT_NAME>"
| traverse "*", "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_TABLESERVICES_TABLES", direction:backward
| fields name, id, azure.resource.group
```

### All Sub-Resources for a Storage Account

Find all storage services (blob, file, queue, table) for a specific account:

```dql-template
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_BLOBSERVICES_CONTAINERS",
    "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_FILESERVICES_SHARES",
    "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_QUEUESERVICES_QUEUES",
    "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_TABLESERVICES_TABLES"
| traverse "*", "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| filter name == "<STORAGE_ACCOUNT_NAME>"
| fieldsAdd accountName = name
| fields accountName, dt.traverse.history[0][id], type
| fieldsRename subResourceId = `dt.traverse.history[0][id]`
| sort type
```

## Managed Disks

List all managed disks:

```dql
smartscapeNodes "AZURE_MICROSOFT_COMPUTE_DISKS"
| fields name, id, azure.resource.group, azure.location, azure.provisioning_state
```

Find managed disks with SKU and size details:

```dql
smartscapeNodes "AZURE_MICROSOFT_COMPUTE_DISKS"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][sku][name],
    skuTier = azjson[configuration][sku][tier],
    diskSizeGB = azjson[configuration][properties][diskSizeGB],
    diskState = azjson[configuration][properties][diskState],
    osType = azjson[configuration][properties][osType]
| fields name, skuName, skuTier, diskSizeGB, diskState, osType,
    azure.resource.group, azure.location
```

Find unattached managed disks (potential cost waste):

```dql
smartscapeNodes "AZURE_MICROSOFT_COMPUTE_DISKS"
| parse azure.object, "JSON:azjson"
| fieldsAdd diskState = azjson[configuration][properties][diskState],
    diskSizeGB = azjson[configuration][properties][diskSizeGB],
    skuName = azjson[configuration][sku][name]
| filter diskState == "Unattached"
| fields name, diskState, diskSizeGB, skuName, azure.resource.group, azure.location
```

Summarize managed disks by SKU:

```dql
smartscapeNodes "AZURE_MICROSOFT_COMPUTE_DISKS"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][sku][name]
| summarize disk_count = count(), by: {skuName}
| sort disk_count desc
```

Find VMs and their attached disks (VM → Disks forward traversal):

```dql
smartscapeNodes "AZURE_MICROSOFT_COMPUTE_VIRTUALMACHINES"
| traverse "*", "AZURE_MICROSOFT_COMPUTE_DISKS"
| fieldsAdd sourceId = dt.traverse.history[0][id]
| parse azure.object, "JSON:azjson"
| fieldsAdd diskSizeGB = azjson[configuration][properties][diskSizeGB],
    skuName = azjson[configuration][sku][name]
| lookup [smartscapeNodes "AZURE_MICROSOFT_COMPUTE_VIRTUALMACHINES" | fields name, id], sourceField: sourceId, lookupField: id, prefix: "vm."
| fields vm.name, name, diskSizeGB, skuName, azure.resource.group
```

Find disks attached to AKS clusters (Disk → AKS backward traversal):

```dql
smartscapeNodes "AZURE_MICROSOFT_COMPUTE_DISKS"
| traverse "*", "AZURE_MICROSOFT_CONTAINERSERVICE_MANAGEDCLUSTERS"
| fieldsAdd sourceId = dt.traverse.history[0][id]
| lookup [smartscapeNodes "AZURE_MICROSOFT_COMPUTE_DISKS" | fields name, id], sourceField: sourceId, lookupField: id, prefix: "disk."
| fields disk.name, name, azure.resource.group
```

## Cross-Service Analysis

Count all storage resources by type:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS",
    "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_BLOBSERVICES_CONTAINERS",
    "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_FILESERVICES_SHARES",
    "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_QUEUESERVICES_QUEUES",
    "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_TABLESERVICES_TABLES",
    "AZURE_MICROSOFT_COMPUTE_DISKS"
| summarize total = count(), by: {type}
| sort total desc
```

Count storage resources by region:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS",
    "AZURE_MICROSOFT_COMPUTE_DISKS"
| summarize total = count(), by: {type, azure.location}
| sort azure.location, total desc
```

Find all storage resources in a specific resource group:

```dql-template
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS",
    "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_BLOBSERVICES_CONTAINERS",
    "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS_FILESERVICES_SHARES",
    "AZURE_MICROSOFT_COMPUTE_DISKS"
| filter azure.resource.group == "<RESOURCE_GROUP>"
| fields type, name, azure.location, azure.provisioning_state
```
