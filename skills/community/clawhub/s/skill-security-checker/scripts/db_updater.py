#!/usr/bin/env python3
"""
Malicious DB Incremental Updater - daily silent sync with graceful fallback.

Follows the OSV cache strategy (死规则9/10):
  - Offline-first: never breaks zero-key gene; uses plain HTTP GET only, no API key.
  - Daily silent check driven by last_sync timestamp (check at most once / 24h).
  - On success: merge new entries (dedupe by name+type), refresh data-point timestamp.
  - On failure (offline / bad payload): KEEP the old DB untouched, mark stale with
    the last known data point so reports stay honest.
  - Update source configurable via env SKILLSEC_DB_URL or ~/.workbuddy/gate-audit/db_source.json.

Pure stdlib (urllib). Cache + config live outside the repo (死规则13).
Author: njskills@agent.qq.com
Version: 1.0.0
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

from malicious_db import DB_PATH, MaliciousDB, _default_db

VERSION = "1.0.0"
SYNC_INTERVAL_HOURS = 24
DEFAULT_SOURCE = ""  # Empty = no remote configured; offline-first, no surprise network.

CONFIG_DIR = Path.home() / ".workbuddy" / "gate-audit"
SYNC_STATE_PATH = CONFIG_DIR / "db_sync_state.json"
SOURCE_CONFIG_PATH = CONFIG_DIR / "db_source.json"
USER_AGENT = "skill-security-checker-db-updater/1.0"


class DBUpdater:
    """Incrementally sync the malicious fingerprint DB with safe fallback."""

    def __init__(self, db_path=None, source=None, timeout=8):
        self.db_path = Path(db_path) if db_path else DB_PATH
        self.timeout = timeout
        self.source = source if source is not None else self._resolve_source()
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    def _resolve_source(self):
        """Resolve update source: env > config file > default (empty)."""
        env = os.environ.get('SKILLSEC_DB_URL', '').strip()
        if env:
            return env
        try:
            if SOURCE_CONFIG_PATH.exists():
                cfg = json.loads(SOURCE_CONFIG_PATH.read_text(encoding='utf-8'))
                url = str(cfg.get('url', '')).strip()
                if url:
                    return url
        except Exception:
            pass
        return DEFAULT_SOURCE

    def _load_state(self):
        if not SYNC_STATE_PATH.exists():
            return {}
        try:
            return json.loads(SYNC_STATE_PATH.read_text(encoding='utf-8'))
        except Exception:
            return {}

    def _save_state(self, state):
        SYNC_STATE_PATH.write_text(
            json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')

    def is_due(self, force=False):
        """Whether a daily sync is due (based on last successful sync time)."""
        if force:
            return True
        state = self._load_state()
        last = state.get('last_sync')
        if not last:
            return True
        try:
            dt = datetime.fromisoformat(last)
        except Exception:
            return True
        return datetime.now() - dt >= timedelta(hours=SYNC_INTERVAL_HOURS)

    def data_point(self):
        """Return the current DB's data point (last_updated) for honest labeling."""
        try:
            data = json.loads(self.db_path.read_text(encoding='utf-8'))
            return data.get('last_updated', '')
        except Exception:
            return ''

    def _fetch(self):
        """Fetch remote payload. Returns parsed dict or raises."""
        import urllib.request
        req = urllib.request.Request(self.source, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            raw = resp.read().decode('utf-8', 'replace')
        data = json.loads(raw)
        if not isinstance(data, dict) or not isinstance(data.get('entries'), list):
            raise ValueError('payload must be an object with an entries list')
        return data

    def _merge(self, remote_entries):
        """Merge remote entries into the current DB. Returns (total, added)."""
        db = MaliciousDB(str(self.db_path))
        existing = {(e.get('name'), e.get('type')) for e in db.db.get('entries', [])}
        added = 0
        for e in remote_entries:
            if not isinstance(e, dict):
                continue
            name = e.get('name')
            if not name:
                continue
            etype = e.get('type', 'package')
            key = (name, etype)
            if key in existing:
                continue
            entry = {
                'type': etype,
                'name': name,
                'fingerprint_sha256': e.get('fingerprint_sha256')
                or hashlib.sha256(str(name).encode()).hexdigest(),
                'severity': e.get('severity', 'critical'),
                'description': e.get('description', f'Known malicious (community sync): {name}'),
                'added_date': e.get('added_date', datetime.now().strftime('%Y-%m-%d')),
                'source': e.get('source', 'community-sync'),
            }
            db.db['entries'].append(entry)
            existing.add(key)
            added += 1
        db.db['total_entries'] = len(db.db['entries'])
        db.db['last_updated'] = datetime.now().isoformat()
        db.db['version'] = db.db.get('version', '1.0')
        db.db['data_source'] = self.source
        db._save()
        return db.db['total_entries'], added

    def sync(self, force=False, dry_run=False):
        """Run a sync attempt. Always returns a status dict, never raises.

        Status: {'status': 'updated'|'skipped'|'stale'|'no-source', ...}
        """
        data_point_before = self.data_point()
        if not self.source:
            return {
                'status': 'no-source',
                'message': '未配置指纹库更新源，使用本地库（离线优先）',
                'data_point': data_point_before,
                'force': force,
                'version': VERSION,
            }
        if not force and not self.is_due():
            state = self._load_state()
            return {
                'status': 'skipped',
                'message': '距上次同步未满 24 小时，跳过',
                'data_point': data_point_before,
                'last_sync': state.get('last_sync'),
                'version': VERSION,
            }
        try:
            payload = self._fetch()
            if dry_run:
                return {
                    'status': 'dry-run',
                    'message': f'预演：远端返回 {len(payload["entries"])} 条，未写入',
                    'remote_entries': len(payload['entries']),
                    'data_point': data_point_before,
                    'version': VERSION,
                }
            total, added = self._merge(payload['entries'])
            self._save_state({
                'last_sync': datetime.now().isoformat(),
                'last_status': 'updated',
                'source': self.source,
                'added': added,
                'total_entries': total,
            })
            return {
                'status': 'updated',
                'message': f'指纹库已更新，新增 {added} 条，共 {total} 条',
                'added': added,
                'total_entries': total,
                'data_point': self.data_point(),
                'source': self.source,
                'version': VERSION,
            }
        except Exception as e:
            # Failure: keep old DB, mark stale with last known data point.
            self._save_state({
                'last_sync': datetime.now().isoformat(),
                'last_status': 'stale',
                'source': self.source,
                'error': str(e)[:200],
            })
            return {
                'status': 'stale',
                'message': f'更新失败，保留旧库（{type(e).__name__}）',
                'data_point': data_point_before,
                'data_point_stale': True,
                'source': self.source,
                'version': VERSION,
            }


def sync_if_due(db_path=None, force=False):
    """Convenience wrapper used by audit's quick/gate path. Never raises."""
    try:
        return DBUpdater(db_path=db_path).sync(force=force)
    except Exception as e:
        return {
            'status': 'stale',
            'message': f'更新检查异常，保留旧库（{type(e).__name__}）',
            'data_point': '',
            'data_point_stale': True,
            'version': VERSION,
        }


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='Malicious fingerprint DB incremental updater')
    p.add_argument('--force', action='store_true', help='Ignore 24h interval, force check')
    p.add_argument('--dry-run', action='store_true', help='Fetch but do not write')
    p.add_argument('--url', help='Override update source URL')
    p.add_argument('--status-only', action='store_true', help='Only show current data point')
    a = p.parse_args()
    up = DBUpdater(source=a.url)
    if a.status_only:
        print(json.dumps({
            'data_point': up.data_point(),
            'source': up.source,
            'due': up.is_due(),
        }, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(up.sync(force=a.force, dry_run=a.dry_run),
                         ensure_ascii=False, indent=2))
