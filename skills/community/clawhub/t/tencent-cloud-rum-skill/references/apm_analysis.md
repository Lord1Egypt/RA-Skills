# APM Correlation Analysis Guide

## Trigger Conditions

When queried logs are related to API requests and the `trace` field is non-empty, correlate with APM data:
1. Call `QueryApmLinkId` to get the linked APM project ID
2. Follow the APM Trace Analysis Steps below

---

## APM Trace Analysis Steps

1. Use `DescribeGeneralSpanTree` to query **error spans** for the trace_id
2. Use `DescribeGeneralSpanTree` to query **slow spans** for the trace_id
3. If the slow span contains a LogTopicID, use `DescribeGeneralSpanTree` to query **log information** for the trace_id. If no LogTopicID exists, proceed to next step
4. Look up APM-Span attribute definitions and extract key Span attributes from the trace:
   - If DB and CVM attributes exist, extract the IP portion of `db.ip` or `cvm.instance.id` and use `GetMonitorData` to query related instance monitoring metrics
   - If TKE attributes exist, extract `k8s.cluster.id` and `k8s.node.ip` and use `GetMonitorData` to query K8sPodRateCpuCoreUsedNode and K8sPodRateMemUsageNode metrics
5. Comprehensive analysis:
   - **Error spans**: Focus on `error` and `exception` prefixed attributes; analyze root cause span, error content, error machine, error reason
   - **Slow spans**: Analyze where latency occurs (specific span processing too long, errors within spans, excessive time between span calls, etc.)
   - Determine if issues correlate with instance monitoring metrics

---

## DescribeGeneralSpanTree Parameter Guide

### Input Rules

- Choose `span_status` based on application state: use SLOW for warnings, ERROR for exceptions
- **Do NOT query full trace data** — do NOT set `span_status` to UNSET
  - Why: Full trace data is too large, will overflow context and hinder analysis
- Choose `scene_type` based on user's question: ERR for errors, SQL for database, MQ for message queue, NORMAL for others
- If there is no specific focus target, do NOT set `scene_type`
- When `scene_type` is not NORMAL, `object` is required (specifying the focus target)
- When using `DescribeGeneralSpanTree`, the time range can be expanded to ±1 hour around the target request time

### Usage Scenarios

| Scenario | Input | Output |
|----------|-------|--------|
| Query application details | Required params, region, app name | A random error/slow trace from the application |
| Query endpoint details | Required params, region, business system ID, app name, endpoint name | An error/slow trace from the endpoint |
| Analyze specific error type/DB/MQ | Required params, region, dimension info, scene_type, object | Trace info for specified error/anomaly (submit ERROR and SLOW separately) |
| Query trace logs | Required params, region, trace_id, span_status=LOG, object=LogTopicID | Log info for the trace (requires both trace_id and LogTopicID) |

---

## DescribeSpanTagList Parameter Guide

| Scenario | Filter Key |
|----------|-----------|
| Query by HTTP info | `http.route` (request path), `http.request.method` (method), `http.response.status_code` (status code) |
| Query by RPC info | `rpc.method` (callee method), `rpc.service` (callee service), `network.peer.address` (peer address), `network.peer.port` (peer port) |

---

## Log Level Enum Values

| Value | Description |
|-------|-------------|
| `1` | API_RESPONSE - All API requests (whitelisted or default reporting) |
| `2` | INFO - General information log |
| `4` | ERROR - Error log |
| `8` | PROMISE_ERROR - Promise error |
| `16` | AJAX_ERROR - AJAX error |
| `32` | SCRIPT_ERROR - JS loading error |
| `64` | IMAGE_ERROR - Image loading error |
| `128` | CSS_ERROR - CSS loading error |
| `256` | CONSOLE_ERROR - Console error |
| `512` | MEDIA_ERROR - Media resource error |
| `1024` | RET_ERROR - API return code error |
| `1025` | PAGE_LOAD - Page load |
| `1026` | SLOW_PAGE_LOAD - Slow page load |
| `1027` | SLOW_NET_REQUEST - Slow network request |
| `1028` | ASSERT_REQUEST - Resource request |
| `1029` | SLOW_ASSET_REQUEST - Slow resource request |
| `1032` | BLANK_SCREEN - Blank screen error |
| `2048` | REPORT - Same as ERROR, triggers alert but does not deduct score |

## RUM Supported Regions

- `ap-guangzhou` (default)
- `ap-singapore`
- `na-siliconvalley`
