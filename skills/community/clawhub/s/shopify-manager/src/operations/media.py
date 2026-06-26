"""Media and assets operations."""

import base64
import mimetypes
from pathlib import Path
from typing import Dict, List, Optional, BinaryIO
from .client import ShopifyClient
from .safety import SafetyManager, AuditLogger


class MediaOperations:
    """Manage store media: product images, files, etc."""
    
    def __init__(self, client: ShopifyClient, safety: SafetyManager, audit: AuditLogger):
        self.client = client
        self.safety = safety
        self.audit = audit
    
    # === Product Images ===
    
    def list_product_images(self, product_id: int) -> List[Dict]:
        """List all images for a product."""
        return self.client.get_product_images(product_id)
    
    def add_product_image(self, product_id: int, image_path: str,
                          alt_text: Optional[str] = None,
                          position: Optional[int] = None,
                          variant_ids: Optional[List[int]] = None,
                          force: bool = False) -> Dict:
        """Add an image to a product."""
        # Read and encode image
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        with open(path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type:
            mime_type = 'image/jpeg'
        
        image_payload = {
            'attachment': image_data,
            'filename': path.name,
            'mime_type': mime_type,
        }
        
        if alt_text:
            image_payload['alt'] = alt_text
        if position:
            image_payload['position'] = position
        if variant_ids:
            image_payload['variant_ids'] = variant_ids
        
        # Preview
        changes = [{
            'action': f"Add image to product {product_id}",
            'details': f"File: {path.name}, Size: {path.stat().st_size} bytes",
        }]
        self.safety.preview_changes("Add Product Image", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'filename': path.name}
        
        result = self.client.create_product_image(product_id, image_payload)
        
        self.audit.log_change('product_image', str(product_id), 'create', {}, result)
        
        return result
    
    def update_image_alt(self, product_id: int, image_id: int,
                         alt_text: str, force: bool = False) -> Dict:
        """Update alt text for a product image."""
        changes = [{
            'action': f"Update image {image_id} alt text",
            'before': 'Previous alt text',
            'after': alt_text,
        }]
        self.safety.preview_changes("Update Image Alt Text", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'alt': alt_text}
        
        result = self.client.update_product_image(product_id, image_id, {'alt': alt_text})
        
        self.audit.log_change('product_image', f"{product_id}:{image_id}", 'update_alt', {}, result)
        
        return result
    
    def delete_product_image(self, product_id: int, image_id: int,
                             force: bool = False) -> Dict:
        """Delete a product image."""
        if self.safety.requires_confirmation('image_deletion'):
            if not self.safety.request_confirmation(
                'Delete Product Image',
                f"Delete image {image_id} from product {product_id}?",
                force=force
            ):
                return {'cancelled': True}
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'image_id': image_id}
        
        self.client.delete_product_image(product_id, image_id)
        
        self.audit.log_change('product_image', f"{product_id}:{image_id}", 'delete', {}, None)
        
        return {'deleted': True, 'image_id': image_id}
    
    def reorder_product_images(self, product_id: int, image_ids: List[int],
                               force: bool = False) -> Dict:
        """Reorder product images."""
        changes = [{
            'action': f"Reorder images for product {product_id}",
            'details': f"New order: {image_ids}",
        }]
        self.safety.preview_changes("Reorder Images", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'new_order': image_ids}
        
        # Update each image position
        for position, image_id in enumerate(image_ids, 1):
            self.client.update_product_image(product_id, image_id, {'position': position})
        
        self.audit.log_change('product_images', str(product_id), 'reorder', {}, {'order': image_ids})
        
        return {'reordered': True, 'new_order': image_ids}
    
    # === Theme Assets (Images, Fonts, etc.) ===
    
    def upload_theme_asset(self, theme_id: int, asset_key: str,
                           file_path: str, force: bool = False) -> Dict:
        """Upload a file as a theme asset."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Determine if binary or text
        mime_type, _ = mimetypes.guess_type(file_path)
        
        with open(path, 'rb') as f:
            content = f.read()
        
        if mime_type and mime_type.startswith('text/'):
            # Text asset
            value = content.decode('utf-8')
        else:
            # Binary asset (base64 encode)
            value = base64.b64encode(content).decode('utf-8')
        
        changes = [{
            'action': f"Upload theme asset: {asset_key}",
            'details': f"File: {path.name}, Type: {mime_type or 'unknown'}",
        }]
        self.safety.preview_changes("Upload Theme Asset", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'asset_key': asset_key}
        
        result = self.client.update_theme_asset(theme_id, asset_key, value)
        
        self.audit.log_change('theme_asset', f"{theme_id}:{asset_key}", 'upload', {}, result)
        
        return result
    
    # === Store Files (Files API) ===
    
    def list_files(self, limit: int = 50) -> List[Dict]:
        """List files in the store's Files section."""
        return self.client.get_files(limit=limit)
    
    def upload_file(self, file_path: str, name: Optional[str] = None,
                    force: bool = False) -> Dict:
        """Upload a file to the store's Files section."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        filename = name or path.name
        
        with open(path, 'rb') as f:
            content = f.read()
        
        mime_type, _ = mimetypes.guess_type(file_path)
        
        file_data = {
            'filename': filename,
            'content': base64.b64encode(content).decode('utf-8'),
            'mime_type': mime_type or 'application/octet-stream',
        }
        
        changes = [{
            'action': f"Upload file to store: {filename}",
            'details': f"Size: {len(content)} bytes, Type: {mime_type or 'unknown'}",
        }]
        self.safety.preview_changes("Upload Store File", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'filename': filename}
        
        result = self.client.create_file(file_data)
        
        self.audit.log_change('file', filename, 'upload', {}, result)
        
        return result
    
    def delete_file(self, file_id: int, force: bool = False) -> Dict:
        """Delete a file from the store."""
        if self.safety.requires_confirmation('file_deletion'):
            if not self.safety.request_confirmation(
                'Delete Store File',
                f"Delete file {file_id}?",
                force=force
            ):
                return {'cancelled': True}
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'file_id': file_id}
        
        self.client.delete_file(file_id)
        
        self.audit.log_change('file', str(file_id), 'delete', {}, None)
        
        return {'deleted': True, 'file_id': file_id}
    
    # === Favicon ===
    
    def update_favicon(self, image_path: str, force: bool = False) -> Dict:
        """Update store favicon."""
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Validate image type
        mime_type, _ = mimetypes.guess_type(image_path)
        if mime_type not in ['image/x-icon', 'image/vnd.microsoft.icon', 'image/png']:
            raise ValueError(f"Invalid favicon format. Use .ico or .png: {mime_type}")
        
        with open(path, 'rb') as f:
            content = f.read()
        
        changes = [{
            'action': "Update store favicon",
            'details': f"File: {path.name}",
        }]
        self.safety.preview_changes("Update Favicon", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'favicon': path.name}
        
        # Upload as settings asset
        result = self.client.update_shop_settings({
            'favicon': base64.b64encode(content).decode('utf-8')
        })
        
        self.audit.log_change('favicon', 'store', 'update', {}, {'filename': path.name})
        
        return result
    
    # === Social Sharing Image ===
    
    def update_social_image(self, image_path: str, force: bool = False) -> Dict:
        """Update the social sharing image (Open Graph)."""
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        changes = [{
            'action': "Update social sharing image",
            'details': f"File: {path.name}",
        }]
        self.safety.preview_changes("Update Social Image", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'social_image': path.name}
        
        with open(path, 'rb') as f:
            content = f.read()
        
        result = self.client.update_shop_settings({
            'social_image': base64.b64encode(content).decode('utf-8')
        })
        
        self.audit.log_change('social_image', 'store', 'update', {}, {'filename': path.name})
        
        return result
    
    def format_images_list(self, images: List[Dict]) -> str:
        """Format image list for display."""
        if not images:
            return "No images found."
        
        lines = [f"{'ID':<12} {'Position':<10} {'Alt Text':<40} {'Size':<15}"]
        lines.append("-" * 77)
        
        for img in images:
            img_id = str(img.get('id', 'N/A'))
            position = str(img.get('position', 'N/A'))
            alt = (img.get('alt') or 'None')[:38]
            size = f"{img.get('width', 0)}x{img.get('height', 0)}"
            lines.append(f"{img_id:<12} {position:<10} {alt:<40} {size:<15}")
        
        return "\n".join(lines)
    
    def format_files_list(self, files: List[Dict]) -> str:
        """Format files list for display."""
        if not files:
            return "No files found."
        
        lines = [f"{'ID':<12} {'Filename':<40} {'Type':<25} {'Size':<15}"]
        lines.append("-" * 92)
        
        for f in files:
            file_id = str(f.get('id', 'N/A'))
            filename = f.get('filename', 'N/A')[:38]
            mime_type = f.get('mime_type', 'unknown')[:23]
            size = f"{f.get('size', 0) / 1024:.1f} KB"
            lines.append(f"{file_id:<12} {filename:<40} {mime_type:<25} {size:<15}")
        
        return "\n".join(files)
