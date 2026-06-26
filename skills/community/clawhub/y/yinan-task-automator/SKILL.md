---
name: task-automator
description: Automate repetitive computer tasks including file operations, data processing, web scraping, and API integrations. Use when you need to batch process files, sync data, schedule recurring tasks, or create custom automation workflows.
---

# Task Automator

## Overview

Universal task automation skill for OpenClaw. Automate file operations, data processing, API calls, and create custom workflows with scheduling support.

## Use Cases

- **File Operations**: Batch rename, convert, organize files
- **Data Processing**: CSV/JSON/Excel manipulation, data cleaning
- **API Integration**: Connect multiple services, sync data
- **Scheduled Tasks**: Cron-like automation, recurring jobs
- **Web Automation**: Scrape, monitor, alert
- **E-commerce**: Order processing, inventory sync, price updates

## Quick Start

### Run a Simple Task

```bash
python scripts/run_task.py --task file_organizer --config tasks/organize.json
```

### Schedule a Recurring Task

```bash
python scripts/schedule_task.py --task data_backup --cron "0 2 * * *"
```

### Create a Workflow

```bash
python scripts/run_workflow.py --workflow ecommerce_sync
```

## Built-in Tasks

### 1. File Organizer

Organize files by type, date, or custom rules.

**Config (tasks/organize.json):**
```json
{
  "source": "~/Downloads",
  "destination": "~/Organized",
  "rules": [
    {"extension": ".pdf", "folder": "Documents"},
    {"extension": ".jpg", "folder": "Images"},
    {"extension": ".mp4", "folder": "Videos"}
  ]
}
```

### 2. Data Converter

Convert between CSV, JSON, Excel formats.

**Usage:**
```bash
python scripts/convert_data.py --input data.csv --output data.json --format json
```

### 3. API Sync

Sync data between two APIs.

**Config (tasks/api_sync.json):**
```json
{
  "source": {
    "type": "api",
    "url": "https://api.source.com/data",
    "auth": "bearer_token"
  },
  "destination": {
    "type": "api",
    "url": "https://api.dest.com/items",
    "auth": "api_key"
  },
  "mapping": {
    "source_field": "dest_field"
  }
}
```

### 4. Web Monitor

Monitor websites and send alerts.

**Config (tasks/monitor.json):**
```json
{
  "urls": [
    {"url": "https://example.com/product", "check": "price < 100"}
  ],
  "alert": {
    "type": "email",
    "to": "you@example.com"
  }
}
```

### 5. E-commerce Order Processor

Process orders from Taobao/Douyin stores.

**Config (tasks/order_process.json):**
```json
{
  "stores": ["taobao", "douyin"],
  "actions": [
    "fetch_new_orders",
    "update_inventory",
    "generate_shipping_labels",
    "send_confirmation_email"
  ]
}
```

## Scripts

### run_task.py

Execute a single automated task.

**Arguments:**
- `--task` - Task name
- `--config` - Task configuration file
- `--dry-run` - Simulate without executing
- `--verbose` - Detailed logging

### schedule_task.py

Schedule recurring tasks.

**Arguments:**
- `--task` - Task name
- `--cron` - Cron expression (e.g., "0 2 * * *")
- `--config` - Task config file

### run_workflow.py

Execute multi-step workflows.

**Arguments:**
- `--workflow` - Workflow name
- `--steps` - Run specific steps only
- `--continue-on-error` - Don't stop on errors

## Creating Custom Tasks

### Step 1: Create Task Script

```python
# scripts/tasks/my_task.py
from base_task import BaseTask

class MyTask(BaseTask):
    def run(self, config):
        # Your automation logic here
        self.log("Starting task...")
        
        # Process
        result = self.process(config)
        
        # Return status
        return {"status": "success", "data": result}
```

### Step 2: Create Configuration

```json
{
  "name": "my_task",
  "description": "What this task does",
  "config_schema": {
    "required": ["input_path", "output_path"],
    "properties": {
      "input_path": {"type": "string"},
      "output_path": {"type": "string"}
    }
  }
}
```

### Step 3: Register Task

Add to `tasks/registry.json`:
```json
{
  "my_task": {
    "script": "tasks/my_task.py",
    "config": "tasks/my_task.json"
  }
}
```

## Workflows

Workflows chain multiple tasks together.

**Example: E-commerce Daily Sync**

```yaml
name: ecommerce_daily_sync
steps:
  - task: fetch_orders
    stores: [taobao, douyin]
  - task: update_inventory
    sync_stores: true
  - task: generate_reports
    format: excel
  - task: send_summary
    channel: email
```

## Scheduling

Use cron expressions for scheduling:

| Expression | Meaning |
|------------|---------|
| `0 * * * *` | Every hour |
| `0 2 * * *` | Daily at 2 AM |
| `0 9 * * 1-5` | Weekdays at 9 AM |
| `0 0 1 * *` | First of every month |

## Integration with E-commerce

### Taobao/Douyin Store Automation

```bash
# Daily order sync
python scripts/run_task.py --task order_sync --config tasks/taobao_sync.json

# Inventory update
python scripts/run_task.py --task inventory_update --config tasks/inventory.json

# Price monitoring
python scripts/run_task.py --task price_monitor --config tasks/prices.json
```

## Best Practices

1. **Test with --dry-run** before running live
2. **Log everything** for debugging
3. **Handle errors gracefully** with retries
4. **Use environment variables** for secrets
5. **Schedule wisely** to avoid rate limits
6. **Monitor task health** with status checks

## Security

- Store API keys in environment variables
- Use `.env` files (never commit them)
- Validate all inputs
- Sanitize file paths to prevent directory traversal
- Rate limit API calls

## Troubleshooting

- **Task fails silently**: Check logs in `logs/` directory
- **API rate limited**: Add delays between requests
- **File not found**: Verify paths are absolute or relative to workspace
- **Permission denied**: Check file/folder permissions
