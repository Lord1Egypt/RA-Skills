# Azure Security & Compliance

Monitor security configurations and compliance across Azure resources including network security groups, storage accounts, encryption, key management, and public access detection.

## Table of Contents

- [NSG Rule Analysis](#nsg-rule-analysis)
- [NSG Blast Radius](#nsg-blast-radius)
- [Storage Account Security](#storage-account-security)
- [Disk Encryption](#disk-encryption)
- [Key Vault & Managed Identity](#key-vault--managed-identity)
- [Public Access Detection](#public-access-detection)
- [Service Bus Security](#service-bus-security)
- [WAF Security Posture](#waf-security-posture)
- [Network Security](#network-security)

## NSG Rule Analysis

NSG security rules are stored in `azure.object` as `properties.securityRules[]` arrays. Since these are arrays within the JSON, convert to strings with `toString()` and use `contains()` to search for risky patterns.

Find NSGs with **any inbound rule open to the internet** (source `0.0.0.0/0` or `*`):

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_NETWORKSECURITYGROUPS"
| parse azure.object, "JSON:azjson"
| fieldsAdd rules = toString(azjson[configuration][properties][securityRules])
| filter contains(rules, "0.0.0.0/0") or contains(rules, "\"sourceAddressPrefix\":\"*\"")
| fields name, id, azure.resource.group, azure.location, rules
```

Count internet-open NSGs per resource group:

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_NETWORKSECURITYGROUPS"
| parse azure.object, "JSON:azjson"
| fieldsAdd rules = toString(azjson[configuration][properties][securityRules])
| filter contains(rules, "0.0.0.0/0") or contains(rules, "\"sourceAddressPrefix\":\"*\"")
| summarize open_nsg_count = count(), by: {azure.resource.group}
```

Find NSGs with rules allowing **SSH (port 22) from the internet** — a common audit finding:

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_NETWORKSECURITYGROUPS"
| parse azure.object, "JSON:azjson"
| fieldsAdd rules = toString(azjson[configuration][properties][securityRules])
| filter contains(rules, "0.0.0.0/0") or contains(rules, "\"sourceAddressPrefix\":\"*\"")
| filter contains(rules, "\"destinationPortRange\":\"22\"")
| fields name, id, azure.resource.group, azure.location, rules
```

Find NSGs with rules allowing **RDP (port 3389) from the internet**:

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_NETWORKSECURITYGROUPS"
| parse azure.object, "JSON:azjson"
| fieldsAdd rules = toString(azjson[configuration][properties][securityRules])
| filter contains(rules, "0.0.0.0/0") or contains(rules, "\"sourceAddressPrefix\":\"*\"")
| filter contains(rules, "\"destinationPortRange\":\"3389\"")
| fields name, id, azure.resource.group, azure.location, rules
```

Find NSGs with rules allowing **SQL (port 1433) from the internet**:

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_NETWORKSECURITYGROUPS"
| parse azure.object, "JSON:azjson"
| fieldsAdd rules = toString(azjson[configuration][properties][securityRules])
| filter contains(rules, "0.0.0.0/0") or contains(rules, "\"sourceAddressPrefix\":\"*\"")
| filter contains(rules, "\"destinationPortRange\":\"1433\"")
| fields name, id, azure.resource.group, azure.location, rules
```

Find NSGs with rules allowing **PostgreSQL (port 5432) from the internet**:

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_NETWORKSECURITYGROUPS"
| parse azure.object, "JSON:azjson"
| fieldsAdd rules = toString(azjson[configuration][properties][securityRules])
| filter contains(rules, "0.0.0.0/0") or contains(rules, "\"sourceAddressPrefix\":\"*\"")
| filter contains(rules, "\"destinationPortRange\":\"5432\"")
| fields name, id, azure.resource.group, azure.location, rules
```

Find NSGs that are **wide open** — all traffic allowed from the internet (protocol `*` combined with source `*` or `0.0.0.0/0`):

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_NETWORKSECURITYGROUPS"
| parse azure.object, "JSON:azjson"
| fieldsAdd rules = toString(azjson[configuration][properties][securityRules])
| filter contains(rules, "\"sourceAddressPrefix\":\"*\"") or contains(rules, "0.0.0.0/0")
| filter contains(rules, "\"protocol\":\"*\"")
| filter contains(rules, "\"access\":\"Allow\"")
| fields name, id, azure.resource.group, azure.location, rules
```

Audit **egress rules** — count NSGs with unrestricted outbound traffic:

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_NETWORKSECURITYGROUPS"
| parse azure.object, "JSON:azjson"
| fieldsAdd rules = toString(azjson[configuration][properties][securityRules])
| filter contains(rules, "\"direction\":\"Outbound\"")
| filter contains(rules, "\"destinationAddressPrefix\":\"*\"") or contains(rules, "0.0.0.0/0")
| filter contains(rules, "\"access\":\"Allow\"")
| summarize egress_open_count = count(), by: {azure.resource.group}
```

> **Tip:** The `securityRules` field is a JSON array. To detect specific open ports (e.g., Redis 6379, MongoDB 27017), combine the internet source filter with a port-specific string match: `contains(rules, "\"destinationPortRange\":\"6379\"")`.

## NSG Blast Radius

Find NSGs associated with the most resources. NSGs can be attached to NICs and subnets. Use backward traversals to find which compute resources are affected.

NSGs with the most NIC associations:

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_NETWORKINTERFACES"
| traverse "*", "AZURE_MICROSOFT_NETWORK_NETWORKSECURITYGROUPS"
| summarize nic_count = count(), by: {name, id, azure.resource.group}
| sort nic_count desc
| limit 20
```

NSGs associated via subnets:

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_VIRTUALNETWORKS_SUBNETS"
| traverse "*", "AZURE_MICROSOFT_NETWORK_NETWORKSECURITYGROUPS"
| summarize subnet_count = count(), by: {name, id, azure.resource.group}
| sort subnet_count desc
```

NSGs associated with VMSS (often AKS-managed):

```dql
smartscapeNodes "AZURE_MICROSOFT_COMPUTE_VIRTUALMACHINESCALESETS"
| traverse "*", "AZURE_MICROSOFT_NETWORK_NETWORKSECURITYGROUPS"
| summarize vmss_count = count(), by: {name, id, azure.resource.group}
| sort vmss_count desc
```

List all NSGs (for finding unused ones, cross-reference with association queries above):

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_NETWORKSECURITYGROUPS"
| fields name, id, azure.resource.group, azure.location
```

## Storage Account Security

Audit **HTTPS enforcement** across all storage accounts:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd httpsOnly = azjson[configuration][properties][supportsHttpsTrafficOnly]
| summarize account_count = count(), by: {httpsOnly}
```

Find storage accounts with **public blob access enabled**:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd allowBlobPublicAccess = azjson[configuration][properties][allowBlobPublicAccess]
| filter allowBlobPublicAccess == true
| fields name, id, azure.resource.group, azure.location
```

Audit **encryption** settings across storage accounts:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd keySource = azjson[configuration][properties][encryption][keySource],
            blobEncryption = azjson[configuration][properties][encryption][services][blob][enabled]
| summarize account_count = count(), by: {keySource, blobEncryption}
```

Audit **TLS version** across storage accounts:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd minTlsVersion = azjson[configuration][properties][minimumTlsVersion]
| summarize account_count = count(), by: {minTlsVersion}
```

Find storage accounts with **no TLS 1.2 minimum** (using legacy TLS):

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd minTlsVersion = azjson[configuration][properties][minimumTlsVersion]
| filter minTlsVersion != "TLS1_2"
| fields name, id, minTlsVersion, azure.resource.group, azure.location
```

Summarize storage account **security posture** — HTTPS, public access, encryption, TLS:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd
    httpsOnly = azjson[configuration][properties][supportsHttpsTrafficOnly],
    allowBlobPublicAccess = azjson[configuration][properties][allowBlobPublicAccess],
    keySource = azjson[configuration][properties][encryption][keySource],
    minTlsVersion = azjson[configuration][properties][minimumTlsVersion]
| fields name, httpsOnly, allowBlobPublicAccess, keySource, minTlsVersion, azure.resource.group
```

Audit storage account **network access rules**:

```dql
smartscapeNodes "AZURE_MICROSOFT_STORAGE_STORAGEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd defaultAction = azjson[configuration][properties][networkAcls][defaultAction]
| summarize account_count = count(), by: {defaultAction}
```

## Disk Encryption

Summarize managed disk encryption status by SKU:

```dql
smartscapeNodes "AZURE_MICROSOFT_COMPUTE_DISKS"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][sku][name],
            diskState = azjson[configuration][properties][diskState],
            encryptionType = azjson[configuration][properties][encryption][type]
| summarize disk_count = count(), by: {encryptionType, skuName}
| sort disk_count desc
```

List managed disks with their encryption details:

```dql
smartscapeNodes "AZURE_MICROSOFT_COMPUTE_DISKS"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][sku][name],
            diskSizeGB = azjson[configuration][properties][diskSizeGB],
            encryptionType = azjson[configuration][properties][encryption][type]
| fields name, skuName, diskSizeGB, encryptionType, azure.resource.group, azure.location
```

## Key Vault & Managed Identity

Audit Key Vault security configuration — RBAC authorization, soft delete, purge protection, and public access:

```dql
smartscapeNodes "AZURE_MICROSOFT_KEYVAULT_VAULTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd
    rbacAuth = azjson[configuration][properties][enableRbacAuthorization],
    softDelete = azjson[configuration][properties][enableSoftDelete],
    softDeleteDays = azjson[configuration][properties][softDeleteRetentionInDays],
    purgeProtection = azjson[configuration][properties][enablePurgeProtection],
    publicAccess = azjson[configuration][properties][publicNetworkAccess]
| fields name, rbacAuth, softDelete, softDeleteDays, purgeProtection, publicAccess, azure.resource.group
```

Find Key Vaults **without RBAC authorization** (using legacy access policies):

```dql
smartscapeNodes "AZURE_MICROSOFT_KEYVAULT_VAULTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd rbacAuth = azjson[configuration][properties][enableRbacAuthorization]
| filter rbacAuth != true
| fields name, id, azure.resource.group, azure.location
```

Find Key Vaults with **public access enabled**:

```dql
smartscapeNodes "AZURE_MICROSOFT_KEYVAULT_VAULTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd publicAccess = azjson[configuration][properties][publicNetworkAccess]
| filter publicAccess == "Enabled"
| fields name, id, azure.resource.group, azure.location
```

List user-assigned managed identities:

```dql
smartscapeNodes "AZURE_MICROSOFT_MANAGEDIDENTITY_USERASSIGNEDIDENTITIES"
| fields name, id, azure.resource.group, azure.location, azure.subscription
```

## Public Access Detection

Find VMs with public IP addresses (via NIC → IP Config, parsing `azure.object` for `publicIPAddress`):

```dql
smartscapeNodes "AZURE_MICROSOFT_COMPUTE_VIRTUALMACHINES"
| traverse "*", "AZURE_MICROSOFT_NETWORK_NETWORKINTERFACES"
| traverse "*", "AZURE_MICROSOFT_NETWORK_NETWORKINTERFACES_IPCONFIGURATIONS"
| parse azure.object, "JSON:azjson"
| fieldsAdd publicIpId = azjson[configuration][properties][publicIPAddress][id]
| filter isNotNull(publicIpId)
| fields name, id, publicIpId, azure.resource.group
```

Find SQL servers with **public network access enabled**:

```dql
smartscapeNodes "AZURE_MICROSOFT_SQL_SERVERS"
| parse azure.object, "JSON:azjson"
| fieldsAdd publicAccess = azjson[configuration][properties][publicNetworkAccess]
| filter publicAccess == "Enabled"
| fields name, id, azure.resource.group, azure.location
```

Identify internet-facing load balancers (via public frontend IP configurations):

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_LOADBALANCERS"
| traverse "*", "AZURE_MICROSOFT_NETWORK_LOADBALANCERS_FRONTENDIPCONFIGURATIONS"
| parse azure.object, "JSON:azjson"
| fieldsAdd publicIpId = azjson[configuration][properties][publicIPAddress][id]
| filter isNotNull(publicIpId)
| fields name, id, publicIpId, azure.resource.group
```

Find App Service / Function apps with **public network access**:

```dql
smartscapeNodes "AZURE_MICROSOFT_WEB_SITES"
| parse azure.object, "JSON:azjson"
| fieldsAdd publicAccess = azjson[configuration][properties][publicNetworkAccess],
            httpsOnly = azjson[configuration][properties][httpsOnly]
| filter publicAccess == "Enabled"
| fields name, id, publicAccess, httpsOnly, azure.resource.group, azure.location
```

Find Container Apps with **external ingress**:

```dql
smartscapeNodes "AZURE_MICROSOFT_APP_CONTAINERAPPS"
| parse azure.object, "JSON:azjson"
| fieldsAdd externalIngress = azjson[configuration][properties][configuration][ingress][external],
            fqdn = azjson[configuration][properties][configuration][ingress][fqdn]
| filter externalIngress == true
| fields name, fqdn, azure.resource.group, azure.location
```

Find Cosmos DB accounts with **VNet filtering disabled**:

```dql
smartscapeNodes "AZURE_MICROSOFT_DOCUMENTDB_DATABASEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd vnetFilter = azjson[configuration][properties][isVirtualNetworkFilterEnabled]
| filter vnetFilter != true
| fields name, id, azure.resource.group, azure.location
```

## Service Bus Security

Check Service Bus namespaces for security configuration:

```dql
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES"
| parse azure.object, "JSON:azjson"
| fieldsAdd minimumTlsVersion = azjson[configuration][properties][minimumTlsVersion],
    publicNetworkAccess = azjson[configuration][properties][publicNetworkAccess],
    disableLocalAuth = azjson[configuration][properties][disableLocalAuth]
| filter minimumTlsVersion != "1.2"
    or publicNetworkAccess == "Enabled"
    or disableLocalAuth == false
| fields name, minimumTlsVersion, publicNetworkAccess, disableLocalAuth,
    azure.resource.group, azure.location
```

This query finds Service Bus namespaces with any security concern: old TLS, public access enabled, or local auth not disabled.

## WAF Security Posture

Find Application Gateways with WAF-capable SKU that have WAF disabled or in Detection mode:

```dql
smartscapeNodes "AZURE_MICROSOFT_NETWORK_APPLICATIONGATEWAYS"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuTier = azjson[configuration][properties][sku][tier],
    wafEnabled = azjson[configuration][properties][webApplicationFirewallConfiguration][enabled],
    wafMode = azjson[configuration][properties][webApplicationFirewallConfiguration][firewallMode]
| filter contains(toString(skuTier), "WAF")
    and (wafEnabled == false or isNull(wafEnabled) or wafMode == "Detection")
| fields name, skuTier, wafEnabled, wafMode, azure.resource.group, azure.location
```

This query identifies gateways that are paying for WAF capability but not fully utilizing it — either WAF is disabled entirely or running in Detection mode (logging only, not blocking).

## Network Security

Audit **TLS version** across all services that expose it:

SQL Servers:

```dql
smartscapeNodes "AZURE_MICROSOFT_SQL_SERVERS"
| parse azure.object, "JSON:azjson"
| fieldsAdd minTls = azjson[configuration][properties][minimalTlsVersion]
| summarize server_count = count(), by: {minTls}
```

Redis Cache:

```dql
smartscapeNodes "AZURE_MICROSOFT_CACHE_REDIS"
| parse azure.object, "JSON:azjson"
| fieldsAdd minTls = azjson[configuration][properties][minimumTlsVersion],
            nonSslPort = azjson[configuration][properties][enableNonSslPort]
| fields name, minTls, nonSslPort, azure.resource.group, azure.location
```

Event Hub namespaces:

```dql
smartscapeNodes "AZURE_MICROSOFT_EVENTHUB_NAMESPACES"
| parse azure.object, "JSON:azjson"
| fieldsAdd minTls = azjson[configuration][properties][minimumTlsVersion]
| summarize namespace_count = count(), by: {minTls}
```

Cosmos DB:

```dql
smartscapeNodes "AZURE_MICROSOFT_DOCUMENTDB_DATABASEACCOUNTS"
| parse azure.object, "JSON:azjson"
| fieldsAdd minTls = azjson[configuration][properties][minimalTlsVersion]
| fields name, minTls, azure.resource.group, azure.location
```

App Service / Functions HTTPS-only enforcement:

```dql
smartscapeNodes "AZURE_MICROSOFT_WEB_SITES"
| parse azure.object, "JSON:azjson"
| fieldsAdd httpsOnly = azjson[configuration][properties][httpsOnly]
| summarize site_count = count(), by: {httpsOnly}
```

Find App Services **not enforcing HTTPS**:

```dql
smartscapeNodes "AZURE_MICROSOFT_WEB_SITES"
| parse azure.object, "JSON:azjson"
| fieldsAdd httpsOnly = azjson[configuration][properties][httpsOnly]
| filter httpsOnly != true
| fields name, id, azure.resource.group, azure.location
```

API Management VNet integration audit:

```dql
smartscapeNodes "AZURE_MICROSOFT_APIMANAGEMENT_SERVICE"
| parse azure.object, "JSON:azjson"
| fieldsAdd vnetType = azjson[configuration][properties][virtualNetworkType]
| fields name, vnetType, azure.resource.group, azure.location
```
