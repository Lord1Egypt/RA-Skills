---
name: inventory-manager
description: E-commerce inventory management for Taobao, Douyin, and other platforms. Use when tracking stock levels, syncing inventory across stores, managing suppliers, or automating reorder alerts. Supports multi-store sync and sales forecasting.
---

# Inventory Manager

## Overview

Professional inventory management skill for e-commerce sellers. Track stock levels, sync across multiple stores (Taobao, Douyin), manage suppliers, and automate reordering.

## Features

- Multi-store inventory sync
- Stock level tracking
- Low stock alerts
- Supplier management
- Sales forecasting
- Purchase order generation
- Barcode/QR code support

## Quick Start

### Check Stock Levels

```bash
python scripts/check_stock.py \
  --stores taobao,douyin \
  --output stock_report.csv
```

### Sync Inventory

```bash
python scripts/sync_inventory.py \
  --source taobao \
  --target douyin \
  --sync-all
```

### Set Low Stock Alerts

```bash
python scripts/stock_alerts.py \
  --threshold 10 \
  --notify email,wechat
```

## Scripts

### check_stock.py

Check current stock levels across stores.

**Arguments:**
- `--stores` - Comma-separated store names
- `--output` - Output file (CSV/Excel)
- `--format` - Output format

### sync_inventory.py

Sync inventory between stores.

**Arguments:**
- `--source` - Source store
- `--target` - Target store(s)
- `--sync-all` - Sync all products
- `--sku` - Sync specific SKU

### stock_alerts.py

Monitor and alert on low stock.

**Arguments:**
- `--threshold` - Low stock threshold
- `--notify` - Notification channels
- `--check-interval` - Check frequency (minutes)

### generate_po.py

Generate purchase orders for suppliers.

**Arguments:**
- `--supplier` - Supplier name
- `--items` - Items to order
- `--output` - PO file

## Multi-Store Sync

### Taobao ↔ Douyin Sync

```bash
# Sync from Taobao to Douyin
python scripts/sync_inventory.py \
  --source taobao \
  --target douyin \
  --conflict-resolution source_wins

# Two-way sync
python scripts/sync_inventory.py \
  --source taobao \
  --target douyin \
  --sync-mode bidirectional
```

### Stock Level Rules

- **Source wins**: Source store quantities override target
- **Target wins**: Keep existing target quantities
- **Max**: Use maximum of both
- **Min**: Use minimum of both (safest)

## Low Stock Alerts

### Alert Configuration

```json
{
  "alerts": {
    "critical": {"threshold": 5, "action": "immediate_reorder"},
    "low": {"threshold": 10, "action": "send_alert"},
    "medium": {"threshold": 20, "action": "log_only"}
  },
  "notifications": {
    "email": "your@email.com",
    "wechat": "your_wechat_id"
  }
}
```

### Alert Actions

- **Email notification**: Send alert email
- **WeChat message**: Send WeChat notification
- **Auto reorder**: Generate purchase order
- **Pause listing**: Hide product from store

## Supplier Management

### Supplier Database

```csv
supplier_id,name,contact,email,lead_time_days,min_order
SUP001,Factory A,John, john@factory.com,7,100
SUP002,Factory B,Jane, jane@factory.com,14,50
```

### Purchase Order Generation

```bash
python scripts/generate_po.py \
  --supplier SUP001 \
  --items "SKU001:50,SKU002:100" \
  --output po_20260307.xlsx
```

## Sales Forecasting

### Forecast Next Month

```bash
python scripts/forecast_sales.py \
  --history sales_history.csv \
  --months 1 \
  --output forecast.csv
```

### Forecast Methods

- **Moving average**: Simple average of recent sales
- **Weighted average**: Recent sales weighted higher
- **Trend analysis**: Linear regression on historical data
- **Seasonal**: Account for seasonal patterns

## Reports

### Daily Stock Report

- Current stock levels
- Today's sales
- Stock changes
- Alerts triggered

### Weekly Summary

- Week-over-week changes
- Top selling products
- Slow moving items
- Reorder recommendations

### Monthly Analytics

- Monthly sales trends
- Inventory turnover
- Stock value
- Supplier performance

## Best Practices

1. **Sync frequently** - At least hourly during business hours
2. **Set buffer stock** - Don't wait until zero to reorder
3. **Track lead times** - Know how long suppliers take
4. **Monitor trends** - Adjust stock based on sales patterns
5. **Audit regularly** - Physical count vs system count

## Integration

### Taobao Store

- API integration for real-time stock
- Order webhook for automatic deduction
- Product mapping by SKU

### Douyin Store

- API integration for stock updates
- Live sales tracking
- Warehouse sync

## Troubleshooting

- **Sync conflicts**: Review conflict resolution settings
- **Stock mismatch**: Run physical audit
- **API errors**: Check API credentials and rate limits
- **Missing products**: Verify SKU mapping
