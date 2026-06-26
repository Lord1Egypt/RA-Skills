"""Metafields and Metaobjects operations for dynamic content."""

from typing import Dict, List, Optional, Any
from .client import ShopifyClient
from .safety import SafetyManager, AuditLogger


class MetafieldOperations:
    """Manage metafields for products, collections, customers, etc."""
    
    def __init__(self, client: ShopifyClient, safety: SafetyManager, audit: AuditLogger):
        self.client = client
        self.safety = safety
        self.audit = audit
    
    # === Product Metafields ===
    
    def get_product_metafields(self, product_id: int) -> List[Dict]:
        """Get all metafields for a product."""
        return self.client.get_metafields('products', product_id)
    
    def set_product_metafield(self, product_id: int, namespace: str, key: str,
                              value: Any, type: str = 'single_line_text_field',
                              force: bool = False) -> Dict:
        """Set a metafield on a product."""
        metafield_data = {
            'namespace': namespace,
            'key': key,
            'value': str(value),
            'type': type
        }
        
        return self._set_metafield('products', product_id, metafield_data, force=force)
    
    def delete_product_metafield(self, product_id: int, metafield_id: int,
                                  force: bool = False) -> Dict:
        """Delete a product metafield."""
        return self._delete_metafield('products', product_id, metafield_id, force=force)
    
    # === Collection Metafields ===
    
    def get_collection_metafields(self, collection_id: int) -> List[Dict]:
        """Get metafields for a collection."""
        return self.client.get_metafields('collections', collection_id)
    
    def set_collection_metafield(self, collection_id: int, namespace: str, key: str,
                                  value: Any, type: str = 'single_line_text_field',
                                  force: bool = False) -> Dict:
        """Set a metafield on a collection."""
        metafield_data = {
            'namespace': namespace,
            'key': key,
            'value': str(value),
            'type': type
        }
        return self._set_metafield('collections', collection_id, metafield_data, force=force)
    
    # === Customer Metafields ===
    
    def get_customer_metafields(self, customer_id: int) -> List[Dict]:
        """Get metafields for a customer."""
        return self.client.get_metafields('customers', customer_id)
    
    def set_customer_metafield(self, customer_id: int, namespace: str, key: str,
                                value: Any, type: str = 'single_line_text_field',
                                force: bool = False) -> Dict:
        """Set a metafield on a customer."""
        metafield_data = {
            'namespace': namespace,
            'key': key,
            'value': str(value),
            'type': type
        }
        return self._set_metafield('customers', customer_id, metafield_data, force=force)
    
    # === Shop Metafields ===
    
    def get_shop_metafields(self) -> List[Dict]:
        """Get shop-level metafields."""
        return self.client.get_metafields('shop', None)
    
    def set_shop_metafield(self, namespace: str, key: str,
                           value: Any, type: str = 'single_line_text_field',
                           force: bool = False) -> Dict:
        """Set a shop-level metafield."""
        metafield_data = {
            'namespace': namespace,
            'key': key,
            'value': str(value),
            'type': type
        }
        return self._set_metafield('shop', None, metafield_data, force=force)
    
    # === Generic Metafield Operations ===
    
    def _set_metafield(self, resource_type: str, resource_id: Optional[int],
                       metafield_data: Dict, force: bool = False) -> Dict:
        """Set a metafield on any resource."""
        # Preview
        changes = [{
            'action': f"Set metafield on {resource_type}",
            'details': f"{metafield_data['namespace']}.{metafield_data['key']} = {metafield_data['value']}",
        }]
        self.safety.preview_changes("Set Metafield", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'data': metafield_data}
        
        result = self.client.create_metafield(resource_type, resource_id, metafield_data)
        
        self.audit.log_change('metafield', f"{resource_type}:{resource_id}", 'set', {}, result)
        
        return result
    
    def _delete_metafield(self, resource_type: str, resource_id: int,
                          metafield_id: int, force: bool = False) -> Dict:
        """Delete a metafield."""
        if self.safety.requires_confirmation('metafield_deletion'):
            if not self.safety.request_confirmation(
                'Delete Metafield',
                f"Delete metafield {metafield_id} from {resource_type}?",
                force=force
            ):
                return {'cancelled': True}
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'metafield_id': metafield_id}
        
        self.client.delete_metafield(resource_type, resource_id, metafield_id)
        
        self.audit.log_change('metafield', f"{resource_type}:{resource_id}", 'delete',
                             {'id': metafield_id}, None)
        
        return {'deleted': True, 'metafield_id': metafield_id}
    
    def format_metafields_list(self, metafields: List[Dict]) -> str:
        """Format metafields for display."""
        if not metafields:
            return "No metafields found."
        
        lines = [f"{'ID':<12} {'Namespace':<20} {'Key':<25} {'Type':<25} {'Value':<30}"]
        lines.append("-" * 112)
        
        for mf in metafields:
            mf_id = str(mf.get('id', 'N/A'))
            namespace = mf.get('namespace', '')[:18]
            key = mf.get('key', '')[:23]
            type_ = mf.get('type', '')[:23]
            value = str(mf.get('value', ''))[:28]
            lines.append(f"{mf_id:<12} {namespace:<20} {key:<25} {type_:<25} {value:<30}")
        
        return "\n".join(lines)


class MetaobjectOperations:
    """Manage metaobjects (custom content types)."""
    
    def __init__(self, client: ShopifyClient, safety: SafetyManager, audit: AuditLogger):
        self.client = client
        self.safety = safety
        self.audit = audit
    
    # === Metaobject Definitions ===
    
    def list_definitions(self) -> List[Dict]:
        """List all metaobject definitions."""
        return self.client.get_metaobject_definitions()
    
    def create_definition(self, name: str, type: str, 
                          field_definitions: List[Dict],
                          force: bool = False) -> Dict:
        """Create a new metaobject definition."""
        definition_data = {
            'name': name,
            'type': type,
            'field_definitions': field_definitions
        }
        
        changes = [{
            'action': f"Create metaobject definition: {name}",
            'details': f"Type: {type}, Fields: {len(field_definitions)}",
        }]
        self.safety.preview_changes("Create Metaobject Definition", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'data': definition_data}
        
        result = self.client.create_metaobject_definition(definition_data)
        
        self.audit.log_change('metaobject_definition', name, 'create', {}, result)
        
        return result
    
    # === Metaobject Entries ===
    
    def list_entries(self, type: str, limit: int = 50) -> List[Dict]:
        """List entries for a metaobject type."""
        return self.client.get_metaobjects(type, limit=limit)
    
    def get_entry(self, metaobject_id: int) -> Optional[Dict]:
        """Get a specific metaobject entry."""
        return self.client.get_metaobject(metaobject_id)
    
    def create_entry(self, type: str, handle: str, fields: Dict,
                     force: bool = False) -> Dict:
        """Create a metaobject entry."""
        entry_data = {
            'type': type,
            'handle': handle,
            'fields': fields
        }
        
        changes = [{
            'action': f"Create metaobject entry: {handle}",
            'details': f"Type: {type}, Fields: {list(fields.keys())}",
        }]
        self.safety.preview_changes("Create Metaobject Entry", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'data': entry_data}
        
        result = self.client.create_metaobject(entry_data)
        
        self.audit.log_change('metaobject', handle, 'create', {}, result)
        
        return result
    
    def update_entry(self, metaobject_id: int, fields: Dict,
                     force: bool = False) -> Dict:
        """Update a metaobject entry."""
        # Get current for backup
        current = self.client.get_metaobject(metaobject_id)
        self.safety.backup_state('metaobject', metaobject_id, current)
        
        changes = [{
            'action': f"Update metaobject entry: {metaobject_id}",
            'details': f"Updating fields: {list(fields.keys())}",
        }]
        self.safety.preview_changes("Update Metaobject Entry", changes)
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'fields': fields}
        
        result = self.client.update_metaobject(metaobject_id, {'fields': fields})
        
        self.audit.log_change('metaobject', str(metaobject_id), 'update', current, result)
        
        return result
    
    def delete_entry(self, metaobject_id: int, force: bool = False) -> Dict:
        """Delete a metaobject entry."""
        if self.safety.requires_confirmation('metaobject_deletion'):
            if not self.safety.request_confirmation(
                'Delete Metaobject',
                f"Delete metaobject entry {metaobject_id}? This cannot be undone.",
                force=force
            ):
                return {'cancelled': True}
        
        if self.safety.is_dry_run():
            return {'dry_run': True, 'metaobject_id': metaobject_id}
        
        self.client.delete_metaobject(metaobject_id)
        
        self.audit.log_change('metaobject', str(metaobject_id), 'delete', {}, None)
        
        return {'deleted': True, 'metaobject_id': metaobject_id}
    
    def format_definitions_list(self, definitions: List[Dict]) -> str:
        """Format metaobject definitions for display."""
        if not definitions:
            return "No metaobject definitions found."
        
        lines = [f"{'Type':<30} {'Name':<30} {'Fields':<10}"]
        lines.append("-" * 70)
        
        for d in definitions:
            type_ = d.get('type', 'N/A')[:28]
            name = d.get('name', 'N/A')[:28]
            field_count = len(d.get('field_definitions', []))
            lines.append(f"{type_:<30} {name:<30} {field_count}")
        
        return "\n".join(lines)
    
    def format_entries_list(self, entries: List[Dict]) -> str:
        """Format metaobject entries for display."""
        if not entries:
            return "No metaobject entries found."
        
        lines = [f"{'ID':<12} {'Handle':<30} {'Type':<30}"]
        lines.append("-" * 72)
        
        for e in entries:
            entry_id = str(e.get('id', 'N/A'))
            handle = e.get('handle', 'N/A')[:28]
            type_ = e.get('type', 'N/A')[:28]
            lines.append(f"{entry_id:<12} {handle:<30} {type_:<30}")
        
        return "\n".join(lines)
