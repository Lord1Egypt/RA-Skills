# Slow Page Load Playbook

Start by segmenting the problem by page, browser, geo location, and `dt.rum.user_type`.

Heuristics:
- High TTFB -> slow backend
- High LCP with normal TTFB -> render bottleneck
- High CLS -> layout shifts (late-loading content, ads, fonts)
- Long tasks dominate -> JavaScript execution bottlenecks (heavy frameworks, large bundles)

## Contents

- [Backend latency (high TTFB)](#backend-latency-high-ttfb)
- [Heavy JavaScript execution (long tasks)](#heavy-javascript-execution-long-tasks)
- [Large JavaScript bundles](#large-javascript-bundles)
- [Large resources](#large-resources)
- [Cache effectiveness](#cache-effectiveness)
- [Compression waste](#compression-waste)
- [Network issues](#network-issues)
- [Third-party dependencies](#third-party-dependencies)

## Backend latency (high TTFB)

```dql
fetch user.events
| filter frontend.name == "my-frontend" and characteristics.has_request == true
| filter page.url.path == "/checkout"
| summarize avg_ttfb = avg(request.time_to_first_byte), avg_duration = avg(duration)
```

If TTFB is high, analyze backend spans by correlating frontend events with backend traces using `trace.id`.

## Heavy JavaScript execution (long tasks)

Long tasks by page:

```dql
fetch user.events, from: now() - 2h
| filter characteristics.has_long_task == true
| summarize
   long_task_count = count(),
   total_blocking_time = sum(duration),
   by: {frontend.name, page.url.path}
| sort total_blocking_time desc
| limit 20
```

Long tasks by script source:

```dql
fetch user.events, from: now() - 2h
| filter frontend.name == "my-frontend"
| filter characteristics.has_long_task == true
| summarize
   long_task_count = count(),
   total_blocking_time = sum(duration),
   by: {long_task.attribution.container_src}
| sort total_blocking_time desc
| limit 20
```

## Large JavaScript bundles

```dql
fetch user.events
| filter frontend.name == "my-frontend"
| filter characteristics.has_request
| filter endsWith(url.full, ".js")
| summarize dls = max(performance.decoded_body_size), by: url.full
| sort dls desc
| limit 20
```

## Large resources

```dql
fetch user.events
| filter frontend.name == "my-frontend"
| filter characteristics.has_request
| summarize dls = max(performance.decoded_body_size), by: url.full
| sort dls desc
| limit 20
```

## Cache effectiveness

```dql
fetch user.events, from: now() - 2h
| filter frontend.name == "my-frontend"
| filter characteristics.has_request == true
| fieldsAdd cache_status = if(
   performance.incomplete_reason == "local_cache" or performance.transfer_size == 0 and
   (performance.encoded_body_size > 0 or performance.decoded_body_size > 0),
   "cached",
   else: if(performance.transfer_size > 0, "network", else: "uncached")
  )
| summarize
   request_count = count(),
   avg_duration = avg(duration),
   by: {url.domain, cache_status}
```

## Compression waste

```dql
fetch user.events, from: now() - 2h
| filter characteristics.has_request == true
| filter isNotNull(performance.encoded_body_size) and isNotNull(performance.decoded_body_size)
| filter performance.encoded_body_size > 0
| fieldsAdd
   expansion_ratio = performance.decoded_body_size / performance.encoded_body_size,
   wasted_bytes = performance.decoded_body_size - performance.encoded_body_size
| summarize
   requests = count(),
   avg_expansion_ratio = avg(expansion_ratio),
   total_wasted_bytes = sum(wasted_bytes),
   by: {request.url.host, request.url.path}
| sort total_wasted_bytes desc
| limit 50
```

## Network issues

Compare by location and domain when TTFB is high but backend performance is good:

```dql
fetch user.events, from: now() - 2h
| filter characteristics.has_request == true
| summarize
   request_count = count(),
   avg_duration = avg(duration),
   p75_duration = percentile(duration, 75),
   p95_duration = percentile(duration, 95),
   by: {geo.country.iso_code, request.url.domain}
| sort p95_duration desc
| limit 50
```

Analyze DNS time:

```dql
fetch user.events, from: now() - 2h
| filter characteristics.has_request == true
| filter isNotNull(performance.domain_lookup_start) and isNotNull(performance.domain_lookup_end)
| fieldsAdd dns_ms = performance.domain_lookup_end - performance.domain_lookup_start
| summarize
   request_count = count(),
   avg_dns_ms = avg(dns_ms),
   p75_dns_ms = percentile(dns_ms, 75),
   p95_dns_ms = percentile(dns_ms, 95),
   by: {request.url.domain}
| sort p95_dns_ms desc
| limit 50
```

Analyze by protocol (http/1.1, h2, h3):

```dql
fetch user.events
| filter characteristics.has_request
| summarize cnt = count(), by: {url.domain, performance.next_hop_protocol}
| sort cnt desc
| limit 50
```

## Third-party dependencies

Analyze request performance by domain:

```dql
fetch user.events, from: now() - 2h
| filter characteristics.has_request == true
| summarize
   request_count = count(),
   avg_duration = avg(duration),
   p75_duration = percentile(duration, 75),
   p95_duration = percentile(duration, 95),
   by: {request.url.domain}
| sort p95_duration desc
| limit 50
```
