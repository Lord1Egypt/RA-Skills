---
name: shopify-store-monitor
description: Track Shopify store sales and monitor store performance using PPSPY sales monitoring tools. Create monitoring tasks, inspect hourly and daily sales, and manage monitored stores.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - PPSPY_API_KEY
      bins:
        - npm
    install:
      command: npm
      args:
        - install
        - -g
        - "ppspy-mcp-server@1.0.1"
    primaryEnv: PPSPY_API_KEY
    emoji: "🔍"
    homepage: https://www.ppspy.com
    mcpServers:
      ppspy:
        command: ppspy-mcp-server
        env:
          PPSPY_API_KEY: "{{PPSPY_API_KEY}}"
---

# Shopify Store Monitor

Track Shopify store sales, monitor store activity, and review real-time order signals.

Keywords: Shopify Sale Tracker, Shopify Store Tracker, Shopify Store Tracker & Monitor.

## Setup

1. Visit the official website at [ppspy.com](https://www.ppspy.com/) to view real-time dashboard data and product UI.
2. Visit the direct API site at [api.ppspy.com](https://api.ppspy.com/) to get your API key and manage billing/recharge.
3. Set the environment variable: `PPSPY_API_KEY`

## Available Tools (12 total)

### Sales Monitoring (12 tools)
- `ppspy_sales_monitor_create_group` — Create sales monitoring group
- `ppspy_sales_monitor_group_list` — List all sales monitoring groups
- `ppspy_sales_monitor_edit_group` — Edit group name
- `ppspy_sales_monitor_delete_group` — Delete group
- `ppspy_sales_monitor_create_task` — Create sales monitoring task(s), batch up to 50 URLs
- `ppspy_sales_monitor_task_list` — List sales monitoring tasks
- `ppspy_sales_monitor_task_details` — Detailed task info with daily/hourly stats
- `ppspy_sales_monitor_task_real_time_sales` — Real-time individual sales records
- `ppspy_sales_monitor_task_update` — Update task metadata (notes, group)
- `ppspy_sales_monitor_task_stop` — Stop a monitoring task
- `ppspy_sales_monitor_task_delete` — Delete stopped task(s)
- `ppspy_sales_monitor_task_overview` — Aggregated sales overview

## Usage Examples

- "Create a Shopify Sale Tracker task for this store"
- "Show me real-time sales for this Shopify store"
- "List all monitored Shopify stores"
- "Get daily and hourly sales stats for this store"
- "Move this store tracker task into another group"

## Credits

Each API call consumes credits from your PPSPY account:
- **Sales Monitoring**: 1 monitoring quota per task
- **Detail/Overview APIs**: Free
