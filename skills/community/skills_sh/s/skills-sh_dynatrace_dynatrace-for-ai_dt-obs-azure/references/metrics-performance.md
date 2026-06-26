# Azure Metrics & Performance

DQL timeseries patterns for Azure Monitor-sourced metrics. Use during investigation to determine whether a resource is saturated, erroring, or slow.

## Table of Contents

- [Query Template](#query-template)
- [VM Metrics](#vm-metrics)
- [Azure SQL Metrics](#azure-sql-metrics)
- [Storage Account Metrics](#storage-account-metrics)
- [Event Hub Metrics](#event-hub-metrics)
- [Service Bus Metrics](#service-bus-metrics)
- [Load Balancer Metrics](#load-balancer-metrics)
- [App Service / Functions Metrics](#app-service--functions-metrics)
- [AKS (Managed Cluster) Metrics](#aks-managed-cluster-metrics)
- [Cosmos DB Metrics](#cosmos-db-metrics)
- [Redis Cache Metrics](#redis-cache-metrics)
- [Application Gateway Metrics](#application-gateway-metrics)
- [Combining Entity Queries with Metrics](#combining-entity-queries-with-metrics)
- [Metric Availability Note](#metric-availability-note)

## Query Template

Azure metrics in Dynatrace follow the naming convention:

```
cloud.azure.<resource_provider_path>.<MetricName>
```

Where `<resource_provider_path>` is `<provider_namespace>.<resource_type>` (lowercase, dots separating hierarchy levels):

| Resource provider path | Service |
|---|---|
| `microsoft_compute.virtualmachines` | Virtual Machines |
| `microsoft_sql.servers.databases` | Azure SQL Databases |
| `microsoft_storage.storageaccounts` | Storage Accounts |
| `microsoft_network.loadbalancers` | Load Balancers |
| `microsoft_eventhub.namespaces` | Event Hub Namespaces |
| `microsoft_servicebus.namespaces` | Service Bus Namespaces |
| `microsoft_web.sites` | App Service / Functions |
| `microsoft_containerservice.managedclusters` | AKS Managed Clusters |
| `microsoft_documentdb.databaseaccounts` | Cosmos DB Accounts |
| `microsoft_cache.redis` | Redis Cache |
| `microsoft_cache.redisenterprise` | Redis Enterprise |
| `microsoft_network.applicationgateways` | Application Gateways |

The `dt.smartscape_source.id` dimension splits results by Dynatrace entity. Use it in the `by:` clause and `filter` to scope metrics to a specific resource.

```dql-template
timeseries cpu = avg(cloud.azure.microsoft_compute.virtualmachines.<METRIC_NAME>),
  by: { dt.smartscape_source.id },
  from: <PROBLEM_START - 30m>, to: <PROBLEM_END + 15m>
| filter dt.smartscape_source.id == toSmartscapeId("<ROOT_CAUSE_ENTITY_ID>")
```

Replace `<METRIC_NAME>` with the metric from the tables below, and `<ROOT_CAUSE_ENTITY_ID>` with the Dynatrace entity ID (e.g., `AZURE_MICROSOFT_COMPUTE_VIRTUALMACHINES-2B0D33F11CE649F4`). Omit the `| filter` clause to get all instances of that metric.

> **Time windows:** The template above uses `<PROBLEM_START>` and `<PROBLEM_END>` for scoping queries to a specific incident window. The per-service examples below use `from: now()-1h` for simplicity — substitute your incident timestamps when investigating a specific problem.

---

## VM Metrics

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.azure.microsoft_compute.virtualmachines.PercentageCPU` | CPU utilization | % | > 85% sustained |
| `cloud.azure.microsoft_compute.virtualmachines.AvailableMemoryBytes` | Available memory | Bytes | Trending toward 0 |
| `cloud.azure.microsoft_compute.virtualmachines.DiskReadBytes` | Disk read throughput | Bytes/sec | Spike vs baseline |
| `cloud.azure.microsoft_compute.virtualmachines.DiskWriteBytes` | Disk write throughput | Bytes/sec | Spike vs baseline |
| `cloud.azure.microsoft_compute.virtualmachines.NetworkInTotal` | Inbound network traffic | Bytes | Spike or drop vs baseline |
| `cloud.azure.microsoft_compute.virtualmachines.NetworkOutTotal` | Outbound network traffic | Bytes | Spike or drop vs baseline |

Check CPU utilization for a specific VM:

```dql-template
timeseries cpu = avg(cloud.azure.microsoft_compute.virtualmachines.PercentageCPU),
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<ROOT_CAUSE_ENTITY_ID>")
```

Check available memory (low values indicate memory pressure):

```dql-template
timeseries mem = avg(cloud.azure.microsoft_compute.virtualmachines.AvailableMemoryBytes),
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<ROOT_CAUSE_ENTITY_ID>")
```

---

## Azure SQL Metrics

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.azure.microsoft_sql.servers.databases.cpu_percent` | Database CPU utilization | % | > 85% sustained |
| `cloud.azure.microsoft_sql.servers.databases.dtu_consumption_percent` | DTU consumption percentage | % | > 90% sustained |
| `cloud.azure.microsoft_sql.servers.databases.storage_percent` | Storage space used | % | > 85% (plan expansion) |
| `cloud.azure.microsoft_sql.servers.databases.deadlock` | Deadlock count | Count | > 0 during incident |
| `cloud.azure.microsoft_sql.servers.databases.connection_failed` | Failed connections | Count | > 0 during incident |

Check CPU and DTU consumption for a specific SQL database:

```dql-template
timeseries { cpu = avg(cloud.azure.microsoft_sql.servers.databases.cpu_percent),
             dtu = avg(cloud.azure.microsoft_sql.servers.databases.dtu_consumption_percent) },
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<SQL_DB_ENTITY_ID>")
```

Check storage percentage and deadlocks:

```dql-template
timeseries { storage = avg(cloud.azure.microsoft_sql.servers.databases.storage_percent),
             deadlocks = sum(cloud.azure.microsoft_sql.servers.databases.deadlock) },
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<SQL_DB_ENTITY_ID>")
```

---

## Storage Account Metrics

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.azure.microsoft_storage.storageaccounts.UsedCapacity` | Total storage used | Bytes | Trending toward account limit |
| `cloud.azure.microsoft_storage.storageaccounts.Ingress` | Data ingress | Bytes | Spike vs baseline |
| `cloud.azure.microsoft_storage.storageaccounts.Egress` | Data egress | Bytes | Spike vs baseline (cost impact) |
| `cloud.azure.microsoft_storage.storageaccounts.Transactions` | Transaction count | Count | Spike vs baseline |
| `cloud.azure.microsoft_storage.storageaccounts.Availability` | Service availability | % | < 100% indicates issues |

Check ingress, egress, and transactions for a storage account:

```dql-template
timeseries { ingress = sum(cloud.azure.microsoft_storage.storageaccounts.Ingress),
             egress = sum(cloud.azure.microsoft_storage.storageaccounts.Egress),
             txn = sum(cloud.azure.microsoft_storage.storageaccounts.Transactions) },
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<STORAGE_ENTITY_ID>")
```

Check availability:

```dql-template
timeseries avail = avg(cloud.azure.microsoft_storage.storageaccounts.Availability),
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<STORAGE_ENTITY_ID>")
```

---

## Event Hub Metrics

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.azure.microsoft_eventhub.namespaces.IncomingMessages` | Messages received | Count | Drop vs baseline (upstream issue) |
| `cloud.azure.microsoft_eventhub.namespaces.OutgoingMessages` | Messages delivered | Count | Drop vs baseline (consumer issue) |
| `cloud.azure.microsoft_eventhub.namespaces.IncomingBytes` | Ingress bytes | Bytes | Near throughput unit limit |
| `cloud.azure.microsoft_eventhub.namespaces.ThrottledRequests` | Throttled requests | Count | > 0 (throughput limit hit) |

Check message flow and throttling:

```dql-template
timeseries { incoming = sum(cloud.azure.microsoft_eventhub.namespaces.IncomingMessages),
             outgoing = sum(cloud.azure.microsoft_eventhub.namespaces.OutgoingMessages),
             throttled = sum(cloud.azure.microsoft_eventhub.namespaces.ThrottledRequests) },
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<EVENTHUB_ENTITY_ID>")
```

---

## Service Bus Metrics

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.azure.microsoft_servicebus.namespaces.IncomingMessages` | Messages received | Count | Drop vs baseline (upstream issue) |
| `cloud.azure.microsoft_servicebus.namespaces.OutgoingMessages` | Messages delivered | Count | Drop vs baseline (consumer issue) |
| `cloud.azure.microsoft_servicebus.namespaces.IncomingRequests` | Total incoming requests | Count | Spike vs baseline |
| `cloud.azure.microsoft_servicebus.namespaces.SuccessfulRequests` | Successful requests | Count | Drop vs baseline |
| `cloud.azure.microsoft_servicebus.namespaces.ServerErrors` | Server errors (5xx) | Count | > 0 during incident |
| `cloud.azure.microsoft_servicebus.namespaces.UserErrors` | User errors (4xx) | Count | Spike vs baseline (bad messages) |
| `cloud.azure.microsoft_servicebus.namespaces.ThrottledRequests` | Throttled requests | Count | > 0 (throughput limit hit) |
| `cloud.azure.microsoft_servicebus.namespaces.ActiveMessages` | Active messages in queue/topic | Count | Growing backlog |
| `cloud.azure.microsoft_servicebus.namespaces.DeadletteredMessages` | Dead-lettered messages | Count | > 0 (poison messages) |
| `cloud.azure.microsoft_servicebus.namespaces.ScheduledMessages` | Scheduled messages | Count | Context-dependent |
| `cloud.azure.microsoft_servicebus.namespaces.Size` | Size of queue/topic in bytes | Bytes | Near max size |

Check message flow and throttling:

```dql-template
timeseries { incoming = sum(cloud.azure.microsoft_servicebus.namespaces.IncomingMessages),
             outgoing = sum(cloud.azure.microsoft_servicebus.namespaces.OutgoingMessages),
             throttled = sum(cloud.azure.microsoft_servicebus.namespaces.ThrottledRequests) },
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<SERVICEBUS_ENTITY_ID>")
```

Check dead-letter accumulation:

```dql-template
timeseries { deadLettered = sum(cloud.azure.microsoft_servicebus.namespaces.DeadletteredMessages),
             active = sum(cloud.azure.microsoft_servicebus.namespaces.ActiveMessages) },
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<SERVICEBUS_ENTITY_ID>")
```

Check server and user errors:

```dql-template
timeseries { serverErrors = sum(cloud.azure.microsoft_servicebus.namespaces.ServerErrors),
             userErrors = sum(cloud.azure.microsoft_servicebus.namespaces.UserErrors),
             requests = sum(cloud.azure.microsoft_servicebus.namespaces.IncomingRequests) },
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<SERVICEBUS_ENTITY_ID>")
```

> **Important:** Non-zero `DeadletteredMessages` indicates poison messages that failed processing. Cross-reference with the dead-letter analysis queries in [messaging-integration.md](messaging-integration.md) to identify root causes.

---

## Load Balancer Metrics

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.azure.microsoft_network.loadbalancers.ByteCount` | Bytes processed | Bytes | Near throughput limit |
| `cloud.azure.microsoft_network.loadbalancers.PacketCount` | Packets processed | Count | Spike vs baseline |
| `cloud.azure.microsoft_network.loadbalancers.DipAvailability` | Backend pool health (data path) | % | < 100% (unhealthy backends) |
| `cloud.azure.microsoft_network.loadbalancers.VipAvailability` | Frontend data path availability | % | < 100% (frontend issues) |

Check backend health and traffic for a load balancer:

```dql-template
timeseries { dipHealth = avg(cloud.azure.microsoft_network.loadbalancers.DipAvailability),
             bytes = sum(cloud.azure.microsoft_network.loadbalancers.ByteCount) },
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<LB_ENTITY_ID>")
```

> **Important:** A `DipAvailability` below 100% indicates one or more backend instances are failing health probes. Cross-reference with VM metrics to identify the unhealthy instance.

---

## App Service / Functions Metrics

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.azure.microsoft_web.sites.HttpResponseTime` | Average HTTP response time | Seconds | > p99 baseline |
| `cloud.azure.microsoft_web.sites.Requests` | Total HTTP requests | Count | Drop vs baseline |
| `cloud.azure.microsoft_web.sites.Http5xx` | 5xx server error responses | Count | > 0 during incident |
| `cloud.azure.microsoft_web.sites.FunctionExecutionCount` | Function execution count | Count | Drop vs baseline |
| `cloud.azure.microsoft_web.sites.FunctionExecutionUnits` | Function execution units | MB-ms | Spike vs baseline |

Check response time and errors for an App Service:

```dql-template
timeseries { responseTime = avg(cloud.azure.microsoft_web.sites.HttpResponseTime),
             errors = sum(cloud.azure.microsoft_web.sites.Http5xx),
             requests = sum(cloud.azure.microsoft_web.sites.Requests) },
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<APP_SERVICE_ENTITY_ID>")
```

Check Function execution metrics:

```dql-template
timeseries { executions = sum(cloud.azure.microsoft_web.sites.FunctionExecutionCount),
             units = sum(cloud.azure.microsoft_web.sites.FunctionExecutionUnits) },
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<FUNCTION_ENTITY_ID>")
```

---

## AKS (Managed Cluster) Metrics

AKS infrastructure-layer metrics cover API server, etcd, and node-level resource usage. For workload-level observability (pods, deployments, services), defer to `dt-obs-kubernetes`.

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.azure.microsoft_containerservice.managedclusters.apiserver_cpu_usage_percentage` | API server CPU | % | > 80% sustained |
| `cloud.azure.microsoft_containerservice.managedclusters.apiserver_memory_usage_percentage` | API server memory | % | > 80% sustained |
| `cloud.azure.microsoft_containerservice.managedclusters.etcd_database_usage_percentage` | etcd storage usage | % | > 80% (risk of cluster instability) |
| `cloud.azure.microsoft_containerservice.managedclusters.node_cpu_usage_percentage` | Node CPU usage | % | > 85% sustained |
| `cloud.azure.microsoft_containerservice.managedclusters.node_memory_working_set_percentage` | Node memory working set | % | > 85% sustained |
| `cloud.azure.microsoft_containerservice.managedclusters.node_disk_usage_percentage` | Node disk usage | % | > 85% (eviction risk) |
| `cloud.azure.microsoft_containerservice.managedclusters.kube_node_status_condition` | Node readiness status | Status | Not-ready nodes |
| `cloud.azure.microsoft_containerservice.managedclusters.kube_pod_status_ready` | Pod readiness | Status | Drop vs baseline |

Check API server and etcd health for an AKS cluster:

```dql-template
timeseries { apiCpu = avg(cloud.azure.microsoft_containerservice.managedclusters.apiserver_cpu_usage_percentage),
             etcd = avg(cloud.azure.microsoft_containerservice.managedclusters.etcd_database_usage_percentage) },
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<AKS_ENTITY_ID>")
```

Check node resource pressure:

```dql-template
timeseries { nodeCpu = avg(cloud.azure.microsoft_containerservice.managedclusters.node_cpu_usage_percentage),
             nodeMem = avg(cloud.azure.microsoft_containerservice.managedclusters.node_memory_working_set_percentage),
             nodeDisk = avg(cloud.azure.microsoft_containerservice.managedclusters.node_disk_usage_percentage) },
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<AKS_ENTITY_ID>")
```

---

## Cosmos DB Metrics

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.azure.microsoft_documentdb.databaseaccounts.TotalRequestUnits` | RU consumption | RU/s | Near provisioned limit |
| `cloud.azure.microsoft_documentdb.databaseaccounts.TotalRequests` | Total requests | Count | Drop vs baseline |
| `cloud.azure.microsoft_documentdb.databaseaccounts.ServerSideLatency` | Server-side latency | ms | > p99 baseline |
| `cloud.azure.microsoft_documentdb.databaseaccounts.ServiceAvailability` | Service availability | % | < 100% |
| `cloud.azure.microsoft_documentdb.databaseaccounts.DataUsage` | Data storage used | Bytes | Near partition limit |
| `cloud.azure.microsoft_documentdb.databaseaccounts.DocumentCount` | Document count | Count | Trending toward partition limit |

Check RU consumption and latency for a Cosmos DB account:

```dql-template
timeseries { ru = sum(cloud.azure.microsoft_documentdb.databaseaccounts.TotalRequestUnits),
             latency = avg(cloud.azure.microsoft_documentdb.databaseaccounts.ServerSideLatency) },
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<COSMOSDB_ENTITY_ID>")
```

Check availability:

```dql-template
timeseries avail = avg(cloud.azure.microsoft_documentdb.databaseaccounts.ServiceAvailability),
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<COSMOSDB_ENTITY_ID>")
```

> **Important:** A `TotalRequestUnits` value near the provisioned RU limit means the account is at risk of 429 (throttled) responses. Cross-reference with `TotalRequests` to check if request volume is spiking.

---

## Redis Cache Metrics

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.azure.microsoft_cache.redis.serverLoad` | Server CPU load | % | > 80% sustained |
| `cloud.azure.microsoft_cache.redis.usedmemorypercentage` | Memory usage | % | > 85% (eviction risk) |
| `cloud.azure.microsoft_cache.redis.cachehits` | Cache hits | Count | Drop vs baseline |
| `cloud.azure.microsoft_cache.redis.cachemisses` | Cache misses | Count | Spike vs baseline |
| `cloud.azure.microsoft_cache.redis.cachemissrate` | Cache miss rate | % | Sustained increase |
| `cloud.azure.microsoft_cache.redis.connectedclients` | Connected clients | Count | Near maxclients limit |
| `cloud.azure.microsoft_cache.redis.evictedkeys` | Evicted keys | Count | > 0 (memory pressure) |
| `cloud.azure.microsoft_cache.redis.cacheLatency` | Operation latency | ms | > p99 baseline |
| `cloud.azure.microsoft_cache.redis.errors` | Error count | Count | > 0 during incident |
| `cloud.azure.microsoft_cache.redis.totalcommandsprocessed` | Commands processed | Count/s | Drop vs baseline |

Check server load and memory for a Redis instance:

```dql-template
timeseries { load = avg(cloud.azure.microsoft_cache.redis.serverLoad),
             mem = avg(cloud.azure.microsoft_cache.redis.usedmemorypercentage) },
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<REDIS_ENTITY_ID>")
```

Check hit/miss ratio and evictions:

```dql-template
timeseries { hits = sum(cloud.azure.microsoft_cache.redis.cachehits),
             misses = sum(cloud.azure.microsoft_cache.redis.cachemisses),
             evictions = sum(cloud.azure.microsoft_cache.redis.evictedkeys) },
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<REDIS_ENTITY_ID>")
```

> **Note:** Redis Enterprise metrics use the `microsoft_cache.redisenterprise` path with the same metric names. Replace `redis` with `redisenterprise` in the metric key. The `dt.smartscape_source.id` dimension works for all entity types.

---

## Application Gateway Metrics

| Metric key | Description | Unit | Investigation threshold |
|---|---|---|---|
| `cloud.azure.microsoft_network.applicationgateways.TotalRequests` | Total requests | Count | Drop vs baseline |
| `cloud.azure.microsoft_network.applicationgateways.FailedRequests` | Failed requests | Count | > 0 during incident |
| `cloud.azure.microsoft_network.applicationgateways.Throughput` | Data throughput | Bytes/sec | Near SKU limit |
| `cloud.azure.microsoft_network.applicationgateways.CurrentConnections` | Active connections | Count | Near connection limit |
| `cloud.azure.microsoft_network.applicationgateways.HealthyHostCount` | Healthy backend hosts | Count | Decrease from baseline |
| `cloud.azure.microsoft_network.applicationgateways.UnhealthyHostCount` | Unhealthy backend hosts | Count | > 0 (backend failure) |
| `cloud.azure.microsoft_network.applicationgateways.WebApplicationFirewallBlockedRequests` | WAF blocked request count | Count | > 0 (active blocking) |
| `cloud.azure.microsoft_network.applicationgateways.WebApplicationFirewallMatchedRequests` | WAF matched (triggered) request count | Count | Spike vs baseline (possible false positives) |
| `cloud.azure.microsoft_network.applicationgateways.WebApplicationFirewallTotalRuleDistribution` | WAF rule hit distribution | Count | Identifies which rules trigger most |
| `cloud.azure.microsoft_network.applicationgateways.WebApplicationFirewallManagedRuleDistribution` | WAF managed rule hit distribution | Count | Identifies managed rules triggering |

Check request volume and errors for an Application Gateway:

```dql-template
timeseries { requests = sum(cloud.azure.microsoft_network.applicationgateways.TotalRequests),
             failures = sum(cloud.azure.microsoft_network.applicationgateways.FailedRequests) },
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<APPGW_ENTITY_ID>")
```

Check backend pool health:

```dql-template
timeseries { healthy = avg(cloud.azure.microsoft_network.applicationgateways.HealthyHostCount),
             unhealthy = avg(cloud.azure.microsoft_network.applicationgateways.UnhealthyHostCount) },
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<APPGW_ENTITY_ID>")
```

> **Important:** An `UnhealthyHostCount` > 0 means backend VMs or containers are failing health probes. Cross-reference with the backend resource metrics (VM, App Service) to identify the root cause.

Check WAF blocked and matched requests during an incident (spikes in matched requests with user-reported issues indicate false positives):

```dql-template
timeseries { blocked = sum(cloud.azure.microsoft_network.applicationgateways.WebApplicationFirewallBlockedRequests),
             matched = sum(cloud.azure.microsoft_network.applicationgateways.WebApplicationFirewallMatchedRequests) },
  by: { dt.smartscape_source.id },
  from: now()-1h
| filter dt.smartscape_source.id == toSmartscapeId("<APPGW_ENTITY_ID>")
```

> **Investigation tip:** A spike in `WebApplicationFirewallMatchedRequests` correlated with user-reported 403 errors strongly suggests a false positive. Cross-reference with the disabled rule groups and exclusions in [load-balancing-api.md](load-balancing-api.md) to identify which rules are triggering and whether they should be tuned.

---

## Combining Entity Queries with Metrics

Find a set of entities by filter, then query metrics for all of them. Example: are all VMs in a resource group experiencing high CPU, or just one?

**Step 1 — Find resource IDs for the group:**

```dql-template
smartscapeNodes "AZURE_MICROSOFT_COMPUTE_VIRTUALMACHINES"
| filter azure.resource.group == "<RESOURCE_GROUP>"
| fields name, id
```

**Step 2 — Query metrics for all VMs (no filter = all series):**

```dql-template
timeseries cpu = avg(cloud.azure.microsoft_compute.virtualmachines.PercentageCPU),
  by: { dt.smartscape_source.id },
  from: now()-1h
```

Cross-reference the `dt.smartscape_source.id` dimension values against the entity IDs from Step 1 to identify which VMs in the resource group are affected.

---

## Metric Availability Note

Azure metrics are only available when Azure Monitor integration is enabled and configured for the relevant services in Dynatrace (Settings > Cloud and Virtualization > Azure). If a timeseries query returns no data:

1. Verify the entity exists: run the corresponding `smartscapeNodes` query
2. Confirm the Azure Monitor integration is configured and metric ingestion is enabled for this service
3. Check the metric name matches the naming convention: `cloud.azure.<resource_provider_path>.<MetricName>`

Do **not** interpret empty timeseries results as "no problem" — it may mean the metric is not configured for this resource type.

> **Note:** All metric keys documented here were verified against a live Dynatrace tenant with Azure Monitor integration enabled. If a metric key is not found in your environment, confirm Azure Monitor integration is configured for that service in Settings > Cloud and Virtualization > Azure.
