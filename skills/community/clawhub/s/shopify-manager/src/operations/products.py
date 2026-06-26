"""Product operations."""

from typing import Dict, List, Optional, Any
from .client import ShopifyClient
from .safety import SafetyManager, AuditLogger


class ProductOperations:
    """Product CRUD operations."""
    
    def __init__(self, client: ShopifyClient, safety: SafetyManager, audit: AuditLogger):
        self.client = client
        self.safety = safety
        self.audit = audit
    
    def list_products(self, limit: int = 20, **filters) -> List[Dict]:
        """List products with optional filters."""
        products = self.client.get_products(limit=limit, **filters)
        return products
    
    def get_product(self, identifier: str) -> Optional[Dict]:
        """Get product by ID or handle."""
        # Try as ID first
        try:
            product_id = int(identifier)
            return self.client.get_product(product_id=product_id)
        except ValueError:
            pass
        
        # Try as handle
        return self.client.get_product(handle=identifier)
    
    def create_product(self, title: str, **kwargs) -> Dict:
        """Create a new product."""
        # Build product data
        product_data = {
            'title': title,
            'body_html': kwargs.get('description', ''),
            'vendor': kwargs.get('vendor', ''),
            'product_type': kwargs.get('product_type', ''),
            'tags': kwargs.get('tags', []),
        }
        
        # Add variants if provided
        variants = kwargs.get('variants', [])
        if variants:
            product_data['variants'] = variants
        else:
            # Default variant
            product_data['variants'] = [{
                'price': str(kwargs.get('price', '0.00')),
                'sku': kwargs.get('sku', ''),
                'inventory_quantity': kwargs.get('inventory', 0),
            }]
        
        # Add images if provided
        if 'images' in kwargs:
            product_data['images'] = kwargs['images']
        
        # Validate
        is_valid, error = self.safety.validate_operation('product_create', product_data)
        if not is_valid:
            raise ValueError(error)
        
        # Preview changes
        changes = [{
            'action': f"Create product: {title}",
            'details': product_data,
        }]
        self.safety.preview_changes("Product Creation", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'data': product_data}
        
        # Create product
        product = self.client.create_product(product_data)
        
        # Audit log
        self.audit.log_change('product', product.get('id'), 'create', None, product)
        
        return product
    
    def update_product(self, identifier: str, **updates) -> Dict:
        """Update existing product."""
        # Get current product
        product = self.get_product(identifier)
        if not product:
            raise ValueError(f"Product not found: {identifier}")
        
        product_id = product['id']
        
        # Build update data
        update_data = {}
        
        if 'title' in updates:
            update_data['title'] = updates['title']
        if 'description' in updates:
            update_data['body_html'] = updates['description']
        if 'price' in updates:
            # Update first variant price
            if product.get('variants'):
                update_data['variants'] = [{'id': product['variants'][0]['id'], 'price': str(updates['price'])}]
        if 'tags' in updates:
            update_data['tags'] = updates['tags']
        if 'vendor' in updates:
            update_data['vendor'] = updates['vendor']
        if 'product_type' in updates:
            update_data['product_type'] = updates['product_type']
        
        # Validate
        is_valid, error = self.safety.validate_operation('product_update', {'id': product_id, **update_data})
        if not is_valid:
            raise ValueError(error)
        
        # Backup before change
        self.safety.backup_state('product', product_id, product)
        
        # Preview changes
        changes = [{
            'action': f"Update product: {product.get('title', identifier)}",
            'before': {k: product.get(k) for k in update_data.keys()},
            'after': update_data,
        }]
        self.safety.preview_changes("Product Update", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'product_id': product_id, 'changes': update_data}
        
        # Update product
        updated = self.client.update_product(product_id, update_data)
        
        # Audit log
        self.audit.log_change('product', product_id, 'update', product, updated)
        
        return updated
    
    def delete_product(self, identifier: str, force: bool = False) -> Dict:
        """Delete a product."""
        # Get product
        product = self.get_product(identifier)
        if not product:
            raise ValueError(f"Product not found: {identifier}")
        
        product_id = product['id']
        
        # Check permissions
        is_valid, error = self.safety.validate_operation('product_delete', {'id': product_id})
        if not is_valid:
            raise ValueError(error)
        
        # Require confirmation
        if self.safety.requires_confirmation('product_deletions'):
            if not self.safety.request_confirmation(
                'Delete Product',
                f"Delete '{product.get('title')}' (ID: {product_id})? This cannot be undone.",
                force=force
            ):
                return {'cancelled': True}
        
        # Preview
        changes = [{
            'action': f"Delete product: {product.get('title')}",
            'warning': 'This will permanently delete the product and cannot be undone.',
        }]
        self.safety.preview_changes("Product Deletion", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'product_id': product_id, 'product': product}
        
        # Backup before deletion
        self.safety.backup_state('product', product_id, product)
        
        # Delete
        self.client.delete_product(product_id)
        
        # Audit log
        self.audit.log_change('product', product_id, 'delete', product, None)
        
        return {'deleted': True, 'product_id': product_id, 'title': product.get('title')}
    
    def adjust_inventory(self, identifier: str, adjustment: int, 
                        location_id: Optional[int] = None, force: bool = False) -> Dict:
        """Adjust product inventory."""
        product = self.get_product(identifier)
        if not product:
            raise ValueError(f"Product not found: {identifier}")
        
        # Get first variant's inventory item
        variants = product.get('variants', [])
        if not variants:
            raise ValueError(f"Product has no variants: {identifier}")
        
        variant = variants[0]
        inventory_item_id = variant.get('inventory_item_id')
        
        if not inventory_item_id:
            raise ValueError(f"Cannot manage inventory for this product variant")
        
        # Get location
        if not location_id:
            locations = self.client.get_locations()
            if locations:
                location_id = locations[0]['id']
        
        if not location_id:
            raise ValueError("No location specified and could not determine default location")
        
        # Check for confirmation on inventory reduction
        if adjustment < 0 and self.safety.requires_confirmation('inventory_reductions'):
            if not self.safety.request_confirmation(
                'Reduce Inventory',
                f"Reduce inventory by {abs(adjustment)} units for '{product.get('title')}'?",
                force=force
            ):
                return {'cancelled': True}
        
        # Preview
        current_level = variant.get('inventory_quantity', 0)
        changes = [{
            'action': f"Adjust inventory for: {product.get('title')}",
            'before': f"{current_level} units",
            'after': f"{current_level + adjustment} units",
        }]
        self.safety.preview_changes("Inventory Adjustment", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'adjustment': adjustment, 'new_level': current_level + adjustment}
        
        # Adjust inventory
        result = self.client.adjust_inventory(inventory_item_id, location_id, adjustment)
        
        # Audit log
        self.audit.log_change(
            'inventory', 
            inventory_item_id, 
            'adjust', 
            {'quantity': current_level}, 
            {'quantity': current_level + adjustment}
        )
        
        return result
    
    def format_product_list(self, products: List[Dict]) -> str:
        """Format product list for display."""
        if not products:
            return "No products found."
        
        lines = [f"{'ID':<12} {'Handle':<30} {'Title':<40} {'Price':<10} {'Inventory':<10}"]
        lines.append("-" * 102)
        
        for p in products:
            variant = p.get('variants', [{}])[0]
            price = variant.get('price', 'N/A')
            inventory = variant.get('inventory_quantity', 'N/A')
            
            title = p.get('title', '')[:38]
            handle = p.get('handle', '')[:28]
            
            lines.append(f"{p.get('id', 'N/A'):<12} {handle:<30} {title:<40} {price:<10} {inventory:<10}")
        
        return "\n".join(lines)
