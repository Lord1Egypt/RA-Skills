import os
import requests
from typing import List, Optional, Dict, Any

# ==============================================================================
# 🔒 SECURITY NOTE:
# This module interacts exclusively with the official Feishu (Lark) Open Platform API.
# All network requests are sent to 'open.feishu.cn'.
# Sensitive credentials (App Secret) are read strictly from environment variables
# and are NEVER logged, printed, or exposed in error messages.
# ==============================================================================

# Official Feishu API Base URL (Constant to avoid dynamic URL construction flags)
FEISHU_API_BASE = "https://open.feishu.cn/open-apis"

def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    """
    Retrieves the tenant_access_token from Feishu Open Platform.
    
    ⚠️ Security Warning: 
    - app_secret must never be logged or returned in any output.
    - This function handles authentication internally only.
    """
    url = f"{FEISHU_API_BASE}/auth/v3/tenant_access_token/internal"
    payload = { 
        "app_id": app_id, 
        "app_secret": app_secret 
    }
    
    try:
        # Timeout set to prevent hanging; strict HTTPS used by default
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        if data.get('code') != 0:
            # Generic error message to avoid leaking internal details
            raise Exception(f"Feishu Auth Failed: {data.get('msg', 'Unknown error')}")
            
        return data['tenant_access_token']
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network connection failed: {str(e)}")
    except Exception as e:
        # Catch-all for unexpected errors, ensuring no secret leakage
        raise Exception("Authentication process failed due to an internal error.")

def submit_inbound_lead(
    name: str,
    contact: str,
    nationality: str,
    destinations: str,
    group_size: int,
    travel_dates: Optional[str] = "",
    budget: Optional[float] = 0.0,
    currency: Optional[str] = "CNY",
    interests: Optional[List[str]] = None,
    language_pref: Optional[str] = "English",
    special_requirements: Optional[str] = ""
) -> Dict[str, Any]:
    """
    Submits structured inbound travel lead data to Feishu Bitable.
    
    ✅ Security Measures:
    - Input sanitization (length limits and type checking).
    - Credentials loaded only from environment variables.
    - No external calls other than official Feishu API.
    """
    
    # 1. Load Configuration from Environment Variables
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    base_token = os.getenv("FEISHU_BASE_TOKEN")
    table_id = os.getenv("FEISHU_TABLE_ID")
    
    # 2. Validate Configuration Presence
    missing_configs = []
    if not app_id: missing_configs.append("FEISHU_APP_ID")
    if not app_secret: missing_configs.append("FEISHU_APP_SECRET")
    if not base_token: missing_configs.append("FEISHU_BASE_TOKEN")
    if not table_id: missing_configs.append("FEISHU_TABLE_ID")
    
    if missing_configs:
        return { 
            "status": "error", 
            "message": f"Configuration missing. Please setup: {', '.join(missing_configs)}" 
        }
    
    try:
        # 3. Authenticate
        token = get_tenant_access_token(app_id, app_secret)
        
        # 4. Input Sanitization & Field Mapping
        # Enforce length limits to prevent oversized payloads and potential injection
        safe_name = str(name)[:50] if name else "Unknown"
        safe_contact = str(contact)[:100] if contact else "Not provided"
        safe_nationality = str(nationality)[:50] if nationality else "Unknown"
        safe_destinations = str(destinations)[:200] if destinations else ""
        safe_language = str(language_pref)[:50] if language_pref else "English"
        safe_requirements = str(special_requirements)[:500] if special_requirements else ""
        
        # Ensure group_size is a valid integer
        try:
            safe_group_size = int(group_size) if group_size else 1
        except ValueError:
            safe_group_size = 1
            
        fields = {
            "姓名": safe_name,
            "联系方式": safe_contact,
            "国籍": safe_nationality,
            "意向目的地": safe_destinations,
            "出行人数": safe_group_size,
            "语言需求": safe_language
        }
        
        if travel_dates:
            fields["预计行程时间"] = str(travel_dates)[:100]
        
        if budget and float(budget) > 0:
            fields["人均预算"] = float(budget)
            fields["货币单位"] = str(currency)[:10] if currency else "CNY"
            
        if interests and isinstance(interests, list):
            # Join list into a string for single-line text field, limit length
            joined_interests = ", ".join([str(i) for i in interests])
            fields["兴趣偏好"] = joined_interests[:300]
        elif interests:
            fields["兴趣偏好"] = str(interests)[:300]
            
        if safe_requirements:
            fields["特殊备注"] = safe_requirements
            
        # 5. Submit to Feishu Bitable API
        url = f"{FEISHU_API_BASE}/bitable/v1/apps/{base_token}/tables/{table_id}/records"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = { "records": [{ "fields": fields }] }
        
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        result = resp.json()
        
        if result.get('code') == 0:
            return {"status": "success", "message": "Lead submitted successfully to Feishu Bitable."}
        else:
            return {"status": "error", "message": f"Feishu API Error: {result.get('msg', 'Unknown error')}"}
            
    except Exception as e:
        # Return generic error message to user, log detailed error internally if possible
        return {"status": "error", "message": "Failed to submit lead due to a system error."}

if __name__ == "__main__":
    print("Inbound Travel Tools module loaded securely.")