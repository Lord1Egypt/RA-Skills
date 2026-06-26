---
name: traceroute-tool
description: Trace network path to a destination host. Use for network diagnostics, latency analysis, and routing path discovery.
---
# Traceroute - Network Path Tracer

Trace the route packets take to reach a network host. Shows each hop with IP address and response time, helping identify network bottlenecks and routing issues.

## Usage
```bash
traceroute-tool [options] <host>
```

## Options

- `-n`: Show numeric addresses only (no DNS)
- `-m N`: Set max hops (default: 30)
- `-w N`: Set wait time per hop
- `-q N`: Set queries per hop

## Examples

```bash
traceroute-tool google.com
traceroute-tool -n 8.8.8.8
traceroute-tool -m 20 example.com
```