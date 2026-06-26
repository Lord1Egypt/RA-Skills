# Azure Messaging & Integration

Monitor Azure Event Hubs, Service Bus, and messaging infrastructure.

## Table of Contents

- [Messaging & Integration Entity Types](#messaging--integration-entity-types)
- [Event Hubs](#event-hubs)
- [Service Bus](#service-bus)
  - [Namespace Inventory](#namespace-inventory-1)
  - [Zone Redundancy](#zone-redundancy-1)
  - [TLS Configuration](#tls-configuration-1)
  - [Public Network Access](#public-network-access)
  - [Topics](#topics)
  - [Subscriptions](#subscriptions)
  - [Queue Configuration](#queue-configuration)
  - [Namespace Traversals](#namespace-traversals)
  - [Dead-Letter Queue Detection](#dead-letter-queue-detection)
- [Cross-Service Analysis](#cross-service-analysis)

## Messaging & Integration Entity Types

All these types support the standard discovery pattern: `smartscapeNodes "<TYPE>" | fields name, id, azure.subscription, azure.resource.group, azure.location, ...`

| Entity Type | Description |
|---|---|
| `AZURE_MICROSOFT_EVENTHUB_NAMESPACES` | Event Hub namespaces |
| `AZURE_MICROSOFT_EVENTHUB_NAMESPACES_EVENTHUBS` | Individual Event Hubs within a namespace |
| `AZURE_MICROSOFT_SERVICEBUS_NAMESPACES` | Service Bus namespaces |
| `AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_QUEUES` | Service Bus queues |
| `AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_TOPICS` | Service Bus topics |
| `AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_TOPICS_SUBSCRIPTIONS` | Service Bus subscriptions |

## Event Hubs

### Namespace Inventory

List all Event Hub namespaces with configuration:

```dql
smartscapeNodes "AZURE_MICROSOFT_EVENTHUB_NAMESPACES"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][sku][name],
    skuTier = azjson[configuration][sku][tier],
    skuCapacity = azjson[configuration][sku][capacity],
    status = azjson[configuration][properties][status],
    kafkaEnabled = azjson[configuration][properties][kafkaEnabled],
    zoneRedundant = azjson[configuration][properties][zoneRedundant]
| fields name, skuName, skuTier, skuCapacity, status, kafkaEnabled, zoneRedundant,
    azure.resource.group, azure.location
```

Summarize Event Hub namespaces by SKU tier:

```dql
smartscapeNodes "AZURE_MICROSOFT_EVENTHUB_NAMESPACES"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][sku][name]
| summarize ns_count = count(), by: {skuName}
| sort ns_count desc
```

### Kafka Enablement

Find Kafka-enabled Event Hub namespaces:

```dql
smartscapeNodes "AZURE_MICROSOFT_EVENTHUB_NAMESPACES"
| parse azure.object, "JSON:azjson"
| fieldsAdd kafkaEnabled = azjson[configuration][properties][kafkaEnabled],
    skuName = azjson[configuration][sku][name]
| filter kafkaEnabled == true
| fields name, skuName, azure.resource.group, azure.location
```

### Throughput Units and Auto-Inflate

Analyze throughput unit allocation and auto-inflate configuration:

```dql
smartscapeNodes "AZURE_MICROSOFT_EVENTHUB_NAMESPACES"
| parse azure.object, "JSON:azjson"
| fieldsAdd throughputUnits = azjson[configuration][sku][capacity],
    autoInflate = azjson[configuration][properties][isAutoInflateEnabled],
    maxThroughputUnits = azjson[configuration][properties][maximumThroughputUnits]
| fields name, throughputUnits, autoInflate, maxThroughputUnits,
    azure.resource.group, azure.location
| sort throughputUnits desc
```

Find namespaces without auto-inflate (potential scaling risk):

```dql
smartscapeNodes "AZURE_MICROSOFT_EVENTHUB_NAMESPACES"
| parse azure.object, "JSON:azjson"
| fieldsAdd autoInflate = azjson[configuration][properties][isAutoInflateEnabled],
    throughputUnits = azjson[configuration][sku][capacity]
| filter autoInflate == false
| fields name, throughputUnits, azure.resource.group, azure.location
```

### Zone Redundancy

Find Event Hub namespaces that are not zone-redundant:

```dql
smartscapeNodes "AZURE_MICROSOFT_EVENTHUB_NAMESPACES"
| parse azure.object, "JSON:azjson"
| fieldsAdd zoneRedundant = azjson[configuration][properties][zoneRedundant],
    skuName = azjson[configuration][sku][name]
| filter zoneRedundant == false
| fields name, skuName, azure.resource.group, azure.location
```

### TLS Configuration

Check minimum TLS version across Event Hub namespaces:

```dql
smartscapeNodes "AZURE_MICROSOFT_EVENTHUB_NAMESPACES"
| parse azure.object, "JSON:azjson"
| fieldsAdd minimumTlsVersion = azjson[configuration][properties][minimumTlsVersion]
| summarize ns_count = count(), by: {minimumTlsVersion}
| sort minimumTlsVersion desc
```

Find namespaces with TLS version below 1.2:

```dql
smartscapeNodes "AZURE_MICROSOFT_EVENTHUB_NAMESPACES"
| parse azure.object, "JSON:azjson"
| fieldsAdd minimumTlsVersion = azjson[configuration][properties][minimumTlsVersion]
| filter minimumTlsVersion != "1.2"
| fields name, minimumTlsVersion, azure.resource.group, azure.location
```

### Event Hub Entities

List all individual Event Hubs:

```dql
smartscapeNodes "AZURE_MICROSOFT_EVENTHUB_NAMESPACES_EVENTHUBS"
| fields name, id, azure.resource.group, azure.location, azure.provisioning_state
```

Find Event Hubs belonging to a specific namespace (Event Hub → Namespace backward traversal):

```dql-template
smartscapeNodes "AZURE_MICROSOFT_EVENTHUB_NAMESPACES"
| filter name == "<NAMESPACE_NAME>"
| traverse "*", "AZURE_MICROSOFT_EVENTHUB_NAMESPACES_EVENTHUBS", direction:backward
| fields name, id, azure.resource.group
```

Count Event Hubs per namespace:

```dql
smartscapeNodes "AZURE_MICROSOFT_EVENTHUB_NAMESPACES_EVENTHUBS"
| traverse "*", "AZURE_MICROSOFT_EVENTHUB_NAMESPACES"
| fieldsAdd namespaceName = name
| summarize eh_count = count(), by: {namespaceName}
| sort eh_count desc
```

## Service Bus

### Namespace Inventory

List all Service Bus namespaces with configuration:

```dql
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][sku][name],
    skuTier = azjson[configuration][sku][tier],
    skuCapacity = azjson[configuration][sku][capacity],
    status = azjson[configuration][properties][status],
    zoneRedundant = azjson[configuration][properties][zoneRedundant],
    minimumTlsVersion = azjson[configuration][properties][minimumTlsVersion],
    disableLocalAuth = azjson[configuration][properties][disableLocalAuth]
| fields name, skuName, skuTier, skuCapacity, status, zoneRedundant, minimumTlsVersion, disableLocalAuth,
    azure.resource.group, azure.location
```

Summarize Service Bus namespaces by SKU tier:

```dql
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES"
| parse azure.object, "JSON:azjson"
| fieldsAdd skuName = azjson[configuration][sku][name]
| summarize ns_count = count(), by: {skuName}
| sort ns_count desc
```

### Zone Redundancy

Find Service Bus namespaces that are not zone-redundant:

```dql
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES"
| parse azure.object, "JSON:azjson"
| fieldsAdd zoneRedundant = azjson[configuration][properties][zoneRedundant],
    skuName = azjson[configuration][sku][name]
| filter zoneRedundant == false
| fields name, skuName, azure.resource.group, azure.location
```

### TLS Configuration

Check minimum TLS version across Service Bus namespaces:

```dql
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES"
| parse azure.object, "JSON:azjson"
| fieldsAdd minimumTlsVersion = azjson[configuration][properties][minimumTlsVersion]
| summarize ns_count = count(), by: {minimumTlsVersion}
| sort minimumTlsVersion desc
```

Find namespaces with TLS version below 1.2:

```dql
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES"
| parse azure.object, "JSON:azjson"
| fieldsAdd minimumTlsVersion = azjson[configuration][properties][minimumTlsVersion]
| filter minimumTlsVersion != "1.2"
| fields name, minimumTlsVersion, azure.resource.group, azure.location
```

### Public Network Access

Find Service Bus namespaces with public network access enabled:

```dql
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES"
| parse azure.object, "JSON:azjson"
| fieldsAdd publicNetworkAccess = azjson[configuration][properties][publicNetworkAccess]
| filter publicNetworkAccess == "Enabled"
| fields name, publicNetworkAccess, azure.resource.group, azure.location
```

### Topics

List all Service Bus topics:

```dql
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_TOPICS"
| fields name, id, azure.resource.group, azure.location, azure.provisioning_state
```

List topics with configuration details:

```dql
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_TOPICS"
| parse azure.object, "JSON:azjson"
| fieldsAdd maxSizeInMegabytes = azjson[configuration][properties][maxSizeInMegabytes],
    status = azjson[configuration][properties][status],
    enablePartitioning = azjson[configuration][properties][enablePartitioning],
    requiresDuplicateDetection = azjson[configuration][properties][requiresDuplicateDetection]
| fields name, maxSizeInMegabytes, status, enablePartitioning, requiresDuplicateDetection,
    azure.resource.group, azure.location
```

### Subscriptions

List all Service Bus subscriptions:

```dql
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_TOPICS_SUBSCRIPTIONS"
| fields name, id, azure.resource.group, azure.location, azure.provisioning_state
```

List subscriptions with configuration details:

```dql
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_TOPICS_SUBSCRIPTIONS"
| parse azure.object, "JSON:azjson"
| fieldsAdd maxDeliveryCount = azjson[configuration][properties][maxDeliveryCount],
    lockDuration = azjson[configuration][properties][lockDuration],
    deadLetteringOnMessageExpiration = azjson[configuration][properties][deadLetteringOnMessageExpiration],
    status = azjson[configuration][properties][status]
| fields name, maxDeliveryCount, lockDuration, deadLetteringOnMessageExpiration, status,
    azure.resource.group, azure.location
```

### Queue Configuration

List all Service Bus queues:

```dql
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_QUEUES"
| fields name, id, azure.resource.group, azure.location, azure.provisioning_state
```

List Service Bus queues with configuration:

```dql
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_QUEUES"
| parse azure.object, "JSON:azjson"
| fieldsAdd maxSizeInMegabytes = azjson[configuration][properties][maxSizeInMegabytes],
    status = azjson[configuration][properties][status],
    enablePartitioning = azjson[configuration][properties][enablePartitioning],
    requiresDuplicateDetection = azjson[configuration][properties][requiresDuplicateDetection],
    deadLetteringOnMessageExpiration = azjson[configuration][properties][deadLetteringOnMessageExpiration],
    maxDeliveryCount = azjson[configuration][properties][maxDeliveryCount],
    lockDuration = azjson[configuration][properties][lockDuration]
| fields name, maxSizeInMegabytes, status, enablePartitioning, requiresDuplicateDetection,
    deadLetteringOnMessageExpiration, maxDeliveryCount, lockDuration,
    azure.resource.group, azure.location
```

Find queues by name pattern:

```dql-template
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_QUEUES"
| filter contains(name, "<PATTERN>")
| fields name, id, azure.resource.group, azure.location
```

### Namespace Traversals

Find queues belonging to a specific Service Bus namespace (Queue → Namespace backward traversal):

```dql-template
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES"
| filter name == "<NAMESPACE_NAME>"
| traverse "*", "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_QUEUES", direction:backward
| fields name, id, azure.resource.group
```

Find topics belonging to a specific Service Bus namespace (Topic → Namespace backward traversal):

```dql-template
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES"
| filter name == "<NAMESPACE_NAME>"
| traverse "*", "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_TOPICS", direction:backward
| fields name, id, azure.resource.group
```

Count queues per namespace:

```dql
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_QUEUES"
| traverse "*", "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES"
| fieldsAdd namespaceName = name
| summarize queue_count = count(), by: {namespaceName}
| sort queue_count desc
```

Count topics per namespace:

```dql
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_TOPICS"
| traverse "*", "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES"
| fieldsAdd namespaceName = name
| summarize topic_count = count(), by: {namespaceName}
| sort topic_count desc
```

Count subscriptions per topic:

```dql
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_TOPICS_SUBSCRIPTIONS"
| traverse "*", "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_TOPICS"
| fieldsAdd topicName = name
| summarize subscription_count = count(), by: {topicName}
| sort subscription_count desc
```

### Dead-Letter Queue Detection

Find queues with dead-lettering on message expiration enabled:

```dql
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_QUEUES"
| parse azure.object, "JSON:azjson"
| fieldsAdd deadLetteringOnMessageExpiration = azjson[configuration][properties][deadLetteringOnMessageExpiration]
| filter deadLetteringOnMessageExpiration == true
| fields name, azure.resource.group, azure.location
```

Find subscriptions with dead-lettering on message expiration enabled:

```dql
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_TOPICS_SUBSCRIPTIONS"
| parse azure.object, "JSON:azjson"
| fieldsAdd deadLetteringOnMessageExpiration = azjson[configuration][properties][deadLetteringOnMessageExpiration]
| filter deadLetteringOnMessageExpiration == true
| fields name, azure.resource.group, azure.location
```

Find queues with low max delivery count (messages reach dead-letter faster):

```dql
smartscapeNodes "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_QUEUES"
| parse azure.object, "JSON:azjson"
| fieldsAdd maxDeliveryCount = azjson[configuration][properties][maxDeliveryCount],
    deadLetteringOnMessageExpiration = azjson[configuration][properties][deadLetteringOnMessageExpiration]
| filter maxDeliveryCount <= 3
| fields name, maxDeliveryCount, deadLetteringOnMessageExpiration, azure.resource.group, azure.location
```

## Cross-Service Analysis

Count all messaging resources by type:

```dql
smartscapeNodes "AZURE_MICROSOFT_EVENTHUB_NAMESPACES", "AZURE_MICROSOFT_EVENTHUB_NAMESPACES_EVENTHUBS",
    "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES", "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_QUEUES",
    "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_TOPICS", "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_TOPICS_SUBSCRIPTIONS"
| summarize total = count(), by: {type}
| sort total desc
```

Count messaging resources by region:

```dql
smartscapeNodes "AZURE_MICROSOFT_EVENTHUB_NAMESPACES", "AZURE_MICROSOFT_EVENTHUB_NAMESPACES_EVENTHUBS",
    "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES", "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_QUEUES",
    "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_TOPICS", "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES_TOPICS_SUBSCRIPTIONS"
| summarize total = count(), by: {type, azure.location}
| sort azure.location, total desc
```

Filter messaging resources to a specific subscription:

```dql-template
smartscapeNodes "AZURE_MICROSOFT_EVENTHUB_NAMESPACES", "AZURE_MICROSOFT_SERVICEBUS_NAMESPACES"
| filter azure.subscription == "<SUBSCRIPTION_ID>"
| fields type, name, azure.resource.group, azure.location
```
