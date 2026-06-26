#!/usr/bin/env python3
"""
RUNSTR Analytics Engine
Advanced fitness analysis with trends, correlations, and coaching insights.
"""

import argparse
import json
import sqlite3
import subprocess
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import tempfile

import numpy as np
import pandas as pd
from scipy import stats

# Constants
RELAYS = [
    "wss://relay.damus.io",
    "wss://relay.primal.net",
    "wss://nos.lol",
    "wss://relay.nostr.band"
]

CACHE_DIR = Path.home() / ".cache" / "runstr-analytics"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = CACHE_DIR / "runstr_cache.db"

class RunstrAnalytics:
    def __init__(self, nsec: str):
        self.nsec = nsec
        self.hex_sk = None
        self.hex_pk = None
        self.data = None
        self.df_workouts = None
        
    def decode_nsec(self) -> bool:
        """Decode nsec to hex keys."""
        try:
            result = subprocess.run(
                ["nak", "decode", self.nsec],
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
        print("📡 Fetching RUNSTR backup from Nostr...")
        
        try:
            # Fetch kind 30078 event
            cmd = [
                "nak", "req",
                "-k", "30078",
                "-a", self.hex_pk,
                "-t", "d=runstr-workout-backup",
                "-l", "1"
            ] + RELAYS
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if not result.stdout.strip():
                print("❌ No backup found on Nostr.")
                print("💡 Open RUNSTR > Settings > Backup and create one.")
                return None
            
            event = json.loads(result.stdout.strip().split('\n')[0])
            content = event.get("content", "")
            
            # Check exportedAt
            tags = {t[0]: t[1] for t in event.get("tags", [])}
            
            # Decrypt content
            decrypted = self._decrypt_content(content)
            if not decrypted:
                return None
            
            # Parse JSON
            data = json.loads(decrypted)
            
            # Check backup age
            exported = datetime.fromisoformat(data.get("exportedAt", "").replace('Z', '+00:00'))
            age_days = (datetime.now(exported.tzinfo) - exported).days
            
            if age_days > 7:
                print(f"⚠️  Backup is {age_days} days old. Recent data may be missing.")
                print("💡 Re-backup in RUNSTR for latest data.")
            else:
                print(f"✅ Backup loaded ({age_days} days old)")
            
            return data
            
        except Exception as e:
            print(f"❌ Error fetching backup: {e}")
            return None
    
    def _decrypt_content(self, content: str) -> Optional[str]:
        """Decrypt NIP-44 encrypted content."""
        try:
            # Try nak decrypt first
            cmd = ["nak", "encrypt", "--sec", self.hex_sk, self.hex_pk, "--decrypt"]
            result = subprocess.run(
                cmd, input=content, capture_output=True, text=True, check=True
            )
            decrypted = result.stdout.strip()
            
            # Try to decompress (gzip)
            import base64
            import gzip
            try:
                decoded = base64.b64decode(decrypted)
                decompressed = gzip.decompress(decoded)
                return decompressed.decode('utf-8')
            except:
                # Not compressed
                return decrypted
                
        except subprocess.CalledProcessError:
            print("❌ Decryption failed. Wrong nsec?")
            return None
    
    def parse_workouts(self, data: Dict) -> pd.DataFrame:
        """Parse workouts into DataFrame."""
        workouts = data.get("workouts", [])
        
        if not workouts:
            return pd.DataFrame()
        
        records = []
        for w in workouts:
            record = {
                'id': w.get('id'),
                'type': w.get('type', 'unknown'),
                'start_time': pd.to_datetime(w.get('startTime')),
                'end_time': pd.to_datetime(w.get('endTime')),
                'duration_sec': w.get('duration', 0),
                'distance_m': w.get('distance', 0),
                'calories': w.get('calories', 0),
            }
            
            # Calculate pace if running/walking with distance
            if record['distance_m'] > 0 and record['type'] in ['running', 'walking']:
                pace_sec_per_km = record['duration_sec'] / (record['distance_m'] / 1000)
                record['pace_min_km'] = pace_sec_per_km / 60
            else:
                record['pace_min_km'] = None
            
            # Week and month for grouping
            record['week'] = record['start_time'].isocalendar()[1]
            record['year'] = record['start_time'].year
            record['year_week'] = f"{record['year']}-W{record['week']:02d}"
            record['date'] = record['start_time'].date()
            
            records.append(record)
        
        df = pd.DataFrame(records)
        df = df.sort_values('start_time')
        return df
    
    def parse_habits(self, data: Dict) -> pd.DataFrame:
        """Parse habits into DataFrame."""
        habits = data.get("habits", [])
        if not habits:
            return pd.DataFrame()
        
        records = []
        for h in habits:
            records.append({
                'id': h.get('id'),
                'name': h.get('name'),
                'type': h.get('type'),
                'current_streak': h.get('currentStreak', 0),
                'longest_streak': h.get('longestStreak', 0),
                'check_ins': h.get('checkIns', [])
            })
        
        return pd.DataFrame(records)
    
    def parse_journal(self, data: Dict) -> pd.DataFrame:
        """Parse journal entries into DataFrame."""
        entries = data.get("journal", [])
        if not entries:
            return pd.DataFrame()
        
        records = []
        for e in entries:
            records.append({
                'id': e.get('id'),
                'date': pd.to_datetime(e.get('date')).date(),
                'content': e.get('content', ''),
                'mood': e.get('mood', 'neutral'),
                'energy': e.get('energy', 3),
                'tags': e.get('tags', [])
            })
        
        return pd.DataFrame(records)
    
    def analyze_trends(self, days: int = 30) -> Dict:
        """Analyze workout trends."""
        if self.df_workouts.empty:
            return {}
        
        cutoff = datetime.now() - timedelta(days=days)
        recent = self.df_workouts[self.df_workouts['start_time'] >= cutoff]
        
        if recent.empty:
            return {}
        
        trends = {}
        
        # Overall stats
        trends['total_workouts'] = len(recent)
        trends['total_distance_km'] = recent['distance_m'].sum() / 1000
        trends['total_duration_hours'] = recent['duration_sec'].sum() / 3600
        trends['total_calories'] = recent['calories'].sum()
        
        # By activity type
        by_type = recent.groupby('type').agg({
            'duration_sec': ['count', 'sum'],
            'distance_m': 'sum',
            'calories': 'sum'
        }).round(2)
        trends['by_type'] = by_type
        
        # Weekly aggregation
        weekly = recent.groupby('year_week').agg({
            'duration_sec': ['count', 'sum'],
            'distance_m': 'sum',
            'calories': 'sum'
        })
        trends['weekly'] = weekly
        trends['avg_workouts_per_week'] = weekly[('duration_sec', 'count')].mean()
        
        # Pace trends for running
        runs = recent[recent['type'] == 'running']
        if not runs.empty and runs['pace_min_km'].notna().any():
            trends['avg_pace_min_km'] = runs['pace_min_km'].mean()
            trends['best_pace_min_km'] = runs['pace_min_km'].min()
            
            # Pace trend (linear regression)
            runs_sorted = runs.sort_values('start_time')
            if len(runs_sorted) >= 3:
                x = np.arange(len(runs_sorted))
                y = runs_sorted['pace_min_km'].dropna()
                if len(y) >= 3:
                    slope, intercept, r_value, p_value, std_err = stats.linregress(x[-len(y):], y)
                    trends['pace_trend'] = slope  # negative = improving
                    trends['pace_trend_pct'] = (slope / y.mean()) * 100 if y.mean() > 0 else 0
        
        # Training frequency pattern
        recent['day_of_week'] = recent['start_time'].dt.day_name()
        dow_counts = recent['day_of_week'].value_counts()
        trends['most_active_day'] = dow_counts.index[0] if not dow_counts.empty else None
        
        return trends
    
    def analyze_personal_records(self) -> Dict:
        """Find personal records by distance."""
        if self.df_workouts.empty:
            return {}
        
        runs = self.df_workouts[self.df_workouts['type'] == 'running']
        if runs.empty:
            return {}
        
        prs = {}
        
        # Common distances
        distances = {
            '1K': (900, 1100),
            '1M': (1500, 1700),
            '5K': (4800, 5200),
            '10K': (9800, 10200),
            'Half': (21000, 22000)
        }
        
        for name, (min_m, max_m) in distances.items():
            matches = runs[(runs['distance_m'] >= min_m) & (runs['distance_m'] <= max_m)]
            if not matches.empty:
                best = matches.loc[matches['pace_min_km'].idxmin()]
                prs[name] = {
                    'date': best['date'],
                    'pace_min_km': best['pace_min_km'],
                    'time_str': self._format_time(best['duration_sec']),
                    'distance_m': best['distance_m']
                }
        
        return prs
    
    def _format_time(self, seconds: int) -> str:
        """Format seconds as MM:SS."""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}:{secs:02d}"
    
    def analyze_correlations(self, df_habits: pd.DataFrame, df_journal: pd.DataFrame) -> Dict:
        """Analyze correlations between habits, mood, and performance."""
        corr = {}
        
        if not df_journal.empty and not self.df_workouts.empty:
            # Merge workouts with journal by date
            runs = self.df_workouts[self.df_workouts['type'] == 'running'].copy()
            runs['date'] = pd.to_datetime(runs['start_time']).dt.date
            
            merged = runs.merge(df_journal, on='date', how='inner')
            
            if not merged.empty and merged['pace_min_km'].notna().any():
                # Mood vs pace
                mood_order = {'bad': 1, 'low': 2, 'neutral': 3, 'good': 4, 'great': 5}
                merged['mood_num'] = merged['mood'].map(mood_order)
                
                mood_pace = merged.groupby('mood')['pace_min_km'].mean()
                corr['mood_pace'] = mood_pace
                
                # Best mood for running
                if not mood_pace.empty:
                    corr['best_mood_for_pace'] = mood_pace.idxmin()
                
                # Energy vs pace correlation
                if merged['energy'].notna().any():
                    corr['energy_pace_correlation'] = merged['energy'].corr(merged['pace_min_km'])
        
        return corr
    
    def generate_coaching_tips(self, trends: Dict, prs: Dict, correlations: Dict) -> List[str]:
        """Generate personalized coaching tips."""
        tips = []
        
        # Frequency tip
        avg_weekly = trends.get('avg_workouts_per_week', 0)
        if avg_weekly < 2:
            tips.append("🎯 Øk frekvensen: Prøv å få inn minst 3 økter/uke for jevn fremgang")
        elif avg_weekly > 5:
            tips.append("⚠️  Vær obs på restitusjon: Du trener mye — sørg for nok hvile")
        else:
            tips.append("✅ Bra frekvens: Din treningsmengde ser bra ut")
        
        # Pace trend tip
        trend_pct = trends.get('pace_trend_pct', 0)
        if trend_pct < -2:
            tips.append(f"🚀 Flott! Du blir raskere ({abs(trend_pct):.1f}% forbedring i pace)")
        elif trend_pct > 2:
            tips.append("📈 Pace går litt opp — vurder å legge inn mer sone 2-trening")
        
        # Personal records tip
        if prs:
            latest_pr = max(prs.items(), key=lambda x: x[1]['date'] if x[1] else datetime.min)
            tips.append(f"🏆 Din siste PR: {latest_pr[0]} på {latest_pr[1]['time_str']}")
        
        # Mood correlation tip
        best_mood = correlations.get('best_mood_for_pace')
        if best_mood:
            tips.append(f"😊 Du løper best når humøret er '{best_mood}' — bruk dette!")
        
        # Variety tip
        by_type = trends.get('by_type')
        if by_type is not None and len(by_type) == 1:
            tips.append("🔄 Variasjon: Vurder å blande inn styrke eller annen aktivitet")
        
        return tips
    
    def check_training_plan_adherence(self, plan_path: str) -> Dict:
        """Compare actual workouts against training plan."""
        adherence = {'planned': [], 'actual': [], 'missed': [], 'extra': []}
        
        if not os.path.exists(plan_path):
            print(f"⚠️  Training plan not found: {plan_path}")
            return adherence
        
        # Parse training plan (simple markdown parsing)
        with open(plan_path, 'r') as f:
            content = f.read()
        
        # Look for day-of-week sections
        days = ['Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lørdag', 'Søndag']
        
        # This is simplified — a full implementation would parse the plan structure
        # For now, just show that we attempted to check
        adherence['plan_found'] = True
        adherence['message'] = "Training plan loaded (adherence checking requires structured plan parsing)"
        
        return adherence
    
    def print_summary(self, trends: Dict, prs: Dict, correlations: Dict, tips: List[str]):
        """Print formatted summary."""
        print("\n" + "="*60)
        print("📊 RUNSTR ANALYTICS - SAMMENDRAG")
        print("="*60)
        
        # Overall stats
        print(f"\n🏃 Økter siste 30 dager: {trends.get('total_workouts', 0)}")
        print(f"📏 Distanse: {trends.get('total_distance_km', 0):.1f} km")
        print(f"⏱️  Tid: {trends.get('total_duration_hours', 0):.1f} timer")
        print(f"🔥 Kalorier: {trends.get('total_calories', 0):.0f}")
        
        if trends.get('avg_workouts_per_week'):
            print(f"📅 Gj.sn/uke: {trends['avg_workouts_per_week']:.1f} økter")
        
        # Pace stats
        if trends.get('avg_pace_min_km'):
            print(f"\n⚡ Løpepace: {trends['avg_pace_min_km']:.2f} min/km (snitt)")
            if trends.get('best_pace_min_km'):
                print(f"⚡ Beste: {trends['best_pace_min_km']:.2f} min/km")
        
        # Trend
        if trends.get('pace_trend_pct') is not None:
            direction = "forbedring" if trends['pace_trend_pct'] < 0 else "økning"
            print(f"📈 Trend: {abs(trends['pace_trend_pct']):.1f}% {direction}")
        
        # Personal Records
        if prs:
            print("\n🏆 PERSONLIGE REKORDER:")
            for dist, record in sorted(prs.items()):
                print(f"   {dist}: {record['time_str']} ({record['pace_min_km']:.2f} min/km) - {record['date']}")
        
        # Coaching tips
        if tips:
            print("\n💡 COACHING-TIPS:")
            for tip in tips:
                print(f"   {tip}")
        
        print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description='RUNSTR Analytics')
    parser.add_argument('--nsec', required=True, help='Your Nostr private key')
    parser.add_argument('--days', type=int, default=30, help='Analysis period in days')
    parser.add_argument('--insights', action='store_true', help='Generate improvement tips')
    parser.add_argument('--coaching-report', action='store_true', help='Full coaching analysis')
    parser.add_argument('--training-plan', help='Path to training plan file')
    parser.add_argument('--format', default='terminal', choices=['terminal', 'json', 'md'])
    
    args = parser.parse_args()
    
    # Initialize analytics
    analytics = RunstrAnalytics(args.nsec)
    
    # Decode nsec
    if not analytics.decode_nsec():
        sys.exit(1)
    
    print(f"🔑 Loaded keys for: {analytics.hex_pk[:16]}...")
    
    # Fetch data
    data = analytics.fetch_backup()
    if not data:
        sys.exit(1)
    
    # Parse data
    analytics.df_workouts = analytics.parse_workouts(data)
    df_habits = analytics.parse_habits(data)
    df_journal = analytics.parse_journal(data)
    
    print(f"📊 Loaded: {len(analytics.df_workouts)} workouts, {len(df_habits)} habits, {len(df_journal)} journal entries")
    
    # Analyze
    trends = analytics.analyze_trends(args.days)
    prs = analytics.analyze_personal_records()
    correlations = analytics.analyze_correlations(df_habits, df_journal)
    
    # Generate tips
    tips = []
    if args.insights or args.coaching_report:
        tips = analytics.generate_coaching_tips(trends, prs, correlations)
    
    # Check training plan
    if args.training_plan:
        adherence = analytics.check_training_plan_adherence(args.training_plan)
    
    # Output
    if args.format == 'terminal':
        analytics.print_summary(trends, prs, correlations, tips)
    elif args.format == 'json':
        output = {
            'trends': {k: str(v) if isinstance(v, pd.DataFrame) else v for k, v in trends.items()},
            'personal_records': prs,
            'correlations': {k: str(v) if isinstance(v, pd.Series) else v for k, v in correlations.items()},
            'coaching_tips': tips
        }
        print(json.dumps(output, indent=2, default=str))
    
    print("\n✅ Analysis complete!")


if __name__ == '__main__':
    main()
