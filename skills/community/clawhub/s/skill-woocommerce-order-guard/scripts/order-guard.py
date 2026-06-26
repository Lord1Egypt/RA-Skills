#!/usr/bin/env python3
"""
WooCommerce Order Guard
- Fetches all 'processing' orders
- Copies billing address → shipping when shipping address is empty
- Deduplicates alerts via a local JSON store
- Prints NEW_ORDER_ID: <id> for each new order (for cron/webhook upstream)
- Prints HEARTBEAT_OK if no new orders

Usage:
  python3 order-guard.py [--creds /path/to/woo-api.json] [--storage /path/to/fulfilled_orders.json]
"""

import requests
import json
import os
import argparse

DEFAULT_CREDS = os.path.expanduser("~/woo-api.json")
DEFAULT_STORAGE = os.path.expanduser("~/.openclaw/workspace/memory/fulfilled_orders.json")


def load_creds(path):
    with open(path) as f:
        return json.load(f)


def load_storage(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f).get("alerted_orders", [])
    return []


def save_storage(path, alerted_orders):
    with open(path, 'w') as f:
        json.dump({"alerted_orders": alerted_orders}, f)


def copy_billing_to_shipping(order):
    billing = order.get('billing', {})
    return {
        "first_name": billing.get('first_name'),
        "last_name": billing.get('last_name'),
        "company": billing.get('company'),
        "address_1": billing.get('address_1'),
        "address_2": billing.get('address_2'),
        "city": billing.get('city'),
        "state": billing.get('state'),
        "postcode": billing.get('postcode'),
        "country": billing.get('country'),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--creds', default=DEFAULT_CREDS)
    parser.add_argument('--storage', default=DEFAULT_STORAGE)
    args = parser.parse_args()

    creds = load_creds(args.creds)
    url = creds['url']
    auth = (creds['consumerKey'], creds['consumerSecret'])
    alerted_orders = load_storage(args.storage)

    resp = requests.get(f"{url}/wp-json/wc/v3/orders?status=processing&per_page=20", auth=auth)
    resp.raise_for_status()
    orders = resp.json()

    new_orders = [o for o in orders if o['id'] not in alerted_orders]

    if not new_orders:
        print("HEARTBEAT_OK")
        return

    for order in new_orders:
        order_id = order['id']
        shipping = order.get('shipping', {})

        if not shipping.get('address_1'):
            update_data = {"shipping": copy_billing_to_shipping(order)}
            requests.put(f"{url}/wp-json/wc/v3/orders/{order_id}", auth=auth, json=update_data)

        alerted_orders.append(order_id)
        print(f"NEW_ORDER_ID: {order_id}")

    save_storage(args.storage, alerted_orders)


if __name__ == "__main__":
    main()
