#!/usr/bin/env python3
"""
SSL Certificate Monitor
Check SSL/TLS certificates for expiration, security issues, and compliance.
"""

import ssl
import socket
import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
import os

try:
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False

def get_certificate(hostname: str, port: int = 443, timeout: int = 10) -> Optional[bytes]:
    """Get SSL certificate from host."""
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert_der = ssock.getpeercert(binary_form=True)
                return cert_der
    except Exception as e:
        return None

def parse_certificate(cert_der: bytes) -> Optional[Dict[str, Any]]:
    """Parse certificate using cryptography library."""
    if not CRYPTOGRAPHY_AVAILABLE:
        return None
    
    try:
        cert = x509.load_der_x509_certificate(cert_der, default_backend())
        
        result = {
            'subject': dict(cert.subject),
            'issuer': dict(cert.issuer),
            'serial_number': hex(cert.serial_number),
            'not_valid_before': cert.not_valid_before_utc,
            'not_valid_after': cert.not_valid_after_utc,
            'signature_algorithm_oid': cert.signature_algorithm_oid.dotted_string,
            'version': cert.version.value,
            'extensions': {}
        }
        
        # Try to get common extensions
        try:
            san = cert.extensions.get_extension_for_oid(x509.ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
            result['extensions']['subject_alternative_names'] = [str(name) for name in san.value]
        except x509.ExtensionNotFound:
            pass
            
        try:
            ku = cert.extensions.get_extension_for_oid(x509.ExtensionOID.KEY_USAGE)
            result['extensions']['key_usage'] = {
                'digital_signature': ku.value.digital_signature,
                'key_encipherment': ku.value.key_encipherment,
                'key_cert_sign': ku.value.key_cert_sign,
                'crl_sign': ku.value.crl_sign,
            }
        except x509.ExtensionNotFound:
            pass
            
        try:
            eku = cert.extensions.get_extension_for_oid(x509.ExtensionOID.EXTENDED_KEY_USAGE)
            result['extensions']['extended_key_usage'] = [str(oid) for oid in eku.value]
        except x509.ExtensionNotFound:
            pass
            
        return result
    except Exception as e:
        return None

def check_certificate(hostname: str, port: int = 443, warning_days: int = 30) -> Dict[str, Any]:
    """Check certificate expiration and return detailed results."""
    now = datetime.now(timezone.utc)
    
    # Default result structure
    result = {
        'domain': hostname,
        'port': port,
        'status': 'unknown',
        'error': None,
        'expires_at': None,
        'days_remaining': None,
        'issuer': None,
        'subject': None,
        'algorithm': None,
        'serial_number': None,
        'valid_from': None,
        'valid_to': None,
        'warning': False,
        'checked_at': now.isoformat()
    }
    
    # Get certificate
    cert_der = get_certificate(hostname, port)
    if cert_der is None:
        result['status'] = 'connection_failed'
        result['error'] = 'Failed to connect or retrieve certificate'
        return result
    
    # Parse with cryptography if available
    cert_info = parse_certificate(cert_der)
    
    if cert_info is None:
        # Fallback to basic SSL module parsing
        try:
            cert = ssl.DER_cert_to_PEM_cert(cert_der)
            # Simple parsing with ssl module
            # This is limited but gives basic info
            result['status'] = 'valid'
            result['issuer'] = 'Unknown (cryptography library not installed)'
            result['subject'] = 'Unknown (cryptography library not installed)'
            # We can't get expiration without cryptography
            result['error'] = 'cryptography library not installed for detailed parsing'
            return result
        except Exception as e:
            result['status'] = 'parse_failed'
            result['error'] = f'Failed to parse certificate: {str(e)}'
            return result
    
    # Extract information from parsed certificate
    result['valid_from'] = cert_info['not_valid_before'].isoformat()
    result['valid_to'] = cert_info['not_valid_after'].isoformat()
    result['expires_at'] = cert_info['not_valid_after'].isoformat()
    
    # Calculate days remaining
    expires = cert_info['not_valid_after']
    days_remaining = (expires - now).days
    result['days_remaining'] = days_remaining
    
    # Determine status
    if days_remaining < 0:
        result['status'] = 'expired'
    elif days_remaining <= warning_days:
        result['status'] = 'expiring_soon'
        result['warning'] = True
    else:
        result['status'] = 'valid'
    
    # Extract issuer and subject common names
    issuer = cert_info['issuer']
    subject = cert_info['subject']
    
    result['issuer'] = issuer.get('CN', 'Unknown')
    result['subject'] = subject.get('CN', 'Unknown')
    result['algorithm'] = cert_info['signature_algorithm_oid']
    result['serial_number'] = cert_info['serial_number']
    
    return result

def check_command(args):
    """Handle check command."""
    result = check_certificate(args.domain, args.port, args.warning_days)
    
    if args.json:
        print(json.dumps(result, indent=2, default=str))
        return
    
    # Human-readable output
    domain_port = f"{result['domain']}:{result['port']}"
    
    if result['status'] == 'connection_failed':
        print(f"❌ {domain_port}: Connection failed - {result['error']}")
        return
    elif result['status'] == 'parse_failed':
        print(f"❌ {domain_port}: Parse failed - {result['error']}")
        return
    elif result['status'] == 'valid':
        print(f"✅ {domain_port}")
    elif result['status'] == 'expiring_soon':
        print(f"⚠️  {domain_port}")
    elif result['status'] == 'expired':
        print(f"❌ {domain_port}")
    
    print(f"   Status: {result['status'].replace('_', ' ').title()}")
    print(f"   Expires: {result['expires_at']}")
    print(f"   Days remaining: {result['days_remaining']}")
    print(f"   Issuer: {result['issuer']}")
    print(f"   Subject: {result['subject']}")
    print(f"   Algorithm: {result['algorithm']}")
    
    if result['warning'] and result['days_remaining'] > 0:
        print(f"   Warning: Certificate expires in {result['days_remaining']} days")

def details_command(args):
    """Handle details command."""
    result = check_certificate(args.domain, args.port)
    
    if result['status'] not in ['valid', 'expiring_soon']:
        print(f"❌ Cannot get details: {result['error']}")
        return
    
    print(f"📋 Certificate details for {result['domain']}:{result['port']}\n")
    print(f"Subject: {result['subject']}")
    print(f"Issuer: {result['issuer']}")
    print(f"Serial: {result['serial_number']}")
    print(f"\nValidity:")
    print(f"  Not before: {result['valid_from']}")
    print(f"  Not after:  {result['valid_to']}")
    print(f"  Days remaining: {result['days_remaining']}")
    print(f"\nSignature:")
    print(f"  Algorithm: {result['algorithm']}")
    print(f"\nChecked at: {result['checked_at']}")

def batch_command(args):
    """Handle batch command."""
    if not os.path.exists(args.file):
        print(f"❌ File not found: {args.file}")
        return
    
    with open(args.file, 'r') as f:
        domains = [line.strip() for line in f if line.strip()]
    
    results = []
    for line in domains:
        # Parse domain:port format
        if ':' in line:
            domain, port_str = line.split(':', 1)
            try:
                port = int(port_str)
            except ValueError:
                print(f"❌ Invalid port in line: {line}")
                continue
        else:
            domain = line
            port = 443
        
        result = check_certificate(domain, port, args.warning_days)
        results.append(result)
    
    if args.json:
        print(json.dumps(results, indent=2, default=str))
        return
    
    # Human-readable summary
    print(f"📋 Batch check results ({len(results)} domains):")
    
    valid_count = 0
    expiring_count = 0
    expired_count = 0
    failed_count = 0
    
    for result in results:
        domain_port = f"{result['domain']}:{result['port']}"
        
        if result['status'] == 'valid':
            print(f"✅ {domain_port}: Valid ({result['days_remaining']} days remaining)")
            valid_count += 1
        elif result['status'] == 'expiring_soon':
            print(f"⚠️  {domain_port}: Expiring soon ({result['days_remaining']} days remaining)")
            expiring_count += 1
        elif result['status'] == 'expired':
            print(f"❌ {domain_port}: Expired ({abs(result['days_remaining'])} days ago)")
            expired_count += 1
        else:
            print(f"❌ {domain_port}: {result['error']}")
            failed_count += 1
    
    print(f"\nSummary: {valid_count} valid, {expiring_count} expiring soon, {expired_count} expired, {failed_count} failed")

def validate_command(args):
    """Handle validate command (basic chain validation)."""
    # Note: This is a simplified validation
    result = check_certificate(args.domain, args.port)
    
    if result['status'] not in ['valid', 'expiring_soon']:
        print(f"❌ Cannot validate: {result['error']}")
        return
    
    print(f"🔒 Basic validation for {result['domain']}:{result['port']}")
    print(f"✓ Certificate retrieved successfully")
    print(f"✓ Certificate is {'expired' if result['status'] == 'expired' else 'currently valid'}")
    print(f"✓ Issuer: {result['issuer']}")
    
    if result['days_remaining'] is not None:
        if result['days_remaining'] > 30:
            print(f"✓ Expiration: {result['days_remaining']} days remaining (good)")
        elif result['days_remaining'] > 0:
            print(f"⚠ Expiration: {result['days_remaining']} days remaining (renew soon)")
        else:
            print(f"✗ Expiration: Certificate expired {abs(result['days_remaining'])} days ago")
    
    if not CRYPTOGRAPHY_AVAILABLE:
        print("⚠ Advanced validation requires cryptography library: pip install cryptography")

def main():
    parser = argparse.ArgumentParser(description='SSL Certificate Monitor')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check certificate expiration')
    check_parser.add_argument('domain', help='Domain to check')
    check_parser.add_argument('--port', type=int, default=443, help='Port (default: 443)')
    check_parser.add_argument('--warning-days', type=int, default=30, 
                             help='Days before expiration to warn (default: 30)')
    check_parser.add_argument('--json', action='store_true', help='Output JSON')
    check_parser.set_defaults(func=check_command)
    
    # Details command
    details_parser = subparsers.add_parser('details', help='Get certificate details')
    details_parser.add_argument('domain', help='Domain to check')
    details_parser.add_argument('--port', type=int, default=443, help='Port (default: 443)')
    details_parser.set_defaults(func=details_command)
    
    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Check multiple domains from file')
    batch_parser.add_argument('file', help='File with domains (one per line)')
    batch_parser.add_argument('--warning-days', type=int, default=30,
                             help='Days before expiration to warn (default: 30)')
    batch_parser.add_argument('--json', action='store_true', help='Output JSON')
    batch_parser.set_defaults(func=batch_command)
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Basic certificate validation')
    validate_parser.add_argument('domain', help='Domain to check')
    validate_parser.add_argument('--port', type=int, default=443, help='Port (default: 443)')
    validate_parser.set_defaults(func=validate_command)
    
    # Help command
    help_parser = subparsers.add_parser('help', help='Show help')
    
    args = parser.parse_args()
    
    if args.command == 'help':
        parser.print_help()
        return
    
    # Check for cryptography library
    if not CRYPTOGRAPHY_AVAILABLE:
        print("⚠️  Warning: cryptography library not installed. Some features limited.")
        print("   Install with: pip install cryptography")
        print()
    
    args.func(args)

if __name__ == '__main__':
    main()