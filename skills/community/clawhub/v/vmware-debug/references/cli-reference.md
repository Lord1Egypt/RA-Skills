# vmware-debug CLI Reference

All commands are read-only and offline (no network, no credentials).

## triage — correlate a set of collected events

```bash
vmware-debug triage [OPTIONS]
  -e, --events PATH     JSON file of event envelopes (reads stdin if omitted)
      --bin-seconds N   Time-bin width (auto if omitted)
      --top-n N         Max hypotheses to return   [default: 5]
```

Input is a JSON array of event envelopes (see `references/event-envelope.md`):

```bash
cat events.json | vmware-debug triage
vmware-debug triage --events events.json --top-n 3
```

Output (JSON): `{event_count, window, spikes, hypotheses, next_checks}`.

## categories — list recognised symptom categories

```bash
vmware-debug categories
```

Prints each category, sample keywords, and the suggested next check (which
skill/tool to run). Use when you don't know what to look at.

## version / mcp

```bash
vmware-debug version    # installed version
vmware-debug mcp        # start the stdio MCP server (no network at startup)
```

## How the agent uses it

In an agent, the cross-skill correlation happens at the agent layer:

1. Fetch events with the data-source skills (vmware-monitor `event_list`,
   vmware-log-insight `log_search`/`log_aggregate`, vmware-aria alerts/anomaly,
   vmware-nsx).
2. Normalise each into the event envelope.
3. Call the `incident_timeline` MCP tool to correlate and rank.
4. Follow `next_checks`; route any fix to vmware-aiops / vmware-pilot.
