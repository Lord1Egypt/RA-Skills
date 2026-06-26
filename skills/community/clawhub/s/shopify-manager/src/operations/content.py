"""Content operations (pages, blogs, product descriptions)."""

from typing import Dict, List, Optional
from .client import ShopifyClient
from .safety import SafetyManager, AuditLogger


class ContentOperations:
    """Content management operations."""
    
    def __init__(self, client: ShopifyClient, safety: SafetyManager, audit: AuditLogger):
        self.client = client
        self.safety = safety
        self.audit = audit
    
    # === Pages ===
    
    def list_pages(self, limit: int = 50) -> List[Dict]:
        """List store pages."""
        return self.client.get_pages(limit=limit)
    
    def get_page(self, identifier: str) -> Optional[Dict]:
        """Get page by ID or handle."""
        try:
            page_id = int(identifier)
            return self.client.get_page(page_id=page_id)
        except ValueError:
            return self.client.get_page(handle=identifier)
    
    def update_page(self, identifier: str, title: Optional[str] = None,
                   body_html: Optional[str] = None, generate_content: Optional[str] = None,
                   force: bool = False) -> Dict:
        """Update a page."""
        page = self.get_page(identifier)
        if not page:
            raise ValueError(f"Page not found: {identifier}")
        
        page_id = page['id']
        
        # Build update data
        update_data = {}
        if title:
            update_data['title'] = title
        if body_html:
            update_data['body_html'] = body_html
        
        # If generate_content specified, that would trigger AI generation
        # For now, we just store the prompt for external processing
        if generate_content:
            update_data['body_html'] = f"[AI GENERATED: {generate_content}]"
        
        if not update_data:
            return {'error': 'No updates specified'}
        
        # Validate
        is_valid, error = self.safety.validate_operation('content_update', {'id': page_id, **update_data})
        if not is_valid:
            raise ValueError(error)
        
        # Backup
        self.safety.backup_state('page', page_id, page)
        
        # Preview
        changes = [{
            'action': f"Update page: {page.get('title')}",
            'before': {k: page.get(k) for k in update_data.keys()},
            'after': update_data,
        }]
        self.safety.preview_changes("Page Update", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'page_id': page_id, 'changes': update_data}
        
        # Update
        updated = self.client.update_page(page_id, update_data)
        
        # Audit log
        self.audit.log_change('page', page_id, 'update', page, updated)
        
        return updated
    
    # === Product Descriptions ===
    
    def update_product_description(self, product_identifier: str, 
                                   description: Optional[str] = None,
                                   generate: bool = False,
                                   force: bool = False) -> Dict:
        """Update product description."""
        from .products import ProductOperations
        
        products = ProductOperations(self.client, self.safety, self.audit)
        product = products.get_product(product_identifier)
        
        if not product:
            raise ValueError(f"Product not found: {product_identifier}")
        
        product_id = product['id']
        
        if generate:
            # Placeholder for AI generation
            description = f"[AI GENERATED DESCRIPTION for {product.get('title')}]"
        
        if not description:
            return {'error': 'No description provided'}
        
        # Preview
        changes = [{
            'action': f"Update description for: {product.get('title')}",
            'before': product.get('body_html', '')[:100] + "..." if len(product.get('body_html', '')) > 100 else product.get('body_html', ''),
            'after': description[:100] + "..." if len(description) > 100 else description,
        }]
        self.safety.preview_changes("Product Description Update", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'product_id': product_id, 'new_description': description}
        
        # Update
        updated = self.client.update_product(product_id, {'body_html': description})
        
        # Audit log
        self.audit.log_change('product_description', product_id, 'update', 
                             {'body_html': product.get('body_html')}, 
                             {'body_html': description})
        
        return updated
    
    def format_page_list(self, pages: List[Dict]) -> str:
        """Format page list for display."""
        if not pages:
            return "No pages found."
        
        lines = [f"{'ID':<12} {'Handle':<25} {'Title':<40}"]
        lines.append("-" * 77)
        
        for p in pages:
            title = p.get('title', '')[:38]
            handle = p.get('handle', '')[:23]
            lines.append(f"{p.get('id', 'N/A'):<12} {handle:<25} {title:<40}")
        
        return "\n".join(lines)
