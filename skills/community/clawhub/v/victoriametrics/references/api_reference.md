# VictoriaMetrics API Reference

This document provides detailed information about VictoriaMetrics API endpoints and features.

## API Endpoints

### Single-Node Deployment

Base URL: `http://<victoriametrics>:8428`

#### Query API

```
GET /api/v1/query
GET /api/v1/query_range
GET /api/v1/series
GET /api/v1/labels
GET /api/v1/label/<label_name>/values
```

#### Write API

```
POST /api/v1/write                    # Prometheus remote write
POST /api/v1/import                   # JSON import
POST /api/v1/import/native            # Native format import
POST /api/v1/import/prometheus        # Prometheus text format
POST /api/v1/import/csv               # CSV import
```

#### Export API

```
GET /api/v1/export                    # JSON export
GET /api/v1/export/native             # Native format export
GET /api/v1/export/csv                # CSV export
```

#### Health & Status

```
GET /health                           # Health check
GET /api/v1/status/tsdb               # TSDB stats
GET /api/v1/targets                   # Scrape targets
GET /api/v1/alerts                    # Active alerts
GET /api/v1/metadata                  # Metric metadata
```

### Cluster Deployment

Base URL: `http://<vmselect>:8481/select/<accountID>/prometheus`

#### Query API (via vmselect)

```
GET /select/<accountID>/prometheus/api/v1/query
GET /select/<accountID>/prometheus/api/v1/query_range
GET /select/<accountID>/prometheus/api/v1/series
GET /select/<accountID>/prometheus/api/v1/labels
GET /select/<accountID>/prometheus/api/v1/label/<label_name>/values
```

#### Multi-Tenant Query

```
GET /select/multitenant/prometheus/api/v1/query
```

Query multiple tenants at once using `vm_account_id` and `vm_project_id` labels:

```promql
up{vm_account_id="7", vm_project_id="9" or vm_account_id="42"}
```

#### Write API (via vminsert)

```
POST http://<vminsert>:8480/insert/<accountID>/prometheus/api/v1/write
POST http://<vminsert>:8480/insert/multitenant/prometheus/api/v1/write
```

## Query Parameters

### Instant Query

```
GET /api/v1/query?query=<promql>&time=<timestamp>
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | PromQL expression |
| `time` | RFC3339 or unix timestamp | Evaluation time (default: now) |
| `timeout` | duration | Query timeout |

### Range Query

```
GET /api/v1/query_range?query=<promql>&start=<start>&end=<end>&step=<step>
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | PromQL expression |
| `start` | RFC3339 or unix timestamp | Start time |
| `end` | RFC3339 or unix timestamp | End time |
| `step` | duration or seconds | Query resolution step |
| `timeout` | duration | Query timeout |

### Series Query

```
GET /api/v1/series?match[]=<selector>&start=<start>&end=<end>
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `match[]` | string | Series selector (can be repeated) |
| `start` | RFC3339 or unix timestamp | Start time |
| `end` | RFC3339 or unix timestamp | End time |

## VictoriaMetrics Enhancements

### Query Enhancements

VictoriaMetrics supports additional query parameters:

| Parameter | Description |
|-----------|-------------|
| `extra_filters[]` | Additional label filters |
| `extra_label=<label>=<value>` | Add extra label to all series |
| `limit` | Limit number of returned series |
| `offset` | Skip first N series |

### Example with Extra Filters

```bash
curl 'http://vmselect:8481/select/0/prometheus/api/v1/query' \
  -d 'query=up' \
  -d 'extra_filters[]={vm_account_id="7",vm_project_id="9"}'
```

## MetricsQL Extensions

VictoriaMetrics extends PromQL with additional functions:

### String Functions

- `label_values(<label>)` - returns all values for the label
- `labels_equal(<label1>, <label2>)` - returns 1 if labels are equal

### Histogram Functions

- `histogram_quantile_over_time(<phi>, <histogram>[<range>])` - quantile over time range

### Aggregation Functions

- `limitk(<k>, ...)` by (<labels>) - returns up to k series per group
- `distinct(...)` by (<labels>) - returns number of distinct values

### Transformation Functions

- `interpolate(<metric>)` - fills gaps with linear interpolation
- `keep_last_value(<metric>)` - fills gaps with the last value
- `keep_next_value(<metric>)` - fills gaps with the next value

## Response Format

### Successful Response

```json
{
  "status": "success",
  "data": {
    "resultType": "vector",
    "result": [
      {
        "metric": {
          "__name__": "up",
          "instance": "localhost:9090",
          "job": "prometheus"
        },
        "value": [1609459200, "1"]
      }
    ]
  }
}
```

### Error Response

```json
{
  "status": "error",
  "errorType": "bad_data",
  "error": "invalid parameter 'query': 1:1: parse error"
}
```

### Partial Response (Cluster)

When some vmstorage nodes are unavailable, cluster returns partial responses:

```json
{
  "status": "success",
  "data": {
    "resultType": "vector",
    "result": [...]
  },
  "isPartial": true
}
```

## Authentication

### Basic Auth

```bash
curl -u user:password http://victoriametrics:8428/api/v1/query?query=up
```

### Bearer Token

```bash
curl -H "Authorization: Bearer <token>" http://victoriametrics:8428/api/v1/query?query=up
```

## Rate Limiting

VictoriaMetrics can be configured with rate limits:

- `-maxConcurrentInserts` - maximum concurrent insert requests
- `-maxInsertRequestSize` - maximum size of insert request
- `-search.maxConcurrentRequests` - maximum concurrent query requests
- `-search.maxQueueDuration` - maximum time a query can wait in queue

## Performance Tips

1. **Use range queries** for dashboards instead of multiple instant queries
2. **Limit label values** with `extra_filters[]` for better performance
3. **Use recording rules** for frequently used queries
4. **Set appropriate `step`** to control data resolution
5. **Use `limit` parameter** to avoid huge responses

## Cluster-Specific Features

### Multi-Tenancy

- Each tenant identified by `accountID` or `accountID:projectID`
- Tenants are isolated - cannot query each other's data
- Tenant data is spread across vmstorage nodes

### Replication

- Data can be replicated across vmstorage nodes
- Configure via `-replicationFactor` flag
- Guarantees data availability when nodes fail

### vmstorage Groups

- Group vmstorage nodes for different purposes
- Configure via `-storageNode=groupName/addr`
- Each group can have different replication factor

## Monitoring VictoriaMetrics

VictoriaMetrics exposes self-monitoring metrics at `/metrics` endpoint:

```bash
# Single-node
curl http://victoriametrics:8428/metrics

# Cluster components
curl http://vminsert:8480/metrics
curl http://vmselect:8481/metrics
curl http://vmstorage:8482/metrics
```

### Key Metrics

| Metric | Description |
|--------|-------------|
| `vm_app_version` | Application version info |
| `vm_rows_ingested_total` | Total rows ingested |
| `vm_rows_inserted_total` | Total rows inserted |
| `vm_request_duration_seconds` | Request latency |
| `vm_active_time_series` | Number of active time series |
| `vm_cache_size_bytes` | Cache memory usage |
| `vm_free_disk_space_bytes` | Available disk space |

## Examples

### Query with Time Range

```bash
# Query last hour of data
curl 'http://localhost:8428/api/v1/query_range' \
  -d 'query=rate(http_requests_total[5m])' \
  -d 'start=-1h' \
  -d 'end=now' \
  -d 'step=60s'
```

### Export Data

```bash
# Export data for specific time range
curl 'http://localhost:8428/api/v1/export' \
  -d 'match[]={__name__=~"node_.*"}' \
  -d 'start=2024-01-01T00:00:00Z' \
  -d 'end=2024-01-02T00:00:00Z'
```

### Multi-Tenant Query (Cluster)

```bash
# Query specific tenant
curl 'http://vmselect:8481/select/42/prometheus/api/v1/query?query=up'

# Query multiple tenants
curl 'http://vmselect:8481/select/multitenant/prometheus/api/v1/query' \
  -d 'query=up{vm_account_id=~"42|43"}'
```

## Error Handling

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad request (invalid query) |
| 401 | Unauthorized (auth required) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not found |
| 422 | Unprocessable entity |
| 429 | Too many requests (rate limited) |
| 500 | Internal server error |
| 503 | Service unavailable (overloaded) |

## Additional Resources

- [VictoriaMetrics Documentation](https://docs.victoriametrics.com/)
- [MetricsQL Guide](https://docs.victoriametrics.com/MetricsQL.html)
- [Cluster Setup Guide](https://docs.victoriametrics.com/Cluster-VictoriaMetrics.html)
- [API Examples](https://docs.victoriametrics.com/url-examples.html)
