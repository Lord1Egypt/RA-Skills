---
name: tiktok-live-cart-automation
description: "Automation for TikTok Live shopping, including monitoring pinned products, adding to cart, and preparing for checkout. Use for: automatically adding products to cart from TikTok Live streams, tracking potential purchases, and streamlining the buying process up to manual confirmation."
---

# TikTok Live Cart Automation

## Overview

This skill enables Manus to automate the process of detecting pinned products in TikTok Live streams, adding them to the shopping cart, and preparing for checkout. It streamlines the initial steps of purchasing, requiring manual confirmation for the final order placement to ensure security.

## Core Capabilities

### 1. Monitor Pinned Products

Automatically detects products that are pinned by the seller during a TikTok Live stream. This feature simulates real-time monitoring of live events to identify items available for purchase.

### 2. Add to Cart Automation

Upon detecting a pinned product, the skill automatically adds the specified quantity of the product to the user's shopping cart. This eliminates the need for manual clicking during fast-paced live sales.

### 3. Prepare for Checkout

After adding items to the cart, the system navigates to the checkout page and pre-fills necessary details, bringing the user to the final step before purchase. **A manual confirmation (clicking "Place Order") by the user is always required for security and to prevent unintended purchases.**

## Usage

To utilize the full automation, run the main script `tiktok_live_cart_automation.py` with the TikTok username of the live streamer and an optional duration for monitoring.

### Main Automation Script: `tiktok_live_cart_automation.py`

This script integrates all core functionalities: monitoring, adding to cart, and preparing for checkout.

**Basic Example:**
```bash
python3 /home/ubuntu/skills/tiktok-live-cart-automation/scripts/tiktok_live_cart_automation.py <tiktok_username>
```

**Advanced Example (with duration and headless mode):**
```bash
# Monitor @shop_owner for 300 seconds (5 minutes) in headless browser mode
python3 /home/ubuntu/skills/tiktok-live-cart-automation/scripts/tiktok_live_cart_automation.py shop_owner --duration 300 --headless
```

**Parameters:**
- `<tiktok_username>` (Required): The TikTok username of the live streamer (without the '@' symbol).
- `--duration` (Optional): The duration in seconds for which to monitor the live stream. Default is 300 seconds.
- `--headless` (Optional): A flag to run the browser in headless mode (without a visible UI). Requires Selenium and ChromeDriver setup.

### Supporting Scripts (for testing or individual use):

- **`monitor_pinned_products.py`**: Simulates the detection of a pinned product and saves its info to `pinned_product.json`.
- **`cart_automation.py`**: Reads `pinned_product.json` and simulates adding the product to the cart and navigating to checkout.

## Important Notes & Prerequisites

*   **Browser Login:** Ensure you are logged into your TikTok account in the browser before starting the automation, especially for cart and checkout steps.
*   **Manual Confirmation:** The final step of clicking "Place Order" must always be done manually by the user.
*   **Dependencies (for real-world usage beyond simulation):**
    *   **Selenium WebDriver:** `pip install selenium`
    *   **TikTok Live API Library:** `pip install TikTokLive` (Note: This is an unofficial API and may be subject to changes or discontinuation by TikTok.)
    *   **ChromeDriver:** Download the appropriate version for your Chrome browser from [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/) and ensure it's in your system's PATH.

For detailed instructions, troubleshooting, and file formats, please refer to the `USAGE_GUIDE.md` file located in the skill's root directory.

## Resources

### scripts/
- `tiktok_live_cart_automation.py`: The main script for full automation.
- `monitor_pinned_products.py`: Simulation script for pinned product detection.
- `cart_automation.py`: Simulation script for adding to cart and checkout preparation.

### references/
- `api_reference.md`: [TODO: Add specific TikTok Live API reference details if available and relevant.]

### templates/
- `example_template.txt`: [TODO: Remove or replace with relevant templates if needed, e.g., for report generation.]
