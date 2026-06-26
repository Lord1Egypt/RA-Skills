#!/usr/bin/env python3
"""
OpenClaw Skills Updater
Detects and upgrades installed skills to their latest versions.

Features:
- Auto-detection of skill updates
- Local caching (24h TTL) to reduce API calls
- Retry logic with exponential backoff for rate limits
- Automatic backup before updates
- Detailed reporting
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import subprocess
import zipfile
import shutil
import urllib.request
import urllib.error
import urllib.parse
import ssl
import time
from typing import Optional, Dict, List, Tuple

# Configuration
SKILLS_DIRS = [
    Path.home() / "OpenClaw" / "skills",
    Path.home() / ".openclaw" / "skills",
    Path.home() / ".openclaw" / "workspace" / "skills",
]
BACKUP_DIR = Path.home() / "Desktop" / "skill-backups"
MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
CACHE_DIR = Path.home() / ".openclaw" / ".skill-updater-cache"
CLAWHUB_API_BASE = "https://clawhub.ai"  # Official ClawHub registry (discovered via /.well-known/clawhub.json)
CACHE_TTL_HOURS = 24
MAX_RETRIES = 3
RETRY_DELAY_BASE = 2  # seconds, exponential backoff

# SSL context setup
class SSLHelper:
    @staticmethod
    def create_context():
        """Create SSL context for secure HTTPS connections."""
        ctx = ssl.create_default_context()
        # Verify hostname and certificate by default
        ctx.check_hostname = True
        ctx.verify_mode = ssl.CERT_REQUIRED
        return ctx

class CacheManager:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        # Restrict cache directory to owner only (700)
        os.chmod(self.cache_dir, 0o700)

    def get_cache_file(self, slug: str) -> Path:
        """Get cache file path for a skill."""
        return self.cache_dir / f"{slug}.json"

    def is_cache_valid(self, slug: str) -> bool:
        """Check if cache exists and is still valid (< 24h old)."""
        cache_file = self.get_cache_file(slug)
        if not cache_file.exists():
            return False
        
        try:
            with open(cache_file) as f:
                data = json.load(f)
            
            cached_at = datetime.fromisoformat(data.get("cached_at", ""))
            age = datetime.now() - cached_at
            is_valid = age < timedelta(hours=CACHE_TTL_HOURS)
            
            if not is_valid and False:  # Set True to log cache expiry
                print(f"  Cache expired for {slug}: {age.total_seconds()/3600:.1f}h old")
            
            return is_valid
        except:
            return False

    def get(self, slug: str) -> Optional[Dict]:
        """Get cached version info."""
        if not self.is_cache_valid(slug):
            return None
        
        try:
            with open(self.get_cache_file(slug)) as f:
                return json.load(f).get("meta")
        except:
            return None

    def set(self, slug: str, meta: Dict):
        """Cache version info."""
        cache_file = self.get_cache_file(slug)
        try:
            with open(cache_file, 'w') as f:
                json.dump({
                    "slug": slug,
                    "meta": meta,
                    "cached_at": datetime.now().isoformat()
                }, f)
        except Exception as e:
            pass  # Fail silently on cache write errors

class SkillUpdater:
    def __init__(self, verbose: bool = False):
        self.backup_dir = BACKUP_DIR
        self.memory_dir = MEMORY_DIR
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.updates_found = []
        self.updates_performed = []
        self.updates_failed = []  # 新增：追踪失败的更新
        self.errors = []
        self.warnings = []
        self.verbose = verbose
        self.cache_only = False  # 新增：仅用缓存模式
        self.dry_run = False     # 新增：预览模式
        self.ssl_context = SSLHelper.create_context()
        self.cache = CacheManager(CACHE_DIR)
        self.start_time = None   # 新增：开始时间
        self.scan_time = 0       # 新增：扫描耗时
        self.update_time = 0     # 新增：更新耗时

    def scan_installed_skills(self) -> List[Tuple[Path, Dict]]:
        """Scan for installed skills and their metadata."""
        skills = []
        
        for skill_dir in SKILLS_DIRS:
            if not skill_dir.exists():
                continue
                
            for item in skill_dir.iterdir():
                if not item.is_dir():
                    continue
                    
                meta_file = item / "_meta.json"
                if meta_file.exists():
                    try:
                        with open(meta_file) as f:
                            meta = json.load(f)
                        skills.append((item, meta))
                        if self.verbose:
                            print(f"  Found: {item.name} v{meta.get('version')}")
                    except Exception as e:
                        self.errors.append(f"Failed to read {meta_file}: {e}")
        
        return skills

    def fetch_latest_version(self, slug: str, retry_count: int = 0) -> Optional[Dict]:
        """Fetch the latest version info for a skill from ClawHub.
        
        Uses the /api/v1/skills/{slug} JSON endpoint to get metadata,
        NOT the /api/v1/download endpoint (which returns a zip).
        """
        # Try cache first
        cached = self.cache.get(slug)
        if cached:
            if self.verbose:
                print(f"    Using cached version info")
            return cached
        
        # If cache-only mode, don't call API
        if self.cache_only:
            if self.verbose:
                print(f"    No cache available (cache-only mode, skipping API call)")
            return None

        try:
            # Use the metadata API endpoint (returns JSON with version info)
            url = f"{CLAWHUB_API_BASE}/api/v1/skills/{urllib.parse.quote(slug, safe='')}"
            request = urllib.request.Request(url, headers={"Accept": "application/json"})
            response = urllib.request.urlopen(request, context=self.ssl_context, timeout=10)
            data = json.loads(response.read().decode('utf-8'))
            
            # Build a meta dict compatible with the rest of the updater
            latest_version = None
            if data.get('latestVersion'):
                latest_version = data['latestVersion'].get('version')
            elif data.get('skill', {}).get('tags', {}).get('latest'):
                latest_version = data['skill']['tags']['latest']
            
            if not latest_version:
                if self.verbose:
                    print(f"    No version info found in API response for '{slug}'")
                return None
            
            meta = {
                'slug': slug,
                'version': latest_version,
                'displayName': data.get('skill', {}).get('displayName', slug),
                'summary': data.get('skill', {}).get('summary', ''),
                'changelog': data.get('latestVersion', {}).get('changelog', ''),
            }
            
            # Cache the result
            self.cache.set(slug, meta)
            return meta
            
        except urllib.error.HTTPError as e:
            if e.code == 429:  # Rate limited
                if retry_count < MAX_RETRIES:
                    delay = RETRY_DELAY_BASE ** (retry_count + 1)
                    print(f"⏱️  Rate limited for '{slug}'. Waiting {delay}s before retry {retry_count + 1}/{MAX_RETRIES}...")
                    time.sleep(delay)
                    return self.fetch_latest_version(slug, retry_count + 1)
                else:
                    msg = f"Rate limit exceeded for '{slug}' after {MAX_RETRIES} retries (HTTP 429). Try again in a few minutes."
                    print(f"⚠️  {msg}")
                    self.warnings.append(msg)
                    return None
            elif e.code == 404:
                msg = f"Skill '{slug}' not found on ClawHub (HTTP 404). May not be published or slug mismatch."
                print(f"⚠️  {msg}")
                self.warnings.append(msg)
                return None
            elif e.code == 503:  # Service unavailable
                msg = f"ClawHub is temporarily unavailable (HTTP 503)."
                print(f"⚠️  {msg}")
                self.warnings.append(msg)
                return None
            else:
                msg = f"Failed to fetch '{slug}': HTTP {e.code}"
                print(f"❌ {msg}")
                self.errors.append(msg)
        except urllib.error.URLError as e:
            if "429" in str(e):
                msg = f"Rate limit for '{slug}' (HTTP 429). Skipping. Try again later."
                print(f"⚠️  {msg}")
                self.warnings.append(msg)
            else:
                msg = f"Network error fetching '{slug}': {e.reason if hasattr(e, 'reason') else e}"
                print(f"❌ {msg}")
                self.errors.append(msg)
        except Exception as e:
            msg = f"Failed to fetch latest version for '{slug}': {e}"
            print(f"❌ {msg}")
            self.errors.append(msg)
        
        return None

    def compare_versions(self, current: str, latest: str) -> bool:
        """Compare semantic versions. Returns True if update available."""
        try:
            current_parts = [int(x) for x in current.split('.')]
            latest_parts = [int(x) for x in latest.split('.')]
            
            # Pad with zeros to same length
            max_len = max(len(current_parts), len(latest_parts))
            current_parts += [0] * (max_len - len(current_parts))
            latest_parts += [0] * (max_len - len(latest_parts))
            
            return latest_parts > current_parts
        except:
            return False

    def backup_skill(self, skill_path: Path, meta: Dict) -> Path:
        """Backup current skill version."""
        skill_name = skill_path.name
        version = meta.get('version', 'unknown')
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        
        backup_name = f"{skill_name}-{version}-{timestamp}"
        backup_path = self.backup_dir / backup_name
        
        try:
            shutil.copytree(skill_path, backup_path)
            return backup_path
        except Exception as e:
            self.errors.append(f"Failed to backup {skill_name}: {e}")
            return None

    def update_skill(self, skill_path: Path, slug: str, latest_meta: Dict) -> bool:
        """Download and update skill to latest version."""
        import tempfile
        try:
            # Use the correct download endpoint: /api/v1/download?slug=X&version=Y
            latest_version = latest_meta.get('version', '')
            url = f"{CLAWHUB_API_BASE}/api/v1/download?slug={urllib.parse.quote(slug, safe='')}"
            if latest_version:
                url += f"&version={urllib.parse.quote(latest_version, safe='')}"
            # Use tempfile for secure paths (prevents TOCTOU attacks)
            with tempfile.NamedTemporaryFile(suffix=f'-{slug}.zip', delete=False) as tmp:
                temp_zip = Path(tmp.name)
            temp_extract = Path(tempfile.mkdtemp(suffix=f'-{slug}-update'))
            
            # Download with SSL context
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request, context=self.ssl_context, timeout=10)
            with open(temp_zip, 'wb') as f:
                f.write(response.read())
            
            # Validate and extract (path traversal protection)
            with zipfile.ZipFile(temp_zip, 'r') as z:
                for name in z.namelist():
                    if name.startswith('/') or '..' in name:
                        raise ValueError(f"Unsafe zip entry rejected: {name}")
                z.extractall(temp_extract)
            
            # Remove old skill and replace
            shutil.rmtree(skill_path)
            shutil.copytree(temp_extract, skill_path)
            
            # Cleanup temp files
            temp_zip.unlink()
            shutil.rmtree(temp_extract)
            
            return True
        except Exception as e:
            self.errors.append(f"Failed to update {slug}: {e}")
            return False

    def check_updates(self) -> List[Dict]:
        """Check all installed skills for updates."""
        start = time.time()
        installed = self.scan_installed_skills()
        if self.verbose:
            print(f"Scanned {len(installed)} installed skill(s)")
        
        for skill_path, current_meta in installed:
            slug = current_meta.get('slug', skill_path.name)
            current_version = current_meta.get('version', '0.0.0')
            
            if self.verbose:
                print(f"  Checking {slug} (current: {current_version})...")
            
            latest_meta = self.fetch_latest_version(slug)
            if not latest_meta:
                continue
            
            latest_version = latest_meta.get('version', current_version)
            
            if self.verbose:
                print(f"    Latest version: {latest_version}")
            
            if self.compare_versions(current_version, latest_version):
                self.updates_found.append({
                    'skill': skill_path.name,
                    'slug': slug,
                    'current': current_version,
                    'latest': latest_version,
                    'path': skill_path,
                    'latest_meta': latest_meta
                })
                if self.verbose:
                    print(f"    ✓ Update available: {current_version} → {latest_version}")
        
        self.scan_time = time.time() - start
        return self.updates_found

    def perform_updates(self, auto_approve: bool = False) -> List[Dict]:
        """Perform updates for found skills."""
        if not auto_approve and self.updates_found:
            print("\n📦 Found updates:")
            for i, update in enumerate(self.updates_found, 1):
                print(f"  {i}. {update['skill']}: {update['current']} → {update['latest']}")
            
            if self.dry_run:
                print("\n🔍 DRY-RUN MODE (no changes will be made)")
            
            response = input("\nProceed with updates? (y/n): ").strip().lower()
            if response != 'y':
                return []
        
        start = time.time()
        
        total = len(self.updates_found)
        for idx, update in enumerate(self.updates_found, 1):
            # Progress indicator
            progress = f"[{idx}/{total}]"
            
            if self.dry_run:
                # Dry-run: just show what would happen
                print(f"{progress} [DRY-RUN] {update['skill']}: {update['current']} → {update['latest']}")
                self.updates_performed.append({
                    'skill': update['skill'],
                    'from': update['current'],
                    'to': update['latest'],
                    'backup': None,
                    'timestamp': datetime.now().isoformat(),
                    'dry_run': True
                })
                continue
            
            # Real update: backup + update
            print(f"{progress} Updating {update['skill']}...", end=" ", flush=True)
            
            backup_path = self.backup_skill(update['path'], update.get('latest_meta', {}))
            if not backup_path:
                self.updates_failed.append({
                    'skill': update['skill'],
                    'from': update['current'],
                    'to': update['latest'],
                    'reason': 'Backup failed'
                })
                print("❌ Backup failed")
                continue
            
            if self.update_skill(update['path'], update['slug'], update['latest_meta']):
                self.updates_performed.append({
                    'skill': update['skill'],
                    'from': update['current'],
                    'to': update['latest'],
                    'backup': str(backup_path),
                    'timestamp': datetime.now().isoformat()
                })
                print(f"✓ {update['current']} → {update['latest']}")
            else:
                self.updates_failed.append({
                    'skill': update['skill'],
                    'from': update['current'],
                    'to': update['latest'],
                    'reason': 'Update failed',
                    'backup': str(backup_path)
                })
                print(f"❌ Update failed (backup: {backup_path})")
        
        self.update_time = time.time() - start
        return self.updates_performed

    def generate_report(self) -> str:
        """Generate upgrade report."""
        today = datetime.now().strftime('%Y-%m-%d')
        report_file = self.memory_dir / f"skill-upgrades-{today}.md"
        
        # 计算统计数据
        success_count = len(self.updates_performed)
        failed_count = len(self.updates_failed)
        total_checked = len(self.updates_found) + success_count + failed_count
        
        # 如果有 dry-run，这些不算真实更新
        dry_run_count = sum(1 for u in self.updates_performed if u.get('dry_run'))
        real_success = success_count - dry_run_count
        
        content = f"""# Skill Updates Report — {today}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Summary

| Metric | Count |
|--------|-------|
| **Total scanned** | {len(set(u['skill'] for u in self.updates_found + self.updates_performed + self.updates_failed))} |
| **Updates available** | {len(self.updates_found)} |
| **Updates successful** | {real_success} |
| **Updates failed** | {failed_count} |
| **Dry-run previewed** | {dry_run_count} |
| **Errors** | {len(self.errors)} |
| **Warnings** | {len(self.warnings)} |

## ⏱️ Performance

- **Scan time:** {self.scan_time:.2f}s
- **Update time:** {self.update_time:.2f}s
- **Total time:** {self.scan_time + self.update_time:.2f}s

"""
        
        if real_success > 0:
            content += "## ✅ Updates Successful\n\n"
            for update in self.updates_performed:
                if not update.get('dry_run'):
                    content += f"### {update['skill']}\n"
                    content += f"- **Version:** {update['from']} → {update['to']}\n"
                    content += f"- **Backup:** `{update['backup']}`\n"
                    content += f"- **Timestamp:** {update['timestamp']}\n\n"
        
        if dry_run_count > 0:
            content += "## 🔍 Dry-Run Preview\n\n"
            content += "_(No changes made - this was a preview)_\n\n"
            for update in self.updates_performed:
                if update.get('dry_run'):
                    content += f"- {update['skill']}: {update['from']} → {update['to']}\n"
            content += "\n"
        
        if failed_count > 0:
            content += "## ❌ Updates Failed\n\n"
            for fail in self.updates_failed:
                content += f"### {fail['skill']}\n"
                content += f"- **Version:** {fail['from']} → {fail['to']}\n"
                content += f"- **Reason:** {fail['reason']}\n"
                if fail.get('backup'):
                    content += f"- **Backup:** `{fail['backup']}`\n"
                content += "\n"
        
        if self.warnings:
            content += "## ⚠️ Warnings\n\n"
            for warning in self.warnings:
                content += f"- {warning}\n"
            content += "\n"
        
        if self.errors:
            content += "## 🚨 Errors\n\n"
            for error in self.errors:
                content += f"- {error}\n"
        
        try:
            with open(report_file, 'w') as f:
                f.write(content)
            return str(report_file)
        except Exception as e:
            print(f"Failed to write report: {e}")
            return None

def main():
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    cache_only = '--cache-only' in sys.argv  # 新增：仅用缓存，不调 API
    dry_run = '--dry-run' in sys.argv        # 新增：预览模式
    
    updater = SkillUpdater(verbose=verbose)
    updater.cache_only = cache_only
    updater.dry_run = dry_run
    updater.start_time = time.time()
    
    # Check for updates
    mode = " (cache only)" if cache_only else ""
    mode += " (dry-run)" if dry_run else ""
    print(f"🔍 Scanning for skill updates{mode}...")
    updates = updater.check_updates()
    
    if updater.warnings and not verbose:
        print(f"\n⚠️  {len(updater.warnings)} warning(s) during scan")
    
    if updater.errors and not verbose:
        print(f"\n❌ {len(updater.errors)} error(s) during scan (use -v for details)")
    
    if not updates:
        print("✓ All skills are up to date!")
        return 0
    
    print(f"\n📦 Found {len(updates)} skill(s) with available updates.")
    
    # Perform updates (unless cache-only)
    if cache_only:
        print("\n⚠️  Cache-only mode: skipping updates. Use without --cache-only to apply.")
        return 0
    
    auto_approve = '--auto' in sys.argv
    performed = updater.perform_updates(auto_approve=auto_approve)
    
    # Generate report
    report_file = updater.generate_report()
    if report_file:
        print(f"\n✓ Report saved: {report_file}")
    
    # Summary
    total_time = time.time() - updater.start_time
    print(f"\n⏱️  Total time: {total_time:.2f}s")
    
    if dry_run:
        print("🔍 (No changes made - this was a preview)")
    
    return 0 if not updater.errors else 1

if __name__ == '__main__':
    sys.exit(main())
