#!/usr/bin/env python3
"""
Salesforce CRM Query Engine
Handles SOQL queries, SOSL searches, and data retrieval
Author: Sawera Khadium
"""

import os
import sys
import json
import re
from typing import Dict, List, Optional, Any
from simple_salesforce import Salesforce, SalesforceResourceNotFound
from dotenv import load_dotenv

load_dotenv()

# ─── Security: Validate inputs before use ───────────────────────────────────
# Scope limited to GTM-relevant objects. No __c wildcard.
ALLOWED_OBJECTS = {
    'Lead', 'Contact', 'Account', 'Opportunity', 'Task', 'User'
}

DANGEROUS_KEYWORDS = ['DROP', 'TRUNCATE', 'DELETE', 'INSERT', 'UPDATE', 'MERGE', 'EXEC', 'EXECUTE']

def validate_soql(query: str) -> tuple[bool, str]:
    """Validate SOQL query for safety"""
    query_upper = query.upper().strip()
    
    # Only allow SELECT statements
    if not query_upper.startswith('SELECT'):
        return False, "Only SELECT queries are allowed through this function. Use create/update/delete functions for modifications."
    
    # Block dangerous keywords
    for keyword in DANGEROUS_KEYWORDS:
        if keyword in query_upper:
            return False, f"Query contains disallowed keyword: {keyword}"
    
    return True, "Valid"

def sanitize_field_value(value: str) -> str:
    """Sanitize field values to prevent SOQL injection"""
    if isinstance(value, str):
        # Escape single quotes
        return value.replace("'", "\\'")
    return str(value)

# ─── Connection ──────────────────────────────────────────────────────────────

def get_connection() -> Optional[Salesforce]:
    """Get Salesforce connection from environment"""
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
        else:
            return None
    except Exception:
        return None

# ─── Query Functions ─────────────────────────────────────────────────────────

def run_soql(query: str, limit: int = 200) -> Dict:
    """Execute a SOQL query and return results"""
    # Validate query
    valid, message = validate_soql(query)
    if not valid:
        return {"success": False, "error": message}
    
    # Add LIMIT if not present
    if 'LIMIT' not in query.upper() and limit:
        query = f"{query.rstrip()} LIMIT {limit}"
    
    sf = get_connection()
    if not sf:
        return {"success": False, "error": "Not connected to Salesforce. Please set credentials."}
    
    try:
        result = sf.query_all(query)
        records = result.get('records', [])
        
        # Clean up records (remove Salesforce metadata)
        clean_records = []
        for record in records:
            clean = {k: v for k, v in record.items() if k not in ['attributes']}
            clean_records.append(clean)
        
        return {
            "success": True,
            "total_size": result.get('totalSize', len(records)),
            "records": clean_records,
            "count": len(clean_records)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def search_records(search_term: str, objects: List[str] = None, fields: str = "ALL FIELDS") -> Dict:
    """Execute SOSL search across multiple objects"""
    if not objects:
        objects = ['Lead', 'Contact', 'Account', 'Opportunity']
    
    # Validate objects
    for obj in objects:
        if obj not in ALLOWED_OBJECTS:
            return {"success": False, "error": f"Object not allowed: {obj}"}
    
    # Sanitize search term
    safe_term = sanitize_field_value(search_term)
    
    # Build SOSL query
    returning_clause = ', '.join(objects)
    sosl = f"FIND {{{safe_term}}} IN {fields} RETURNING {returning_clause}"
    
    sf = get_connection()
    if not sf:
        return {"success": False, "error": "Not connected to Salesforce. Please set credentials."}
    
    try:
        result = sf.search(sosl)
        
        all_records = {}
        for obj in objects:
            if obj in result.get('searchRecords', {}):
                records = result['searchRecords'][obj]
                all_records[obj] = [
                    {k: v for k, v in r.items() if k != 'attributes'}
                    for r in records
                ]
        
        total = sum(len(v) for v in all_records.values())
        
        return {
            "success": True,
            "total_found": total,
            "results": all_records
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_record(object_type: str, record_id: str, fields: List[str] = None) -> Dict:
    """Get a specific record by ID"""
    if object_type not in ALLOWED_OBJECTS:
        return {"success": False, "error": f"Object not allowed: {object_type}"}
    
    sf = get_connection()
    if not sf:
        return {"success": False, "error": "Not connected to Salesforce. Please set credentials."}
    
    try:
        sf_object = getattr(sf, object_type)
        
        if fields:
            record = sf_object.get(record_id, fields=fields)
        else:
            record = sf_object.get(record_id)
        
        clean_record = {k: v for k, v in record.items() if k != 'attributes'}
        
        return {
            "success": True,
            "record": clean_record
        }
    except SalesforceResourceNotFound:
        return {"success": False, "error": f"Record {record_id} not found in {object_type}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_object_fields(object_type: str) -> Dict:
    """Get all available fields for a Salesforce object"""
    if object_type not in ALLOWED_OBJECTS:
        return {"success": False, "error": f"Object not allowed: {object_type}"}
    
    sf = get_connection()
    if not sf:
        return {"success": False, "error": "Not connected to Salesforce. Please set credentials."}
    
    try:
        sf_object = getattr(sf, object_type)
        describe = sf_object.describe()
        
        fields = []
        for field in describe['fields']:
            fields.append({
                "name": field['name'],
                "label": field['label'],
                "type": field['type'],
                "required": not field['nillable'] and not field['defaultedOnCreate'],
                "updateable": field['updateable'],
                "createable": field['createable']
            })
        
        return {
            "success": True,
            "object": object_type,
            "field_count": len(fields),
            "fields": fields
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_leads(filters: Dict = None, fields: List[str] = None, limit: int = 50) -> Dict:
    """Get leads with optional filters"""
    default_fields = ['Id', 'Name', 'Email', 'Phone', 'Company', 'Status', 'LeadSource', 'CreatedDate', 'OwnerId']
    query_fields = ', '.join(fields or default_fields)
    
    where_clause = ""
    if filters:
        conditions = []
        for key, value in filters.items():
            safe_value = sanitize_field_value(str(value))
            if isinstance(value, str):
                conditions.append(f"{key} = '{safe_value}'")
            else:
                conditions.append(f"{key} = {safe_value}")
        if conditions:
            where_clause = f" WHERE {' AND '.join(conditions)}"
    
    query = f"SELECT {query_fields} FROM Lead{where_clause} ORDER BY CreatedDate DESC LIMIT {limit}"
    return run_soql(query, limit=limit)

def get_contacts(filters: Dict = None, fields: List[str] = None, limit: int = 50) -> Dict:
    """Get contacts with optional filters"""
    default_fields = ['Id', 'Name', 'Email', 'Phone', 'AccountId', 'Account.Name', 'Title', 'CreatedDate']
    query_fields = ', '.join(fields or default_fields)
    
    where_clause = ""
    if filters:
        conditions = []
        for key, value in filters.items():
            safe_value = sanitize_field_value(str(value))
            if isinstance(value, str):
                conditions.append(f"{key} = '{safe_value}'")
            else:
                conditions.append(f"{key} = {safe_value}")
        if conditions:
            where_clause = f" WHERE {' AND '.join(conditions)}"
    
    query = f"SELECT {query_fields} FROM Contact{where_clause} ORDER BY CreatedDate DESC LIMIT {limit}"
    return run_soql(query, limit=limit)

def get_opportunities(filters: Dict = None, fields: List[str] = None, limit: int = 50) -> Dict:
    """Get opportunities with optional filters"""
    default_fields = ['Id', 'Name', 'Amount', 'StageName', 'CloseDate', 'AccountId', 'Account.Name', 'OwnerId', 'Probability']
    query_fields = ', '.join(fields or default_fields)
    
    where_clause = ""
    if filters:
        conditions = []
        for key, value in filters.items():
            safe_value = sanitize_field_value(str(value))
            if isinstance(value, str):
                conditions.append(f"{key} = '{safe_value}'")
            else:
                conditions.append(f"{key} = {safe_value}")
        if conditions:
            where_clause = f" WHERE {' AND '.join(conditions)}"
    
    query = f"SELECT {query_fields} FROM Opportunity{where_clause} ORDER BY CloseDate ASC LIMIT {limit}"
    return run_soql(query, limit=limit)

def get_accounts(filters: Dict = None, fields: List[str] = None, limit: int = 50) -> Dict:
    """Get accounts with optional filters"""
    default_fields = ['Id', 'Name', 'Industry', 'BillingCity', 'BillingState', 'Phone', 'Website', 'NumberOfEmployees', 'AnnualRevenue']
    query_fields = ', '.join(fields or default_fields)
    
    where_clause = ""
    if filters:
        conditions = []
        for key, value in filters.items():
            safe_value = sanitize_field_value(str(value))
            if isinstance(value, str):
                conditions.append(f"{key} = '{safe_value}'")
            else:
                conditions.append(f"{key} = {safe_value}")
        if conditions:
            where_clause = f" WHERE {' AND '.join(conditions)}"
    
    query = f"SELECT {query_fields} FROM Account{where_clause} ORDER BY Name ASC LIMIT {limit}"
    return run_soql(query, limit=limit)

# ─── CLI Interface ────────────────────────────────────────────────────────────

def main():
    """CLI interface for query operations"""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python query.py <command> [args]"}))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "soql":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: python query.py soql '<SOQL query>'"}))
            sys.exit(1)
        query = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 200
        result = run_soql(query, limit)
        print(json.dumps(result, default=str))
    
    elif command == "search":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: python query.py search '<term>'"}))
            sys.exit(1)
        term = sys.argv[2]
        objects = sys.argv[3].split(',') if len(sys.argv) > 3 else None
        result = search_records(term, objects)
        print(json.dumps(result, default=str))
    
    elif command == "leads":
        filters = json.loads(sys.argv[2]) if len(sys.argv) > 2 else None
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 50
        result = get_leads(filters, limit=limit)
        print(json.dumps(result, default=str))
    
    elif command == "contacts":
        filters = json.loads(sys.argv[2]) if len(sys.argv) > 2 else None
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 50
        result = get_contacts(filters, limit=limit)
        print(json.dumps(result, default=str))
    
    elif command == "opportunities":
        filters = json.loads(sys.argv[2]) if len(sys.argv) > 2 else None
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 50
        result = get_opportunities(filters, limit=limit)
        print(json.dumps(result, default=str))
    
    elif command == "accounts":
        filters = json.loads(sys.argv[2]) if len(sys.argv) > 2 else None
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 50
        result = get_accounts(filters, limit=limit)
        print(json.dumps(result, default=str))
    
    elif command == "record":
        if len(sys.argv) < 4:
            print(json.dumps({"error": "Usage: python query.py record <ObjectType> <RecordId>"}))
            sys.exit(1)
        result = get_record(sys.argv[2], sys.argv[3])
        print(json.dumps(result, default=str))
    
    elif command == "fields":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: python query.py fields <ObjectType>"}))
            sys.exit(1)
        result = get_object_fields(sys.argv[2])
        print(json.dumps(result, default=str))
    
    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))

if __name__ == "__main__":
    main()
