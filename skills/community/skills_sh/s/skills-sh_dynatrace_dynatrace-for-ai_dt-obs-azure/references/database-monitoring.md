# Azure Database Monitoring

Monitor and analyze Azure database services including Azure SQL, Cosmos DB, and Redis Cache.

## Table of Contents

- [Database Entity Types](#database-entity-types)
- [Azure SQL Monitoring](#azure-sql-monitoring)
- [Cosmos DB Monitoring](#cosmos-db-monitoring)
- [Redis Cache](#redis-cache)
- [Database Security](#database-security)
- [Cross-Service Analysis](#cross-service-analysis)

## Database Entity Types

All these types support the standard discovery pattern: `smartscapeNodes "<TYPE>" | fields name, id, azure.subscription, azure.resource.group, azure.location, ...`

| Entity Type | Description |
|---|---|
| `AZURE_MICROSOFT_SQL_SERVERS` | Azure SQL logical servers |
| `AZURE_MICROSOFT_SQL_SERVERS_DATABASES` | Azure SQL databases |
| `AZURE_MICROSOFT_CACHE_REDIS` | Azure Cache for Redis |
| `AZURE_MICROSOFT_CACHE_REDISENTERPRISE` | Azure Cache for Redis Enterprise |
| `AZURE_MICROSOFT_CACHE_REDISENTERPRISE_DATABASES` | Redis Enterprise databases |
| `AZURE_MICROSOFT_DOCUMENTDB_DATABASEACCOUNTS` | Cosmos DB accounts |
| `AZURE_MICROSOFT_DOCUMENTDB_DATABASEACCOUNTS_SQLDATABASES` | Cosmos DB SQL databases |

## Azure SQL Monitoring

List all SQL servers:

```dql
smartscapeNodes "AZURE_MICROSOFT_SQL_SERVERS"
| parse azure.object, "JSON:azjson"
| fieldsAdd fqdn = azjson[configuration][properties][fullyQualifiedDomainName],
    state = azjson[configuration][properties][state],
    version = azjson[configuration][properties][version],
    adminLogin = azjson[configuration][properties][administratorLogin]
| fields name, fqdn, state, version, adminLogin, azure.resource.group, azure.location
```

List all SQL databases with SKU and tier details:

```dql
smartscapeNodes "AZURE_MICROSOFT_SQL_SERVERS_DATABASES"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][sku][name],
    skuTier = azjson[configuration][sku][tier],
    skuCapacity = azjson[configuration][sku][capacity],
    status = azjson[configuration][properties][status],
    serviceObjective = azjson[configuration][properties][currentServiceObjectiveName],
    maxSizeBytes = azjson[configuration][properties][maxSizeBytes]
| fields name, skuName, skuTier, skuCapacity, status, serviceObjective, maxSizeBytes,
    azure.resource.group, azure.location
```

Find SQL databases by service tier:

```dql
smartscapeNodes "AZURE_MICROSOFT_SQL_SERVERS_DATABASES"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuTier = azjson[configuration][sku][tier]
| summarize db_count = count(), by: {skuTier}
| sort db_count desc
```

Find zone-redundant SQL databases:

```dql
smartscapeNodes "AZURE_MICROSOFT_SQL_SERVERS_DATABASES"
| parse azure.object, "JSON:azjson"
| fieldsAdd zoneRedundant = azjson[configuration][properties][zoneRedundant],
    skuTier = azjson[configuration][sku][tier]
| fields name, zoneRedundant, skuTier, azure.resource.group, azure.location
```

Find SQL databases belonging to a specific server (SQL Database → SQL Server backward traversal):

```dql-template
smartscapeNodes "AZURE_MICROSOFT_SQL_SERVERS"
| filter name == "<SQL_SERVER_NAME>"
| traverse "*", "AZURE_MICROSOFT_SQL_SERVERS_DATABASES", direction:backward
| fields name, id, azure.resource.group
```

Analyze backup redundancy configuration:

```dql
smartscapeNodes "AZURE_MICROSOFT_SQL_SERVERS_DATABASES"
| parse azure.object, "JSON:azjson"
| fieldsAdd backupRedundancy = azjson[configuration][properties][currentBackupStorageRedundancy],
    skuTier = azjson[configuration][sku][tier]
| summarize db_count = count(), by: {backupRedundancy, skuTier}
| sort db_count desc
```

## Cosmos DB Monitoring

List Cosmos DB accounts with configuration details:

```dql
smartscapeNodes "AZURE_MICROSOFT_DOCUMENTDB_DATABASEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd accountKind = azjson[configuration][kind],
    apiTypes = azjson[configuration][properties][EnabledApiTypes],
    consistencyLevel = azjson[configuration][properties][consistencyPolicy][defaultConsistencyLevel],
    autoFailover = azjson[configuration][properties][enableAutomaticFailover],
    multiWrite = azjson[configuration][properties][enableMultipleWriteLocations],
    endpoint = azjson[configuration][properties][documentEndpoint]
| fields name, accountKind, apiTypes, consistencyLevel, autoFailover, multiWrite, endpoint,
    azure.resource.group, azure.location
```

Find serverless Cosmos DB accounts:

```dql
smartscapeNodes "AZURE_MICROSOFT_DOCUMENTDB_DATABASEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd capabilities = azjson[configuration][properties][capabilities]
| expand capabilities
| filter capabilities[name] == "EnableServerless"
| fields name, azure.resource.group, azure.location
```

Analyze Cosmos DB backup configuration:

```dql
smartscapeNodes "AZURE_MICROSOFT_DOCUMENTDB_DATABASEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd backupType = azjson[configuration][properties][backupPolicy][type],
    vnetFilter = azjson[configuration][properties][isVirtualNetworkFilterEnabled]
| fields name, backupType, vnetFilter, azure.resource.group, azure.location
```

## Redis Cache

List all Redis Cache instances with configuration:

```dql
smartscapeNodes "AZURE_MICROSOFT_CACHE_REDIS"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][properties][sku][name],
    skuFamily = azjson[configuration][properties][sku][family],
    skuCapacity = azjson[configuration][properties][sku][capacity],
    hostName = azjson[configuration][properties][hostName],
    redisVersion = azjson[configuration][properties][redisVersion],
    sslPort = azjson[configuration][properties][sslPort]
| fields name, skuName, skuFamily, skuCapacity, hostName, redisVersion, sslPort,
    azure.resource.group, azure.location
```

List Redis Enterprise clusters:

```dql
smartscapeNodes "AZURE_MICROSOFT_CACHE_REDISENTERPRISE"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][sku][name],
    skuCapacity = azjson[configuration][sku][capacity]
| fields name, skuName, skuCapacity, azure.resource.group, azure.location
```

Find Redis Enterprise databases:

```dql
smartscapeNodes "AZURE_MICROSOFT_CACHE_REDISENTERPRISE_DATABASES"
| fields name, id, azure.resource.group, azure.location, azure.provisioning_state
```

Check Redis non-SSL port status:

```dql
smartscapeNodes "AZURE_MICROSOFT_CACHE_REDIS"
| parse azure.object, "JSON:azjson"
| fieldsAdd enableNonSslPort = azjson[configuration][properties][enableNonSslPort],
    minimumTlsVersion = azjson[configuration][properties][minimumTlsVersion]
| fields name, enableNonSslPort, minimumTlsVersion, azure.resource.group
```

## Database Security

Find SQL servers with public network access enabled:

```dql
smartscapeNodes "AZURE_MICROSOFT_SQL_SERVERS"
| parse azure.object, "JSON:azjson"
| fieldsAdd publicAccess = azjson[configuration][properties][publicNetworkAccess],
    minTls = azjson[configuration][properties][minimalTlsVersion],
    outboundRestriction = azjson[configuration][properties][restrictOutboundNetworkAccess]
| fields name, publicAccess, minTls, outboundRestriction, azure.resource.group, azure.location
```

Analyze TLS versions across all database services:

```dql
smartscapeNodes "AZURE_MICROSOFT_SQL_SERVERS"
| parse azure.object, "JSON:azjson"
| fieldsAdd minTls = azjson[configuration][properties][minimalTlsVersion], service = "SQL Server"
| fields name, minTls, service
| append [
    smartscapeNodes "AZURE_MICROSOFT_CACHE_REDIS"
    | parse azure.object, "JSON:azjson"
    | fieldsAdd minTls = azjson[configuration][properties][minimumTlsVersion], service = "Redis"
    | fields name, minTls, service
  ]
| append [
    smartscapeNodes "AZURE_MICROSOFT_DOCUMENTDB_DATABASEACCOUNTS"
    | parse azure.object, "JSON:azjson"
    | fieldsAdd minTls = azjson[configuration][properties][minimalTlsVersion], service = "Cosmos DB"
    | fields name, minTls, service
  ]
| sort service, minTls
```

Find Redis instances with non-SSL port enabled (security risk):

```dql
smartscapeNodes "AZURE_MICROSOFT_CACHE_REDIS"
| parse azure.object, "JSON:azjson"
| fieldsAdd enableNonSslPort = azjson[configuration][properties][enableNonSslPort]
| filter enableNonSslPort == true
| fields name, azure.resource.group, azure.location
```

## Cross-Service Analysis

Count all database resources by type:

```dql
smartscapeNodes "AZURE_MICROSOFT_SQL_SERVERS", "AZURE_MICROSOFT_SQL_SERVERS_DATABASES",
    "AZURE_MICROSOFT_CACHE_REDIS", "AZURE_MICROSOFT_CACHE_REDISENTERPRISE",
    "AZURE_MICROSOFT_DOCUMENTDB_DATABASEACCOUNTS"
| summarize db_count = count(), by: {type}
| sort db_count desc
```

Count databases across regions:

```dql
smartscapeNodes "AZURE_MICROSOFT_SQL_SERVERS_DATABASES", "AZURE_MICROSOFT_CACHE_REDIS",
    "AZURE_MICROSOFT_DOCUMENTDB_DATABASEACCOUNTS"
| summarize db_count = count(), by: {type, azure.location}
| sort azure.location, db_count desc
```

Find all databases in a specific resource group:

```dql-template
smartscapeNodes "AZURE_MICROSOFT_SQL_SERVERS", "AZURE_MICROSOFT_SQL_SERVERS_DATABASES",
    "AZURE_MICROSOFT_CACHE_REDIS", "AZURE_MICROSOFT_DOCUMENTDB_DATABASEACCOUNTS"
| filter azure.resource.group == "<RESOURCE_GROUP>"
| fields type, name, azure.location, azure.provisioning_state
```
