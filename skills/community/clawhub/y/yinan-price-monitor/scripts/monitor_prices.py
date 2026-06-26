#!/usr/bin/env python3
"""
Price Monitor Script
Monitors product prices from a CSV list and logs changes.

Usage:
    python monitor_prices.py products.csv [--alert-threshold 10]

Output:
    - price-history.csv: Historical price data
    - Console output for immediate feedback
"""

import csv
import json
import subprocess
import sys
import argparse
from datetime import datetime
from pathlib import Path

def run_agent_browser(args, timeout=30000):
    """Run agent-browser command and return output."""
    cmd = ["agent-browser"] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Timeout", -1
    except Exception as e:
        return "", str(e), -1

def get_page_snapshot(url):
    """Open URL and get interactive snapshot."""
    # Open the page
    stdout, stderr, code = run_agent_browser(["open", url])
    if code != 0:
        return None, f"Failed to open {url}: {stderr}"
    
    # Get snapshot
    stdout, stderr, code = run_agent_browser(["snapshot", "-i", "--json"])
    if code != 0:
        return None, f"Failed to get snapshot: {stderr}"
    
    try:
        elements = json.loads(stdout)
        return elements, None
    except json.JSONDecodeError:
        return None, "Failed to parse snapshot JSON"

def extract_price(url, selector):
    """Extract price from a webpage using agent-browser."""
    # Open the page
    stdout, stderr, code = run_agent_browser(["open", url])
    if code != 0:
        return None, f"Failed to open page: {stderr}"
    
    # Try to find element by selector
    stdout, stderr, code = run_agent_browser(["get", "text", selector])
    if code != 0:
        # Fallback: get snapshot and search manually
        elements, err = get_page_snapshot(url)
        if elements:
            # Look for price-like elements
            for elem in elements.get("elements", []):
                text = elem.get("text", "")
                if "$" in text or "¥" in text or "€" in text:
                    return text.strip(), None
        return None, f"Failed to extract price: {stderr}"
    
    return stdout.strip(), None

def load_products(csv_path):
    """Load product list from CSV file."""
    products = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append({
                'url': row.get('url', ''),
                'selector': row.get('selector', ''),
                'name': row.get('name', row.get('url', 'Unknown')),
                'min_price': float(row.get('min_price', 0)) if row.get('min_price') else None,
                'max_price': float(row.get('max_price', 0)) if row.get('max_price') else None,
            })
    return products

def load_history(history_path):
    """Load existing price history."""
    history = {}
    if Path(history_path).exists():
        with open(history_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = row.get('name', row.get('url'))
                history[key] = {
                    'last_price': row.get('price', ''),
                    'last_check': row.get('timestamp', ''),
                }
    return history

def save_history(history_path, results):
    """Save price results to history file."""
    file_exists = Path(history_path).exists()
    
    with open(history_path, 'a', encoding='utf-8', newline='') as f:
        fieldnames = ['timestamp', 'name', 'url', 'price', 'status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        for result in results:
            writer.writerow(result)

def check_price_change(current_price, last_price, threshold_percent):
    """Check if price changed beyond threshold."""
    try:
        # Extract numeric value from price strings
        import re
        curr_num = float(re.sub(r'[^\d.]', '', current_price.replace(',', '')))
        last_num = float(re.sub(r'[^\d.]', '', last_price.replace(',', '')))
        
        if last_num == 0:
            return False, 0
        
        change_percent = abs(curr_num - last_num) / last_num * 100
        return change_percent > threshold_percent, change_percent
    except (ValueError, AttributeError):
        return False, 0

def main():
    parser = argparse.ArgumentParser(description='Monitor product prices')
    parser.add_argument('products_csv', help='Path to products CSV file')
    parser.add_argument('--alert-threshold', type=float, default=10.0,
                        help='Price change percentage to trigger alert (default: 10)')
    parser.add_argument('--output', default='price-history.csv',
                        help='Output history file (default: price-history.csv)')
    args = parser.parse_args()
    
    # Load products
    print(f"Loading products from {args.products_csv}...")
    products = load_products(args.products_csv)
    print(f"Found {len(products)} products to monitor\n")
    
    # Load existing history
    history = load_history(args.output)
    
    # Monitor each product
    results = []
    alerts = []
    
    for i, product in enumerate(products, 1):
        print(f"[{i}/{len(products)}] Checking {product['name']}...")
        
        price, error = extract_price(product['url'], product['selector'])
        timestamp = datetime.now().isoformat()
        
        if error:
            print(f"  ❌ Error: {error}")
            results.append({
                'timestamp': timestamp,
                'name': product['name'],
                'url': product['url'],
                'price': f'ERROR: {error}',
                'status': 'error'
            })
            continue
        
        print(f"  ✓ Price: {price}")
        
        # Check for price change
        status = 'unchanged'
        if product['name'] in history:
            last_price = history[product['name']]['last_price']
            is_significant, change_pct = check_price_change(
                price, last_price, args.alert_threshold
            )
            if is_significant:
                status = 'changed'
                alert_msg = f"🚨 PRICE ALERT: {product['name']} changed from {last_price} to {price} ({change_pct:.1f}%)"
                print(f"  {alert_msg}")
                alerts.append(alert_msg)
            elif price != last_price:
                status = 'minor_change'
        
        results.append({
            'timestamp': timestamp,
            'name': product['name'],
            'url': product['url'],
            'price': price,
            'status': status
        })
        
        # Small delay to be polite to servers
        import time
        time.sleep(2)
    
    # Save results
    save_history(args.output, results)
    print(f"\n✅ Results saved to {args.output}")
    
    # Print alerts summary
    if alerts:
        print(f"\n🚨 {len(alerts)} price alert(s):")
        for alert in alerts:
            print(f"  - {alert}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
