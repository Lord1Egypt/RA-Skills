#!/usr/bin/env python3
"""
macOS Notification Reader - Skill Version
Reads macOS notification center database to collect recent notifications.

Usage:
    python3 read_notifications.py --minutes 35
    python3 read_notifications.py --hours 1
    python3 read_notifications.py --output /path/to/output.txt
"""

import os
import sys
import sqlite3
import shutil
import subprocess
import plistlib
from pathlib import Path
from datetime import datetime, timezone, timedelta
import argparse

# CoreData epoch offset (seconds from 1970 to 2001)
CORE_DATA_OFFSET = 978307200

# Get skill directory for default output
SKILL_DIR = Path(__file__).parent.resolve()
DEFAULT_OUTPUT_DIR = SKILL_DIR / "output"


def get_notification_db_path():
    """Locate macOS notification database path"""
    # macOS 15+ path
    db_path = Path.home() / 'Library' / 'Group Containers' / 'group.com.apple.usernoted' / 'db2' / 'db'
    if db_path.exists():
        return db_path
    
    # Legacy path (macOS 14 and earlier)
    try:
        conf_dir = subprocess.check_output(["getconf", "DARWIN_USER_DIR"]).decode().strip()
        db_path = Path(conf_dir) / 'com.apple.notificationcenter' / 'db2' / 'db'
        if db_path.exists():
            return db_path
    except Exception:
        pass
    return None


def parse_notification_data(data_blob):
    """Parse bplist format notification data"""
    if not data_blob:
        return {}
    try:
        if isinstance(data_blob, bytes) and data_blob.startswith(b'bplist00'):
            obj = plistlib.loads(data_blob)
            req = obj.get('req', {})
            if isinstance(req, dict):
                return {
                    'title': req.get('titl', ''),
                    'body': req.get('body', ''),
                    'category': req.get('cate', ''),
                }
    except Exception:
        pass
    return {}


def simplify_app_name(app_id):
    """Simplify app bundle ID to display name"""
    mapping = {
        'com.tencent.xinWeChat': 'WeChat',
        'com.microsoft.teams2': 'Teams',
        'com.microsoft.Outlook': 'Outlook',
        'com.apple.mail': 'Mail',
        'com.apple.mobilesms': 'iMessage',
        'com.apple.ical': 'Calendar',
        'com.apple.reminders': 'Reminders',
    }
    return mapping.get(app_id, app_id.split('.')[-1][:15] if app_id else 'Unknown')


def core_data_to_unix(core_data_ts):
    """Convert CoreData timestamp to Unix timestamp"""
    return core_data_ts + CORE_DATA_OFFSET


def main():
    parser = argparse.ArgumentParser(
        description='Read macOS notification center database'
    )
    parser.add_argument(
        '--minutes', type=int, default=35,
        help='Collect notifications from the last N minutes'
    )
    parser.add_argument(
        '--hours', type=int,
        help='Collect notifications from the last N hours (alternative to minutes)'
    )
    parser.add_argument(
        '--output', type=str,
        help='Output file path (default: ./output/notifications_<timestamp>.txt)'
    )
    parser.add_argument(
        '--limit', type=int, default=0,
        help='Maximum number of notifications (0 = unlimited)'
    )
    args = parser.parse_args()
    
    # Calculate time range
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)
    
    if args.hours:
        since = now - timedelta(hours=args.hours)
    else:
        since = now - timedelta(minutes=args.minutes)
    
    # Convert to Unix timestamp
    since_unix = since.timestamp()
    
    # Convert to CoreData timestamp (for database query)
    since_core = since_unix - CORE_DATA_OFFSET
    
    # Generate output filename
    timestamp = now.strftime('%Y-%m-%d_%H%M%S')
    
    if args.output:
        output_file = Path(args.output)
    else:
        # Create output directory if it doesn't exist
        DEFAULT_OUTPUT_DIR.mkdir(exist_ok=True)
        output_file = DEFAULT_OUTPUT_DIR / f'notifications_{timestamp}.txt'
    
    # Find database
    original_db = get_notification_db_path()
    if not original_db:
        with open(output_file, 'w') as f:
            f.write(f"ERROR: Cannot find notification database\n")
            f.write("Please ensure you have granted Full Disk Access to python3:\n")
            f.write("  System Settings → Privacy & Security → Full Disk Access → Add /usr/bin/python3\n")
        print(f"ERROR: Cannot find notification database: {output_file}")
        return
    
    # Copy database to temp directory
    # NOTE: Notification DB uses WAL mode. We must copy db + sidecar files
    # (-wal/-shm), otherwise recent notifications may appear as 0.
    temp_db = Path("/tmp/notif_pipeline.db")
    temp_wal = Path("/tmp/notif_pipeline.db-wal")
    temp_shm = Path("/tmp/notif_pipeline.db-shm")
    src_wal = Path(str(original_db) + "-wal")
    src_shm = Path(str(original_db) + "-shm")

    try:
        shutil.copy2(original_db, temp_db)
        if src_wal.exists():
            shutil.copy2(src_wal, temp_wal)
        if src_shm.exists():
            shutil.copy2(src_shm, temp_shm)
    except PermissionError:
        with open(output_file, 'w') as f:
            f.write("ERROR: Permission denied\n")
            f.write("Please grant Full Disk Access to python3:\n")
            f.write("  System Settings → Privacy & Security → Full Disk Access → Add /usr/bin/python3\n")
        print(f"ERROR: Permission denied: {output_file}")
        return
    except Exception as e:
        with open(output_file, 'w') as f:
            f.write(f"ERROR: {e}\n")
        print(f"ERROR: {e}")
        return
    
    # Read database
    conn = sqlite3.connect(str(temp_db))
    cursor = conn.cursor()
    
    # Get app mapping
    cursor.execute("SELECT app_id, identifier FROM app")
    app_map = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Query with time filter
    if args.limit > 0:
        cursor.execute("""
            SELECT rec_id, app_id, data, delivered_date
            FROM record 
            WHERE delivered_date >= ?
            ORDER BY delivered_date DESC
            LIMIT ?
        """, (since_core, args.limit))
    else:
        cursor.execute("""
            SELECT rec_id, app_id, data, delivered_date
            FROM record 
            WHERE delivered_date >= ?
            ORDER BY delivered_date DESC
        """, (since_core,))
    
    rows = cursor.fetchall()
    
    # Parse notifications
    lines = []
    for rec_id, app_id, data, delivered_date in rows:
        app_name = app_map.get(app_id, f'unknown({app_id})')
        notif_data = parse_notification_data(data)
        
        # Convert CoreData timestamp to readable time
        unix_ts = core_data_to_unix(delivered_date) if delivered_date else 0
        t = datetime.fromtimestamp(unix_ts).strftime('%Y-%m-%d %H:%M:%S') if unix_ts else 'unknown'
        
        title = notif_data.get('title', '')
        body = notif_data.get('body', '')
        category = notif_data.get('category', '')
        
        content = title or body
        if title and body:
            content = f"{title}: {body}"
        
        if content:
            app_display = simplify_app_name(app_name)
            cat_tag = f"[{category}]" if category else ""
            lines.append(f"{t} | {app_display} {cat_tag} | {content}")
    
    conn.close()
    for p in [temp_db, temp_wal, temp_shm]:
        if p.exists():
            p.unlink()
    
    # Write output
    output_file.parent.mkdir(parents=True, exist_ok=True)
    time_range = f"Last {args.hours}h" if args.hours else f"Last {args.minutes}min"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"=== macOS Notifications ({len(lines)} items) - {time_range} - {timestamp} ===\n\n")
        f.write("\n".join(lines))
    
    print(f"Written to: {output_file} ({len(lines)} items)")


if __name__ == "__main__":
    main()
