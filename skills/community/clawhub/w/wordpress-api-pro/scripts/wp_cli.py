#!/usr/bin/env python3
"""
WordPress CLI - Multi-site wrapper (v3.0.0 - Secure)

Usage:
    # Using env vars (recommended): set WP_APP_PASSWORD in your shell first.
    WP_URL="https://site.com" WP_USERNAME="wp-api-user" \\
        wp_cli.py update-post --id 123 --content "..."
    
    # Using config file (fallback):
    wp_cli.py <site-name> update-post --id 123 --content "..."
    
    # List sites:
    wp_cli.py --list-sites
    
Environment:
    WP_CONFIG - Path to sites config (default: config/sites.json)
    WP_URL - WordPress site URL (overrides config)
    WP_USERNAME - WordPress username (overrides config)
    WP_APP_PASSWORD - Application Password (overrides config)
"""

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path
from security import warn_insecure_wp_url

def load_config(config_path=None):
    """Load sites configuration (optional fallback)"""
    if config_path is None:
        script_dir = Path(__file__).parent
        config_path = script_dir.parent / 'config' / 'sites.json'
    
    config_path = Path(config_path)
    
    if not config_path.exists():
        return None  # Config is optional now
    
    with open(config_path, 'r') as f:
        return json.load(f)

def get_site_config(config, site_name):
    """Get configuration for a specific site"""
    if config is None:
        return None
    
    if site_name not in config.get('sites', {}):
        # Check if it's a group
        if site_name in config.get('groups', {}):
            return 'group', config['groups'][site_name]
        
        print(f"Error: Site '{site_name}' not found in config", file=sys.stderr)
        print(f"Available sites: {', '.join(config.get('sites', {}).keys())}", file=sys.stderr)
        print(f"Available groups: {', '.join(config.get('groups', {}).keys())}", file=sys.stderr)
        sys.exit(1)
    
    return 'site', config['sites'][site_name]

def list_sites(config):
    """List all configured sites"""
    if config is None:
        print("No config file found", file=sys.stderr)
        sys.exit(1)
    
    print("Configured sites:")
    for name, site in config.get('sites', {}).items():
        desc = site.get('description', '')
        has_pwd = '✓' if site.get('app_password') else '✗'
        print(f"  {name:20} {site['url']:40} {desc:30} [auth: {has_pwd}]")

def list_groups(config):
    """List all configured groups"""
    if config is None:
        print("No config file found", file=sys.stderr)
        sys.exit(1)
    
    print("Configured groups:")
    for name, sites in config.get('groups', {}).items():
        print(f"  {name:20} → {', '.join(sites)}")

def run_command(site_config, command, args):
    """Run a WordPress command on a site"""
    script_dir = Path(__file__).parent
    
    # Map commands to scripts
    command_map = {
        'update-post': 'update_post.py',
        'create-post': 'create_post.py',
        'get-post': 'get_post.py',
        'list-posts': 'list_posts.py'
    }
    
    if command not in command_map:
        print(f"Error: Unknown command '{command}'", file=sys.stderr)
        print(f"Available: {', '.join(command_map.keys())}", file=sys.stderr)
        sys.exit(1)
    
    script_path = script_dir / command_map[command]
    
    # Build command (NO CREDENTIALS IN ARGS!)
    cmd = ['python3', str(script_path)]
    cmd.extend(args)
    
    # Pass credentials via ENVIRONMENT VARIABLES (secure!)
    env = os.environ.copy()
    
    if site_config:
        env['WP_URL'] = site_config.get('url', env.get('WP_URL', ''))
        env['WP_USERNAME'] = site_config.get('username', env.get('WP_USERNAME', ''))
        env['WP_APP_PASSWORD'] = site_config.get('app_password', env.get('WP_APP_PASSWORD', ''))
    
    # Validate credentials exist
    if not all([env.get('WP_URL'), env.get('WP_USERNAME'), env.get('WP_APP_PASSWORD')]):
        print("Error: Missing credentials. Set WP_URL, WP_USERNAME, WP_APP_PASSWORD or use config file", file=sys.stderr)
        sys.exit(1)

    warn_insecure_wp_url(env['WP_URL'])

    # Run with modified environment
    result = subprocess.run(cmd, env=env)
    return result.returncode

def main():
    parser = argparse.ArgumentParser(description='WordPress Multi-Site CLI (Secure)')
    parser.add_argument('site', nargs='?', help='Site name or group (optional if using env vars)')
    parser.add_argument('command', nargs='?', help='Command (update-post, create-post, get-post, list-posts)')
    parser.add_argument('--list-sites', action='store_true', help='List configured sites')
    parser.add_argument('--list-groups', action='store_true', help='List configured groups')
    parser.add_argument('--config', default=os.getenv('WP_CONFIG'), help='Config file path')
    parser.add_argument('--execute-group', action='store_true', help='Required for commands that run across a configured group')
    parser.add_argument('--allow-all', action='store_true', help='Required when the target group is named all')
    
    # Parse known args, pass rest to underlying script
    args, remaining = parser.parse_known_args()
    
    # Load config (optional)
    config = load_config(args.config)
    
    # Handle list commands
    if args.list_sites:
        list_sites(config)
        return
    
    if args.list_groups:
        list_groups(config)
        return
    
    # Check if using env vars directly (no site name needed)
    if not args.site and os.getenv('WP_URL'):
        # Direct env var mode
        if not args.command:
            parser.print_help()
            sys.exit(1)
        run_command(None, args.command, remaining)
        return
    
    # Require site and command for config mode
    if not args.site or not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Get site config
    site_type, site_data = get_site_config(config, args.site)
    
    if site_type == 'group':
        # Run on all sites in group only after explicit opt-in.
        if not args.execute_group:
            print("Error: group operations require --execute-group", file=sys.stderr)
            sys.exit(1)
        if args.site == 'all' and not args.allow_all:
            print("Error: group 'all' requires --allow-all", file=sys.stderr)
            sys.exit(1)
        print(f"Running on group '{args.site}': {', '.join(site_data)}")
        for site_name in site_data:
            site_config = config['sites'][site_name]
            print(f"\n{'='*60}")
            print(f"Site: {site_name} ({site_config['url']})")
            print('='*60)
            run_command(site_config, args.command, remaining)
    else:
        # Run on single site
        run_command(site_data, args.command, remaining)

if __name__ == '__main__':
    main()
