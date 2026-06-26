"""Shopify Manager CLI."""

import sys
import argparse
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from client import ShopifyClient
from safety import SafetyManager, AuditLogger
from operations.products import ProductOperations
from operations.orders import OrderOperations
from operations.content import ContentOperations
from operations.themes import ThemeOperations
from operations.theme_settings import ThemeSettingsOperations
from operations.metafields import MetafieldOperations, MetaobjectOperations
from operations.media import MediaOperations


def print_header(title: str):
    """Print section header."""
    print(f"\n{'='*60}")
    print(f"🛍️  {title}")
    print(f"{'='*60}\n")


def cmd_ask(args):
    """Handle natural language requests."""
    print_header("Shopify Assistant")
    
    config = Config(args.config)
    client = ShopifyClient(config)
    safety = SafetyManager(config)
    audit = AuditLogger(config)
    
    if args.execute:
        safety.set_dry_run(False)
    
    prompt = args.prompt
    
    # Simple keyword-based routing (in real implementation, use LLM)
    prompt_lower = prompt.lower()
    
    # Product-related
    if any(word in prompt_lower for word in ['add', 'create', 'new']) and 'product' in prompt_lower:
        print(f"📝 Interpreted as: Create product")
        print(f"   Prompt: {prompt}")
        print("\n⚠️  This would use LLM to parse product details from the prompt")
        print("   For now, use: /shopify products create")
        
    elif any(word in prompt_lower for word in ['update', 'change', 'edit']) and 'product' in prompt_lower:
        print(f"📝 Interpreted as: Update product")
        print(f"   Prompt: {prompt}")
        print("\n⚠️  This would use LLM to identify product and updates")
        print("   For now, use: /shopify products update <handle>")
        
    elif 'sale' in prompt_lower or 'discount' in prompt_lower:
        print(f"📝 Interpreted as: Create sale/discount")
        print(f"   Prompt: {prompt}")
        print("\n⚠️  Discount operations not yet implemented")
        
    elif 'fulfill' in prompt_lower or 'order' in prompt_lower:
        print(f"📝 Interpreted as: Order operation")
        print(f"   Prompt: {prompt}")
        orders = OrderOperations(client, safety, audit)
        
        # Try to extract order ID
        words = prompt.split()
        for word in words:
            if word.startswith('#'):
                order_id = word[1:]
                print(f"\n📦 Order #{order_id}")
                order = orders.get_order(order_id)
                if order:
                    print(f"   Customer: {order.get('customer', {}).get('email', 'Guest')}")
                    print(f"   Total: {order.get('total_price')}")
                    print(f"   Status: {order.get('financial_status')} / {order.get('fulfillment_status') or 'unfulfilled'}")
                else:
                    print(f"   Order not found")
                break
        
    elif 'report' in prompt_lower or 'sales' in prompt_lower:
        print(f"📝 Interpreted as: Generate report")
        print(f"   Prompt: {prompt}")
        print("\n⚠️  Report operations not yet implemented")
        
    else:
        print(f"📝 Prompt: {prompt}")
        print("\n⚠️  Full natural language processing requires LLM integration")
        print("   For now, use specific commands:")
        print("   - /shopify products list")
        print("   - /shopify orders list")
        print("   - /shopify content pages list")


def cmd_products(args):
    """Handle product commands."""
    print_header("Product Management")
    
    config = Config(args.config)
    client = ShopifyClient(config)
    safety = SafetyManager(config)
    audit = AuditLogger(config)
    
    if args.execute:
        safety.set_dry_run(False)
    
    products = ProductOperations(client, safety, audit)
    
    if args.action == 'list':
        filters = {}
        if args.collection:
            filters['collection_id'] = args.collection
        if args.tag:
            filters['tag'] = args.tag
            
        items = products.list_products(limit=args.limit, **filters)
        print(products.format_product_list(items))
        print(f"\n📊 Showing {len(items)} products")
        
    elif args.action == 'get':
        product = products.get_product(args.identifier)
        if product:
            print(f"\n📦 Product: {product.get('title')}")
            print(f"   ID: {product.get('id')}")
            print(f"   Handle: {product.get('handle')}")
            print(f"   Type: {product.get('product_type')}")
            print(f"   Vendor: {product.get('vendor')}")
            print(f"   Tags: {', '.join(product.get('tags', []))}")
            print(f"\n   Variants:")
            for v in product.get('variants', []):
                print(f"   - {v.get('title')}: ${v.get('price')} (SKU: {v.get('sku')}) - Stock: {v.get('inventory_quantity', 0)}")
        else:
            print(f"❌ Product not found: {args.identifier}")
            
    elif args.action == 'create':
        print("Interactive product creation not yet implemented.")
        print("Use: /shopify ask \"Add product...\" --execute")
        
    elif args.action == 'update':
        if args.price:
            result = products.update_product(args.identifier, price=args.price)
            if 'error' in result:
                print(f"❌ {result['error']}")
            elif result.get('dry_run'):
                print("\n✋ Dry run complete. Add --execute to apply.")
            else:
                print(f"✅ Product updated: {result.get('title')}")
                
    elif args.action == 'delete':
        result = products.delete_product(args.identifier, force=args.force)
        if result.get('cancelled'):
            print("❌ Operation cancelled")
        elif result.get('dry_run'):
            print("\n✋ Dry run complete. Add --execute --force to apply.")
        else:
            print(f"✅ Product deleted: {result.get('title')}")


def cmd_orders(args):
    """Handle order commands."""
    print_header("Order Management")
    
    config = Config(args.config)
    client = ShopifyClient(config)
    safety = SafetyManager(config)
    audit = AuditLogger(config)
    
    if args.execute:
        safety.set_dry_run(False)
    
    orders = OrderOperations(client, safety, audit)
    
    if args.action == 'list':
        items = orders.list_orders(status=args.status, limit=args.limit)
        print(orders.format_order_list(items))
        print(f"\n📊 Showing {len(items)} orders")
        
    elif args.action == 'get':
        order = orders.get_order(args.order_id)
        if order:
            print(f"\n📋 Order: {order.get('name')}")
            print(f"   Date: {order.get('created_at')}")
            print(f"   Customer: {order.get('customer', {}).get('email', 'Guest')}")
            print(f"   Total: {order.get('total_price')} {order.get('currency')}")
            print(f"   Payment: {order.get('financial_status')}")
            print(f"   Fulfillment: {order.get('fulfillment_status') or 'unfulfilled'}")
            print(f"\n   Items:")
            for item in order.get('line_items', []):
                print(f"   - {item.get('quantity')}x {item.get('title')} - ${item.get('price')}")
        else:
            print(f"❌ Order not found: {args.order_id}")
            
    elif args.action == 'fulfill':
        result = orders.fulfill_order(
            args.order_id, 
            tracking_number=args.tracking,
            tracking_company=args.carrier,
            force=args.force
        )
        if result.get('cancelled'):
            print("❌ Operation cancelled")
        elif result.get('error'):
            print(f"❌ {result['error']}")
        elif result.get('dry_run'):
            print("\n✋ Dry run complete. Add --execute to apply.")
        else:
            print(f"✅ Order fulfilled: {result.get('name')}")
            if result.get('tracking_number'):
                print(f"   Tracking: {result.get('tracking_number')}")


def cmd_content(args):
    """Handle content commands."""
    print_header("Content Management")
    
    config = Config(args.config)
    client = ShopifyClient(config)
    safety = SafetyManager(config)
    audit = AuditLogger(config)
    
    if args.execute:
        safety.set_dry_run(False)
    
    content = ContentOperations(client, safety, audit)
    
    if args.action == 'pages':
        if args.subaction == 'list':
            pages = content.list_pages(limit=args.limit)
            print(content.format_page_list(pages))
            print(f"\n📊 Showing {len(pages)} pages")
        else:
            print("Page operations: list")
            
    elif args.action == 'products':
        if args.subaction == 'update':
            result = content.update_product_description(
                args.identifier,
                description=args.description,
                generate=args.generate,
                force=args.force
            )
            if result.get('dry_run'):
                print("\n✋ Dry run complete. Add --execute to apply.")
            else:
                print(f"✅ Product description updated")


def cmd_themes(args):
    """Handle theme commands with safe preview workflow."""
    print_header("Theme Management")
    
    config = Config(args.config)
    client = ShopifyClient(config)
    safety = SafetyManager(config)
    audit = AuditLogger(config)
    
    if args.execute:
        safety.set_dry_run(False)
    
    themes = ThemeOperations(client, safety, audit)
    
    if args.action == 'list':
        items = themes.get_themes()
        print(themes.format_theme_list(items))
        print(f"\n📊 {len(items)} themes")
        
        live = themes.get_live_theme()
        if live:
            print(f"\n🌐 Live theme: {live.get('name')} (ID: {live.get('id')})")
        
    elif args.action == 'copy':
        print("📋 Creating working copy of live theme...")
        working = themes.create_working_copy(name=args.name)
        print(f"\n✅ Working copy ready!")
        print(f"   Theme ID: {working.get('id')}")
        print(f"   Preview URL: {working.get('preview_url')}")
        print(f"\n👁️  Review your changes at the preview URL")
        print(f"   When satisfied, run: /shopify themes publish {working.get('id')} --execute")
        
    elif args.action == 'assets':
        if args.subaction == 'list':
            theme_id = args.theme_id or themes.get_live_theme().get('id')
            assets = themes.get_theme_assets(theme_id)
            print(f"\n📁 Theme Assets (ID: {theme_id}):")
            print(f"{'Key':<50} {'Size':<10} {'Type':<15}")
            print("-" * 75)
            for asset in assets[:args.limit]:
                key = asset.get('key', 'N/A')[:48]
                size = str(asset.get('size', 'N/A'))
                content_type = asset.get('content_type', 'unknown')[:13]
                print(f"{key:<50} {size:<10} {content_type:<15}")
            print(f"\n📊 Showing {min(len(assets), args.limit)} of {len(assets)} assets")
            
    elif args.action == 'edit':
        theme_id = args.theme_id
        asset_key = args.asset_key
        
        if not theme_id or not asset_key:
            print("❌ Usage: /shopify themes edit <theme_id> --asset <asset_key>")
            return
        
        # Get current content
        current = themes.get_asset(theme_id, asset_key)
        current_content = current.get('value', '') if current else ''
        
        if args.generate:
            new_content = themes.generate_asset_content(asset_key, args.generate, current_content)
        elif args.file:
            with open(args.file, 'r') as f:
                new_content = f.read()
        elif args.content:
            new_content = args.content
        else:
            print("❌ Provide content via --generate, --file, or --content")
            return
        
        result = themes.update_asset(theme_id, asset_key, new_content, force=args.force)
        
        if result.get('cancelled'):
            print("❌ Operation cancelled")
        elif result.get('dry_run'):
            print("\n✋ Dry run complete. Add --execute to apply.")
            preview_url = themes.get_preview_url(theme_id)
            if preview_url:
                print(f"👁️  Preview: {preview_url}")
        else:
            print(f"✅ Asset updated: {asset_key}")
            preview_url = themes.get_preview_url(theme_id)
            if preview_url:
                print(f"👁️  Preview: {preview_url}")
    
    elif args.action == 'publish':
        if not args.theme_id:
            print("❌ Usage: /shopify themes publish <theme_id> --execute")
            return
        
        result = themes.publish_theme(args.theme_id, force=args.force)
        
        if result.get('cancelled'):
            print("❌ Publication cancelled")
        else:
            print(f"✅ Theme published and now live!")
            print(f"   Theme ID: {args.theme_id}")
    
    elif args.action == 'delete':
        if not args.theme_id:
            print("❌ Usage: /shopify themes delete <theme_id>")
            return
        
        result = themes.delete_theme(args.theme_id, force=args.force)
        
        if result.get('cancelled'):
            print("❌ Deletion cancelled")
        else:
            print(f"✅ Theme deleted")


def cmd_themesettings(args):
    """Handle theme settings commands."""
    print_header("Theme Settings")
    
    config = Config(args.config)
    client = ShopifyClient(config)
    safety = SafetyManager(config)
    audit = AuditLogger(config)
    
    if args.execute:
        safety.set_dry_run(False)
    
    settings = ThemeSettingsOperations(client, safety, audit)
    
    if args.action == 'colors':
        result = settings.update_color_scheme(
            args.theme_id,
            primary=args.primary,
            secondary=args.secondary,
            background=args.background,
            text=args.text,
            accent=args.accent,
            force=args.force
        )
        if result.get('dry_run'):
            print("\n✋ Dry run complete. Add --execute to apply.")
        else:
            print(f"✅ Color scheme updated")
    
    elif args.action == 'fonts':
        result = settings.update_typography(
            args.theme_id,
            heading_font=args.heading,
            body_font=args.body,
            base_size=args.base_size,
            force=args.force
        )
        if result.get('dry_run'):
            print("\n✋ Dry run complete. Add --execute to apply.")
        else:
            print(f"✅ Typography updated")
    
    elif args.action == 'header':
        result = settings.update_header_settings(
            args.theme_id,
            logo_width=args.logo_width,
            sticky_header=args.sticky,
            announcement_bar=args.announcement,
            force=args.force
        )
        if result.get('dry_run'):
            print("\n✋ Dry run complete. Add --execute to apply.")
        else:
            print(f"✅ Header settings updated")


def cmd_sections(args):
    """Handle theme sections commands."""
    print_header("Theme Sections")
    
    config = Config(args.config)
    client = ShopifyClient(config)
    safety = SafetyManager(config)
    audit = AuditLogger(config)
    
    if args.execute:
        safety.set_dry_run(False)
    
    sections = ThemeSettingsOperations(client, safety, audit)
    
    if args.action == 'list':
        items = sections.get_page_sections(args.theme_id, args.page or 'index')
        print(sections.format_sections_list(items))
        print(f"\n📊 {len(items)} sections on {args.page or 'index'}")
    
    elif args.action == 'available':
        items = sections.list_available_sections()
        print(f"\n📦 Available Section Types:")
        print(f"{'Type':<30} {'Name':<25} {'Description'}")
        print("-" * 90)
        for s in items:
            print(f"{s['type']:<30} {s['name']:<25} {s['description'][:40]}...")
    
    elif args.action == 'add':
        result = sections.add_section(
            args.theme_id,
            args.page or 'index',
            args.type,
            position=args.position,
            force=args.force
        )
        if result.get('cancelled'):
            print("❌ Operation cancelled")
        elif result.get('dry_run'):
            print("\n✋ Dry run complete. Add --execute to apply.")
        else:
            print(f"✅ Section added: {result.get('section_id')}")
    
    elif args.action == 'remove':
        result = sections.remove_section(
            args.theme_id,
            args.page or 'index',
            args.section_id,
            force=args.force
        )
        if result.get('cancelled'):
            print("❌ Operation cancelled")
        elif result.get('dry_run'):
            print("\n✋ Dry run complete. Add --execute --force to apply.")
        else:
            print(f"✅ Section removed")


def cmd_metafields(args):
    """Handle metafield commands."""
    print_header("Metafields")
    
    config = Config(args.config)
    client = ShopifyClient(config)
    safety = SafetyManager(config)
    audit = AuditLogger(config)
    
    if args.execute:
        safety.set_dry_run(False)
    
    metafields = MetafieldOperations(client, safety, audit)
    
    if args.action == 'list':
        if args.resource_type == 'product':
            items = metafields.get_product_metafields(args.resource_id)
        elif args.resource_type == 'collection':
            items = metafields.get_collection_metafields(args.resource_id)
        elif args.resource_type == 'customer':
            items = metafields.get_customer_metafields(args.resource_id)
        elif args.resource_type == 'shop':
            items = metafields.get_shop_metafields()
        else:
            print(f"❌ Unknown resource type: {args.resource_type}")
            return
        
        print(metafields.format_metafields_list(items))
        print(f"\n📊 {len(items)} metafields")
    
    elif args.action == 'set':
        if args.resource_type == 'product':
            result = metafields.set_product_metafield(
                args.resource_id, args.namespace, args.key,
                args.value, args.type or 'single_line_text_field',
                force=args.force
            )
        elif args.resource_type == 'collection':
            result = metafields.set_collection_metafield(
                args.resource_id, args.namespace, args.key,
                args.value, args.type or 'single_line_text_field',
                force=args.force
            )
        elif args.resource_type == 'shop':
            result = metafields.set_shop_metafield(
                args.namespace, args.key,
                args.value, args.type or 'single_line_text_field',
                force=args.force
            )
        else:
            print(f"❌ Unknown resource type: {args.resource_type}")
            return
        
        if result.get('dry_run'):
            print("\n✋ Dry run complete. Add --execute to apply.")
        else:
            print(f"✅ Metafield set")


def cmd_media(args):
    """Handle media commands."""
    print_header("Media Management")
    
    config = Config(args.config)
    client = ShopifyClient(config)
    safety = SafetyManager(config)
    audit = AuditLogger(config)
    
    if args.execute:
        safety.set_dry_run(False)
    
    media = MediaOperations(client, safety, audit)
    
    if args.action == 'images':
        if args.subaction == 'list':
            items = media.list_product_images(args.product_id)
            print(media.format_images_list(items))
            print(f"\n📊 {len(items)} images")
        
        elif args.subaction == 'add':
            result = media.add_product_image(
                args.product_id, args.file,
                alt_text=args.alt,
                position=args.position,
                force=args.force
            )
            if result.get('dry_run'):
                print("\n✋ Dry run complete. Add --execute to apply.")
            else:
                print(f"✅ Image added: {result.get('id')}")
        
        elif args.subaction == 'delete':
            result = media.delete_product_image(
                args.product_id, args.image_id,
                force=args.force
            )
            if result.get('cancelled'):
                print("❌ Operation cancelled")
            elif result.get('dry_run'):
                print("\n✋ Dry run complete. Add --execute --force to apply.")
            else:
                print(f"✅ Image deleted")
    
    elif args.action == 'files':
        if args.subaction == 'list':
            items = media.list_files(args.limit)
            print(media.format_files_list(items))
            print(f"\n📊 {len(items)} files")
        
        elif args.subaction == 'upload':
            result = media.upload_file(args.file, name=args.name, force=args.force)
            if result.get('dry_run'):
                print("\n✋ Dry run complete. Add --execute to apply.")
            else:
                print(f"✅ File uploaded: {result.get('url', 'N/A')}")
    
    elif args.action == 'favicon':
        result = media.update_favicon(args.file, force=args.force)
        if result.get('dry_run'):
            print("\n✋ Dry run complete. Add --execute to apply.")
        else:
            print(f"✅ Favicon updated")
    
    elif args.action == 'social':
        result = media.update_social_image(args.file, force=args.force)
        if result.get('dry_run'):
            print("\n✋ Dry run complete. Add --execute to apply.")
        else:
            print(f"✅ Social sharing image updated")


def cmd_config(args):
    """Show configuration."""
    print_header("Configuration")
    
    try:
        config = Config(args.config)
        print(f"Store Domain: {config.store_domain}")
        print(f"API Version: {config.api_version}")
        print(f"Dry Run Default: {config.dry_run_by_default}")
        print(f"Audit Log: {config.audit_log_path}")
        
        # Test connection
        client = ShopifyClient(config)
        shop = client.get_shop()
        print(f"\n✅ Connected to: {shop.get('name', 'Unknown')}")
        print(f"   Plan: {shop.get('plan_name', 'Unknown')}")
        print(f"   Currency: {shop.get('currency', 'Unknown')}")
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Shopify Store Manager - AI-powered store management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Products & Orders
  /shopify ask "Show me recent orders"
  /shopify products list --limit 10
  /shopify orders fulfill 1234 --tracking 1Z999AA10123456784 --execute
  
  # Theme editing (SAFE workflow)
  /shopify themes list
  /shopify themes copy
  /shopify themes edit 12345 --asset templates/index.liquid --generate "add banner" --execute
  /shopify themes publish 12345 --execute
  
  # Theme Settings (colors, fonts, header)
  /shopify theme-settings colors --theme-id 12345 --primary "#FF5733" --execute
  /shopify theme-settings fonts --theme-id 12345 --heading "Inter" --body "Inter" --execute
  
  # Sections (drag-and-drop content)
  /shopify sections list --theme-id 12345
  /shopify sections available
  /shopify sections add --theme-id 12345 --type image-banner --position 1 --execute
  
  # Metafields (custom data)
  /shopify metafields list product --resource-id 12345
  /shopify metafields set product --resource-id 12345 --namespace custom --key size_guide --value "Size Chart" --execute
  
  # Media
  /shopify media images list --product-id 12345
  /shopify media images add --product-id 12345 --file ./photo.jpg --alt "Product photo" --execute
  /shopify media favicon --file ./favicon.ico --execute
  /shopify media social --file ./og-image.jpg --execute
        """
    )
    
    parser.add_argument('--config', '-c', help='Path to config file')
    parser.add_argument('--execute', '-x', action='store_true', 
                       help='Execute changes (default is dry-run)')
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # Ask command
    ask_parser = subparsers.add_parser('ask', help='Natural language request')
    ask_parser.add_argument('prompt', nargs='+', help='Your request')
    
    # Products command
    prod_parser = subparsers.add_parser('products', help='Product management')
    prod_parser.add_argument('action', choices=['list', 'get', 'create', 'update', 'delete'])
    prod_parser.add_argument('identifier', nargs='?', help='Product ID or handle')
    prod_parser.add_argument('--price', type=float, help='New price')
    prod_parser.add_argument('--limit', type=int, default=20)
    prod_parser.add_argument('--collection')
    prod_parser.add_argument('--tag')
    prod_parser.add_argument('--force', action='store_true')
    
    # Orders command
    order_parser = subparsers.add_parser('orders', help='Order management')
    order_parser.add_argument('action', choices=['list', 'get', 'fulfill', 'refund'])
    order_parser.add_argument('order_id', nargs='?')
    order_parser.add_argument('--status', default='any')
    order_parser.add_argument('--limit', type=int, default=20)
    order_parser.add_argument('--tracking')
    order_parser.add_argument('--carrier')
    order_parser.add_argument('--force', action='store_true')
    
    # Content command
    content_parser = subparsers.add_parser('content', help='Content management')
    content_parser.add_argument('action', choices=['pages', 'products'])
    content_parser.add_argument('subaction', nargs='?', choices=['list', 'update'])
    content_parser.add_argument('--limit', type=int, default=50)
    content_parser.add_argument('--identifier')
    content_parser.add_argument('--description')
    content_parser.add_argument('--generate', action='store_true')
    content_parser.add_argument('--force', action='store_true')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Show configuration')

    # Themes command
    theme_parser = subparsers.add_parser('themes', help='Theme management (with preview workflow)')
    theme_parser.add_argument('action', choices=['list', 'copy', 'assets', 'edit', 'publish', 'delete'])
    theme_parser.add_argument('theme_id', nargs='?', help='Theme ID')
    theme_parser.add_argument('--name', help='Name for new theme copy')
    theme_parser.add_argument('--subaction', choices=['list'], help='Asset subaction')
    theme_parser.add_argument('--asset', '--asset-key', dest='asset_key', help='Asset key to edit')
    theme_parser.add_argument('--generate', help='Generate content with AI prompt')
    theme_parser.add_argument('--file', help='Read content from file')
    theme_parser.add_argument('--content', help='Content string')
    theme_parser.add_argument('--limit', type=int, default=50)
    theme_parser.add_argument('--force', action='store_true')

    # Theme Settings command
    settings_parser = subparsers.add_parser('theme-settings', help='Update theme appearance settings')
    settings_parser.add_argument('action', choices=['colors', 'fonts', 'header'])
    settings_parser.add_argument('--theme-id', required=True, type=int, help='Theme ID')
    settings_parser.add_argument('--primary', help='Primary color (hex)')
    settings_parser.add_argument('--secondary', help='Secondary color (hex)')
    settings_parser.add_argument('--background', help='Background color (hex)')
    settings_parser.add_argument('--text', help='Text color (hex)')
    settings_parser.add_argument('--accent', help='Accent color (hex)')
    settings_parser.add_argument('--heading', help='Heading font family')
    settings_parser.add_argument('--body', help='Body font family')
    settings_parser.add_argument('--base-size', type=int, help='Base font size (px)')
    settings_parser.add_argument('--logo-width', type=int, help='Logo width (px)')
    settings_parser.add_argument('--sticky', action='store_true', help='Enable sticky header')
    settings_parser.add_argument('--announcement', help='Announcement bar text')
    settings_parser.add_argument('--force', action='store_true')

    # Sections command
    sections_parser = subparsers.add_parser('sections', help='Manage theme sections (drag-and-drop content)')
    sections_parser.add_argument('action', choices=['list', 'available', 'add', 'remove'])
    sections_parser.add_argument('--theme-id', required=True, type=int)
    sections_parser.add_argument('--page', default='index', help='Page template (default: index)')
    sections_parser.add_argument('--type', help='Section type to add')
    sections_parser.add_argument('--position', type=int, help='Position to insert')
    sections_parser.add_argument('--section-id', help='Section ID to remove')
    sections_parser.add_argument('--force', action='store_true')

    # Metafields command
    meta_parser = subparsers.add_parser('metafields', help='Manage metafields (custom data)')
    meta_parser.add_argument('action', choices=['list', 'set'])
    meta_parser.add_argument('resource_type', choices=['product', 'collection', 'customer', 'shop'])
    meta_parser.add_argument('--resource-id', type=int, help='Resource ID (not needed for shop)')
    meta_parser.add_argument('--namespace', help='Metafield namespace')
    meta_parser.add_argument('--key', help='Metafield key')
    meta_parser.add_argument('--value', help='Metafield value')
    meta_parser.add_argument('--type', default='single_line_text_field', help='Metafield type')
    meta_parser.add_argument('--force', action='store_true')

    # Media command
    media_parser = subparsers.add_parser('media', help='Manage images and files')
    media_parser.add_argument('action', choices=['images', 'files', 'favicon', 'social'])
    media_parser.add_argument('subaction', nargs='?', choices=['list', 'add', 'delete', 'upload'])
    media_parser.add_argument('--product-id', type=int, help='Product ID')
    media_parser.add_argument('--image-id', type=int, help='Image ID')
    media_parser.add_argument('--file', help='File path')
    media_parser.add_argument('--name', help='Custom filename')
    media_parser.add_argument('--alt', help='Alt text for images')
    media_parser.add_argument('--position', type=int, help='Image position')
    media_parser.add_argument('--limit', type=int, default=50)
    media_parser.add_argument('--force', action='store_true')
    
    args = parser.parse_args()
    
    if args.command == 'ask':
        args.prompt = ' '.join(args.prompt)
        cmd_ask(args)
    elif args.command == 'products':
        cmd_products(args)
    elif args.command == 'orders':
        cmd_orders(args)
    elif args.command == 'content':
        cmd_content(args)
    elif args.command == 'themes':
        cmd_themes(args)
    elif args.command == 'theme-settings':
        cmd_themesettings(args)
    elif args.command == 'sections':
        cmd_sections(args)
    elif args.command == 'metafields':
        cmd_metafields(args)
    elif args.command == 'media':
        cmd_media(args)
    elif args.command == 'config':
        cmd_config(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
