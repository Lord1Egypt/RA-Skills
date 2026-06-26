"""Shopify API client."""

import json
import time
from typing import Dict, Any, List, Optional
import requests

from .config import Config


class ShopifyClient:
    """Client for Shopify Admin API."""
    
    def __init__(self, config: Config):
        self.config = config
        self.base_url = f"https://{config.store_domain}/admin/api/{config.api_version}"
        self.session = requests.Session()
        self.session.headers.update({
            'X-Shopify-Access-Token': config.access_token,
            'Content-Type': 'application/json',
        })
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Apply rate limiting between requests."""
        delay = self.config.get('safety.rate_limit_delay', 0.5)
        elapsed = time.time() - self.last_request_time
        if elapsed < delay:
            time.sleep(delay - elapsed)
        self.last_request_time = time.time()
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling."""
        self._rate_limit()
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            
            if response.status_code == 429:
                # Rate limited - wait and retry once
                retry_after = int(response.headers.get('Retry-After', 60))
                time.sleep(retry_after)
                response = self.session.request(method, url, **kwargs)
            
            response.raise_for_status()
            
            if response.content:
                return response.json()
            return {}
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"API Error: {e}"
            try:
                error_data = e.response.json()
                if 'errors' in error_data:
                    error_msg = f"API Error: {error_data['errors']}"
            except:
                pass
            raise ShopifyAPIError(error_msg, status_code=e.response.status_code)
        
        except requests.exceptions.RequestException as e:
            raise ShopifyAPIError(f"Network error: {e}")
    
    # === Products ===
    
    def get_products(self, limit: int = 50, **filters) -> List[Dict]:
        """Get list of products."""
        params = {'limit': min(limit, 250), **filters}
        response = self._request('GET', 'products.json', params=params)
        return response.get('products', [])
    
    def get_product(self, product_id: Optional[int] = None, handle: Optional[str] = None) -> Optional[Dict]:
        """Get single product by ID or handle."""
        if product_id:
            response = self._request('GET', f'products/{product_id}.json')
            return response.get('product')
        elif handle:
            products = self.get_products(handle=handle, limit=1)
            return products[0] if products else None
        return None
    
    def create_product(self, product_data: Dict) -> Dict:
        """Create a new product."""
        response = self._request('POST', 'products.json', json={'product': product_data})
        return response.get('product', {})
    
    def update_product(self, product_id: int, product_data: Dict) -> Dict:
        """Update existing product."""
        response = self._request('PUT', f'products/{product_id}.json', json={'product': product_data})
        return response.get('product', {})
    
    def delete_product(self, product_id: int):
        """Delete a product."""
        self._request('DELETE', f'products/{product_id}.json')
    
    # === Inventory ===
    
    def get_inventory_levels(self, inventory_item_ids: List[int]) -> List[Dict]:
        """Get inventory levels for items."""
        params = {'inventory_item_ids': ','.join(map(str, inventory_item_ids))}
        response = self._request('GET', 'inventory_levels.json', params=params)
        return response.get('inventory_levels', [])
    
    def adjust_inventory(self, inventory_item_id: int, location_id: int, adjustment: int) -> Dict:
        """Adjust inventory level."""
        data = {
            'location_id': location_id,
            'inventory_item_id': inventory_item_id,
            'available_adjustment': adjustment
        }
        response = self._request('POST', 'inventory_levels/adjust.json', json=data)
        return response.get('inventory_level', {})
    
    def set_inventory(self, inventory_item_id: int, location_id: int, available: int) -> Dict:
        """Set absolute inventory level."""
        data = {
            'location_id': location_id,
            'inventory_item_id': inventory_item_id,
            'available': available
        }
        response = self._request('POST', 'inventory_levels/set.json', json=data)
        return response.get('inventory_level', {})
    
    # === Orders ===
    
    def get_orders(self, status: str = 'any', limit: int = 50, **filters) -> List[Dict]:
        """Get list of orders."""
        params = {'status': status, 'limit': min(limit, 250), **filters}
        response = self._request('GET', 'orders.json', params=params)
        return response.get('orders', [])
    
    def get_order(self, order_id: int) -> Optional[Dict]:
        """Get single order."""
        response = self._request('GET', f'orders/{order_id}.json')
        return response.get('order')
    
    def fulfill_order(self, order_id: int, fulfillment_data: Dict) -> Dict:
        """Create fulfillment for order."""
        response = self._request(
            'POST',
            f'orders/{order_id}/fulfillments.json',
            json={'fulfillment': fulfillment_data}
        )
        return response.get('fulfillment', {})
    
    def calculate_refund(self, order_id: int, refund_line_items: List[Dict]) -> Dict:
        """Calculate refund amounts."""
        data = {'refund': {'refund_line_items': refund_line_items}}
        response = self._request(
            'POST',
            f'orders/{order_id}/refunds/calculate.json',
            json=data
        )
        return response.get('refund', {})
    
    def create_refund(self, order_id: int, refund_data: Dict) -> Dict:
        """Process refund."""
        response = self._request(
            'POST',
            f'orders/{order_id}/refunds.json',
            json={'refund': refund_data}
        )
        return response.get('refund', {})
    
    # === Pages ===
    
    def get_pages(self, limit: int = 50) -> List[Dict]:
        """Get store pages."""
        response = self._request('GET', 'pages.json', params={'limit': limit})
        return response.get('pages', [])
    
    def get_page(self, page_id: Optional[int] = None, handle: Optional[str] = None) -> Optional[Dict]:
        """Get single page."""
        if page_id:
            response = self._request('GET', f'pages/{page_id}.json')
            return response.get('page')
        elif handle:
            pages = self.get_pages()
            for page in pages:
                if page.get('handle') == handle:
                    return page
        return None
    
    def update_page(self, page_id: int, page_data: Dict) -> Dict:
        """Update page."""
        response = self._request('PUT', f'pages/{page_id}.json', json={'page': page_data})
        return response.get('page', {})
    
    # === Collections ===
    
    def get_custom_collections(self, limit: int = 50) -> List[Dict]:
        """Get custom collections."""
        response = self._request('GET', 'custom_collections.json', params={'limit': limit})
        return response.get('custom_collections', [])
    
    def get_smart_collections(self, limit: int = 50) -> List[Dict]:
        """Get smart collections."""
        response = self._request('GET', 'smart_collections.json', params={'limit': limit})
        return response.get('smart_collections', [])
    
    def get_collection_products(self, collection_id: int, limit: int = 50) -> List[Dict]:
        """Get products in a collection."""
        response = self._request(
            'GET',
            f'collections/{collection_id}/products.json',
            params={'limit': limit}
        )
        return response.get('products', [])
    
    # === Shop Info ===
    
    def get_shop(self) -> Dict:
        """Get shop information."""
        response = self._request('GET', 'shop.json')
        return response.get('shop', {})
    
    def get_locations(self) -> List[Dict]:
        """Get store locations."""
        response = self._request('GET', 'locations.json')
        return response.get('locations', [])
    
    # === Themes ===
    
    def get_themes(self) -> List[Dict]:
        """Get all themes."""
        response = self._request('GET', 'themes.json')
        return response.get('themes', [])
    
    def get_theme(self, theme_id: int) -> Optional[Dict]:
        """Get single theme."""
        response = self._request('GET', f'themes/{theme_id}.json')
        return response.get('theme')
    
    def duplicate_theme(self, theme_id: int, name: str) -> Dict:
        """Duplicate a theme."""
        data = {
            'theme': {
                'name': name,
                'src': f'https://{self.config.store_domain}/admin/themes/{theme_id}'
            }
        }
        response = self._request('POST', 'themes.json', json=data)
        return response.get('theme', {})
    
    def publish_theme(self, theme_id: int) -> Dict:
        """Publish a theme (make it live)."""
        data = {'theme': {'role': 'main'}}
        response = self._request('PUT', f'themes/{theme_id}.json', json=data)
        return response.get('theme', {})
    
    def delete_theme(self, theme_id: int):
        """Delete a theme."""
        self._request('DELETE', f'themes/{theme_id}.json')
    
    # === Theme Assets ===
    
    def get_theme_assets(self, theme_id: int) -> List[Dict]:
        """List theme assets."""
        response = self._request('GET', f'themes/{theme_id}/assets.json')
        return response.get('assets', [])
    
    def get_theme_asset(self, theme_id: int, asset_key: str) -> Optional[Dict]:
        """Get a specific theme asset."""
        params = {'asset[key]': asset_key}
        response = self._request('GET', f'themes/{theme_id}/assets.json', params=params)
        return response.get('asset')
    
    def update_theme_asset(self, theme_id: int, asset_key: str, content: str) -> Dict:
        """Update or create a theme asset."""
        data = {
            'asset': {
                'key': asset_key,
                'value': content
            }
        }
        response = self._request('PUT', f'themes/{theme_id}/assets.json', json=data)
        return response.get('asset', {})
    
    def delete_theme_asset(self, theme_id: int, asset_key: str):
        """Delete a theme asset."""
        params = {'asset[key]': asset_key}
        self._request('DELETE', f'themes/{theme_id}/assets.json', params=params)
    
    # === Product Images ===
    
    def get_product_images(self, product_id: int) -> List[Dict]:
        """Get product images."""
        response = self._request('GET', f'products/{product_id}/images.json')
        return response.get('images', [])
    
    def create_product_image(self, product_id: int, image_data: Dict) -> Dict:
        """Add image to product."""
        response = self._request('POST', f'products/{product_id}/images.json', json={'image': image_data})
        return response.get('image', {})
    
    def update_product_image(self, product_id: int, image_id: int, image_data: Dict) -> Dict:
        """Update product image."""
        response = self._request('PUT', f'products/{product_id}/images/{image_id}.json', json={'image': image_data})
        return response.get('image', {})
    
    def delete_product_image(self, product_id: int, image_id: int):
        """Delete product image."""
        self._request('DELETE', f'products/{product_id}/images/{image_id}.json')
    
    # === Metafields ===
    
    def get_metafields(self, resource_type: str, resource_id: Optional[int]) -> List[Dict]:
        """Get metafields for a resource."""
        if resource_id:
            endpoint = f'{resource_type}/{resource_id}/metafields.json'
        else:
            endpoint = f'{resource_type}/metafields.json'
        response = self._request('GET', endpoint)
        return response.get('metafields', [])
    
    def create_metafield(self, resource_type: str, resource_id: Optional[int], metafield_data: Dict) -> Dict:
        """Create a metafield."""
        if resource_id:
            endpoint = f'{resource_type}/{resource_id}/metafields.json'
        else:
            endpoint = f'{resource_type}/metafields.json'
        response = self._request('POST', endpoint, json={'metafield': metafield_data})
        return response.get('metafield', {})
    
    def delete_metafield(self, resource_type: str, resource_id: int, metafield_id: int):
        """Delete a metafield."""
        self._request('DELETE', f'{resource_type}/{resource_id}/metafields/{metafield_id}.json')
    
    # === Metaobjects (GraphQL required for full support, basic REST where available) ===
    
    def get_metaobject_definitions(self) -> List[Dict]:
        """Get metaobject definitions."""
        # Note: Full metaobject support requires GraphQL API
        # This is a placeholder for REST API endpoints
        return []
    
    def create_metaobject_definition(self, definition_data: Dict) -> Dict:
        """Create metaobject definition."""
        # Placeholder - requires GraphQL
        return {}
    
    def get_metaobjects(self, type: str, limit: int = 50) -> List[Dict]:
        """Get metaobject entries."""
        # Placeholder - requires GraphQL
        return []
    
    def get_metaobject(self, metaobject_id: int) -> Optional[Dict]:
        """Get single metaobject."""
        # Placeholder - requires GraphQL
        return None
    
    def create_metaobject(self, metaobject_data: Dict) -> Dict:
        """Create metaobject entry."""
        # Placeholder - requires GraphQL
        return {}
    
    def update_metaobject(self, metaobject_id: int, metaobject_data: Dict) -> Dict:
        """Update metaobject entry."""
        # Placeholder - requires GraphQL
        return {}
    
    def delete_metaobject(self, metaobject_id: int):
        """Delete metaobject entry."""
        # Placeholder - requires GraphQL
        pass
    
    # === Files ===
    
    def get_files(self, limit: int = 50) -> List[Dict]:
        """Get store files."""
        response = self._request('GET', 'files.json', params={'limit': limit})
        return response.get('files', [])
    
    def create_file(self, file_data: Dict) -> Dict:
        """Create a file."""
        response = self._request('POST', 'files.json', json={'file': file_data})
        return response.get('file', {})
    
    def delete_file(self, file_id: int):
        """Delete a file."""
        self._request('DELETE', f'files/{file_id}.json')
    
    # === Shop Settings ===
    
    def update_shop_settings(self, settings: Dict) -> Dict:
        """Update shop-level settings."""
        response = self._request('PUT', 'shop.json', json={'shop': settings})
        return response.get('shop', {})


class ShopifyAPIError(Exception):
    """Shopify API error."""
    
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code
