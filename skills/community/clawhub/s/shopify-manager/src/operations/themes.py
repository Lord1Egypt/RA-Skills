"""Theme operations for safe layout/design changes."""

from typing import Dict, List, Optional
from .client import ShopifyClient
from .safety import SafetyManager, AuditLogger


class ThemeOperations:
    """Theme management with preview workflow."""
    
    def __init__(self, client: ShopifyClient, safety: SafetyManager, audit: AuditLogger):
        self.client = client
        self.safety = safety
        self.audit = audit
        self._working_theme_id = None  # Track the unpublished copy
    
    def get_themes(self) -> List[Dict]:
        """Get all themes in the store."""
        return self.client.get_themes()
    
    def get_live_theme(self) -> Optional[Dict]:
        """Get the currently live/published theme."""
        themes = self.get_themes()
        for theme in themes:
            if theme.get('role') == 'main':
                return theme
        return themes[0] if themes else None
    
    def duplicate_theme(self, theme_id: int, name: Optional[str] = None) -> Dict:
        """Create a duplicate of a theme for safe editing."""
        source_theme = None
        themes = self.get_themes()
        for t in themes:
            if t['id'] == theme_id:
                source_theme = t
                break
        
        if not source_theme:
            raise ValueError(f"Theme not found: {theme_id}")
        
        new_name = name or f"{source_theme.get('name')} - AI Edit {self._timestamp()}"
        
        # Duplicate the theme
        new_theme = self.client.duplicate_theme(theme_id, new_name)
        self._working_theme_id = new_theme.get('id')
        
        # Audit log
        self.audit.log_change('theme', new_theme.get('id'), 'duplicate', 
                             {'source_theme_id': theme_id}, new_theme)
        
        return new_theme
    
    def create_working_copy(self, name: Optional[str] = None) -> Dict:
        """Create a working copy of the live theme."""
        live_theme = self.get_live_theme()
        if not live_theme:
            raise ValueError("No live theme found")
        
        working_name = name or f"AI Working Copy - {self._timestamp()}"
        
        print(f"📋 Duplicating live theme: {live_theme.get('name')}")
        print(f"   Creating working copy: {working_name}")
        
        working_theme = self.duplicate_theme(live_theme['id'], working_name)
        
        print(f"\n✅ Working copy created!")
        print(f"   Theme ID: {working_theme.get('id')}")
        print(f"   Preview: {working_theme.get('preview_url')}")
        
        return working_theme
    
    def get_theme_assets(self, theme_id: int) -> List[Dict]:
        """List all assets in a theme."""
        return self.client.get_theme_assets(theme_id)
    
    def get_asset(self, theme_id: int, asset_key: str) -> Optional[Dict]:
        """Get a specific theme asset."""
        return self.client.get_theme_asset(theme_id, asset_key)
    
    def update_asset(self, theme_id: int, asset_key: str, content: str,
                     force: bool = False) -> Dict:
        """Update a theme asset (template, CSS, JS, etc.)."""
        # Validate operation
        is_valid, error = self.safety.validate_operation('theme_edit', {
            'theme_id': theme_id,
            'asset_key': asset_key
        })
        if not is_valid:
            raise ValueError(error)
        
        # Get current asset for backup
        current_asset = self.get_asset(theme_id, asset_key)
        if current_asset:
            self.safety.backup_state('theme_asset', f"{theme_id}:{asset_key}", current_asset)
        
        # Check if this is the live theme
        themes = self.get_themes()
        is_live = any(t['id'] == theme_id and t.get('role') == 'main' for t in themes)
        
        if is_live:
            raise ValueError(
                "Cannot edit live theme directly! "
                "Use 'create_working_copy' first, then edit the copy."
            )
        
        # Validate Liquid syntax if it's a template
        if asset_key.endswith('.liquid'):
            if not self._validate_liquid(content):
                raise ValueError(f"Invalid Liquid syntax in {asset_key}")
        
        # Require confirmation for theme changes
        if self.safety.requires_confirmation('theme_changes'):
            if not self.safety.request_confirmation(
                'Edit Theme Asset',
                f"Update {asset_key} in theme {theme_id}? "
                f"This will modify the unpublished theme.",
                force=force
            ):
                return {'cancelled': True}
        
        # Preview changes
        changes = [{
            'action': f"Update theme asset: {asset_key}",
            'before': f"{len(current_asset.get('value', ''))} characters" if current_asset else 'New file',
            'after': f"{len(content)} characters",
            'warning': 'Theme changes affect store appearance. Review preview before publishing.'
        }]
        self.safety.preview_changes("Theme Asset Update", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'theme_id': theme_id, 'asset_key': asset_key}
        
        # Update asset
        updated = self.client.update_theme_asset(theme_id, asset_key, content)
        
        # Audit log
        self.audit.log_change('theme_asset', f"{theme_id}:{asset_key}", 'update',
                             current_asset, updated)
        
        return updated
    
    def generate_asset_content(self, asset_key: str, prompt: str, 
                               current_content: Optional[str] = None) -> str:
        """Generate new asset content using AI (placeholder for LLM integration)."""
        # This would integrate with an LLM to generate/modify content
        # For now, returns a placeholder with instructions
        
        if asset_key.endswith('.css'):
            return f"/* AI Generated CSS based on: {prompt} */\n\n/* TODO: Implement LLM-generated styles */\n"
        elif asset_key.endswith('.js'):
            return f"// AI Generated JS based on: {prompt}\n\n// TODO: Implement LLM-generated script\n"
        elif asset_key.endswith('.liquid'):
            # Use .format() with placeholders to avoid f-string interpolation issues with Liquid syntax
            return "{{comment_start}} AI Generated Liquid based on: {prompt} {{comment_end}}\n\n<!-- TODO: Implement LLM-generated template -->\n".format(
                prompt=prompt,
                comment_start="{% comment %}",
                comment_end="{% endcomment %}"
            )
        else:
            return f"# AI Generated content based on: {prompt}\n\n# TODO: Implement LLM-generated content\n"
    
    def get_preview_url(self, theme_id: int) -> Optional[str]:
        """Get preview URL for a theme."""
        themes = self.get_themes()
        for theme in themes:
            if theme['id'] == theme_id:
                return theme.get('preview_url')
        return None
    
    def publish_theme(self, theme_id: int, force: bool = False) -> Dict:
        """Publish a theme (make it live)."""
        themes = self.get_themes()
        theme = None
        for t in themes:
            if t['id'] == theme_id:
                theme = t
                break
        
        if not theme:
            raise ValueError(f"Theme not found: {theme_id}")
        
        if theme.get('role') == 'main':
            return {'message': 'Theme is already live'}
        
        # Require strong confirmation for publishing
        if not force:
            print(f"\n{'='*60}")
            print("⚠️  PUBLISH THEME - THIS WILL MAKE CHANGES LIVE")
            print(f"{'='*60}")
            print(f"Theme: {theme.get('name')}")
            print(f"Theme ID: {theme_id}")
            print(f"\nThis will replace your current live theme.")
            print("All visitors to your store will see these changes immediately.")
            print(f"\n{'='*60}")
            print("Type 'publish' to proceed, or anything else to cancel:")
            
            response = input("> ").strip().lower()
            if response != 'publish':
                return {'cancelled': True}
        
        # Backup current live theme
        live_theme = self.get_live_theme()
        if live_theme:
            self.safety.backup_state('theme_live', live_theme['id'], live_theme)
        
        # Publish
        result = self.client.publish_theme(theme_id)
        
        # Audit log
        self.audit.log_change('theme', theme_id, 'publish',
                             {'previous_live': live_theme.get('id') if live_theme else None},
                             {'new_live': theme_id})
        
        return result
    
    def delete_theme(self, theme_id: int, force: bool = False) -> Dict:
        """Delete an unpublished theme."""
        themes = self.get_themes()
        theme = None
        for t in themes:
            if t['id'] == theme_id:
                theme = t
                break
        
        if not theme:
            raise ValueError(f"Theme not found: {theme_id}")
        
        if theme.get('role') == 'main':
            raise ValueError("Cannot delete the live theme!")
        
        if not force:
            print(f"\nDelete theme '{theme.get('name')}'? This cannot be undone.")
            print("Type 'delete' to confirm:")
            response = input("> ").strip().lower()
            if response != 'delete':
                return {'cancelled': True}
        
        self.client.delete_theme(theme_id)
        
        self.audit.log_change('theme', theme_id, 'delete', theme, None)
        
        return {'deleted': True, 'theme_id': theme_id}
    
    def _validate_liquid(self, content: str) -> bool:
        """Basic Liquid syntax validation."""
        # Check for unmatched tags
        tags = ['if', 'for', 'capture', 'form', 'paginate', 'case', 'unless']
        
        for tag in tags:
            open_count = content.count(f'{{% {tag} ')
            close_count = content.count(f'{{% end{tag} %}}')
            if open_count != close_count:
                return False
        
        # Check for basic syntax errors
        if '{{' in content and '}}' not in content:
            return False
        if '{%' in content and '%}' not in content:
            return False
        
        return True
    
    def _timestamp(self) -> str:
        """Generate timestamp string."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M")
    
    def format_theme_list(self, themes: List[Dict]) -> str:
        """Format theme list for display."""
        if not themes:
            return "No themes found."
        
        lines = [f"{'ID':<12} {'Role':<10} {'Name':<40} {'Preview':<50}"]
        lines.append("-" * 112)
        
        for t in themes:
            theme_id = str(t.get('id', 'N/A'))
            role = t.get('role', 'unpublished')[:8]
            name = t.get('name', '')[:38]
            preview = t.get('preview_url', 'N/A')[:48]
            lines.append(f"{theme_id:<12} {role:<10} {name:<40} {preview:<50}")
        
        return "\n".join(lines)
