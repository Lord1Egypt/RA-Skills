---
name: token-usage-monitor
description: Monitor and display token usage metrics for AI models. Use when you need to track token consumption rates, view historical usage data, or get alerts about high token usage. Ideal for optimizing prompt costs and controlling AI service expenses.
---

# Token Usage Monitor

## Overview

This skill provides comprehensive token usage monitoring and reporting capabilities for AI models. It helps you track token consumption in real-time, analyze historical usage patterns, and receive alerts when usage exceeds predefined thresholds. Ideal for optimizing prompt costs, controlling AI service expenses, and ensuring efficient use of model resources.

## Core Capabilities

### 1. Real-Time Token Usage Monitoring
- Track token consumption per request, per session, and per model
- Monitor token usage speed (tokens per second/minute)
- View live usage metrics including prompt tokens, completion tokens, and total tokens

### 2. Historical Usage Analysis
- Generate usage reports for specified time periods (daily, weekly, monthly)
- Analyze usage trends across different models and applications
- Identify peak usage times and cost drivers

### 3. Threshold Alerts
- Set custom token usage thresholds for different models or sessions
- Receive notifications when usage exceeds defined limits
- Configure alert channels (chat, email, or system notifications)

### 4. Cost Estimation
- Calculate approximate costs based on token usage and model pricing
- Compare costs across different models and providers
- Optimize prompts to reduce token usage and costs

## Quick Start

### Monitor Current Session Usage
```bash
# Check current session token usage
python scripts/token_usage_tracker.py --session
```

### Generate Daily Usage Report
```bash
# Generate report for today's usage
python scripts/token_usage_tracker.py --report --period day
```

### Set Usage Threshold
```bash
# Set threshold of 100,000 tokens per day for GPT-4
python scripts/token_usage_tracker.py --set-threshold --model gpt-4 --limit 100000 --period day
```

## Resources

### scripts/

Create only the resource directories this skill actually needs. Delete this section if no resources are required.

### scripts/
- `token_usage_tracker.py`: Main script for tracking and reporting token usage
  
  **Key features:**
  - Tracks token usage per session, model, and time period
  - Generates daily usage reports with cost estimates
  - Supports custom usage thresholds and alerts
  - Provides real-time and historical usage analytics

  **Usage examples:**
  ```bash
  # Track a single usage event
  python scripts/token_usage_tracker.py --track --model doubao-seed --prompt-tokens 100 --completion-tokens 200
  
  # View current session usage
  python scripts/token_usage_tracker.py --session
  
  # Generate daily usage report
  python scripts/token_usage_tracker.py --report --period day
  
  # Set usage threshold (100,000 tokens/day for Doubao)
  python scripts/token_usage_tracker.py --set-threshold --model doubao-seed --limit 100000
  
  # View overall usage summary
  python scripts/token_usage_tracker.py --summary
  ```

**Note:** The script automatically creates and manages a data file at `~/.openclaw/token_usage.json` to store usage data.

### references/
Documentation and reference material intended to be loaded into context to inform Codex's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Codex should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Codex produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Not every skill requires all three types of resources.**
