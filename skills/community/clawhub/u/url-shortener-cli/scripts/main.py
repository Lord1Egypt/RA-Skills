#!/usr/bin/env python3
"""
URL Shortener CLI - Local URL shortening tool
"""
import argparse
import json
import os
import sys
import random
import string
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


CONFIG_DIR = Path.home() / ".url-shortener"
DATA_FILE = CONFIG_DIR / "mappings.json"


def ensure_config_dir():
    """Create config directory if it doesn't exist"""
    CONFIG_DIR.mkdir(exist_ok=True)


def load_mappings() -> Dict[str, Dict[str, Any]]:
    """Load URL mappings from JSON file"""
    ensure_config_dir()
    if not DATA_FILE.exists():
        return {}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_mappings(mappings: Dict[str, Dict[str, Any]]):
    """Save URL mappings to JSON file"""
    ensure_config_dir()
    with open(DATA_FILE, 'w') as f:
        json.dump(mappings, f, indent=2)


def generate_slug(length: int = 6) -> str:
    """Generate a random slug"""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def shorten_url(url: str, slug: Optional[str] = None, description: str = "", tags: List[str] = None) -> Dict[str, Any]:
    """Create a new shortened URL"""
    mappings = load_mappings()
    
    # Generate slug if not provided
    if not slug:
        slug = generate_slug()
        # Ensure uniqueness
        while slug in mappings:
            slug = generate_slug()
    elif slug in mappings:
        raise ValueError(f"Slug '{slug}' already exists")
    
    # Validate URL (basic)
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    entry = {
        'url': url,
        'slug': slug,
        'clicks': 0,
        'created': datetime.utcnow().isoformat() + 'Z',
        'description': description,
        'tags': tags or [],
        'last_accessed': None
    }
    
    mappings[slug] = entry
    save_mappings(mappings)
    return entry


def expand_url(slug: str, increment_clicks: bool = True) -> Optional[Dict[str, Any]]:
    """Get URL for a slug, optionally increment click count"""
    mappings = load_mappings()
    if slug not in mappings:
        return None
    
    entry = mappings[slug]
    if increment_clicks:
        entry['clicks'] += 1
        entry['last_accessed'] = datetime.utcnow().isoformat() + 'Z'
        save_mappings(mappings)
    
    return entry


def delete_url(slug: str) -> bool:
    """Delete a URL mapping"""
    mappings = load_mappings()
    if slug not in mappings:
        return False
    
    del mappings[slug]
    save_mappings(mappings)
    return True


def list_urls(sort_by: str = 'created', reverse: bool = True, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """List all URL mappings"""
    mappings = load_mappings()
    entries = list(mappings.values())
    
    # Sort
    if sort_by == 'created':
        entries.sort(key=lambda x: x.get('created', ''), reverse=reverse)
    elif sort_by == 'clicks':
        entries.sort(key=lambda x: x.get('clicks', 0), reverse=reverse)
    elif sort_by == 'slug':
        entries.sort(key=lambda x: x.get('slug', ''), reverse=reverse)
    elif sort_by == 'url':
        entries.sort(key=lambda x: x.get('url', ''), reverse=reverse)
    
    # Limit
    if limit:
        entries = entries[:limit]
    
    return entries


def search_urls(query: str, field: str = 'all') -> List[Dict[str, Any]]:
    """Search for URLs"""
    mappings = load_mappings()
    results = []
    query_lower = query.lower()
    
    for entry in mappings.values():
        match = False
        
        if field in ('all', 'url'):
            if query_lower in entry.get('url', '').lower():
                match = True
        if field in ('all', 'description'):
            if query_lower in entry.get('description', '').lower():
                match = True
        if field in ('all', 'tags'):
            for tag in entry.get('tags', []):
                if query_lower in tag.lower():
                    match = True
        
        if match:
            results.append(entry)
    
    return results


def get_stats() -> Dict[str, Any]:
    """Get usage statistics"""
    mappings = load_mappings()
    entries = list(mappings.values())
    
    total_clicks = sum(e.get('clicks', 0) for e in entries)
    avg_clicks = total_clicks / len(entries) if entries else 0
    
    # Most popular
    most_popular = sorted(entries, key=lambda x: x.get('clicks', 0), reverse=True)[:5]
    
    # Recently created
    recent = sorted(entries, key=lambda x: x.get('created', ''), reverse=True)[:5]
    
    return {
        'total_urls': len(entries),
        'total_clicks': total_clicks,
        'average_clicks': round(avg_clicks, 2),
        'most_popular': [e['slug'] for e in most_popular],
        'recently_added': [e['slug'] for e in recent]
    }


def export_mappings(file_path: str):
    """Export mappings to JSON file"""
    mappings = load_mappings()
    with open(file_path, 'w') as f:
        json.dump(mappings, f, indent=2)


def import_mappings(file_path: str, overwrite: bool = False):
    """Import mappings from JSON file"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r') as f:
        imported = json.load(f)
    
    mappings = load_mappings()
    
    if overwrite:
        mappings.clear()
    
    # Merge, skipping duplicates
    for slug, entry in imported.items():
        if slug not in mappings:
            mappings[slug] = entry
        else:
            # Update existing
            mappings[slug].update(entry)
    
    save_mappings(mappings)


def cleanup_urls(older_than_days: Optional[int] = None, max_clicks: Optional[int] = None, dry_run: bool = False) -> List[str]:
    """Clean up old or unused URLs"""
    mappings = load_mappings()
    to_delete = []
    
    now = datetime.utcnow()
    
    for slug, entry in list(mappings.items()):
        delete = False
        
        # Older than X days
        if older_than_days:
            created_str = entry.get('created')
            if created_str:
                try:
                    created = datetime.fromisoformat(created_str.replace('Z', '+00:00'))
                    age_days = (now - created).days
                    if age_days > older_than_days:
                        delete = True
                except (ValueError, TypeError):
                    pass
        
        # Fewer than X clicks
        if max_clicks is not None:
            if entry.get('clicks', 0) < max_clicks:
                delete = True
        
        if delete:
            to_delete.append(slug)
    
    if not dry_run:
        for slug in to_delete:
            del mappings[slug]
        save_mappings(mappings)
    
    return to_delete


def print_table(entries: List[Dict[str, Any]]):
    """Print entries as a table"""
    if not entries:
        print("No entries found.")
        return
    
    # Determine column widths
    max_slug = max(len(e.get('slug', '')) for e in entries)
    max_url = min(50, max(len(e.get('url', '')) for e in entries))
    
    # Header
    print(f"{'Slug':<{max_slug}}  {'URL':<{max_url}}  {'Clicks':>6}  {'Created':<19}")
    print("-" * (max_slug + max_url + 30))
    
    # Rows
    for entry in entries:
        slug = entry.get('slug', '')
        url = entry.get('url', '')
        if len(url) > 50:
            url = url[:47] + "..."
        clicks = entry.get('clicks', 0)
        created = entry.get('created', '')[:19].replace('T', ' ')
        print(f"{slug:<{max_slug}}  {url:<{max_url}}  {clicks:>6}  {created:<19}")


def main():
    parser = argparse.ArgumentParser(description='URL Shortener CLI')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Shorten command
    shorten_parser = subparsers.add_parser('shorten', help='Shorten a URL')
    shorten_parser.add_argument('url', help='URL to shorten')
    shorten_parser.add_argument('--slug', help='Custom slug (optional)')
    shorten_parser.add_argument('--description', default='', help='Description (optional)')
    shorten_parser.add_argument('--tags', help='Comma-separated tags (optional)')
    
    # Expand command
    expand_parser = subparsers.add_parser('expand', help='Expand a slug to URL')
    expand_parser.add_argument('slug', help='Slug to expand')
    expand_parser.add_argument('--no-count', action='store_true', help="Don't increment click count")
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all URLs')
    list_parser.add_argument('--sort', choices=['created', 'clicks', 'slug', 'url'], default='created', help='Sort by')
    list_parser.add_argument('--reverse', action='store_true', default=True, help='Reverse sort (default: newest first)')
    list_parser.add_argument('--limit', type=int, help='Limit results')
    list_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Get detailed info for a slug')
    info_parser.add_argument('slug', help='Slug to inspect')
    info_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a slug')
    delete_parser.add_argument('slug', help='Slug to delete')
    delete_parser.add_argument('--force', action='store_true', help='Skip confirmation')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search URLs')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--field', choices=['url', 'description', 'tags', 'all'], default='all', help='Search field')
    search_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show statistics')
    stats_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export mappings')
    export_parser.add_argument('--file', default='urls-export.json', help='Output file')
    
    # Import command
    import_parser = subparsers.add_parser('import', help='Import mappings')
    import_parser.add_argument('--file', required=True, help='Input file')
    import_parser.add_argument('--overwrite', action='store_true', help='Overwrite existing mappings')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Clean up old/unused URLs')
    cleanup_parser.add_argument('--older-than-days', type=int, help='Remove entries older than N days')
    cleanup_parser.add_argument('--max-clicks', type=int, help='Remove entries with fewer than N clicks')
    cleanup_parser.add_argument('--dry-run', action='store_true', help='Show what would be removed')
    
    # Help command
    help_parser = subparsers.add_parser('help', help='Show help')
    
    args = parser.parse_args()
    
    if not args.command or args.command == 'help':
        parser.print_help()
        return
    
    try:
        if args.command == 'shorten':
            tags = args.tags.split(',') if args.tags else []
            entry = shorten_url(args.url, args.slug, args.description, tags)
            print(f"Shortened: {entry['url']}")
            print(f"Slug:      {entry['slug']}")
            print(f"Full command: ./scripts/main.py expand {entry['slug']}")
            
        elif args.command == 'expand':
            entry = expand_url(args.slug, not args.no_count)
            if not entry:
                print(f"Slug '{args.slug}' not found.")
                sys.exit(1)
            print(entry['url'])
            
        elif args.command == 'list':
            entries = list_urls(args.sort, args.reverse, args.limit)
            if args.json:
                print(json.dumps(entries, indent=2))
            else:
                print_table(entries)
                
        elif args.command == 'info':
            mappings = load_mappings()
            if args.slug not in mappings:
                print(f"Slug '{args.slug}' not found.")
                sys.exit(1)
            entry = mappings[args.slug]
            if args.json:
                print(json.dumps(entry, indent=2))
            else:
                print(f"Slug:        {entry['slug']}")
                print(f"URL:         {entry['url']}")
                print(f"Clicks:      {entry['clicks']}")
                print(f"Created:     {entry['created']}")
                print(f"Description: {entry.get('description', '')}")
                print(f"Tags:        {', '.join(entry.get('tags', []))}")
                if entry.get('last_accessed'):
                    print(f"Last access: {entry['last_accessed']}")
                    
        elif args.command == 'delete':
            if not args.force:
                confirm = input(f"Delete slug '{args.slug}'? [y/N]: ")
                if confirm.lower() != 'y':
                    print("Cancelled.")
                    return
            if delete_url(args.slug):
                print(f"Deleted '{args.slug}'.")
            else:
                print(f"Slug '{args.slug}' not found.")
                sys.exit(1)
                
        elif args.command == 'search':
            results = search_urls(args.query, args.field)
            if args.json:
                print(json.dumps(results, indent=2))
            else:
                print(f"Found {len(results)} result(s):")
                print_table(results)
                
        elif args.command == 'stats':
            stats = get_stats()
            if args.json:
                print(json.dumps(stats, indent=2))
            else:
                print(f"Total URLs:     {stats['total_urls']}")
                print(f"Total clicks:   {stats['total_clicks']}")
                print(f"Avg clicks:     {stats['average_clicks']}")
                print(f"Most popular:   {', '.join(stats['most_popular'])}")
                print(f"Recently added: {', '.join(stats['recently_added'])}")
                
        elif args.command == 'export':
            export_mappings(args.file)
            print(f"Exported to {args.file}")
            
        elif args.command == 'import':
            import_mappings(args.file, args.overwrite)
            print(f"Imported from {args.file}")
            
        elif args.command == 'cleanup':
            to_delete = cleanup_urls(args.older_than_days, args.max_clicks, args.dry_run)
            if args.dry_run:
                print(f"Would delete {len(to_delete)} entries:")
                for slug in to_delete[:10]:
                    print(f"  {slug}")
                if len(to_delete) > 10:
                    print(f"  ... and {len(to_delete) - 10} more")
            else:
                print(f"Deleted {len(to_delete)} entries.")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()