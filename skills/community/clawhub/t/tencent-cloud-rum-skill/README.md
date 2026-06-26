# Tencent Cloud RUM — Frontend Performance Analysis Skill (v2.1)

## Overview

This Skill is deeply integrated with [Tencent Cloud Real User Monitoring (RUM)](https://www.tencentcloud.com/document/product/1131/44486), providing AI-powered frontend performance analysis. It relies on the RUM MCP (Model Context Protocol) service to query metrics and logs, and delivers actionable analytical insights. The MCP endpoint used by this Skill, `https://app.rumt-zh.com/sse`, is the official Tencent Cloud RUM MCP service.

> Major changes in v2.1 vs v2.0: restructured the "Application Info Lookup Rules" into four scenarios (ID only / name only / ID + name / neither) with fallbacks for the 50-record cap and "no permission" errors; the decision tree has been streamlined to avoid duplication with the lookup rules.

## Directory Structure

```
Tencent Cloud RUM 2.1/
├── SKILL.md                              # Core Skill instruction file
├── setup.sh                              # One-click setup script (MCP config)
├── README.md                             # This file
└── references/                           # Reference docs (AI loads on demand)
    ├── rum_tools_docs.md                 # Parameter reference for the 5 RUM MCP tools
    ├── common_queries.md                 # Detailed steps for the 4 analysis flows
    └── apm_analysis.md                   # APM correlation + log enums + regions
```

## Quick Start

### Prerequisites

1. **Tencent Cloud Account**: Register at [Tencent Cloud](https://www.tencentcloud.com/)
2. **RUM Application**: Create a Web application in the [RUM Console](https://console.tencentcloud.com/rum)
3. **API Credentials**: Get your `SecretId` and `SecretKey` from [API Key Management](https://console.tencentcloud.com/cam/capi)

### Getting Started

1. **Try the Demo**: Visit the [RUM Console Demo](https://console.tencentcloud.com/rum/web/demo) to see RUM in action
2. **Install the SDK**: Follow the [Application Integration Guide](https://www.tencentcloud.com/zh/document/product/1131/44496) to complete SDK setup
   > 💡 For SDK integration, updating reporting config, enabling white-screen/jank monitoring, or adding custom reporting → use the **[`rum-sdk-setup` Skill](https://skillhub.cn/skills/rum-sdk-setup)** (covers 10 platforms)
3. **Configure This Skill**: Run `bash setup.sh`, or configure the MCP manually

### MCP Configuration

```json
{
  "mcpServers": {
    "rum": {
      "transportType": "sse",
      "url": "https://app.rumt-zh.com/sse",
      "headers": {
        "SecretId": "<YOUR_SECRET_ID>",
        "SecretKey": "<YOUR_SECRET_KEY>"
      }
    }
  }
}
```

## Features

### Available Tools

| Tool | Purpose |
|------|---------|
| QueryRumWebProjects | List RUM-WEB applications |
| QueryRumWebMetric | Query network / exception / PV / UV / performance / resource metrics |
| QueryRumWebLog | Full log search |
| QueryResourceByPage | Query resource metrics per page |
| QueryApmLinkId | Get the linked APM application ID |

### Built-in Analysis Flows

| Flow | Description |
|------|-------------|
| TOP Exception Analysis | Diagnose JS / Promise errors and resource loading errors |
| TOP Page Performance Analysis | Analyze LCP / FCP and WebVitals; pinpoint performance bottlenecks |
| TOP API Performance & Stability | Analyze API latency, status-code errors, retcode errors |
| TOP Slow Resource Loading | Diagnose static-resource loading bottlenecks |

### Advanced Capabilities

- **APM correlation**: When logs contain trace info, correlate with APM for deep backend-link analysis
- **Multi-dimensional drill-down**: Break down by region, ISP, platform, version, page, etc.
- **Smart routing**: Automatically match the most suitable analysis flow based on user intent

## Useful Links

| Resource | URL |
|----------|-----|
| RUM Console | https://console.tencentcloud.com/rum |
| RUM Console Demo | https://console.tencentcloud.com/rum/web/demo |
| Application Integration Guide | https://www.tencentcloud.com/zh/document/product/1131/44496 |
| Web SDK Connection Guide | https://www.tencentcloud.com/document/product/1131/44517 |
| Getting Started | https://www.tencentcloud.com/document/product/1131/44493 |
| RUM Product Overview | https://www.tencentcloud.com/document/product/1131/44486 |
| RUM Pricing | https://www.tencentcloud.com/document/product/1131/44490 |
| API Key Management | https://console.tencentcloud.com/cam/capi |

## Notes

1. RUM MCP uses the `SSE` protocol
2. Authentication is done via `SecretId` and `SecretKey` in HTTP headers — keep them secure
3. Recommended timeout: 15–30 seconds
