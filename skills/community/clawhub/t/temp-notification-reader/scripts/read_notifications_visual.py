#!/usr/bin/env python3
"""
macOS Notification Reader - Visual Version
For interactive use (displays output directly to console).

Usage:
    python3 read_notifications_visual.py --minutes 35
    python3 read_notifications_visual.py --limit 20
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

# CoreData epoch offset
CORE_DATA_OFFSET = 978307200


def get_notification_db_path():
    db_path = Path.home() / 'Library' / 'Group Containers' / 'group.com.apple.usernoted' / 'db2' / 'db'
    if db_path.exists():
        return db_path
    try:
        conf_dir = subprocess.check_output(["getconf", "DARWIN_USER_DIR"]).decode().strip()
        db_path = Path(conf_dir) / 'com.apple.notificationcenter' / 'db2' / 'db'
        if db_path.exists():
            return db_path
    except Exception:
        pass
    return None


def parse_notification_data(data_blob):
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
    mapping = {
        'com.tencent.xinWeChat': '💬 WeChat',
        'com.microsoft.teams2': '📊 Teams',
        'com.microsoft.Outlook': '📧 Outlook',
        'com.apple.mail': '📬 Mail',
        'com.apple.mobilesms': '💬 iMessage',
        'com.apple.ical': '📅 Calendar',
        'com.apple.reminders': '✅ Reminders',
    }
    return mapping.get(app_id, f'📱 {app_id.split(".")[-1][:12]}')


def main():
    parser = argparse.ArgumentParser(description='Read macOS notifications (visual mode)')
    parser.add_argument('--minutes', type=int, default=35)
    parser.add_argument('--hours', type=int)
    parser.add_argument('--limit', type=int, default=20)
    args = parser.parse_args()
    
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)
    
    if args.hours:
        since = now - timedelta(hours=args.hours)
    else:
        since = now - timedelta(minutes=args.minutes)
    
    since_unix = since.timestamp()
    since_core = since_unix - CORE_DATA_OFFSET
    
    original_db = get_notification_db_path()
    if not original_db:
        print("❌ Cannot find notification database")
        print("Please grant Full Disk Access to python3:")
        print("  System Settings → Privacy & Security → Full Disk Access → Add /usr/bin/python3")
        return
    
    temp_db = Path("/tmp/notif_visual.db")
    try:
        shutil.copy2(original_db, temp_db)
    except PermissionError:
        print("❌ Permission denied")
        print("Please grant Full Disk Access to python3:")
        print("  System Settings → Privacy & Security → Full Disk Access → Add /usr/bin/python3")
        return
    
    conn = sqlite3.connect(str(temp_db))
    cursor = conn.cursor()
    
    cursor.execute("SELECT app_id, identifier FROM app")
    app_map = {row[0]: row[1] for row in cursor.fetchall()}
    
    if args.hours:
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
            LIMIT ?
        """, (since_core, args.limit))
    
    rows = cursor.fetchall()
    
    time_unit = f"{args.hours}h" if args.hours else f"{args.minutes}min"
    print(f"\n🔔 macOS Notifications (Last {time_unit}, {len(rows)} items)\n")
    print("=" * 120)
    
    for rec_id, app_id, data, delivered_date in rows:
        app_name = app_map.get(app_id, f'unknown({app_id})')
        notif_data = parse_notification_data(data)
        
        unix_ts = (delivered_date or 0) + CORE_DATA_OFFSET if delivered_date else 0
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
            content = (content[:200] + '…') if len(content) > 200 else content
            print(f"{t} | {app_display} {cat_tag} | {content}")
    
    print("=" * 120)
    
    conn.close()
    if temp_db.exists():
        temp_db.unlink()


if __name__ == "__main__":
    main()
