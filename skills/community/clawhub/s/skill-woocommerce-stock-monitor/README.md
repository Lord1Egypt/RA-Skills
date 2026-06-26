# skill-woocommerce-stock-monitor — WooCommerce Out-of-Stock Alerts

Monitor WooCommerce products for out-of-stock changes and send Telegram alerts.

## Use When
- Monitoring product stock levels daily
- Getting notified when products go out of stock
- Tracking restocks after a product was OOS
- Running automated inventory health checks

## Key Features
- Fetches all WooCommerce products via REST API
- Detects out-of-stock status changes
- Sends Telegram alert with product name and link
- Designed to run daily via OpenClaw cron

## Requirements
- WooCommerce REST API key (read access)
- Telegram bot token and chat ID

## Scheduling
Recommended: daily cron at 08:00 local time.
Load the SKILL.md for cron setup instructions.

## Version
1.0.0
