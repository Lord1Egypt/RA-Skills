"""Safety features: dry-run mode, confirmations, rollback."""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path

from .config import Config


class SafetyManager:
    """Manages safety features for store operations."""
    
    def __init__(self, config: Config):
        self.config = config
        self.dry_run = config.dry_run_by_default
        self.backups: List[Dict] = []
    
    def set_dry_run(self, enabled: bool):
        """Set dry-run mode."""
        self.dry_run = enabled
    
    def is_dry_run(self) -> bool:
        """Check if in dry-run mode."""
        return self.dry_run
    
    def requires_confirmation(self, operation_type: str, details: Optional[Dict] = None) -> bool:
        """Check if operation requires explicit confirmation."""
        required_ops = self.config.get('safety.require_confirmation_for', [])
        
        if operation_type in required_ops:
            return True
        
        # Check for bulk operations
        if operation_type == 'bulk_operations' and details:
            item_count = details.get('item_count', 0)
            max_bulk = self.config.get('safety.max_products_per_bulk', 50)
            if item_count > max_bulk:
                return True
        
        # Check for inventory reductions
        if operation_type == 'inventory' and details:
            if details.get('adjustment', 0) < 0:
                return True
        
        return False
    
    def request_confirmation(self, operation: str, details: str, force: bool = False) -> bool:
        """Request user confirmation for operation."""
        if force:
            return True
        
        print(f"\n⚠️  CONFIRMATION REQUIRED")
        print(f"Operation: {operation}")
        print(f"Details: {details}")
        print(f"\nType 'yes' to proceed, or anything else to cancel:")
        
        response = input("> ").strip().lower()
        return response == 'yes'
    
    def preview_changes(self, title: str, changes: List[Dict[str, Any]]):
        """Display preview of changes in dry-run mode."""
        print(f"\n{'='*60}")
        print(f"🔍 DRY RUN PREVIEW: {title}")
        print(f"{'='*60}")
        
        for i, change in enumerate(changes, 1):
            print(f"\n{i}. {change.get('action', 'Unknown action')}")
            
            if 'before' in change and 'after' in change:
                print(f"   Before: {self._format_value(change['before'])}")
                print(f"   After:  {self._format_value(change['after'])}")
            elif 'details' in change:
                print(f"   Details: {change['details']}")
            
            if 'warning' in change:
                print(f"   ⚠️  {change['warning']}")
        
        print(f"\n{'='*60}")
        
        if self.dry_run:
            print("\n✋ Dry-run mode: No changes will be applied.")
            print("   Add --execute to apply these changes.")
        else:
            print("\n✅ These changes will be applied.")
        
        print(f"{'='*60}\n")
    
    def _format_value(self, value: Any) -> str:
        """Format value for display."""
        if isinstance(value, dict):
            return json.dumps(value, indent=2)[:200] + "..." if len(str(value)) > 200 else json.dumps(value, indent=2)
        if isinstance(value, list):
            return f"[{len(value)} items]"
        return str(value)
    
    def backup_state(self, resource_type: str, resource_id: str, data: Dict):
        """Store backup of resource state before modification."""
        backup = {
            'timestamp': datetime.utcnow().isoformat(),
            'resource_type': resource_type,
            'resource_id': str(resource_id),
            'data': data,
        }
        self.backups.append(backup)
        return backup
    
    def get_backup(self, resource_type: str, resource_id: str) -> Optional[Dict]:
        """Get backup for a resource."""
        for backup in reversed(self.backups):
            if (backup['resource_type'] == resource_type and 
                backup['resource_id'] == str(resource_id)):
                return backup
        return None
    
    def validate_operation(self, operation: str, data: Dict) -> tuple[bool, Optional[str]]:
        """Validate operation data. Returns (is_valid, error_message)."""
        
        # Check permissions
        permission_map = {
            'product_create': 'allow_product_changes',
            'product_update': 'allow_product_changes',
            'product_delete': 'allow_product_changes',
            'order_fulfill': 'allow_order_fulfillment',
            'order_refund': 'allow_refunds',
            'content_update': 'allow_content_updates',
            'theme_edit': 'allow_theme_edits',
        }
        
        permission_key = permission_map.get(operation)
        if permission_key:
            allowed = self.config.get(f'permissions.{permission_key}', False)
            if not allowed:
                return False, f"Operation '{operation}' is not permitted in configuration"
        
        # Check for required fields
        required_fields = {
            'product_create': ['title'],
            'product_update': ['id'],
            'order_fulfill': ['order_id'],
            'order_refund': ['order_id', 'amount'],
        }
        
        fields = required_fields.get(operation, [])
        for field in fields:
            if field not in data or data[field] is None:
                return False, f"Missing required field: {field}"
        
        return True, None
    
    def sanitize_for_log(self, data: Dict) -> Dict:
        """Remove sensitive data before logging."""
        sanitized = data.copy()
        sensitive_keys = ['access_token', 'password', 'credit_card', 'token']
        
        def remove_sensitive(obj):
            if isinstance(obj, dict):
                return {
                    k: '[REDACTED]' if any(s in k.lower() for s in sensitive_keys) else remove_sensitive(v)
                    for k, v in obj.items()
                }
            elif isinstance(obj, list):
                return [remove_sensitive(item) for item in obj]
            return obj
        
        return remove_sensitive(sanitized)


class AuditLogger:
    """Logs all store changes for audit trail."""
    
    # Sensitive keys that should never appear in logs
    SENSITIVE_KEYS = ['access_token', 'password', 'credit_card', 'token', 'api_key', 'secret']
    
    def __init__(self, config: Config):
        self.config = config
        self.log_path = Path(config.audit_log_path)
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Ensure log directory exists."""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _sanitize(self, obj):
        """Recursively remove sensitive data from objects."""
        if isinstance(obj, dict):
            return {
                k: '[REDACTED]' if any(s in k.lower() for s in self.SENSITIVE_KEYS) else self._sanitize(v)
                for k, v in obj.items()
            }
        elif isinstance(obj, list):
            return [self._sanitize(item) for item in obj]
        return obj
    
    def log(self, operation: str, status: str, data: Dict, error: Optional[str] = None):
        """Log an operation."""
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'operation': operation,
            'status': status,
            'data': self._sanitize(data),
        }
        
        if error:
            entry['error'] = error
        
        # Append to log file
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def log_change(self, resource_type: str, resource_id: str, 
                   action: str, before: Optional[Dict], after: Dict,
                   dry_run: bool = False):
        """Log a resource change."""
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': 'change',
            'resource_type': resource_type,
            'resource_id': str(resource_id),
            'action': action,
            'before': self._sanitize(before) if before else None,
            'after': self._sanitize(after),
            'dry_run': dry_run,
        }
        
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def get_recent_changes(self, limit: int = 50) -> List[Dict]:
        """Get recent changes from log."""
        if not self.log_path.exists():
            return []
        
        changes = []
        with open(self.log_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        changes.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        
        return changes[-limit:]
