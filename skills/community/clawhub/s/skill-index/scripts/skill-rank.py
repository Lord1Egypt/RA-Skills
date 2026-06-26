#!/usr/bin/env python3
"""
Skill Rank - Multi-Platform Skill Ranking & Discovery System

Supports:
- Xfyun SkillHub (skill.xfyun.cn) - 891 skills
- Tencent SkillHub (skillhub.tencent.com) - 25,000 skills
- Local installed skills
- Cross-platform search
- One-click installation
"""

import argparse
import json
import math
import os
import re
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import base64

# Configuration
DEFAULT_CONFIG = {
    "weights": {
        "activity": 0.30,
        "popularity": 0.25,
        "documentation": 0.20,
        "dependencies": 0.10,
        "compatibility": 0.10,
        "maintainer": 0.05
    },
    "cache_ttl_hours": 24,
    "github_api_token": os.environ.get("GITHUB_TOKEN", ""),
    "tencent_api_url": "https://lightmake.site/api/skills",
    "xfyun_api_url": "https://skill.xfyun.cn/api/v1/skills",
    "top_n_default": 10
}

DATA_DIR = Path.home() / ".openclaw" / "skill-rank"
DB_PATH = DATA_DIR / "rankings.db"
CACHE_DIR = DATA_DIR / "cache"
CONFIG_PATH = DATA_DIR / "config.json"


def ensure_data_dir():
    """Ensure data directories exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict:
    """Load configuration from file."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            config = json.load(f)
            return {**DEFAULT_CONFIG, **config}
    return DEFAULT_CONFIG


def save_config(config: Dict):
    """Save configuration to file."""
    ensure_data_dir()
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)


def init_database():
    """Initialize SQLite database."""
    ensure_data_dir()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            name TEXT PRIMARY KEY,
            repo_url TEXT,
            description TEXT,
            stars INTEGER DEFAULT 0,
            forks INTEGER DEFAULT 0,
            downloads INTEGER DEFAULT 0,
            rating REAL DEFAULT 0,
            last_commit TIMESTAMP,
            created_at TIMESTAMP,
            license TEXT,
            doc_content TEXT,
            doc_quality_score REAL DEFAULT 0,
            activity_score REAL DEFAULT 50,
            popularity_score REAL DEFAULT 50,
            doc_score REAL DEFAULT 50,
            deps_score REAL DEFAULT 50,
            compat_score REAL DEFAULT 50,
            maintainer_score REAL DEFAULT 50,
            total_score REAL DEFAULT 0,
            rank INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source TEXT DEFAULT 'local',
            metadata TEXT
        )
    ''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_source ON skills(source)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_score ON skills(total_score DESC)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_name ON skills(name)')
    
    conn.commit()
    conn.close()


def parse_download_count(s: str) -> int:
    """Parse download count string like '25.3 万' to integer."""
    if not s:
        return 0
    s = s.strip()
    try:
        if '万' in s:
            return int(float(s.replace('万', '')) * 10000)
        elif '千' in s:
            return int(float(s.replace('千', '')) * 1000)
        elif '百' in s:
            return int(float(s.replace('百', '')) * 100)
        else:
            return int(float(s))
    except (ValueError, TypeError):
        return 0


def calculate_popularity_score(downloads: int, stars: int) -> float:
    """Calculate popularity score (0-100)."""
    # Use log scale to handle wide range
    downloads_score = min(math.log10(downloads + 1) * 15, 60)
    stars_score = min(math.log10(stars + 1) * 20, 40)
    return min(downloads_score + stars_score, 100)


def save_skills_to_db(skills: List[Dict], source: str):
    """Save skills to database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for skill in skills:
        name = skill.get("name", "")
        if not name:
            continue
        
        # For local skills, check if already exists from remote source
        if source == "local":
            cursor.execute('SELECT source FROM skills WHERE name = ?', (name,))
            existing = cursor.fetchone()
            if existing and existing[0] in ("tencent", "xfyun"):
                # Don't overwrite remote skills with local
                continue
            
        description = skill.get("description", "")
        downloads = parse_download_count(str(skill.get("downloads", 0)))
        stars = skill.get("stars", 0)
        rating = skill.get("rating", 0)
        version = skill.get("version", "")
        repo_url = skill.get("repo_url", f"https://{source}.com/skill/{name}")
        
        # Calculate scores
        popularity_score = calculate_popularity_score(downloads, stars)
        total_score = popularity_score  # Simplified for now
        
        cursor.execute('''
            INSERT OR REPLACE INTO skills (
                name, repo_url, description, stars, downloads, rating,
                popularity_score, total_score, last_updated, source, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?, ?)
        ''', (
            name, repo_url, description, stars, downloads, rating,
            popularity_score, total_score, source,
            json.dumps({"version": version, "source": source})
        ))
    
    conn.commit()
    conn.close()


def update_rankings():
    """Update rank column based on total scores."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE skills SET rank = (
            SELECT COUNT(*) + 1 FROM skills s2 
            WHERE s2.total_score > skills.total_score
        )
    ''')
    
    conn.commit()
    conn.close()


# ============== Platform Fetchers ==============

def fetch_xfyun_skillhub(config: Dict) -> List[Dict]:
    """Fetch skills from Xfyun SkillHub API."""
    skills = []
    
    try:
        print("Fetching from Xfyun SkillHub API...")
        api_url = config.get("xfyun_api_url", DEFAULT_CONFIG["xfyun_api_url"])
        
        # Xfyun API returns all skills in one request (max 1000)
        url = f"{api_url}?limit=1000"
        req = Request(url, headers={
            "Accept": "application/json",
            "User-Agent": "OpenClaw-SkillRank/1.0"
        })
        
        with urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        items = data.get("items", [])
        
        for skill in items:
            stats = skill.get("stats", {}) or {}
            latest_version = skill.get("latestVersion") or {}
            skills.append({
                "name": skill.get("slug") or skill.get("displayName", ""),
                "display_name": skill.get("displayName", ""),
                "description": skill.get("summary", ""),
                "downloads": stats.get("downloads", 0) or 0,
                "stars": stats.get("stars", 0) or 0,
                "version": latest_version.get("version", "") if latest_version else "",
                "source": "xfyun"
            })
        
        print(f"  ✓ Total: {len(skills)} skills from Xfyun SkillHub")
        
    except Exception as e:
        print(f"  ✗ Error: {e}", file=sys.stderr)
    
    return skills


def fetch_tencent_skillhub(config: Dict) -> List[Dict]:
    """Fetch skills from Tencent SkillHub API."""
    skills = []
    
    try:
        print("Fetching from Tencent SkillHub API...")
        api_url = config.get("tencent_api_url", DEFAULT_CONFIG["tencent_api_url"])
        
        # Fetch top 100 skills sorted by downloads
        page = 1
        page_size = 100
        total_fetched = 0
        
        while True:
            url = f"{api_url}?page={page}&pageSize={page_size}&sortBy=downloads"
            req = Request(url, headers={
                "Accept": "application/json",
                "User-Agent": "OpenClaw-SkillRank/1.0"
            })
            
            with urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            if data.get("code") != 0:
                print(f"  API error: {data.get('message', 'Unknown error')}")
                break
            
            skills_data = data.get("data", {}).get("skills", [])
            if not skills_data:
                break
            
            for skill in skills_data:
                skills.append({
                    "name": skill.get("slug", skill.get("name", "")),
                    "description": skill.get("description_zh") or skill.get("description", ""),
                    "downloads": skill.get("downloads", 0),
                    "stars": skill.get("stars", 0),
                    "installs": skill.get("installs", 0),
                    "version": skill.get("version", ""),
                    "category": skill.get("category", ""),
                    "owner": skill.get("ownerName", ""),
                    "homepage": skill.get("homepage", ""),
                    "repo_url": skill.get("homepage", f"https://skillhub.tencent.com/skill/{skill.get('slug', '')}"),
                    "source": "tencent"
                })
            
            total_fetched += len(skills_data)
            print(f"  Page {page}: {len(skills_data)} skills (total: {total_fetched})")
            
            # Check if there are more pages
            total = data.get("data", {}).get("total", 0)
            if total_fetched >= total or len(skills_data) < page_size:
                break
            
            page += 1
        
        print(f"  ✓ Total: {len(skills)} skills from Tencent SkillHub")
        
    except Exception as e:
        print(f"  ✗ Error: {e}", file=sys.stderr)
    
    return skills


def fetch_local_skills() -> List[Dict]:
    """Scan locally installed skills."""
    skills = []
    installed_dir = Path.home() / ".openclaw" / "workspace" / "skills"
    
    if installed_dir.exists():
        for skill_dir in installed_dir.iterdir():
            if skill_dir.is_dir():
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    # Read description from SKILL.md
                    description = ""
                    try:
                        with open(skill_md, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Extract description from frontmatter or first paragraph
                            desc_match = re.search(r'description:\s*["\']?(.+?)["\']?\n', content)
                            if desc_match:
                                description = desc_match.group(1)[:200]
                    except:
                        pass
                    
                    skills.append({
                        "name": skill_dir.name,
                        "repo_url": f"local:{skill_dir}",
                        "description": description,
                        "source": "local"
                    })
    
    return skills


# ============== Commands ==============

def cmd_update(args):
    """Update skill database from all sources."""
    print("="*60)
    print("Updating Skill Database")
    print("="*60 + "\n")
    
    config = load_config()
    init_database()
    
    total_skills = 0
    
    # 1. Fetch from Xfyun SkillHub
    print("\n[1/3] Fetching from Xfyun SkillHub...")
    xfyun_skills = fetch_xfyun_skillhub(config)
    if xfyun_skills:
        save_skills_to_db(xfyun_skills, "xfyun")
        total_skills += len(xfyun_skills)
    
    # 2. Fetch from Tencent SkillHub
    print("\n[2/3] Fetching from Tencent SkillHub...")
    tencent_skills = fetch_tencent_skillhub(config)
    if tencent_skills:
        save_skills_to_db(tencent_skills, "tencent")
        total_skills += len(tencent_skills)
    
    # 3. Fetch from local
    print("\n[3/3] Scanning local skills...")
    local_skills = fetch_local_skills()
    if local_skills:
        save_skills_to_db(local_skills, "local")
        print(f"  ✓ Found {len(local_skills)} local skills")
        total_skills += len(local_skills)
    
    # Update rankings
    update_rankings()
    
    # Show summary
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM skills")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM skills WHERE source = 'xfyun'")
    xfyun_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM skills WHERE source = 'tencent'")
    tencent_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM skills WHERE source = 'local'")
    local_count = cursor.fetchone()[0]
    conn.close()
    
    print("\n" + "="*60)
    print(f"Database updated: {total} skills total")
    print(f"  - Xfyun SkillHub: {xfyun_count}")
    print(f"  - Tencent SkillHub: {tencent_count}")
    print(f"  - Local: {local_count}")
    print("="*60)


def cmd_import_xfyun(args):
    """Import skills from Xfyun SkillHub (requires JSON data)."""
    if args.json_file:
        with open(args.json_file, 'r') as f:
            skills = json.load(f)
    elif args.json_data:
        skills = json.loads(args.json_data)
    else:
        print("Error: Provide --json-file or --json-data")
        return
    
    init_database()
    save_skills_to_db(skills, "xfyun")
    update_rankings()
    print(f"✓ Imported {len(skills)} skills from Xfyun SkillHub")


def cmd_import_tencent(args):
    """Import skills from Tencent SkillHub (requires JSON data)."""
    if args.json_file:
        with open(args.json_file, 'r') as f:
            skills = json.load(f)
    elif args.json_data:
        skills = json.loads(args.json_data)
    else:
        print("Error: Provide --json-file or --json-data")
        return
    
    init_database()
    save_skills_to_db(skills, "tencent")
    update_rankings()
    print(f"✓ Imported {len(skills)} skills from Tencent SkillHub")


def should_update_database(config: Dict) -> bool:
    """Check if database needs update based on TTL."""
    if not DB_PATH.exists():
        return True
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(last_updated) FROM skills")
    last_update = cursor.fetchone()[0]
    conn.close()
    
    if not last_update:
        return True
    
    try:
        last_time = datetime.fromisoformat(str(last_update).replace(' ', 'T'))
        ttl_hours = config.get("cache_ttl_hours", 24)
        age = datetime.now() - last_time
        return age.total_seconds() > ttl_hours * 3600
    except:
        return True


def cmd_list(args):
    """List top skills."""
    config = load_config()
    
    # Check if database needs update
    if should_update_database(config):
        print("⚠️  Database is outdated. Run 'skill-rank --update' to refresh.\n")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    top_n = args.top or DEFAULT_CONFIG["top_n_default"]
    source_filter = args.source if hasattr(args, 'source') and args.source else None
    
    if source_filter:
        cursor.execute('''
            SELECT name, total_score, description, stars, downloads, source
            FROM skills
            WHERE source = ?
            ORDER BY total_score DESC
            LIMIT ?
        ''', (source_filter, top_n))
    else:
        cursor.execute('''
            SELECT name, total_score, description, stars, downloads, source
            FROM skills
            ORDER BY total_score DESC
            LIMIT ?
        ''', (top_n,))
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        print("No skills found. Run 'skill-rank --update' first.")
        return
    
    print(f"\n{'='*90}")
    print(f"Top {len(results)} Skills by Quality Score")
    print(f"{'='*90}\n")
    
    print(f"{'Rank':<6}{'Score':<8}{'Stars':<8}{'Downloads':<12}{'Source':<10}{'Name':<25}{'Description'}")
    print("-" * 90)
    
    for i, (name, score, desc, stars, downloads, source) in enumerate(results, 1):
        desc_short = (desc[:35] + '...') if desc and len(desc) > 35 else (desc or "")
        downloads_str = f"{downloads:,}" if downloads else "0"
        print(f"{i:<6}{score:<8.1f}{stars:<8}{downloads_str:<12}{source:<10}{name:<25}{desc_short}")
    
    print()


def cmd_search(args):
    """Search skills by keyword."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    keyword = f"%{args.keyword}%"
    source_filter = args.source if hasattr(args, 'source') and args.source else None
    
    if source_filter:
        cursor.execute('''
            SELECT name, total_score, description, stars, downloads, source
            FROM skills
            WHERE (name LIKE ? OR description LIKE ?) AND source = ?
            ORDER BY total_score DESC
            LIMIT 20
        ''', (keyword, keyword, source_filter))
    else:
        cursor.execute('''
            SELECT name, total_score, description, stars, downloads, source
            FROM skills
            WHERE name LIKE ? OR description LIKE ?
            ORDER BY total_score DESC
            LIMIT 20
        ''', (keyword, keyword))
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        print(f"No skills found matching '{args.keyword}'" + (f" in source '{source_filter}'" if source_filter else ""))
        return
    
    print(f"\nSkills matching '{args.keyword}'" + (f" (source: {source_filter})" if source_filter else "") + ":\n")
    print(f"{'Score':<8}{'Stars':<8}{'Source':<10}{'Name':<30}{'Description'}")
    print("-" * 90)
    
    for name, score, desc, stars, downloads, source in results:
        desc_short = (desc[:40] + '...') if desc and len(desc) > 40 else (desc or "")
        print(f"{score:<8.1f}{stars:<8}{source:<10}{name:<30}{desc_short}")


def cmd_info(args):
    """Show detailed skill info."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM skills WHERE name = ?
    ''', (args.skill_name,))
    
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        print(f"Skill '{args.skill_name}' not found.")
        return
    
    columns = [
        "name", "repo_url", "description", "stars", "forks", "downloads",
        "rating", "last_commit", "created_at", "license", "doc_content",
        "doc_quality_score", "activity_score", "popularity_score", "doc_score",
        "deps_score", "compat_score", "maintainer_score", "total_score", "rank",
        "last_updated", "source", "metadata"
    ]
    
    skill = dict(zip(columns, result))
    
    print(f"\n{'='*70}")
    print(f"Skill: {skill['name']}")
    print(f"{'='*70}\n")
    
    print(f"📊 Overall Rank: #{skill['rank']}")
    print(f"📈 Total Score: {skill['total_score']:.1f}/100")
    print(f"🏷️  Source: {skill['source']}\n")
    
    if skill['popularity_score']:
        print("Quality Dimensions:")
        print(f"  Popularity:     {skill['popularity_score']:.1f}/100")
        if skill['activity_score']:
            print(f"  Activity:       {skill['activity_score']:.1f}/100")
            print(f"  Documentation:  {skill['doc_score']:.1f}/100")
        print()
    
    print("Statistics:")
    print(f"  ⭐ Stars:     {skill['stars']:,}")
    if skill['downloads']:
        print(f"  📥 Downloads: {skill['downloads']:,}")
    if skill['rating']:
        print(f"  ⭐ Rating:    {skill['rating']:.1f}/5")
    print()
    
    print(f"📝 Description:")
    print(f"  {skill['description'] or 'No description available'}\n")
    
    print(f"🔗 URL: {skill['repo_url']}")
    print(f"📅 Last Updated: {skill['last_updated']}\n")
    
    # Installation hint
    if skill['source'] == 'local':
        print("✅ Already installed locally")
    elif skill['source'] == 'tencent':
        print(f"💡 To install: skillhub install {skill['name']}")
    else:
        print(f"💡 To install: clawhub install {skill['name']}")


def check_cli_installed(cli_name: str) -> bool:
    """Check if a CLI tool is installed."""
    try:
        result = subprocess.run([cli_name, '--version'], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def cmd_install(args):
    """Install a skill with automatic CLI detection."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT source, repo_url, description FROM skills WHERE name = ?', (args.install_skill,))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        print(f"❌ Skill '{args.install_skill}' not found in database.")
        print("   Try searching first: skill-rank --search <keyword>")
        return 1
    
    source, repo_url, description = result
    
    print(f"\n{'='*60}")
    print(f"Installing: {args.install_skill}")
    print(f"{'='*60}")
    print(f"Source: {source}")
    print(f"Description: {description[:80]}..." if description and len(description) > 80 else f"Description: {description or 'N/A'}")
    print()
    
    if source == 'local':
        print("✅ Already installed locally!")
        return 0
    
    # Determine which CLI to use
    cli_name = 'skillhub' if source == 'tencent' else 'clawhub'
    cmd = [cli_name, 'install', args.install_skill]
    
    # Dry run mode - just show what would be done
    if hasattr(args, 'dry_run') and args.dry_run:
        print("🔍 DRY RUN MODE - No actual installation\n")
        print(f"Command to run: {' '.join(cmd)}")
        
        if check_cli_installed(cli_name):
            print(f"✅ CLI '{cli_name}' is installed")
        else:
            print(f"⚠️  CLI '{cli_name}' is NOT installed")
            print(f"\n📦 Installation instructions:")
            if cli_name == 'skillhub':
                print(f"   npm install -g @clawdbot/skillhub")
            else:
                print(f"   npm install -g clawhub")
        
        print(f"\nTo actually install, run:")
        print(f"   skill-rank --install {args.install_skill}")
        return 0
    
    # Check if CLI is installed
    if not check_cli_installed(cli_name):
        print(f"❌ CLI tool '{cli_name}' not found!")
        print(f"\n📦 Installation instructions:")
        if cli_name == 'skillhub':
            print(f"   npm install -g @clawdbot/skillhub")
            print(f"   or visit: https://skillhub.tencent.com")
        else:
            print(f"   npm install -g clawhub")
            print(f"   or visit: https://clawhub.ai")
        return 1
    
    # Show CLI version
    try:
        version_result = subprocess.run([cli_name, '--version'], capture_output=True, text=True, timeout=5)
        if version_result.returncode == 0:
            print(f"📋 Using {cli_name} {version_result.stdout.strip()}")
    except:
        pass
    
    # Run installation
    print(f"\n🚀 Running: {' '.join(cmd)}\n")
    print("-" * 60)
    
    try:
        # Run with real-time output
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Stream output
        for line in process.stdout:
            print(line, end='')
        
        process.wait()
        
        print("-" * 60)
        
        if process.returncode == 0:
            print(f"\n✅ Successfully installed {args.install_skill}!")
            print(f"   You can now use this skill in your OpenClaw agent.")
            return 0
        else:
            print(f"\n❌ Installation failed with code {process.returncode}")
            print(f"   Try running manually: {' '.join(cmd)}")
            return process.returncode
            
    except FileNotFoundError:
        print(f"❌ Command '{cli_name}' not found. Please install it first.")
        return 1
    except Exception as e:
        print(f"❌ Error during installation: {e}")
        return 1


def cmd_config(args):
    """Show configuration."""
    config = load_config()
    
    print("\n" + "="*50)
    print("Skill Rank Configuration")
    print("="*50 + "\n")
    
    print("Ranking Weights:")
    weights = config.get("weights", DEFAULT_CONFIG["weights"])
    for dim, weight in weights.items():
        print(f"  {dim:<15}: {weight*100:.0f}%")
    
    print(f"\nData Directory: {DATA_DIR}")
    print(f"Database: {DB_PATH}")
    print(f"Config: {CONFIG_PATH}")
    
    # Check last update time
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(last_updated) FROM skills")
    last_update = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM skills")
    total = cursor.fetchone()[0]
    conn.close()
    
    print(f"\nDatabase Status:")
    print(f"  Total Skills: {total}")
    print(f"  Last Updated: {last_update or 'Never'}")
    
    print("\nTo modify, edit the config file or set environment variables:")
    print("  GITHUB_TOKEN=your_token  # For GitHub API")
    
    print("\nAuto-Update:")
    print("  Run 'skill-rank --update' to refresh data")
    print("  Or set up cron: openclaw cron add --name 'skill-rank-update' --cron '0 3 * * *' --message 'skill-rank --update'")


def main():
    parser = argparse.ArgumentParser(
        description="Skill Rank - Multi-Platform Skill Ranking System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  skill-rank --update                    # Update local skills
  skill-rank --list --top 20             # Show top 20 skills
  skill-rank --search "pdf"              # Search for PDF-related skills
  skill-rank --info github               # Show details for 'github' skill
  skill-rank --install github            # Install the 'github' skill
  skill-rank --import-tencent --json-file skills.json  # Import from Tencent
        """
    )
    
    # Commands
    parser.add_argument('--list', action='store_true', help='List top skills')
    parser.add_argument('--top', type=int, help='Number of skills to list')
    parser.add_argument('--source', type=str, help='Filter by source (local/xfyun/tencent)')
    parser.add_argument('--search', dest='keyword', help='Search skills by keyword')
    parser.add_argument('--info', dest='skill_name', help='Show detailed skill info')
    parser.add_argument('--install', dest='install_skill', help='Install a skill')
    parser.add_argument('--dry-run', action='store_true', help='Preview installation without executing')
    parser.add_argument('--update', action='store_true', help='Update skill database')
    parser.add_argument('--config', action='store_true', help='Show configuration')
    
    # Import commands
    parser.add_argument('--import-xfyun', action='store_true', help='Import from Xfyun SkillHub')
    parser.add_argument('--import-tencent', action='store_true', help='Import from Tencent SkillHub')
    parser.add_argument('--json-file', type=str, help='JSON file with skill data')
    parser.add_argument('--json-data', type=str, help='JSON string with skill data')
    
    args = parser.parse_args()
    
    # Default to list if no command specified
    has_install = hasattr(args, 'install_skill') and args.install_skill
    has_info = hasattr(args, 'skill_name') and args.skill_name
    
    if not any([args.list, args.keyword, has_info, has_install, args.update, args.config,
                args.import_xfyun, args.import_tencent]):
        args.list = True
    
    if args.update:
        cmd_update(args)
    elif args.import_xfyun:
        cmd_import_xfyun(args)
    elif args.import_tencent:
        cmd_import_tencent(args)
    elif args.list:
        cmd_list(args)
    elif args.keyword:
        cmd_search(args)
    elif has_install:
        cmd_install(args)
    elif has_info:
        cmd_info(args)
    elif args.config:
        cmd_config(args)


if __name__ == "__main__":
    main()
