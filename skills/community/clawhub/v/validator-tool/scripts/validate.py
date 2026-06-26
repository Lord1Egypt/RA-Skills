#!/usr/bin/env python3
"""Validator Tool - Validate data formats."""

import re
import sys
import json
import ipaddress
from typing import Optional, Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """Validate email address."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, "Valid email address"
    return False, "Invalid email address"


def validate_phone(phone: str) -> Tuple[bool, str]:
    """Validate phone number."""
    # Remove common separators
    cleaned = re.sub(r'[\s\-\.\(\)]', '', phone)
    
    # Check if it starts with + and has digits
    if cleaned.startswith('+'):
        if cleaned[1:].isdigit() and len(cleaned) >= 10:
            return True, "Valid international phone number"
    elif cleaned.isdigit():
        if len(cleaned) >= 7:
            return True, "Valid phone number"
    
    return False, "Invalid phone number"


def validate_url(url: str) -> Tuple[bool, str]:
    """Validate URL."""
    pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
    if re.match(pattern, url):
        return True, "Valid URL"
    return False, "Invalid URL"


def validate_ip(ip: str) -> Tuple[bool, str]:
    """Validate IP address (IPv4/IPv6)."""
    try:
        ipaddress.ip_address(ip)
        return True, f"Valid {type(ipaddress.ip_address(ip)).__name__} address"
    except ValueError:
        return False, "Invalid IP address"


def validate_credit_card(card: str) -> Tuple[bool, str]:
    """Validate credit card using Luhn algorithm."""
    # Remove spaces and dashes
    cleaned = re.sub(r'[\s\-]', '', card)
    
    if not cleaned.isdigit():
        return False, "Credit card must contain only digits"
    
    if len(cleaned) < 13 or len(cleaned) > 19:
        return False, "Credit card number length invalid"
    
    # Luhn algorithm
    def luhn_checksum(card_num):
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(card_num)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10
    
    if luhn_checksum(cleaned) == 0:
        # Identify card type
        card_type = "Unknown"
        if cleaned.startswith('4'):
            card_type = "Visa"
        elif cleaned.startswith(('51', '52', '53', '54', '55')):
            card_type = "Mastercard"
        elif cleaned.startswith(('34', '37')):
            card_type = "American Express"
        elif cleaned.startswith('6011') or cleaned.startswith('65'):
            card_type = "Discover"
        return True, f"Valid credit card ({card_type})"
    
    return False, "Invalid credit card number (failed Luhn check)"


def validate_json(data: str) -> Tuple[bool, str]:
    """Validate JSON syntax."""
    try:
        json.loads(data)
        return True, "Valid JSON"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}"


def validate_uuid(uuid: str) -> Tuple[bool, str]:
    """Validate UUID format."""
    pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    if re.match(pattern, uuid.lower()):
        return True, "Valid UUID"
    return False, "Invalid UUID"


def validate_hex(hex_str: str) -> Tuple[bool, str]:
    """Validate hexadecimal string."""
    pattern = r'^[0-9a-fA-F]+$'
    if re.match(pattern, hex_str):
        return True, f"Valid hexadecimal ({len(hex_str)//2} bytes)"
    return False, "Invalid hexadecimal string"


def validate_date(date_str: str, format: str = "%Y-%m-%d") -> Tuple[bool, str]:
    """Validate date string."""
    from datetime import datetime
    try:
        datetime.strptime(date_str, format)
        return True, f"Valid date ({format})"
    except ValueError:
        return False, f"Invalid date (expected format: {format})"


def validate_all(value: str) -> None:
    """Try all validators."""
    validators = [
        ("Email", validate_email),
        ("Phone", validate_phone),
        ("URL", validate_url),
        ("IP", validate_ip),
        ("Credit Card", validate_credit_card),
        ("JSON", validate_json),
        ("UUID", validate_uuid),
        ("Hex", validate_hex),
    ]
    
    print(f"Testing '{value}' with all validators:")
    print("-" * 50)
    
    any_valid = False
    for name, validator in validators:
        try:
            valid, msg = validator(value)
            status = "✓" if valid else "✗"
            print(f"{status} {name}: {msg}")
            if valid:
                any_valid = True
        except Exception as e:
            print(f"? {name}: Error - {e}")
    
    print("-" * 50)
    if any_valid:
        print("At least one validation passed")
    else:
        print("No validation passed")


def main():
    if len(sys.argv) < 2:
        print("Validator Tool")
        print("=" * 50)
        print("Usage: validate.py <type> <value>")
        print("\nTypes: email, phone, url, ip, credit-card, json, uuid, hex, all")
        print("\nExamples:")
        print("  validate.py email user@example.com")
        print("  validate.py phone +1-555-123-4567")
        print("  validate.py url https://example.com")
        print("  validate.py ip 192.168.1.1")
        print("  validate.py credit-card 4532015112830366")
        print("  validate.py json '{\"key\": \"value\"}'")
        print("  validate.py all test@example.com")
        sys.exit(1)
    
    if len(sys.argv) < 3:
        print("Error: Missing value to validate")
        sys.exit(1)
    
    validator_type = sys.argv[1].lower()
    value = sys.argv[2]
    
    # Handle JSON with spaces (from shell)
    if validator_type == "json" and len(sys.argv) > 3:
        value = " ".join(sys.argv[2:])
    
    validators = {
        "email": validate_email,
        "phone": validate_phone,
        "url": validate_url,
        "ip": validate_ip,
        "credit-card": validate_credit_card,
        "creditcard": validate_credit_card,
        "json": validate_json,
        "uuid": validate_uuid,
        "hex": validate_hex,
        "date": validate_date,
        "all": None,
    }
    
    if validator_type not in validators:
        print(f"Unknown validator: {validator_type}")
        print(f"Available: {', '.join(validators.keys())}")
        sys.exit(1)
    
    if validator_type == "all":
        validate_all(value)
    else:
        validator = validators[validator_type]
        valid, msg = validator(value)
        
        status = "✓" if valid else "✗"
        print(f"{status} {msg}")
        
        sys.exit(0 if valid else 1)


if __name__ == '__main__':
    main()
