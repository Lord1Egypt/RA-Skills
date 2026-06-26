#!/usr/bin/env python3
"""
OAuth 授权工具 - 支持 Gmail 和 Outlook
"""

import sys
import json
import argparse
from pathlib import Path
from oauth_handler import authorize_gmail, authorize_outlook

def main():
    parser = argparse.ArgumentParser(description='📧 OAuth 授权工具')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # Gmail 授权
    gmail_parser = subparsers.add_parser('gmail', help='授权 Gmail')
    gmail_parser.add_argument('--client-id', required=True, help='Gmail Client ID')
    gmail_parser.add_argument('--client-secret', required=True, help='Gmail Client Secret')
    gmail_parser.add_argument('--name', default='gmail', help='账户名称')
    
    # Outlook 授权
    outlook_parser = subparsers.add_parser('outlook', help='授权 Outlook')
    outlook_parser.add_argument('--client-id', required=True, help='Azure Client ID')
    outlook_parser.add_argument('--client-secret', required=True, help='Azure Client Secret')
    outlook_parser.add_argument('--tenant-id', required=True, help='Azure Tenant ID')
    outlook_parser.add_argument('--name', default='outlook', help='账户名称')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'gmail':
        authorize_gmail(args.client_id, args.client_secret, args.name)
    
    elif args.command == 'outlook':
        authorize_outlook(args.client_id, args.client_secret, args.tenant_id, args.name)

if __name__ == '__main__':
    main()
