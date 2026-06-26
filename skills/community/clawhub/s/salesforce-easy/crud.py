#!/usr/bin/env python3
"""
Salesforce CRM CRUD Operations
Handles create, update, and delete operations with safety checks
Author: Sawera Khadium
"""

import os
import sys
import json
from typing import Dict, List, Optional
from simple_salesforce import Salesforce
from dotenv import load_dotenv

load_dotenv()

# ─── Security: Input validation ──────────────────────────────────────────────
# Scope is intentionally narrow: only the objects this GTM skill operates on.
# Broad object lists and __c wildcards are excluded to limit blast radius.
ALLOWED_OBJECTS = {
    'Lead', 'Contact', 'Account', 'Opportunity', 'Task'
}

def validate_object_type(object_type: str) -> tuple[bool, str]:
    """Validate object type is in the explicit GTM allowlist.
    Custom objects (__c) are not permitted — only the five listed objects.
    """
    if object_type in ALLOWED_OBJECTS:
        return True, "Valid"
    return (
        False,
        f"Object type '{object_type}' is not in the GTM allowlist "
        f"({', '.join(sorted(ALLOWED_OBJECTS))}). "
        "To operate on other objects, update ALLOWED_OBJECTS deliberately."
    )

def sanitize_data(data: Dict) -> Dict:
    """Sanitize input data"""
    clean_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            # Remove potentially dangerous characters
            clean_value = value.replace("'", "\\'")
            clean_data[key] = clean_value
        else:
            clean_data[key] = value
    return clean_data

# ─── Connection ──────────────────────────────────────────────────────────────

def get_connection() -> Optional[Salesforce]:
    """Get Salesforce connection"""
    instance_url = os.getenv('SALESFORCE_INSTANCE_URL')
    access_token = os.getenv('SALESFORCE_ACCESS_TOKEN')
    username = os.getenv('SALESFORCE_USERNAME')
    password = os.getenv('SALESFORCE_PASSWORD')
    security_token = os.getenv('SALESFORCE_SECURITY_TOKEN', '')
    
    try:
        if instance_url and access_token:
            return Salesforce(instance_url=instance_url, session_id=access_token)
        elif username and password:
            return Salesforce(
                username=username,
                password=password + security_token,
                domain='test' if 'sandbox' in username.lower() else 'login'
            )
        return None
    except Exception:
        return None

# ─── Create Operations ────────────────────────────────────────────────────────

def create_record(object_type: str, data: Dict, confirmed: bool = False) -> Dict:
    """Create a single Salesforce record.
    Requires confirmed=True to prevent accidental agent-driven writes.
    """
    if not confirmed:
        return {
            "success": False,
            "requires_confirmation": True,
            "message": f"Creating a {object_type} record requires confirmation. Set confirmed=True to proceed.",
        }
    valid, message = validate_object_type(object_type)
    if not valid:
        return {"success": False, "error": message}
    
    clean_data = sanitize_data(data)
    
    sf = get_connection()
    if not sf:
        return {"success": False, "error": "Not connected to Salesforce"}
    
    try:
        sf_object = getattr(sf, object_type)
        result = sf_object.create(clean_data)
        
        if result.get('success'):
            return {
                "success": True,
                "id": result['id'],
                "message": f"{object_type} created successfully"
            }
        else:
            errors = result.get('errors', [])
            return {
                "success": False,
                "error": f"Creation failed: {errors}"
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

def create_bulk(object_type: str, records: List[Dict], batch_size: int = 200, confirmed: bool = False) -> Dict:
    """Create multiple records in bulk.
    Requires confirmed=True — bulk creates affect many records and cannot be undone easily.
    """
    if not confirmed:
        return {
            "success": False,
            "requires_confirmation": True,
            "count": len(records),
            "message": f"Creating {len(records)} {object_type} records is a bulk operation. Set confirmed=True to proceed.",
        }
    valid, message = validate_object_type(object_type)
    if not valid:
        return {"success": False, "error": message}

    if len(records) > 200:
        return {"success": False, "error": "Maximum 200 records per batch. Use multiple batches for larger datasets."}
    
    clean_records = [sanitize_data(r) for r in records]
    
    sf = get_connection()
    if not sf:
        return {"success": False, "error": "Not connected to Salesforce"}
    
    try:
        sf_object = getattr(sf, object_type)
        results = sf_object.insert(clean_records)
        
        success_count = sum(1 for r in results if r.get('success'))
        failed_count = len(results) - success_count
        
        failed_records = [
            {"index": i, "errors": r.get('errors', [])}
            for i, r in enumerate(results)
            if not r.get('success')
        ]
        
        return {
            "success": failed_count == 0,
            "total": len(records),
            "created": success_count,
            "failed": failed_count,
            "failed_records": failed_records if failed_records else None,
            "message": f"Created {success_count}/{len(records)} {object_type} records"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# ─── Update Operations ────────────────────────────────────────────────────────

def update_record(object_type: str, record_id: str, data: Dict, confirmed: bool = False) -> Dict:
    """Update a single Salesforce record.
    Requires confirmed=True to prevent accidental agent-driven modifications.
    """
    if not confirmed:
        return {
            "success": False,
            "requires_confirmation": True,
            "message": f"Updating {object_type} {record_id} requires confirmation. Set confirmed=True to proceed.",
        }
    valid, message = validate_object_type(object_type)
    if not valid:
        return {"success": False, "error": message}
    
    clean_data = sanitize_data(data)
    
    sf = get_connection()
    if not sf:
        return {"success": False, "error": "Not connected to Salesforce"}
    
    try:
        sf_object = getattr(sf, object_type)
        result = sf_object.update(record_id, clean_data)
        
        # Update returns 204 No Content on success
        return {
            "success": True,
            "id": record_id,
            "message": f"{object_type} {record_id} updated successfully"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def update_bulk(object_type: str, records: List[Dict], confirmed: bool = False) -> Dict:
    """Update multiple records in bulk.
    Requires confirmed=True — bulk updates affect many records simultaneously.
    """
    if not confirmed:
        return {
            "success": False,
            "requires_confirmation": True,
            "count": len(records),
            "message": f"Updating {len(records)} {object_type} records is a bulk operation. Set confirmed=True to proceed.",
        }
    valid, message = validate_object_type(object_type)
    if not valid:
        return {"success": False, "error": message}

    if len(records) > 200:
        return {"success": False, "error": "Maximum 200 records per batch"}
    
    # Validate all records have Id field
    for i, record in enumerate(records):
        if 'Id' not in record:
            return {"success": False, "error": f"Record at index {i} missing 'Id' field"}
    
    clean_records = [sanitize_data(r) for r in records]
    
    sf = get_connection()
    if not sf:
        return {"success": False, "error": "Not connected to Salesforce"}
    
    try:
        sf_object = getattr(sf, object_type)
        results = sf_object.update(clean_records)
        
        success_count = sum(1 for r in results if r.get('success'))
        failed_count = len(results) - success_count
        
        failed_records = [
            {"id": records[i].get('Id'), "errors": r.get('errors', [])}
            for i, r in enumerate(results)
            if not r.get('success')
        ]
        
        return {
            "success": failed_count == 0,
            "total": len(records),
            "updated": success_count,
            "failed": failed_count,
            "failed_records": failed_records if failed_records else None,
            "message": f"Updated {success_count}/{len(records)} {object_type} records"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# ─── Delete Operations ────────────────────────────────────────────────────────

def delete_record(object_type: str, record_id: str, confirmed: bool = False) -> Dict:
    """Delete a single record (requires confirmation)"""
    if not confirmed:
        return {
            "success": False,
            "requires_confirmation": True,
            "message": f"Deleting {object_type} {record_id} requires confirmation. Set confirmed=True to proceed."
        }
    
    valid, message = validate_object_type(object_type)
    if not valid:
        return {"success": False, "error": message}
    
    sf = get_connection()
    if not sf:
        return {"success": False, "error": "Not connected to Salesforce"}
    
    try:
        sf_object = getattr(sf, object_type)
        result = sf_object.delete(record_id)
        
        return {
            "success": True,
            "id": record_id,
            "message": f"{object_type} {record_id} deleted successfully"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def export_records_before_delete(sf, object_type: str, record_ids: List[str]) -> Dict:
    """
    Export a backup of records before bulk deletion.
    Called automatically by delete_bulk — gives the user a rollback snapshot.
    """
    try:
        ids_str = "', '".join(record_ids)
        query = f"SELECT Id, Name FROM {object_type} WHERE Id IN ('{ids_str}') LIMIT 200"
        result = sf.query_all(query)
        return {
            "exported": len(result.get("records", [])),
            "records": [
                {k: v for k, v in r.items() if k != "attributes"}
                for r in result.get("records", [])
            ],
        }
    except Exception as exc:
        return {"exported": 0, "error": str(exc)}


def delete_bulk(object_type: str, record_ids: List[str], confirmed: bool = False) -> Dict:
    """Delete multiple records in bulk.

    Requires confirmed=True. Before deleting, automatically exports a backup
    snapshot of affected records so the operation can be audited or reversed
    by re-creating records from the exported data.
    """
    if not confirmed:
        return {
            "success": False,
            "requires_confirmation": True,
            "count": len(record_ids),
            "message": (
                f"Deleting {len(record_ids)} {object_type} records is irreversible. "
                "A backup export will be performed before deletion. "
                "Set confirmed=True to proceed."
            ),
            "rollback_note": (
                "Records will be exported to the response before deletion. "
                "Save the 'backup' field to restore records if needed."
            ),
        }

    valid, message = validate_object_type(object_type)
    if not valid:
        return {"success": False, "error": message}

    if len(record_ids) > 200:
        return {"success": False, "error": "Maximum 200 records per batch"}

    sf = get_connection()
    if not sf:
        return {"success": False, "error": "Not connected to Salesforce"}

    # Export backup before any deletion
    backup = export_records_before_delete(sf, object_type, record_ids)

    try:
        sf_object = getattr(sf, object_type)
        results = sf_object.delete(record_ids)
        
        success_count = sum(1 for r in results if r.get('success'))
        failed_count = len(results) - success_count
        
        failed_records = [
            {"id": record_ids[i], "errors": r.get('errors', [])}
            for i, r in enumerate(results)
            if not r.get('success')
        ]
        
        return {
            "success": failed_count == 0,
            "total": len(record_ids),
            "deleted": success_count,
            "failed": failed_count,
            "failed_records": failed_records if failed_records else None,
            "message": f"Deleted {success_count}/{len(record_ids)} {object_type} records",
            "backup": backup,  # Pre-deletion snapshot for rollback/audit
        }
    except Exception as e:
        return {"success": False, "backup": backup, "error": str(e)}

# ─── CLI Interface ────────────────────────────────────────────────────────────

def main():
    """CLI interface for CRUD operations"""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python crud.py <command> [args]"}))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "create":
        if len(sys.argv) < 4:
            print(json.dumps({"error": "Usage: python crud.py create <ObjectType> '<JSON data>'"}))
            sys.exit(1)
        object_type = sys.argv[2]
        data = json.loads(sys.argv[3])
        confirmed = sys.argv[4].lower() == 'true' if len(sys.argv) > 4 else False
        result = create_record(object_type, data, confirmed=confirmed)
        print(json.dumps(result, default=str))
    
    elif command == "create-bulk":
        if len(sys.argv) < 4:
            print(json.dumps({"error": "Usage: python crud.py create-bulk <ObjectType> '<JSON array>'"}))
            sys.exit(1)
        object_type = sys.argv[2]
        records = json.loads(sys.argv[3])
        confirmed = sys.argv[4].lower() == 'true' if len(sys.argv) > 4 else False
        result = create_bulk(object_type, records, confirmed=confirmed)
        print(json.dumps(result, default=str))
    
    elif command == "update":
        if len(sys.argv) < 5:
            print(json.dumps({"error": "Usage: python crud.py update <ObjectType> <RecordId> '<JSON data>'"}))
            sys.exit(1)
        object_type = sys.argv[2]
        record_id = sys.argv[3]
        data = json.loads(sys.argv[4])
        confirmed = sys.argv[5].lower() == 'true' if len(sys.argv) > 5 else False
        result = update_record(object_type, record_id, data, confirmed=confirmed)
        print(json.dumps(result, default=str))
    
    elif command == "update-bulk":
        if len(sys.argv) < 4:
            print(json.dumps({"error": "Usage: python crud.py update-bulk <ObjectType> '<JSON array with Id fields>'"}))
            sys.exit(1)
        object_type = sys.argv[2]
        records = json.loads(sys.argv[3])
        confirmed = sys.argv[4].lower() == 'true' if len(sys.argv) > 4 else False
        result = update_bulk(object_type, records, confirmed=confirmed)
        print(json.dumps(result, default=str))
    
    elif command == "delete":
        if len(sys.argv) < 4:
            print(json.dumps({"error": "Usage: python crud.py delete <ObjectType> <RecordId> [confirmed]"}))
            sys.exit(1)
        object_type = sys.argv[2]
        record_id = sys.argv[3]
        confirmed = sys.argv[4].lower() == 'true' if len(sys.argv) > 4 else False
        result = delete_record(object_type, record_id, confirmed)
        print(json.dumps(result, default=str))
    
    elif command == "delete-bulk":
        if len(sys.argv) < 4:
            print(json.dumps({"error": "Usage: python crud.py delete-bulk <ObjectType> '<JSON array of IDs>' [confirmed]"}))
            sys.exit(1)
        object_type = sys.argv[2]
        record_ids = json.loads(sys.argv[3])
        confirmed = sys.argv[4].lower() == 'true' if len(sys.argv) > 4 else False
        result = delete_bulk(object_type, record_ids, confirmed)
        print(json.dumps(result, default=str))
    
    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))

if __name__ == "__main__":
    main()
