"""Theme sections and settings management."""

import json
from typing import Dict, List, Optional, Any
from .client import ShopifyClient
from .safety import SafetyManager, AuditLogger


class ThemeSettingsOperations:
    """Manage theme settings, sections, and visual appearance."""
    
    def __init__(self, client: ShopifyClient, safety: SafetyManager, audit: AuditLogger):
        self.client = client
        self.safety = safety
        self.audit = audit
    
    # === Theme Settings ===
    
    def get_theme_settings(self, theme_id: int) -> Dict:
        """Get theme settings_data.json."""
        asset = self.client.get_theme_asset(theme_id, 'config/settings_data.json')
        if asset and 'value' in asset:
            try:
                return json.loads(asset['value'])
            except json.JSONDecodeError:
                return {}
        return {}
    
    def update_theme_settings(self, theme_id: int, settings: Dict, force: bool = False) -> Dict:
        """Update theme settings."""
        # Check if this is the live theme
        themes = self.client.get_themes()
        is_live = any(t['id'] == theme_id and t.get('role') == 'main' for t in themes)
        
        if is_live:
            raise ValueError(
                "Cannot edit live theme settings directly! "
                "Use 'shopify themes copy' first, then edit the copy."
            )
        
        # Get current settings for backup
        current_settings = self.get_theme_settings(theme_id)
        self.safety.backup_state('theme_settings', theme_id, current_settings)
        
        # Merge new settings
        new_settings = self._deep_merge(current_settings, settings)
        
        # Preview changes
        changes = [{
            'action': f"Update theme settings for theme {theme_id}",
            'details': f"Updating {len(settings)} setting groups",
        }]
        self.safety.preview_changes("Theme Settings Update", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'theme_id': theme_id, 'settings': new_settings}
        
        # Save settings
        content = json.dumps(new_settings, indent=2)
        result = self.client.update_theme_asset(theme_id, 'config/settings_data.json', content)
        
        # Audit log
        self.audit.log_change('theme_settings', theme_id, 'update', current_settings, new_settings)
        
        return result
    
    def update_color_scheme(self, theme_id: int, 
                           primary: Optional[str] = None,
                           secondary: Optional[str] = None,
                           background: Optional[str] = None,
                           text: Optional[str] = None,
                           accent: Optional[str] = None,
                           force: bool = False) -> Dict:
        """Update theme color scheme."""
        color_settings = {}
        
        if primary:
            color_settings['colors'] = color_settings.get('colors', {})
            color_settings['colors']['primary'] = primary
        if secondary:
            color_settings['colors'] = color_settings.get('colors', {})
            color_settings['colors']['secondary'] = secondary
        if background:
            color_settings['colors'] = color_settings.get('colors', {})
            color_settings['colors']['background'] = background
        if text:
            color_settings['colors'] = color_settings.get('colors', {})
            color_settings['colors']['text'] = text
        if accent:
            color_settings['colors'] = color_settings.get('colors', {})
            color_settings['colors']['accent'] = accent
        
        return self.update_theme_settings(theme_id, color_settings, force=force)
    
    def update_typography(self, theme_id: int,
                         heading_font: Optional[str] = None,
                         body_font: Optional[str] = None,
                         base_size: Optional[int] = None,
                         force: bool = False) -> Dict:
        """Update theme typography."""
        font_settings = {}
        
        if heading_font:
            font_settings['typography'] = font_settings.get('typography', {})
            font_settings['typography']['heading_font'] = heading_font
        if body_font:
            font_settings['typography'] = font_settings.get('typography', {})
            font_settings['typography']['body_font'] = body_font
        if base_size:
            font_settings['typography'] = font_settings.get('typography', {})
            font_settings['typography']['base_size'] = base_size
        
        return self.update_theme_settings(theme_id, font_settings, force=force)
    
    def update_header_settings(self, theme_id: int,
                              logo_width: Optional[int] = None,
                              sticky_header: Optional[bool] = None,
                              announcement_bar: Optional[str] = None,
                              force: bool = False) -> Dict:
        """Update header appearance."""
        header_settings = {'header': {}}
        
        if logo_width is not None:
            header_settings['header']['logo_width'] = logo_width
        if sticky_header is not None:
            header_settings['header']['sticky'] = sticky_header
        if announcement_bar is not None:
            header_settings['header']['announcement_bar'] = announcement_bar
        
        return self.update_theme_settings(theme_id, header_settings, force=force)
    
    def update_product_card_settings(self, theme_id: int,
                                     image_ratio: Optional[str] = None,
                                     show_quick_add: Optional[bool] = None,
                                     show_vendor: Optional[bool] = None,
                                     force: bool = False) -> Dict:
        """Update product card display settings."""
        card_settings = {'product_card': {}}
        
        if image_ratio:
            card_settings['product_card']['image_ratio'] = image_ratio
        if show_quick_add is not None:
            card_settings['product_card']['show_quick_add'] = show_quick_add
        if show_vendor is not None:
            card_settings['product_card']['show_vendor'] = show_vendor
        
        return self.update_theme_settings(theme_id, card_settings, force=force)
    
    # === Theme Sections ===
    
    def get_page_sections(self, theme_id: int, page_type: str = 'index') -> List[Dict]:
        """Get sections for a page template."""
        template_file = f'templates/{page_type}.json'
        asset = self.client.get_theme_asset(theme_id, template_file)
        
        if asset and 'value' in asset:
            try:
                template_data = json.loads(asset['value'])
                sections = template_data.get('sections', {})
                order = template_data.get('order', [])
                
                # Return ordered list
                result = []
                for section_id in order:
                    if section_id in sections:
                        section = sections[section_id]
                        section['id'] = section_id
                        result.append(section)
                return result
            except json.JSONDecodeError:
                return []
        return []
    
    def add_section(self, theme_id: int, page_type: str, section_type: str,
                    position: Optional[int] = None, settings: Optional[Dict] = None,
                    force: bool = False) -> Dict:
        """Add a section to a page."""
        # Check if live theme
        themes = self.client.get_themes()
        is_live = any(t['id'] == theme_id and t.get('role') == 'main' for t in themes)
        
        if is_live:
            raise ValueError("Cannot edit live theme directly! Create a copy first.")
        
        template_file = f'templates/{page_type}.json'
        
        # Get current template
        asset = self.client.get_theme_asset(theme_id, template_file)
        if not asset or 'value' not in asset:
            # Create new template
            template_data = {'sections': {}, 'order': []}
        else:
            try:
                template_data = json.loads(asset['value'])
            except json.JSONDecodeError:
                template_data = {'sections': {}, 'order': []}
        
        # Backup
        self.safety.backup_state('template', f"{theme_id}:{template_file}", template_data)
        
        # Generate section ID
        import uuid
        section_id = str(uuid.uuid4())[:8]
        
        # Create section
        new_section = {
            'type': section_type,
            'settings': settings or {}
        }
        
        # Add to sections
        template_data.setdefault('sections', {})[section_id] = new_section
        
        # Add to order
        template_data.setdefault('order', [])
        if position is not None:
            template_data['order'].insert(position, section_id)
        else:
            template_data['order'].append(section_id)
        
        # Preview
        changes = [{
            'action': f"Add {section_type} section to {page_type}",
            'details': f"Section ID: {section_id}, Position: {position or 'end'}",
        }]
        self.safety.preview_changes("Add Section", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'section_id': section_id, 'template': template_data}
        
        # Save template
        content = json.dumps(template_data, indent=2)
        result = self.client.update_theme_asset(theme_id, template_file, content)
        
        # Audit
        self.audit.log_change('template', f"{theme_id}:{template_file}", 'add_section',
                             {'order': template_data['order'][:-1]}, template_data)
        
        return {'section_id': section_id, 'result': result}
    
    def remove_section(self, theme_id: int, page_type: str, section_id: str,
                       force: bool = False) -> Dict:
        """Remove a section from a page."""
        themes = self.client.get_themes()
        is_live = any(t['id'] == theme_id and t.get('role') == 'main' for t in themes)
        
        if is_live:
            raise ValueError("Cannot edit live theme directly!")
        
        template_file = f'templates/{page_type}.json'
        
        asset = self.client.get_theme_asset(theme_id, template_file)
        if not asset or 'value' not in asset:
            raise ValueError(f"Template not found: {template_file}")
        
        template_data = json.loads(asset['value'])
        
        # Backup
        self.safety.backup_state('template', f"{theme_id}:{template_file}", template_data)
        
        # Remove section
        if section_id in template_data.get('sections', {}):
            del template_data['sections'][section_id]
        if section_id in template_data.get('order', []):
            template_data['order'].remove(section_id)
        
        # Preview
        changes = [{
            'action': f"Remove section {section_id} from {page_type}",
            'warning': 'Section will be permanently removed.',
        }]
        self.safety.preview_changes("Remove Section", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'section_id': section_id}
        
        # Save
        content = json.dumps(template_data, indent=2)
        result = self.client.update_theme_asset(theme_id, template_file, content)
        
        self.audit.log_change('template', f"{theme_id}:{template_file}", 'remove_section',
                             {'section_id': section_id}, template_data)
        
        return {'removed': True, 'section_id': section_id}
    
    def reorder_sections(self, theme_id: int, page_type: str, 
                        new_order: List[str], force: bool = False) -> Dict:
        """Reorder sections on a page."""
        themes = self.client.get_themes()
        is_live = any(t['id'] == theme_id and t.get('role') == 'main' for t in themes)
        
        if is_live:
            raise ValueError("Cannot edit live theme directly!")
        
        template_file = f'templates/{page_type}.json'
        
        asset = self.client.get_theme_asset(theme_id, template_file)
        if not asset or 'value' not in asset:
            raise ValueError(f"Template not found: {template_file}")
        
        template_data = json.loads(asset['value'])
        
        # Backup
        old_order = template_data.get('order', [])
        self.safety.backup_state('template', f"{theme_id}:{template_file}", template_data)
        
        # Update order
        template_data['order'] = new_order
        
        # Preview
        changes = [{
            'action': f"Reorder sections on {page_type}",
            'before': old_order,
            'after': new_order,
        }]
        self.safety.preview_changes("Reorder Sections", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'new_order': new_order}
        
        # Save
        content = json.dumps(template_data, indent=2)
        result = self.client.update_theme_asset(theme_id, template_file, content)
        
        self.audit.log_change('template', f"{theme_id}:{template_file}", 'reorder',
                             {'order': old_order}, template_data)
        
        return {'reordered': True, 'new_order': new_order}
    
    def list_available_sections(self) -> List[Dict]:
        """List common section types available in themes."""
        # Common Shopify Online Store 2.0 sections
        return [
            {'type': 'image-banner', 'name': 'Image Banner', 'description': 'Full-width hero image with text overlay'},
            {'type': 'featured-collection', 'name': 'Featured Collection', 'description': 'Grid of products from a collection'},
            {'type': 'image-with-text', 'name': 'Image with Text', 'description': 'Side-by-side image and text'},
            {'type': 'multicolumn', 'name': 'Multicolumn', 'description': 'Multiple text columns with icons'},
            {'type': 'rich-text', 'name': 'Rich Text', 'description': 'Text content block'},
            {'type': 'video', 'name': 'Video', 'description': 'Embedded video section'},
            {'type': 'slideshow', 'name': 'Slideshow', 'description': 'Image carousel'},
            {'type': 'newsletter', 'name': 'Newsletter', 'description': 'Email signup form'},
            {'type': 'collection-list', 'name': 'Collection List', 'description': 'Grid of collection links'},
            {'type': 'collage', 'name': 'Collage', 'description': 'Mixed media grid'},
            {'type': 'product-recommendations', 'name': 'Product Recommendations', 'description': 'You may also like products'},
        ]
    
    def format_sections_list(self, sections: List[Dict]) -> str:
        """Format sections list for display."""
        if not sections:
            return "No sections found."
        
        lines = [f"{'#':<4} {'ID':<12} {'Type':<30} {'Settings':<40}"]
        lines.append("-" * 86)
        
        for i, section in enumerate(sections, 1):
            section_id = section.get('id', 'N/A')[:10]
            section_type = section.get('type', 'N/A')[:28]
            settings_count = len(section.get('settings', {}))
            lines.append(f"{i:<4} {section_id:<12} {section_type:<30} {settings_count} settings")
        
        return "\n".join(lines)
    
    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Deep merge dictionaries."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
