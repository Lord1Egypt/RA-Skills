# EdgeOne Observability Reference

> **Telemetry note:** You are now in module **`observability`**. Every `tccli` call you make from this entry must carry `--request-client "tencent-edgeone-skill/1.1.0 module/observability"`.

Operational guides for traffic daily report generation, origin health inspection, offline log download, and log analysis.

## Quick Decision Tree

```
What does the user want to do?
│
├─ "Generate yesterday's traffic daily report"
│  "Show me the bandwidth peak over the last 24 hours"
│  └─ → `eo-traffic-daily-report.md`  🟢 Low Risk · Auto-collect L7/L4 data and generate a Markdown daily report
│
├─ "Check the origin status for example.com"
│  "Is the origin healthy?" "Is it a CDN issue or an origin issue?"
│  └─ → `eo-origin-health-check.md`  🟢 Low Risk · Origin status code distribution + health ratio + quick root cause analysis
│
├─ "Download the logs for example.com from yesterday afternoon"
│  "Download the last 6 hours of L4 logs"
│  └─ → `eo-log-downloader.md`  🟢 Low Risk · Natural language driven offline log download link retrieval
│
├─ "Analyze the logs — too many 502 errors"
│  "Which URIs have the most abnormal requests?"
│  "Show me per-URL download traffic breakdown"
│  └─ → `eo-log-analyzer.md`  🟢 Low Risk · Log download + local parsing + pattern recognition + fault inference + traffic aggregation
│
└─ Not sure which API to call
   └─ → `../api/api-discovery.md`
```

## Prerequisites

All operations require API calls via tccli. Before first use, complete the following:

1. **Tool Setup** — Read `../api/README.md` to install tccli and configure credentials
2. **Get ZoneId** — Read `../api/zone-discovery.md` to obtain the zone ID

## Files in This Directory

| File | Risk Level | Core Trigger Scenario |
|---|---|---|
| `eo-traffic-daily-report.md` | 🟢 Low Risk | Query L7/L4 traffic trends daily and generate a Markdown report with bandwidth peak, request volume, and Top domains/regions |
| `eo-origin-health-check.md` | 🟢 Low Risk | Query origin status code distribution and origin health ratio for quick origin fault root cause analysis |
| `eo-log-downloader.md` | 🟢 Low Risk | Describe time range and domain in natural language to automatically retrieve offline log download links |
| `eo-log-analyzer.md` | 🟢 Low Risk | Automatically download and parse logs locally, extract anomaly details, provide pattern recognition conclusions with fault inference, or aggregate traffic by domain/URL |

## Reference Links

- [EdgeOne Product Documentation](https://edgeone.ai/document/56978)
- [EdgeOne API Documentation](https://edgeone.ai/document/50454)
- API Usage Guide: `../api/README.md`
