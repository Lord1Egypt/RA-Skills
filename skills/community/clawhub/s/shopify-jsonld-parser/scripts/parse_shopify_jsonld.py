#!/usr/bin/env python3
\"\"\"Parse Shopify JSON-LD for product offers/inventory.
Usage: python3 parse_shopify_jsonld.py [input.html] [--query FIELD] [--output json|yaml]

Extracts schema.org/Product + offers from HTML's JSON-LD scripts.
\"\"\"

import sys
import json
import re
import argparse
from pathlib import Path
from typing import Dict, Any, List, Union

def extract_jsonld_scripts(html: str) -> List[Dict[str, Any]]:
    \"\"\"Extract all application/ld+json scripts.\"\"\"
    scripts = []
    pattern = r'<script type="application/ld\\+json">(.*?)</script>'
    matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
    for match in matches:
        try:
            data = json.loads(match)
            scripts.append(data)
        except json.JSONDecodeError:
            pass
    return scripts

def find_product(jsonld: Dict[str, Any]) -> Dict[str, Any]:
    \"\"\"Find first @type: Product (recursive).\"\"\"
    if isinstance(jsonld, dict):
        atype = jsonld.get('@type')
        if atype == 'Product':
            return jsonld
        for key, val in jsonld.items():
            found = find_product(val)
            if found:
                return found
    elif isinstance(jsonld, list):
        for item in jsonld:
            found = find_product(item)
            if found:
                return found
    return None

def extract_offers(product: Dict[str, Any]) -> List[Dict[str, Any]]:
    \"\"\"Extract offers array or single.\"\"\"
    offers = product.get('offers', [])
    if isinstance(offers, dict):
        offers = [offers]
    extracted = []
    for offer in offers:
        if isinstance(offer, dict) and offer.get('@type') == 'Offer':
            ext = {
                'price': offer.get('price'),
                'priceCurrency': offer.get('priceCurrency'),
                'availability': offer.get('availability'),
                'url': offer.get('url'),
                'itemCondition': offer.get('itemCondition'),
                'sku': offer.get('sku'),
                'validFrom': offer.get('validFrom'),
            }
            extracted.append(ext)
    return extracted

def get_inventory_status(product: Dict[str, Any], offers: List) -> str:
    \"\"\"Infer inventory: InStock/OutOfStock/etc.\"\"\"
    prod_avail = product.get('availability')
    if prod_avail:
        return prod_avail.split('/')[-1]  # http://schema.org/InStock → InStock
    if offers:
        offer_avail = offers[0].get('availability')
        if offer_avail:
            return offer_avail.split('/')[-1]
    return 'Unknown'

def parse_file(input_path: Path) -> Dict[str, Any]:
    \"\"\"Parse HTML file.\"\"\"
    html = input_path.read_text()
    scripts = extract_jsonld_scripts(html)
    products = []
    for script in scripts:
        product = find_product(script)
        if product:
            offers = extract_offers(product)
            status = get_inventory_status(product, offers)
            result = {
                'name': product.get('name'),
                'description': product.get('description'),
                'image': product.get('image'),
                'sku': product.get('sku'),
                'brand': product.get('brand', {}).get('name'),
                'offers': offers,
                'inventory_status': status,
                'offers_count': len(offers),
            }
            products.append(result)
    if products:
        return {'products': products}
    return {'error': 'No product JSON-LD found'}

def main():
    parser = argparse.ArgumentParser(description='Parse Shopify JSON-LD')
    parser.add_argument('input', nargs='?', default=None, help='HTML file')
    parser.add_argument('--query', help='Query field e.g. offers[0].price')
    parser.add_argument('--output', default='json', choices=['json', 'yaml'])
    args = parser.parse_args()

    if args.input:
        input_path = Path(args.input)
    else:
        input_path = Path(sys.stdin.buffer.read())

    result = parse_file(input_path)

    if args.query:
        # Simple JSONPath-like query
        keys = args.query.split('.')
        val = result
        for k in keys:
            if '[' in k:
                key, idx = k.split('[')
                idx = int(idx.rstrip(']'))
                val = val.get(key, [])[idx]
            else:
                val = val.get(k)
        print(json.dumps(val))
    else:
        print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
