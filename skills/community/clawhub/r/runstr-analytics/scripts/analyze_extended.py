#!/usr/bin/env python3
"""
RUNSTR Analytics - Extended Version with Local Cache
Week-to-week comparison, personal records, and local data storage.
"""

import argparse
import json
import sqlite3
import subprocess
import sys
import os
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from typing import Dict, List, Optional
from pathlib import Path

RELAYS = [
    "wss://relay.damus.io",
    "wss://relay.primal.net",
    "wss://nos.lol",
    "wss://relay.nostr.band"
]

# Local cache directory
CACHE_DIR = Path.home() / ".cache" / "runstr-analytics"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = CACHE_DIR / "runstr_cache.db"

class RunstrAnalyticsExtended:
    def __init__(self, nsec: str, use_cache: bool = True):
        self.nsec = nsec
        self.hex_sk = None
        self.hex_pk = None
        self.workouts = []
        self.habits = []
        self.journal = []
        self.use_cache = use_cache
        self.conn = None
        
    def init_cache(self):
        """Initialize SQLite cache with restrictive permissions."""
        # Ensure cache directory exists with restrictive permissions (user only)
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        os.chmod(CACHE_DIR, 0o700)  # Only user can read/write/execute
        
        self.conn = sqlite3.connect(DB_PATH)
        
        # Set restrictive permissions on database file
        if DB_PATH.exists():
            os.chmod(DB_PATH, 0o600)  # Only user can read/write
        
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workouts (
                id TEXT PRIMARY KEY,
                type TEXT,
                start_time TEXT,
                duration_sec INTEGER,
                distance_m REAL,
                calories INTEGER,
                pace_min_km REAL,
                week_key TEXT,
                data TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekly_stats (
                week_key TEXT PRIMARY KEY,
                total_workouts INTEGER,
                total_distance_km REAL,
                total_duration_hours REAL,
                total_calories INTEGER,
                strength_count INTEGER,
                walking_count INTEGER,
                running_count INTEGER,
                avg_pace REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personal_records (
                distance TEXT PRIMARY KEY,
                best_time_sec INTEGER,
                best_pace_min_km REAL,
                date TEXT,
                workout_id TEXT
            )
        ''')
        
        self.conn.commit()
        
    def decode_nsec(self) -> bool:
        """Decode nsec to hex keys using stdin to avoid exposing secret in CLI."""
        try:
            # Use stdin instead of CLI args to prevent nsec exposure in ps/process list
            result = subprocess.run(
                ["nak", "decode"],
                input=self.nsec,
                capture_output=True, text=True, check=True
            )
            self.hex_sk = result.stdout.strip()
            
            result = subprocess.run(
                ["nak", "key", "public", self.hex_sk],
                capture_output=True, text=True, check=True
            )
            self.hex_pk = result.stdout.strip()
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error decoding nsec: {e}")
            return False
    
    def fetch_backup(self) -> Optional[Dict]:
        """Fetch encrypted backup from Nostr."""
        print("📡 Henter RUNSTR backup fra Nostr...")
        
        try:
            cmd = [
                "nak", "req",
                "-k", "30078",
                "-a", self.hex_pk,
                "-t", "d=runstr-workout-backup",
                "-l", "1"
            ] + RELAYS
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if not result.stdout.strip():
                print("❌ Ingen backup funnet på Nostr.")
                print("💡 Åpne RUNSTR > Settings > Backup og opprett en.")
                return None
            
            event = json.loads(result.stdout.strip().split('\n')[0])
            content = event.get("content", "")
            
            decrypted = self._decrypt_content(content)
            if not decrypted:
                return None
            
            data = json.loads(decrypted)
            
            exported = datetime.fromisoformat(data.get("exportedAt", "").replace('Z', '+00:00'))
            age_days = (datetime.now(timezone.utc) - exported).days
            
            if age_days > 7:
                print(f"⚠️  Backup er {age_days} dager gammel.")
            else:
                print(f"✅ Backup lastet ({age_days} dager gammel)")
            
            return data
            
        except Exception as e:
            print(f"❌ Feil ved henting: {e}")
            return None
    
    def _decrypt_content(self, content: str) -> Optional[str]:
        """Decrypt NIP-44 encrypted content."""
        try:
            cmd = ["nak", "decrypt", "--sec", self.hex_sk, "--sender-pubkey", self.hex_pk, content]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            decrypted = result.stdout.strip()
            
            import base64
            import gzip
            try:
                decoded = base64.b64decode(decrypted)
                decompressed = gzip.decompress(decoded)
                return decompressed.decode('utf-8')
            except Exception as e:
                print(f"⚠️  Kunne ikke pakke ut gzip: {e}")
                return decrypted
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Dekryptering feilet: {e}")
            return None
    
    def parse_and_cache_data(self, data: Dict):
        """Parse data and store in local cache."""
        self.workouts = data.get("workouts", [])
        self.habits = data.get("habits", [])
        self.journal = data.get("journal", [])
        
        if not self.use_cache or not self.conn:
            return
        
        cursor = self.conn.cursor()
        
        for w in self.workouts:
            try:
                start = datetime.fromisoformat(w.get('startTime', '').replace('Z', '+00:00'))
                week_key = f"{start.year}-W{start.isocalendar()[1]:02d}"
                
                duration = w.get('duration', 0)
                distance_m = w.get('distance', 0)
                
                # Calculate pace for running/walking
                pace = None
                if w.get('type') in ['running', 'walking'] and distance_m > 0:
                    pace = (duration / 60) / (distance_m / 1000)
                
                cursor.execute('''
                    INSERT OR REPLACE INTO workouts 
                    (id, type, start_time, duration_sec, distance_m, calories, pace_min_km, week_key, data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    w.get('id'),
                    w.get('type'),
                    start.isoformat(),
                    duration,
                    distance_m,
                    w.get('calories', 0),
                    pace,
                    week_key,
                    json.dumps(w)
                ))
            except Exception as e:
                pass
        
        self.conn.commit()
        print(f"💾 Lagret {len(self.workouts)} økter i lokal cache")
    
    def load_from_cache(self, days: int = 30) -> bool:
        """Load recent workouts from local cache."""
        if not self.use_cache or not DB_PATH.exists():
            return False
        
        try:
            self.conn = sqlite3.connect(DB_PATH)
            cursor = self.conn.cursor()
            
            cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
            
            cursor.execute('''
                SELECT data FROM workouts WHERE start_time >= ? ORDER BY start_time
            ''', (cutoff,))
            
            rows = cursor.fetchall()
            self.workouts = [json.loads(row[0]) for row in rows]
            
            print(f"📂 Lastet {len(self.workouts)} økter fra cache")
            return True
            
        except Exception as e:
            print(f"⚠️  Kunne ikke lese cache: {e}")
            return False
    
    def analyze_weekly_comparison(self, weeks: int = 4) -> List[Dict]:
        """Compare stats week by week."""
        if not self.conn:
            return []
        
        cursor = self.conn.cursor()
        
        # Get all weeks in descending order
        cursor.execute('''
            SELECT week_key, 
                   COUNT(*) as workouts,
                   SUM(distance_m)/1000.0 as distance_km,
                   SUM(duration_sec)/3600.0 as hours,
                   SUM(calories) as calories,
                   AVG(pace_min_km) as avg_pace
            FROM workouts
            WHERE week_key IS NOT NULL
            GROUP BY week_key
            ORDER BY week_key DESC
            LIMIT ?
        ''', (weeks,))
        
        rows = cursor.fetchall()
        
        weekly_data = []
        for row in rows:
            weekly_data.append({
                'week': row[0],
                'workouts': row[1] or 0,
                'distance_km': round(row[2] or 0, 1),
                'hours': round(row[3] or 0, 1),
                'calories': row[4] or 0,
                'avg_pace': round(row[5], 2) if row[5] else None
            })
        
        return weekly_data
    
    def analyze_personal_records(self) -> Dict:
        """Find personal records by distance."""
        runs = [w for w in self.workouts 
                if w.get('type') == 'running' and w.get('distance', 0) > 0]
        
        if not runs:
            return {}
        
        prs = {}
        distances = [
            ('1K', 900, 1100),
            ('5K', 4800, 5200),
            ('10K', 9800, 10200),
            ('Half', 21000, 22000)
        ]
        
        for name, min_m, max_m in distances:
            matches = [w for w in runs if min_m <= w.get('distance', 0) <= max_m]
            if matches:
                best = min(matches, key=lambda x: x.get('duration', 999999) / max(x.get('distance', 1), 1))
                pace = (best.get('duration', 0) / 60) / (best.get('distance', 1) / 1000)
                
                # Format time as MM:SS
                secs = best.get('duration', 0)
                time_str = f"{secs//60}:{secs%60:02d}"
                
                prs[name] = {
                    'date': best.get('startTime', '')[:10],
                    'time_str': time_str,
                    'pace_min_km': pace,
                    'distance_m': best.get('distance', 0)
                }
                
                # Cache PR
                if self.conn:
                    cursor = self.conn.cursor()
                    cursor.execute('''
                        INSERT OR REPLACE INTO personal_records
                        (distance, best_time_sec, best_pace_min_km, date, workout_id)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (name, secs, pace, best.get('startTime', '')[:10], best.get('id')))
                    self.conn.commit()
        
        return prs
    
    def calculate_trends(self, weekly_data: List[Dict]) -> Dict:
        """Calculate trends between weeks."""
        if len(weekly_data) < 2:
            return {}
        
        trends = {}
        latest = weekly_data[0]
        previous = weekly_data[1]
        
        trends['workouts_change'] = latest['workouts'] - previous['workouts']
        trends['distance_change'] = latest['distance_km'] - previous['distance_km']
        trends['calories_change'] = latest['calories'] - previous['calories']
        
        # Calculate percentage changes
        if previous['workouts'] > 0:
            trends['workouts_pct'] = (trends['workouts_change'] / previous['workouts']) * 100
        if previous['distance_km'] > 0:
            trends['distance_pct'] = (trends['distance_change'] / previous['distance_km']) * 100
        
        return trends
    
    def generate_extended_tips(self, weekly_data: List[Dict], trends: Dict, prs: Dict) -> List[str]:
        """Generate extended coaching tips."""
        tips = []
        
        # Weekly comparison tips
        if weekly_data:
            latest = weekly_data[0]
            tips.append(f"📅 Denne uken ({latest['week']}): {latest['workouts']} økter, {latest['distance_km']} km")
            
            if len(weekly_data) > 1:
                prev = weekly_data[1]
                if trends.get('workouts_change', 0) > 0:
                    tips.append(f"📈 {trends['workouts_change']:+d} økter vs forrige uke")
                elif trends.get('workouts_change', 0) < 0:
                    tips.append(f"📉 {trends['workouts_change']:+d} økter vs forrige uke — hvileuke?")
        
        # Frequency tip
        if weekly_data and weekly_data[0]['workouts'] > 10:
            tips.append("⚠️  Høy treningsmengde — sørg for nok restitusjon")
        elif weekly_data and weekly_data[0]['workouts'] < 3:
            tips.append("🎯 Lav treningsmengde — prøv å øke til minst 4 økter/uke")
        
        # PR tips
        if prs:
            tips.append(f"🏆 Personlige rekorder: {', '.join(prs.keys())}")
            for dist, record in prs.items():
                tips.append(f"   • {dist}: {record['time_str']} ({record['pace_min_km']:.2f} min/km)")
        else:
            tips.append("💡 Ingen løpe-PR-er funnet — prøv å logge løpeturer med GPS")
        
        # Consistency tip
        if len(weekly_data) >= 3:
            avg_workouts = sum(w['workouts'] for w in weekly_data) / len(weekly_data)
            variance = max(w['workouts'] for w in weekly_data) - min(w['workouts'] for w in weekly_data)
            if variance <= 2:
                tips.append(f"✅ Bra konsistens: {avg_workouts:.1f} økter/uke i snitt")
            else:
                tips.append("🔄 Varierende treningsmengde — prøv å holde det jevnere")
        
        return tips
    
    def generate_ascii_chart(self, data: List[float], labels: List[str], title: str, width: int = 40) -> str:
        """Generate ASCII bar chart."""
        if not data or max(data) == 0:
            return ""
        
        max_val = max(data)
        lines = [f"\n📊 {title}"]
        
        for label, value in zip(labels, data):
            bar_len = int((value / max_val) * width) if max_val > 0 else 0
            bar = "█" * bar_len
            lines.append(f"   {label:<10} |{bar:<{width}}| {value:.1f}")
        
        return "\n".join(lines)
    
    def generate_trend_sparkline(self, values: List[float]) -> str:
        """Generate sparkline trend indicator."""
        if len(values) < 2:
            return ""
        
        chars = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
        min_val, max_val = min(values), max(values)
        
        if max_val == min_val:
            return "▃" * len(values)
        
        sparkline = ""
        for v in values:
            idx = int(((v - min_val) / (max_val - min_val)) * (len(chars) - 1))
            sparkline += chars[idx]
        
        direction = "📈" if values[-1] > values[0] else "📉" if values[-1] < values[0] else "➡️"
        return f"{sparkline} {direction}"
    
    def print_extended_report(self, weekly_data: List[Dict], trends: Dict, prs: Dict, tips: List[str]):
        """Print extended formatted report with charts."""
        print("\n" + "="*70)
        print("📊 RUNSTR ANALYTICS - UTVidET RAPPORT")
        print("="*70)
        
        # Weekly comparison table
        if weekly_data:
            print(f"\n📅 UKETIL-UKET SAMMENLIGNING")
            print(f"   {'Uke':<12} {'Økter':<8} {'Km':<8} {'Timer':<8} {'Kal':<8}")
            print(f"   {'-'*50}")
            for w in weekly_data[:4]:
                print(f"   {w['week']:<12} {w['workouts']:<8} {w['distance_km']:<8} {w['hours']:<8} {w['calories']:<8}")
        
        # ASCII Charts
        if weekly_data:
            weeks = [w['week'] for w in weekly_data[:4]]
            weeks.reverse()  # Oldest first for chart
            
            # Workouts chart
            workouts = [w['workouts'] for w in weekly_data[:4]]
            workouts.reverse()
            print(self.generate_ascii_chart(workouts, weeks, "ØKTER PER UKE"))
            
            # Distance chart
            distances = [w['distance_km'] for w in weekly_data[:4]]
            distances.reverse()
            print(self.generate_ascii_chart(distances, weeks, "KILOMETER PER UKE"))
            
            # Calories chart (scaled)
            calories = [w['calories'] / 100 for w in weekly_data[:4]]  # Scale for display
            calories.reverse()
            print(self.generate_ascii_chart(calories, weeks, "KALORIER PER UKE (/100)"))
        
        # Sparkline trends
        if weekly_data and len(weekly_data) >= 2:
            print(f"\n📈 TREND-OVERSIKT")
            workouts_trend = [w['workouts'] for w in weekly_data[:4]]
            workouts_trend.reverse()
            print(f"   Økter:      {self.generate_trend_sparkline(workouts_trend)}")
            
            dist_trend = [w['distance_km'] for w in weekly_data[:4]]
            dist_trend.reverse()
            print(f"   Distanse:   {self.generate_trend_sparkline(dist_trend)}")
        
        # Trends numbers
        if trends:
            print(f"\n📊 ENDRING SISTE UKE vs FORRIGE")
            print(f"   Økter:    {trends.get('workouts_change', 0):+d} ({trends.get('workouts_pct', 0):+.1f}%)")
            print(f"   Distanse: {trends.get('distance_change', 0):+.1f} km ({trends.get('distance_pct', 0):+.1f}%)")
        
        # Personal Records
        if prs:
            print(f"\n🏆 PERSONLIGE REKORDER (Løping)")
            for dist, r in sorted(prs.items()):
                print(f"   {dist:>5}: {r['time_str']} ({r['pace_min_km']:.2f} min/km) — {r['date']}")
        else:
            print(f"\n💡 Ingen løpe-PR-er — prøv å logge løpeturer med GPS for å se rekorder her")
        
        # Coaching tips
        if tips:
            print(f"\n💡 COACHING-TIPS")
            for tip in tips:
                print(f"   {tip}")
        
        print("\n" + "="*70)


def main():
    parser = argparse.ArgumentParser(description='RUNSTR Analytics Extended')
    parser.add_argument('--nsec', help='Din Nostr private key')
    parser.add_argument('--days', type=int, default=30, help='Analyseperiode i dager')
    parser.add_argument('--insights', action='store_true', help='Generer forbedringstips')
    parser.add_argument('--no-cache', action='store_true', help='Ikke bruk lokal cache')
    parser.add_argument('--force-refresh', action='store_true', help='Tving ny henting fra Nostr')
    
    args = parser.parse_args()
    
    analytics = RunstrAnalyticsExtended(args.nsec, use_cache=not args.no_cache)
    
    # Initialize cache
    if analytics.use_cache:
        analytics.init_cache()
    
    # Try to load from cache first (unless force refresh)
    loaded_from_cache = False
    if not args.force_refresh and analytics.use_cache:
        loaded_from_cache = analytics.load_from_cache(args.days)
    
    # If no cache or force refresh, fetch from Nostr
    if not loaded_from_cache:
        if not args.nsec:
            print("❌ Krever --nsec for å hente fra Nostr")
            sys.exit(1)
        
        if not analytics.decode_nsec():
            sys.exit(1)
        
        print(f"🔑 Laster nøkler for: {analytics.hex_pk[:16]}...")
        
        data = analytics.fetch_backup()
        if not data:
            sys.exit(1)
        
        analytics.parse_and_cache_data(data)
    
    print(f"📊 Analyserer {len(analytics.workouts)} økter...")
    
    # Run analyses
    weekly_data = analytics.analyze_weekly_comparison(weeks=4)
    prs = analytics.analyze_personal_records()
    trends = analytics.calculate_trends(weekly_data)
    
    tips = []
    if args.insights:
        tips = analytics.generate_extended_tips(weekly_data, trends, prs)
    
    # Print report
    analytics.print_extended_report(weekly_data, trends, prs, tips)
    
    if analytics.conn:
        analytics.conn.close()
    
    print("\n✅ Analyse fullført!")
    print(f"💾 Data lagret i: {DB_PATH}")


if __name__ == '__main__':
    main()
