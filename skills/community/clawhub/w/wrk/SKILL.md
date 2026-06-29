---
name: wrk
description: Use wrk for HTTP load testing, including Lua scripting for dynamic request headers such as randomized X-Forwarded-For IPs.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - wrk
    install:
      - kind: brew
        formula: wrk
        bins: [wrk]
    emoji: "⚡"
---

# wrk Load Testing Skill

Use this skill when a user wants to run, design, or interpret HTTP load tests with [`wrk`](https://github.com/wg/wrk), especially when they need realistic request generation through Lua scripting.

`wrk` is a high-performance HTTP benchmarking tool. It can generate substantial load from a single machine by combining multiple threads, persistent connections, and an event-driven architecture. It is best suited for controlled testing of services the user is authorized to assess.

## Safety and scope

Before helping with a load test:

1. Confirm the target is authorized for load testing.
2. Prefer local, dev, staging, sandbox, or explicitly approved performance-test environments.
3. Warn the user before suggesting settings that may be disruptive, such as very high connection counts, long durations, or tests against production.
4. Start small and scale gradually while watching service health, logs, autoscaling, rate limits, and downstream dependencies.

Avoid recommending uncontrolled tests against third-party systems or production endpoints without explicit authorization.

## Basic `wrk` command pattern

```bash
wrk -t4 -c100 -d30s https://example.internal/health
```

Common options:

- `-t`: number of threads.
- `-c`: number of open connections.
- `-d`: test duration, such as `30s`, `2m`, or `10m`.
- `-s`: Lua script file for custom request behavior.
- `--latency`: include latency distribution statistics.
- `-H`: add a static header to every request.

Example with latency reporting:

```bash
wrk -t4 -c100 -d60s --latency https://example.internal/api/v1/items
```

Example with a static header:

```bash
wrk -t4 -c100 -d60s \
  -H 'Authorization: Bearer test-token' \
  -H 'Accept: application/json' \
  https://example.internal/api/v1/items
```

## Lua scripting with `wrk`

Use Lua when requests need dynamic headers, randomized inputs, multiple paths, request bodies, or per-request behavior.

A Lua script can define functions such as:

- `setup(thread)`: called once per thread before the test starts.
- `init(args)`: called when a thread initializes.
- `request()`: returns the HTTP request to send.
- `response(status, headers, body)`: called for each response.
- `done(summary, latency, requests)`: called after the benchmark finishes.

## Example: random `X-Forwarded-For` IP per request

Create a file named `random_xff.lua`:

```lua
-- random_xff.lua
-- Sends each request with a randomized X-Forwarded-For IPv4 address.

local counter = 0

local function random_octet(min, max)
  return math.random(min, max)
end

local function random_public_ipv4()
  -- Avoid common private, loopback, link-local, multicast, and reserved ranges
  -- by choosing from documentation-safe-ish public-looking ranges for testing.
  -- Adjust this for your environment if specific source ranges are required.
  local first_octets = { 8, 23, 34, 44, 52, 63, 74, 96, 104, 128, 137, 150, 172, 198 }
  local first = first_octets[math.random(#first_octets)]

  -- Avoid 172.16.0.0/12 when first octet is 172.
  local second
  if first == 172 then
    local allowed = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 32, 64, 96, 128, 160, 192, 224 }
    second = allowed[math.random(#allowed)]
  else
    second = random_octet(0, 255)
  end

  return string.format(
    "%d.%d.%d.%d",
    first,
    second,
    random_octet(0, 255),
    random_octet(1, 254)
  )
end

request = function()
  counter = counter + 1

  -- Seed periodically with time plus a per-thread counter. wrk runs Lua per thread,
  -- so this keeps sequences from being identical for long-running tests.
  if counter == 1 then
    math.randomseed(os.time() + counter)
  end

  local ip = random_public_ipv4()
  local headers = {
    ["X-Forwarded-For"] = ip,
    ["X-Real-IP"] = ip,
    ["Accept"] = "application/json",
    ["User-Agent"] = "wrk-random-xff/1.0"
  }

  return wrk.format("GET", nil, headers)
end
```

Run it with:

```bash
wrk -t4 -c100 -d60s --latency -s random_xff.lua https://example.internal/api/v1/items
```

## Example: POST JSON with random `X-Forwarded-For`

```lua
-- post_random_xff.lua

local function random_public_ipv4()
  local first_octets = { 8, 23, 34, 44, 52, 63, 74, 96, 104, 128, 137, 150, 198 }
  return string.format(
    "%d.%d.%d.%d",
    first_octets[math.random(#first_octets)],
    math.random(0, 255),
    math.random(0, 255),
    math.random(1, 254)
  )
end

init = function(args)
  math.randomseed(os.time())
end

request = function()
  local ip = random_public_ipv4()
  local body = string.format('{"requestId":"wrk-%d","sourceIp":"%s"}', math.random(1000000000), ip)

  local headers = {
    ["Content-Type"] = "application/json",
    ["Accept"] = "application/json",
    ["X-Forwarded-For"] = ip
  }

  return wrk.format("POST", "/api/v1/events", headers, body)
end
```

Run it with a base URL; the path comes from the Lua script:

```bash
wrk -t4 -c100 -d60s --latency -s post_random_xff.lua https://example.internal
```

## Choosing safe starting parameters

For initial validation, suggest conservative values:

```bash
wrk -t2 -c20 -d30s --latency https://example.internal/health
```

Then increase gradually:

```bash
wrk -t4 -c100 -d2m --latency https://example.internal/api/v1/items
wrk -t8 -c500 -d5m --latency https://example.internal/api/v1/items
```

Only recommend higher values after confirming the environment, service capacity, downstream dependencies, and monitoring coverage.

## Interpreting output

Important fields:

- `Requests/sec`: approximate throughput achieved by the client.
- `Latency`: average, standard deviation, max, and distribution if `--latency` is used.
- `Socket errors`: connection, read, write, or timeout failures; these often indicate saturation, network issues, or server-side limits.
- `Non-2xx or 3xx responses`: application errors, authorization failures, rate limits, or expected negative responses depending on the test.
- `Transfer/sec`: response bandwidth observed by the client.

When results look suspicious, check whether the bottleneck is the client machine, network path, proxy/load balancer, service, database, cache, or downstream dependency.

## Useful investigation checklist

When helping an agent run or analyze `wrk` tests, gather:

- Target URL and method.
- Environment: local, dev, staging, production, or approved external target.
- Desired traffic shape: threads, connections, duration, ramp-up strategy if any.
- Headers, authentication, cookies, tenant IDs, or feature flags needed.
- Whether randomized `X-Forwarded-For` is safe and meaningful in that environment.
- Expected status codes and response-size profile.
- Monitoring links, logs, dashboards, and alert thresholds.
- Known rate limits, WAF rules, bot protection, CDN behavior, and load balancer behavior.

## Common pitfalls

- `wrk` does not model browser behavior, JavaScript, or full user journeys.
- Very high connection counts can exhaust client resources before the service is saturated.
- Randomizing `X-Forwarded-For` may bypass or invalidate IP-based aggregation in logs, dashboards, caches, rate limiters, or abuse controls; use only when this is the intended authorized test.
- Some proxies overwrite or append to `X-Forwarded-For`; verify what the application actually receives.
- Production tests can be disruptive even with moderate settings if they hit expensive endpoints or shared dependencies.
