#!/usr/bin/env python3
"""
Salesforce CRM Duplicate Detection
Intelligent duplicate detection for Leads, Contacts, and Accounts
Author: Sawera Khadium
"""

import os
import sys
import json
from typing import Dict, List, Tuple
from collections import defaultdict
from difflib import SequenceMatcher
from simple_salesforce import Salesforce
from dotenv import load_dotenv

load_dotenv()

def get_connection() -> Salesforce:
    """Get Salesforce connection"""
    instance_url = os.getenv('SALESFORCE_INSTANCE_URL')
    access_token = os.getenv('SALESFORCE_ACCESS_TOKEN')
    username = os.getenv('SALESFORCE_USERNAME')
    password = os.getenv('SALESFORCE_PASSWORD')
    security_token = os.getenv('SALESFORCE_SECURITY_TOKEN', '')
    
    if instance_url and access_token:
        return Salesforce(instance_url=instance_url, session_id=access_token)
    elif username and password:
        return Salesforce(
            username=username,
            password=password + security_token,
            domain='test' if 'sandbox' in username.lower() else 'login'
        )
    return None

def normalize_phone(phone: str) -> str:
    """Normalize phone number for comparison"""
    if not phone:
        return ""
    # Remove all non-digit characters
    digits = ''.join(c for c in phone if c.isdigit())
    # Take last 10 digits (US format)
    return digits[-10:] if len(digits) >= 10 else digits

def normalize_email(email: str) -> str:
    """Normalize email for comparison"""
    if not email:
        return ""
    return email.lower().strip()

def normalize_name(name: str) -> str:
    """Normalize name for comparison"""
    if not name:
        return ""
    return ' '.join(name.lower().strip().split())

def string_similarity(str1: str, str2: str) -> float:
    """Calculate similarity between two strings (0-1)"""
    if not str1 or not str2:
        return 0.0
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def find_duplicate_leads(match_fields: List[str] = None, similarity_threshold: float = 0.85) -> Dict:
    """Find duplicate leads based on specified fields"""
    if not match_fields:
        match_fields = ['Email']  # Default to email matching
    
    sf = get_connection()
    if not sf:
        return {"success": False, "error": "Not connected to Salesforce"}
    
    try:
        # Query all leads with relevant fields
        fields = ['Id', 'Name', 'Email', 'Phone', 'Company', 'Status', 'CreatedDate']
        query = f"SELECT {', '.join(fields)} FROM Lead ORDER BY CreatedDate DESC"
        result = sf.query_all(query)
        leads = result.get('records', [])
        
        duplicates = defaultdict(list)
        
        # Email-based matching
        if 'Email' in match_fields:
            email_map = defaultdict(list)
            for lead in leads:
                email = normalize_email(lead.get('Email', ''))
                if email:
                    email_map[email].append(lead)
            
            for email, lead_list in email_map.items():
                if len(lead_list) > 1:
                    duplicates[f"email:{email}"] = lead_list
        
        # Phone-based matching
        if 'Phone' in match_fields:
            phone_map = defaultdict(list)
            for lead in leads:
                phone = normalize_phone(lead.get('Phone', ''))
                if phone:
                    phone_map[phone].append(lead)
            
            for phone, lead_list in phone_map.items():
                if len(lead_list) > 1:
                    key = f"phone:{phone}"
                    if key not in duplicates:
                        duplicates[key] = lead_list
        
        # Name + Company matching (fuzzy)
        if 'Name' in match_fields and 'Company' in match_fields:
            for i, lead1 in enumerate(leads):
                name1 = normalize_name(lead1.get('Name', ''))
                company1 = normalize_name(lead1.get('Company', ''))
                
                if not name1 or not company1:
                    continue
                
                for lead2 in leads[i+1:]:
                    name2 = normalize_name(lead2.get('Name', ''))
                    company2 = normalize_name(lead2.get('Company', ''))
                    
                    if not name2 or not company2:
                        continue
                    
                    name_sim = string_similarity(name1, name2)
                    company_sim = string_similarity(company1, company2)
                    
                    if name_sim >= similarity_threshold and company_sim >= similarity_threshold:
                        key = f"name_company:{name1}_{company1}"
                        if key not in duplicates:
                            duplicates[key] = [lead1]
                        if lead2 not in duplicates[key]:
                            duplicates[key].append(lead2)
        
        # Format results
        duplicate_groups = []
        for key, lead_list in duplicates.items():
            group = {
                "match_key": key,
                "count": len(lead_list),
                "leads": [
                    {
                        "Id": l.get('Id'),
                        "Name": l.get('Name'),
                        "Email": l.get('Email'),
                        "Phone": l.get('Phone'),
                        "Company": l.get('Company'),
                        "Status": l.get('Status'),
                        "CreatedDate": l.get('CreatedDate')
                    }
                    for l in lead_list
                ]
            }
            duplicate_groups.append(group)
        
        total_duplicates = sum(g['count'] for g in duplicate_groups)
        
        return {
            "success": True,
            "total_leads": len(leads),
            "duplicate_groups": len(duplicate_groups),
            "total_duplicates": total_duplicates,
            "groups": duplicate_groups
        }
    
    except Exception as e:
        return {"success": False, "error": str(e)}

def find_duplicate_contacts(match_fields: List[str] = None, similarity_threshold: float = 0.85) -> Dict:
    """Find duplicate contacts based on specified fields"""
    if not match_fields:
        match_fields = ['Email']
    
    sf = get_connection()
    if not sf:
        return {"success": False, "error": "Not connected to Salesforce"}
    
    try:
        fields = ['Id', 'Name', 'Email', 'Phone', 'AccountId', 'Account.Name', 'Title', 'CreatedDate']
        query = f"SELECT {', '.join(fields)} FROM Contact ORDER BY CreatedDate DESC"
        result = sf.query_all(query)
        contacts = result.get('records', [])
        
        duplicates = defaultdict(list)
        
        # Email-based matching
        if 'Email' in match_fields:
            email_map = defaultdict(list)
            for contact in contacts:
                email = normalize_email(contact.get('Email', ''))
                if email:
                    email_map[email].append(contact)
            
            for email, contact_list in email_map.items():
                if len(contact_list) > 1:
                    duplicates[f"email:{email}"] = contact_list
        
        # Phone-based matching
        if 'Phone' in match_fields:
            phone_map = defaultdict(list)
            for contact in contacts:
                phone = normalize_phone(contact.get('Phone', ''))
                if phone:
                    phone_map[phone].append(contact)
            
            for phone, contact_list in phone_map.items():
                if len(contact_list) > 1:
                    key = f"phone:{phone}"
                    if key not in duplicates:
                        duplicates[key] = contact_list
        
        # Format results
        duplicate_groups = []
        for key, contact_list in duplicates.items():
            group = {
                "match_key": key,
                "count": len(contact_list),
                "contacts": [
                    {
                        "Id": c.get('Id'),
                        "Name": c.get('Name'),
                        "Email": c.get('Email'),
                        "Phone": c.get('Phone'),
                        "Account": c.get('Account', {}).get('Name') if c.get('Account') else None,
                        "Title": c.get('Title'),
                        "CreatedDate": c.get('CreatedDate')
                    }
                    for c in contact_list
                ]
            }
            duplicate_groups.append(group)
        
        total_duplicates = sum(g['count'] for g in duplicate_groups)
        
        return {
            "success": True,
            "total_contacts": len(contacts),
            "duplicate_groups": len(duplicate_groups),
            "total_duplicates": total_duplicates,
            "groups": duplicate_groups
        }
    
    except Exception as e:
        return {"success": False, "error": str(e)}

def find_duplicate_accounts(match_fields: List[str] = None, similarity_threshold: float = 0.85) -> Dict:
    """Find duplicate accounts based on specified fields"""
    if not match_fields:
        match_fields = ['Name']
    
    sf = get_connection()
    if not sf:
        return {"success": False, "error": "Not connected to Salesforce"}
    
    try:
        fields = ['Id', 'Name', 'Website', 'Phone', 'BillingCity', 'BillingState', 'Industry', 'CreatedDate']
        query = f"SELECT {', '.join(fields)} FROM Account ORDER BY CreatedDate DESC"
        result = sf.query_all(query)
        accounts = result.get('records', [])
        
        duplicates = defaultdict(list)
        
        # Name-based matching (exact)
        if 'Name' in match_fields:
            name_map = defaultdict(list)
            for account in accounts:
                name = normalize_name(account.get('Name', ''))
                if name:
                    name_map[name].append(account)
            
            for name, account_list in name_map.items():
                if len(account_list) > 1:
                    duplicates[f"name:{name}"] = account_list
        
        # Website-based matching
        if 'Website' in match_fields:
            website_map = defaultdict(list)
            for account in accounts:
                website = account.get('Website', '').lower().strip()
                if website:
                    # Normalize website (remove http/https, www)
                    website = website.replace('http://', '').replace('https://', '').replace('www.', '')
                    website_map[website].append(account)
            
            for website, account_list in website_map.items():
                if len(account_list) > 1:
                    key = f"website:{website}"
                    if key not in duplicates:
                        duplicates[key] = account_list
        
        # Format results
        duplicate_groups = []
        for key, account_list in duplicates.items():
            group = {
                "match_key": key,
                "count": len(account_list),
                "accounts": [
                    {
                        "Id": a.get('Id'),
                        "Name": a.get('Name'),
                        "Website": a.get('Website'),
                        "Phone": a.get('Phone'),
                        "City": a.get('BillingCity'),
                        "State": a.get('BillingState'),
                        "Industry": a.get('Industry'),
                        "CreatedDate": a.get('CreatedDate')
                    }
                    for a in account_list
                ]
            }
            duplicate_groups.append(group)
        
        total_duplicates = sum(g['count'] for g in duplicate_groups)
        
        return {
            "success": True,
            "total_accounts": len(accounts),
            "duplicate_groups": len(duplicate_groups),
            "total_duplicates": total_duplicates,
            "groups": duplicate_groups
        }
    
    except Exception as e:
        return {"success": False, "error": str(e)}

def check_duplicate_before_create(object_type: str, data: Dict) -> Dict:
    """Check if a record would be a duplicate before creating it"""
    sf = get_connection()
    if not sf:
        return {"success": False, "error": "Not connected to Salesforce"}
    
    try:
        conditions = []
        
        # Check email
        if 'Email' in data and data['Email']:
            email = normalize_email(data['Email'])
            conditions.append(f"Email = '{email}'")
        
        # Check phone
        if 'Phone' in data and data['Phone']:
            phone = data['Phone']
            conditions.append(f"Phone = '{phone}'")
        
        # Check name + company (for Leads)
        if object_type == 'Lead' and 'Name' in data and 'Company' in data:
            name = data['Name']
            company = data['Company']
            conditions.append(f"(Name = '{name}' AND Company = '{company}')")
        
        if not conditions:
            return {"success": True, "is_duplicate": False, "message": "No duplicate check criteria provided"}
        
        # Build query
        where_clause = ' OR '.join(conditions)
        query = f"SELECT Id, Name, Email, Phone FROM {object_type} WHERE {where_clause} LIMIT 10"
        
        result = sf.query(query)
        existing = result.get('records', [])
        
        if existing:
            return {
                "success": True,
                "is_duplicate": True,
                "duplicate_count": len(existing),
                "existing_records": [
                    {
                        "Id": r.get('Id'),
                        "Name": r.get('Name'),
                        "Email": r.get('Email'),
                        "Phone": r.get('Phone')
                    }
                    for r in existing
                ]
            }
        else:
            return {
                "success": True,
                "is_duplicate": False,
                "message": "No duplicates found"
            }
    
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    """CLI interface for duplicate detection"""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python duplicates.py <command> [args]"}))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "leads":
        match_fields = sys.argv[2].split(',') if len(sys.argv) > 2 else ['Email']
        threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 0.85
        result = find_duplicate_leads(match_fields, threshold)
        print(json.dumps(result, default=str))
    
    elif command == "contacts":
        match_fields = sys.argv[2].split(',') if len(sys.argv) > 2 else ['Email']
        threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 0.85
        result = find_duplicate_contacts(match_fields, threshold)
        print(json.dumps(result, default=str))
    
    elif command == "accounts":
        match_fields = sys.argv[2].split(',') if len(sys.argv) > 2 else ['Name']
        threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 0.85
        result = find_duplicate_accounts(match_fields, threshold)
        print(json.dumps(result, default=str))
    
    elif command == "check":
        if len(sys.argv) < 4:
            print(json.dumps({"error": "Usage: python duplicates.py check <ObjectType> '<JSON data>'"}))
            sys.exit(1)
        object_type = sys.argv[2]
        data = json.loads(sys.argv[3])
        result = check_duplicate_before_create(object_type, data)
        print(json.dumps(result, default=str))
    
    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))

if __name__ == "__main__":
    main()
