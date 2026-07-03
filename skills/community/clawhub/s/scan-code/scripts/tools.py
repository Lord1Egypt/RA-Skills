from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def scanCode(
    code: str,
    language: str,
    securityLevel: str
) -> Dict[str, Any]:
    """
    Scan code for security vulnerabilities, secrets, and compliance issues
    
    Args:
        code: null
        language: null
        securityLevel: null
    
    Returns:
        
    """
    arguments = {
        "code": code,
        "language": language,
        "securityLevel": securityLevel
    }
    
    return call_api("1777316659447811", "scanCode", arguments)

def scanVulnerabilities(
    code: str,
    language: str
) -> Dict[str, Any]:
    """
    Quick scan for code vulnerabilities only
    
    Args:
        code: null
        language: null
    
    Returns:
        
    """
    arguments = {
        "code": code,
        "language": language
    }
    
    return call_api("1777316659447811", "scanVulnerabilities", arguments)

def detectSecrets(
    code: str
) -> Dict[str, Any]:
    """
    Detect exposed secrets, API keys, and credentials
    
    Args:
        code: null
    
    Returns:
        
    """
    arguments = {
        "code": code
    }
    
    return call_api("1777316659447811", "detectSecrets", arguments)

def suggestSecureFix(
    vulnerability: null,
    context: str
) -> Dict[str, Any]:
    """
    Generate secure code fixes for vulnerabilities
    
    Args:
        vulnerability: null
        context: null
    
    Returns:
        
    """
    arguments = {
        "vulnerability": vulnerability,
        "context": context
    }
    
    return call_api("1777316659447811", "suggestSecureFix", arguments)

def checkCompliance(
    code: str,
    securityLevel: str,
    standards: null
) -> Dict[str, Any]:
    """
    Check code for regulatory compliance (GDPR, HIPAA, SOC2, PCI DSS)
    
    Args:
        code: null
        securityLevel: null
        standards: null
    
    Returns:
        
    """
    arguments = {
        "code": code,
        "securityLevel": securityLevel,
        "standards": standards
    }
    
    return call_api("1777316659447811", "checkCompliance", arguments)

