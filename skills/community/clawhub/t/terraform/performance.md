# Performance — Slow Plans, Big States, And Throttled Providers

## Where The Time Actually Goes

Three phases, and they fail differently:

1. **Init** — downloading providers. Slow on ephemeral CI runners, invisible on a laptop with a warm cache.
2. **Refresh** — one or more API calls per managed resource and per data source, at `-parallelism` concurrency (default 10). This is almost always the phase you are waiting on.
3. **Graph walk** — the provider's plan calls plus, for large states, serializing and transferring the state itself.

Isolate before tuning: `terraform plan -refresh=false` versus a full plan tells you in one comparison whether refresh is the cost. If both are slow, the state file or the provider is.

## Levers, In Order

1. **`-refresh=false` while iterating.** You plan against last-known state, which is exactly what you want when you are editing HCL and not the cloud. Turn it back on before the plan you actually apply.
2. **`plan -target=<address>` for a single resource while iterating.** A targeted *plan* is read-only: it narrows the graph walk to preview one resource faster and changes nothing. `apply -target` is the separate, emergency-only case (SKILL.md Traps) — it leaves the graph partially applied and must be followed by a clean full plan. Never either form in the merged pipeline.
3. **`-parallelism=N`.** Default 10. Raise toward 20-30 when the API is fast and the graph is wide; **lower to 2-5 the moment you see throttling**. Symptoms of throttling: "Rate exceeded", 429s, or `TooManyRequests` retried in `TF_LOG=DEBUG`, and apply time growing faster than resource count. More concurrency against a throttling API is slower, not faster.
4. **Cut fan-out data sources.** A data source inside a module used with `for_each` runs once per instance, on every plan. Hoist it to the root and pass the value in.
5. **Remove module-level `depends_on`.** It defers every data source inside to apply time, which makes downstream values unknown and prevents the graph from resolving in parallel. Often the single biggest win in a slow module (`modules.md`).
6. **Split the state by blast radius.** The only fix that scales. The signal is the same one in `state.md`: plans you stop watching (~3 min+, typically 300-500 resources in one state).

## Provider Install Time In CI

- Ephemeral runners re-download every provider on every job. Cache the plugin directory keyed on the hash of `.terraform.lock.hcl` — that file is exactly what determines the contents.
- `TF_PLUGIN_CACHE_DIR` shares one copy across stacks on the same runner; the large cloud providers are hundreds of megabytes each, so a monorepo with a dozen stacks feels this immediately (`providers.md`).

## Big State Files

- Every plan pulls the whole state and every apply pushes it. Size grows the lock hold time, which grows the queue behind it.
- Do not store large blobs in resources that keep their content in state: file contents, rendered templates, certificates, generated documents. Reference them by path or hash instead.
- Symptom of state bloat rather than resource count: `terraform state pull | wc -c` is large while `terraform state list | wc -l` is modest.

## Slow Versus Stuck

- An apply waiting on a cloud resource that genuinely takes twenty minutes (managed database, cluster, certificate validation) is the cloud's clock. `TF_LOG=DEBUG` shows the polling loop and the elapsed time per attempt.
- No log output at all for minutes, with no polling, is a hung provider or a lost network path — not slowness (`debug.md`).
- Repeated timeouts on the same resource type are capacity or quota, and no amount of parallelism tuning helps.

## Ask Cheaply

Most questions do not need a plan:

- `terraform state show <addr>` — the last-known attributes, no API calls.
- `terraform console` — evaluate any expression against real state.
- `terraform output -json` — what other stacks consume.
- `terraform graph -type=plan | dot -Tsvg > graph.svg` — dependency shape without running anything against the cloud.

A team that runs full plans to answer questions burns the lock and the API budget that the deploy pipeline needs.
