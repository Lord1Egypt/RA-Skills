#!/usr/bin/env python3
"""Manage WooCommerce products via REST API"""
import argparse, json, os, sys, urllib.request, urllib.parse
from base64 import b64encode
from security import require_secure_wp_url, should_confirm_publish, urlopen_authenticated

def make_wc_request(url, consumer_key, consumer_secret, endpoint, method='GET', data=None):
    """Make a WooCommerce REST API request"""
    api_url = f"{url.rstrip('/')}/wp-json/wc/v3/{endpoint}"
    
    # WooCommerce uses consumer key/secret as basic auth
    credentials = f"{consumer_key}:{consumer_secret}".encode('utf-8')
    auth_header = b64encode(credentials).decode('ascii')
    
    request_data = json.dumps(data).encode('utf-8') if data else None
    request = urllib.request.Request(api_url, data=request_data, method=method)
    request.add_header('Authorization', f'Basic {auth_header}')
    
    if data:
        request.add_header('Content-Type', 'application/json')
    
    try:
        with urlopen_authenticated(request) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        try:
            error_json = json.loads(error_body)
            print(json.dumps({"error": error_json}), file=sys.stderr)
        except:
            print(json.dumps({"error": f"HTTP {e.code}: {error_body}"}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

def confirm_live_product(url, status, assume_yes, verb, is_tty=None):
    """Prompt before a product goes live, exactly as create_post does for a post.

    Non-interactive runs (an agent, CI) are unchanged: should_confirm_publish
    returns False without a TTY, so this is a guard for a human at a terminal,
    not a gate an automation has to work around.
    """

    if is_tty is None:
        is_tty = sys.stdin.isatty()
    if not should_confirm_publish(status, assume_yes, is_tty):
        return
    print("About to %s a LIVE, purchasable product on %s. Type 'PUBLISH' to confirm:"
          % (verb, url), file=sys.stderr)
    print("> ", end="", file=sys.stderr)
    if input().strip() != "PUBLISH":
        print("Aborted: publish not confirmed.", file=sys.stderr)
        sys.exit(1)


def list_products(url, consumer_key, consumer_secret, per_page=10, page=1):
    """List WooCommerce products"""
    params = {'per_page': per_page, 'page': page}
    endpoint = f"products?{urllib.parse.urlencode(params)}"
    return make_wc_request(url, consumer_key, consumer_secret, endpoint)

def get_product(url, consumer_key, consumer_secret, product_id):
    """Get a single product"""
    return make_wc_request(url, consumer_key, consumer_secret, f"products/{product_id}")

def create_product(url, consumer_key, consumer_secret, title, price, description=None, **kwargs):
    """Create a new product.

    Defaults to a DRAFT. WooCommerce publishes a product whose status is
    omitted, so this put a priced, purchasable, indexable product straight onto
    a live storefront - while the skill's own instructions say to prefer drafts
    and get approval before live writes. Pass status explicitly to override.
    """

    data = {
        'name': title,
        'regular_price': str(price),
        'type': 'simple',
        'status': kwargs.get('status') or 'draft',
    }
    
    if description:
        data['description'] = description
    
    # Add optional fields
    for key in ['short_description', 'sku', 'status', 'stock_quantity', 'manage_stock', 'categories', 'images']:
        if key in kwargs and kwargs[key] is not None:
            data[key] = kwargs[key]
    
    return make_wc_request(url, consumer_key, consumer_secret, 'products', method='POST', data=data)

def update_product(url, consumer_key, consumer_secret, product_id, **kwargs):
    """Update a product"""
    data = {}
    
    # Add fields to update
    for key in ['name', 'regular_price', 'sale_price', 'description', 'short_description', 
                'status', 'sku', 'stock_quantity', 'manage_stock', 'categories', 'images']:
        if key in kwargs and kwargs[key] is not None:
            data[key] = kwargs[key]
    
    if not data:
        print(json.dumps({"error": "No fields to update"}), file=sys.stderr)
        sys.exit(1)
    
    return make_wc_request(url, consumer_key, consumer_secret, f"products/{product_id}", method='PUT', data=data)

def main():
    parser = argparse.ArgumentParser(description='Manage WooCommerce products')
    parser.add_argument('--url', default=os.getenv('WP_URL'))
    parser.add_argument('--consumer-key', default=os.getenv('WC_CONSUMER_KEY'), help='WooCommerce Consumer Key')
    parser.add_argument('--consumer-secret', default=os.getenv('WC_CONSUMER_SECRET'), help='WooCommerce Consumer Secret')
    parser.add_argument('--action', choices=['list', 'get', 'create', 'update'], required=True)
    parser.add_argument('--product-id', type=int, help='Product ID (for get/update)')
    parser.add_argument('--per-page', type=int, default=10, help='Products per page (for list)')
    parser.add_argument('--page', type=int, default=1, help='Page number (for list)')

    # Create/Update fields
    parser.add_argument('--title', '--name', dest='title', help='Product name/title')
    parser.add_argument('--price', help='Regular price')
    parser.add_argument('--sale-price', help='Sale price')
    parser.add_argument('--description', help='Product description')
    parser.add_argument('--short-description', help='Short description')
    parser.add_argument('--status', choices=['publish', 'draft', 'pending', 'private'], help='Product status')
    parser.add_argument('--sku', help='Product SKU')
    parser.add_argument('--stock-quantity', type=int, help='Stock quantity')
    parser.add_argument('--manage-stock', action='store_true', help='Enable stock management')
    parser.add_argument('--yes', '-y', action='store_true',
                        help='Skip the interactive confirmation for a live (publish) product')

    args = parser.parse_args()

    if not all([args.url, args.consumer_key, args.consumer_secret]):
        print(json.dumps({"error": "Missing WooCommerce credentials (--consumer-key, --consumer-secret)"}), file=sys.stderr)
        sys.exit(1)
    require_secure_wp_url(args.url)

    if args.action == 'list':
        result = list_products(args.url, args.consumer_key, args.consumer_secret, args.per_page, args.page)
        print(json.dumps(result, indent=2))

    elif args.action == 'get':
        if not args.product_id:
            print(json.dumps({"error": "--product-id required for get action"}), file=sys.stderr)
            sys.exit(1)
        result = get_product(args.url, args.consumer_key, args.consumer_secret, args.product_id)
        print(json.dumps(result, indent=2))

    elif args.action == 'create':
        if not args.title or not args.price:
            print(json.dumps({"error": "--title and --price required for create action"}), file=sys.stderr)
            sys.exit(1)

        status = args.status or 'draft'
        confirm_live_product(args.url, status, args.yes, "CREATE")
        result = create_product(
            args.url, args.consumer_key, args.consumer_secret,
            args.title, args.price,
            description=args.description,
            short_description=args.short_description,
            status=status,
            sku=args.sku,
            stock_quantity=args.stock_quantity,
            manage_stock=args.manage_stock
        )
        print(json.dumps(result, indent=2))

    elif args.action == 'update':
        if not args.product_id:
            print(json.dumps({"error": "--product-id required for update action"}), file=sys.stderr)
            sys.exit(1)

        update_fields = {}
        if args.title:
            update_fields['name'] = args.title
        if args.price:
            update_fields['regular_price'] = args.price
        if args.sale_price:
            update_fields['sale_price'] = args.sale_price
        if args.description:
            update_fields['description'] = args.description
        if args.short_description:
            update_fields['short_description'] = args.short_description
        if args.status:
            update_fields['status'] = args.status
            confirm_live_product(args.url, args.status, args.yes, "PUBLISH")
        if args.sku:
            update_fields['sku'] = args.sku
        if args.stock_quantity is not None:
            update_fields['stock_quantity'] = args.stock_quantity
        if args.manage_stock:
            update_fields['manage_stock'] = True

        result = update_product(args.url, args.consumer_key, args.consumer_secret, args.product_id, **update_fields)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
