#!/usr/bin/env python3
"""
search-1688-supplier: Search 1688 suppliers via AlphaShop AI Select Provider API.
Supports text query, 1688 product URL, or image URL as input.
"""
import sys
import json
import os
import re
import argparse
import urllib.parse
import time
import requests
import jwt

API_URL = "https://api.alphashop.cn/ai.select.provider.search/1.0"


def get_api_key():
    """Generate JWT token using ALPHASHOP_ACCESS_KEY and ALPHASHOP_SECRET_KEY."""
    ak = os.environ.get("ALPHASHOP_ACCESS_KEY", "").strip()
    sk = os.environ.get("ALPHASHOP_SECRET_KEY", "").strip()

    if not ak:
        print("Error: ALPHASHOP_ACCESS_KEY not set. Configure it in OpenClaw:\n"
              '  skills.entries.search-1688-supplier.env.ALPHASHOP_ACCESS_KEY',
              file=sys.stderr)
        sys.exit(1)

    if not sk:
        print("Error: ALPHASHOP_SECRET_KEY not set. Configure it in OpenClaw:\n"
              '  skills.entries.search-1688-supplier.env.ALPHASHOP_SECRET_KEY',
              file=sys.stderr)
        sys.exit(1)

    current_time = int(time.time())
    token = jwt.encode(
        payload={
            "iss": ak,
            "exp": current_time + 1800,
            "nbf": current_time - 5,
        },
        key=sk,
        algorithm="HS256",
        headers={"alg": "HS256"},
    )
    # PyJWT < 2.0 returns bytes, >= 2.0 returns str
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


def detect_input_type(value):
    """Detect whether input is: image_url, product_url, or text query."""
    value = value.strip()

    # Image URL patterns
    image_exts = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff')
    parsed = urllib.parse.urlparse(value)

    if parsed.scheme in ('http', 'https'):
        path_lower = parsed.path.lower()
        # Check if it's a 1688 product URL
        if '1688.com' in parsed.netloc:
            product_match = re.search(r'/offer/([0-9]+)\.html', value)
            if product_match:
                return 'product_url', value
            query_params = urllib.parse.parse_qs(parsed.query)
            if 'offerId' in query_params:
                return 'product_url', value

        # Check if it looks like an image URL
        if any(path_lower.endswith(ext) for ext in image_exts):
            return 'image_url', value
        # Common image hosting patterns
        if any(h in parsed.netloc for h in ['img.', 'image.', 'cdn.', 'cbu01.alicdn']):
            return 'image_url', value
        # If URL but not 1688 product, assume image
        return 'image_url', value

    # Pure numeric → treat as product ID, convert to URL
    if value.isdigit():
        url = f"https://detail.1688.com/offer/{value}.html"
        return 'product_url', url

    # Otherwise, it's a text query
    return 'query', value


def extract_product_title_from_url(product_url, api_key):
    """Use the existing product detail API to get the product title for searching."""
    detail_api = "https://api.alphashop.cn/alphashop.openclaw.offer.detail.query/1.0"
    product_match = re.search(r'/offer/([0-9]+)\.html', product_url)
    if not product_match:
        parsed = urllib.parse.urlparse(product_url)
        params = urllib.parse.parse_qs(parsed.query)
        pid = params.get('offerId', [None])[0]
    else:
        pid = product_match.group(1)

    if not pid:
        return None, None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    try:
        resp = requests.post(detail_api, json={"productId": pid}, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            # Try to extract title and image from response
            result = data.get("result", {})
            if isinstance(result, dict):
                r = result.get("result", result)
                title = r.get("subjectTrans") or r.get("subject") or r.get("title")
                # Try to get first image
                images = r.get("productImage", {}).get("images", [])
                img_url = images[0] if images else None
                return title, img_url
    except Exception:
        pass
    return None, None


def call_search_api(api_key, intention="AUTO", query=None, image_url=None):
    """Call the AlphaShop AI Select Provider Search API."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {"intention": intention}
    if query:
        payload["query"] = query
    if image_url:
        payload["searchImageUrl"] = image_url

    resp = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    if resp.status_code != 200:
        print(f"Error: HTTP {resp.status_code}\n{resp.text[:500]}", file=sys.stderr)
        sys.exit(1)

    data = resp.json()
    if data.get("resultCode") != "SUCCESS":
        print(f"API Error: {json.dumps(data, ensure_ascii=False, indent=2)}", file=sys.stderr)
        sys.exit(1)

    return data


def parse_price(price_str):
    """Extract numeric price from string like '¥12.50' or '12.50-15.00'."""
    if not price_str:
        return None
    # Take the first number found
    match = re.search(r'[\d]+\.?\d*', str(price_str))
    return float(match.group()) if match else None


def parse_moq(infos):
    """Extract MOQ from purchaseInfos list. Label is '起批量', value like 'X件起批'."""
    if not infos:
        return None
    for item in infos:
        label = str(item.get("label", ""))
        if label == "起批量":
            val = str(item.get("value", ""))
            match = re.search(r'(\d+)', val)
            if match:
                return int(match.group(1))
    return None


def parse_ship_rate_48h(infos):
    """Extract 48H shipping rate from shipInfos list. Label like '48H发货率', value like '95%'."""
    if not infos:
        return None
    for item in infos:
        label = str(item.get("label", ""))
        if "48" in label and "发货" in label:
            val = str(item.get("value", ""))
            match = re.search(r'([\d]+\.?\d*)', val)
            if match:
                return float(match.group(1))
    return None


def filter_offers(offers, max_price=None, max_moq=None, min_ship_rate_48h=None):
    """Filter offer list based on user criteria."""
    filtered = []
    for offer in offers:
        # Price filter (no data → keep, since price is usually available)
        if max_price is not None:
            price = parse_price(offer.get("itemPrice"))
            if price is not None and price > max_price:
                continue

        # MOQ filter (no data → keep, since MOQ is usually available)
        if max_moq is not None:
            moq = parse_moq(offer.get("purchaseInfos", []))
            if moq is not None and moq > max_moq:
                continue

        # 48H shipping rate filter (no data → exclude, user explicitly requires this metric)
        if min_ship_rate_48h is not None:
            rate = parse_ship_rate_48h(offer.get("shipInfos", []))
            if rate is None or rate < min_ship_rate_48h:
                continue

        filtered.append(offer)
    return filtered


def format_first_offer(offer):
    """Extract key product + supplier info from first matching offer."""
    result = {
        "product": {
            "itemId": offer.get("itemId"),
            "title": offer.get("title"),
            "price": offer.get("itemPrice"),
            "imageUrl": offer.get("imageUrl"),
            "detailUrl": offer.get("offerDetailUrl"),
            "aiAttentions": offer.get("aiAttentions", []),
            "coreAttributes": offer.get("coreAttributes", []),
            "salesInfos": offer.get("salesInfos", []),
            "purchaseInfos": offer.get("purchaseInfos", []),
            "shipInfos": offer.get("shipInfos", []),
        },
        "supplier": {},
    }
    pi = offer.get("providerInfo", {})
    if pi:
        result["supplier"] = {
            "companyName": pi.get("companyName"),
            "factoryUrl": pi.get("factoryUrl"),
            "tags": [t.get("tagName") for t in pi.get("providerTags", []) if t.get("tagName")],
        }
    # Extra supplier fields at offer level
    result["supplier"]["services"] = offer.get("providerServices", [])
    result["supplier"]["kjCustomTags"] = offer.get("providerKjCustomTags", [])
    return result


def format_first_provider(provider):
    """Extract key info from first matching provider."""
    result = {
        "supplier": {
            "companyName": provider.get("companyName"),
            "factoryUrl": provider.get("factoryUrl"),
            "loginId": provider.get("loginId"),
            "mainCategory": provider.get("mainCategoryName"),
            "tags": [t.get("tagName") for t in provider.get("providerTags", []) if t.get("tagName")],
            "kjCustomTags": provider.get("providerKjCustomTags", []),
            "aiAttentions": provider.get("aiAttentions", []),
            "services": provider.get("providerServices", []),
        },
        "recommendedProducts": [],
    }
    for item in provider.get("recommendItems", []):
        result["recommendedProducts"].append({
            "itemId": item.get("itemId"),
            "title": item.get("title"),
            "price": item.get("itemPrice"),
            "imageUrl": item.get("imageUrl"),
            "detailUrl": item.get("offerDetailUrl"),
        })
    return result


def format_output(data, max_price=None, max_moq=None, min_ship_rate_48h=None, exclude_item_id=None):
    """Format API response — output only the first matching result."""
    result = data.get("result", {}).get("result", {})
    real_intention = result.get("realIntention", "")
    output = {
        "realIntention": real_intention,
        "filters_applied": {
            "max_price": max_price,
            "max_moq": max_moq,
            "min_ship_rate_48h": min_ship_rate_48h
        },
        "match": None,
    }
    if exclude_item_id:
        output["excluded_item_id"] = exclude_item_id

    if real_intention == "SEARCH_OFFER":
        offer_info = result.get("offerInfo", {})
        offers = offer_info.get("offerList", [])

        # Exclude the source product when searching by 1688 URL
        if exclude_item_id:
            offers = [o for o in offers if str(o.get("itemId", "")) != str(exclude_item_id)]

        total = len(offers)

        if max_price is not None or max_moq is not None or min_ship_rate_48h is not None:
            offers = filter_offers(offers, max_price, max_moq, min_ship_rate_48h)

        output["total_before_filter"] = total
        output["total_after_filter"] = len(offers)

        if offers:
            output["match"] = format_first_offer(offers[0])
        else:
            output["match"] = None
            output["message"] = "No offers match the filter criteria."

    elif real_intention == "SEARCH_PROVIDER":
        provider_info = result.get("providerInfo", {})
        providers = provider_info.get("providerList", [])

        output["total_results"] = len(providers)
        if providers:
            output["match"] = format_first_provider(providers[0])
        else:
            output["match"] = None
            output["message"] = "No providers found."

    elif real_intention in ("DIRECT_SEARCH_PROVIDER", "OTHER"):
        output["chatResponse"] = result.get("chatResponse", "")

    return output


def main():
    parser = argparse.ArgumentParser(description="Search 1688 suppliers via AlphaShop API")
    parser.add_argument("input", help="1688 product URL, image URL, or text query")
    parser.add_argument("--mode", choices=["AUTO", "SEARCH_OFFER", "SEARCH_PROVIDER"],
                        default="AUTO", help="Search mode (default: AUTO)")
    parser.add_argument("--max-price", type=float, default=None,
                        help="Maximum unit price filter")
    parser.add_argument("--max-moq", type=int, default=None,
                        help="Maximum minimum order quantity filter")
    parser.add_argument("--min-ship-rate-48h", type=float, default=None,
                        help="Minimum 48H shipping rate percentage (e.g. 90 means >=90%%)")

    args = parser.parse_args()
    api_key = get_api_key()

    input_type, value = detect_input_type(args.input)

    query = None
    image_url = None
    exclude_item_id = None

    if input_type == 'image_url':
        image_url = value
    elif input_type == 'product_url':
        # Extract product ID to exclude from results (user wants OTHER suppliers)
        product_match = re.search(r'/offer/([0-9]+)\.html', value)
        if product_match:
            exclude_item_id = product_match.group(1)
        else:
            parsed = urllib.parse.urlparse(value)
            params = urllib.parse.parse_qs(parsed.query)
            pid = params.get('offerId', [None])[0]
            if pid:
                exclude_item_id = pid

        # Get product info first, then search by title + image
        title, img = extract_product_title_from_url(value, api_key)
        if title:
            query = title
        if img:
            image_url = img
        if not query and not image_url:
            print(f"Error: Could not extract product info from URL: {value}", file=sys.stderr)
            sys.exit(1)
    else:
        query = value

    data = call_search_api(api_key, intention=args.mode, query=query, image_url=image_url)
    output = format_output(data, args.max_price, args.max_moq, args.min_ship_rate_48h, exclude_item_id=exclude_item_id)
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
