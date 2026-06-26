#!/usr/bin/env python3
"""
RUNSTR Analytics - Lightweight Version
Works with standard library only. Full analytics requires pandas/numpy.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Optional

RELAYS = [
    "wss://relay.damus.io",
    "wss://relay.primal.net",
    "wss://nos.lol",
    "wss://relay.nostr.band"
]

class RunstrAnalyticsLight:
    def __init__(self, nsec: str):
        self.nsec = nsec
        self.hex_sk = None
        self.hex_pk = None
        self.workouts = []
        self.habits = []
        self.journal = []
        
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
            age_days = (datetime.now(exported.tzinfo) - exported).days
            
            if age_days > 7:
                print(f"⚠️  Backup er {age_days} dager gammel.")
                print("💡 Ta ny backup i RUNSTR for nyeste data.")
            else:
                print(f"✅ Backup lastet ({age_days} dager gammel)")
            
            return data
            
        except Exception as e:
            print(f"❌ Feil ved henting: {e}")
            return None
    
    def _decrypt_content(self, content: str) -> Optional[str]:
        """Decrypt NIP-44 encrypted content (base64 gzip)."""
        try:
            # Use nak decrypt with sender-pubkey (self-encrypted)
            cmd = ["nak", "decrypt", "--sec", self.hex_sk, "--sender-pubkey", self.hex_pk, content]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            decrypted = result.stdout.strip()
            
            # Decompress gzip
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
            print("💡 Sjekk at nsec er korrekt")
            return None
    
    def parse_data(self, data: Dict):
        """Parse all data from backup."""
        self.workouts = data.get("workouts", [])
        self.habits = data.get("habits", [])
        self.journal = data.get("journal", [])
        
        # Parse workout timestamps
        for w in self.workouts:
            try:
                w['_start'] = datetime.fromisoformat(w.get('startTime', '').replace('Z', '+00:00'))
                w['_date'] = w['_start'].date()
                w['_duration_min'] = w.get('duration', 0) / 60
                w['_distance_km'] = w.get('distance', 0) / 1000
                
                # Calculate pace for running
                if w.get('type') == 'running' and w.get('distance', 0) > 0:
                    w['_pace_min_km'] = (w.get('duration', 0) / 60) / (w.get('distance', 0) / 1000)
                else:
                    w['_pace_min_km'] = None
            except:
                w['_start'] = None
    
    def analyze_trends(self, days: int = 30) -> Dict:
        """Analyze workout trends."""
        from datetime import timezone
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        recent = [w for w in self.workouts if w.get('_start') and w['_start'] >= cutoff]
        
        if not recent:
            return {}
        
        trends = {
            'total_workouts': len(recent),
            'total_distance_km': sum(w.get('_distance_km', 0) for w in recent),
            'total_duration_hours': sum(w.get('_duration_min', 0) for w in recent) / 60,
            'total_calories': sum(w.get('calories', 0) for w in recent),
        }
        
        # By type
        by_type = defaultdict(lambda: {'count': 0, 'distance': 0, 'duration': 0})
        for w in recent:
            t = w.get('type', 'unknown')
            by_type[t]['count'] += 1
            by_type[t]['distance'] += w.get('_distance_km', 0)
            by_type[t]['duration'] += w.get('_duration_min', 0)
        trends['by_type'] = dict(by_type)
        
        # Weekly stats
        weekly = defaultdict(lambda: {'count': 0, 'distance': 0})
        for w in recent:
            if w.get('_start'):
                week_key = f"{w['_start'].year}-W{w['_start'].isocalendar()[1]:02d}"
                weekly[week_key]['count'] += 1
                weekly[week_key]['distance'] += w.get('_distance_km', 0)
        
        trends['weekly'] = dict(sorted(weekly.items()))
        if weekly:
            trends['avg_workouts_per_week'] = sum(w['count'] for w in weekly.values()) / len(weekly)
        
        # Running pace analysis
        runs = [w for w in recent if w.get('type') == 'running' and w.get('_pace_min_km')]
        if runs:
            paces = [w['_pace_min_km'] for w in runs]
            trends['avg_pace_min_km'] = sum(paces) / len(paces)
            trends['best_pace_min_km'] = min(paces)
            
            # Simple trend (compare first half vs second half)
            mid = len(paces) // 2
            if len(paces) >= 4:
                first_half = sum(paces[:mid]) / mid if mid > 0 else 0
                second_half = sum(paces[mid:]) / (len(paces) - mid) if (len(paces) - mid) > 0 else 0
                trends['pace_trend_improving'] = second_half < first_half
                trends['pace_trend_pct'] = ((first_half - second_half) / first_half * 100) if first_half > 0 else 0
        
        # Day of week pattern
        dow_counts = defaultdict(int)
        for w in recent:
            if w.get('_start'):
                dow_counts[w['_start'].strftime('%A')] += 1
        if dow_counts:
            trends['most_active_day'] = max(dow_counts.items(), key=lambda x: x[1])[0]
        
        return trends
    
    def analyze_personal_records(self) -> Dict:
        """Find personal records by distance."""
        runs = [w for w in self.workouts if w.get('type') == 'running' and w.get('_pace_min_km')]
        if not runs:
            return {}
        
        prs = {}
        distances = [
            ('1K', 900, 1100),
            ('1M', 1500, 1700),
            ('5K', 4800, 5200),
            ('10K', 9800, 10200),
            ('Half', 21000, 22000)
        ]
        
        for name, min_m, max_m in distances:
            matches = [w for w in runs if min_m <= w.get('distance', 0) <= max_m]
            if matches:
                best = min(matches, key=lambda x: x['_pace_min_km'])
                prs[name] = {
                    'date': best['_date'],
                    'pace_min_km': best['_pace_min_km'],
                    'time_str': self._format_time(best.get('duration', 0)),
                    'distance_m': best.get('distance', 0)
                }
        
        return prs
    
    def _format_time(self, seconds: int) -> str:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}:{secs:02d}"
    
    def analyze_habits(self) -> Dict:
        """Analyze habit data."""
        if not self.habits:
            return {}
        
        habit_stats = {}
        for h in self.habits:
            habit_stats[h.get('name')] = {
                'current_streak': h.get('currentStreak', 0),
                'longest_streak': h.get('longestStreak', 0),
                'type': h.get('type', 'positive')
            }
        return habit_stats
    
    def analyze_mood_trends(self) -> Dict:
        """Analyze mood from journal."""
        if not self.journal:
            return {}
        
        mood_scores = {'bad': 1, 'low': 2, 'neutral': 3, 'good': 4, 'great': 5}
        scores = [mood_scores.get(e.get('mood', 'neutral'), 3) for e in self.journal]
        
        return {
            'entries': len(self.journal),
            'avg_mood': sum(scores) / len(scores) if scores else 0,
            'mood_distribution': {
                m: sum(1 for e in self.journal if e.get('mood') == m) 
                for m in set(e.get('mood') for e in self.journal)
            }
        }
    
    def generate_coaching_tips(self, trends: Dict, prs: Dict, habits: Dict, mood: Dict) -> List[str]:
        """Generate personalized coaching tips."""
        tips = []
        
        # Frequency
        avg_weekly = trends.get('avg_workouts_per_week', 0)
        if avg_weekly < 2:
            tips.append("🎯 Øk frekvensen: Prøv å få inn minst 3 økter/uke")
        elif avg_weekly > 5:
            tips.append("⚠️  Pass på restitusjonen — du trener mye!")
        else:
            tips.append("✅ Bra treningsfrekvens")
        
        # Pace trend
        if trends.get('pace_trend_improving'):
            pct = trends.get('pace_trend_pct', 0)
            tips.append(f"🚀 Du blir raskere! {pct:.1f}% forbedring i pace")
        
        # PRs
        if prs:
            latest = max(prs.items(), key=lambda x: str(x[1].get('date', '')))
            tips.append(f"🏆 Siste PR: {latest[0]} på {latest[1]['time_str']}")
        
        # Habits
        for name, stats in habits.items():
            if stats['current_streak'] > 7:
                tips.append(f"🔥 '{name}': {stats['current_streak']} dagers streak!")
        
        # Mood
        if mood.get('avg_mood', 0) >= 4:
            tips.append("😊 Bra humør i perioden — flott!")
        elif mood.get('avg_mood', 0) <= 2.5:
            tips.append("💙 Humøret ser lavt ut — prioriter søvn og rolige turer")
        
        # Variety
        by_type = trends.get('by_type', {})
        if len(by_type) == 1 and 'running' in by_type:
            tips.append("🔄 Vurder å blande inn styrke eller yoga for variasjon")
        
        return tips
    
    def print_report(self, trends: Dict, prs: Dict, habits: Dict, mood: Dict, tips: List[str]):
        """Print formatted report."""
        print("\n" + "="*60)
        print("📊 RUNSTR ANALYTICS - RAPPORT")
        print("="*60)
        
        print(f"\n🏃 ØKTER SISTE 30 DAGER")
        print(f"   Antall: {trends.get('total_workouts', 0)}")
        print(f"   Distanse: {trends.get('total_distance_km', 0):.1f} km")
        print(f"   Tid: {trends.get('total_duration_hours', 0):.1f} timer")
        print(f"   Kalorier: {trends.get('total_calories', 0):.0f}")
        
        if trends.get('avg_workouts_per_week'):
            print(f"   Gj.sn/uke: {trends['avg_workouts_per_week']:.1f} økter")
        
        # By type
        if trends.get('by_type'):
            print(f"\n📋 FORDELING ETTER TYPE")
            for t, s in trends['by_type'].items():
                print(f"   {t}: {s['count']} økter, {s['distance']:.1f} km")
        
        # Running stats
        if trends.get('avg_pace_min_km'):
            print(f"\n⚡ LØPESTATISTIKK")
            print(f"   Gj.sn. pace: {trends['avg_pace_min_km']:.2f} min/km")
            if trends.get('best_pace_min_km'):
                print(f"   Beste pace: {trends['best_pace_min_km']:.2f} min/km")
            if trends.get('pace_trend_improving'):
                print(f"   📈 Trend: Raskere! ({trends.get('pace_trend_pct', 0):.1f}%)")
        
        # Personal Records
        if prs:
            print(f"\n🏆 PERSONLIGE REKORDER")
            for dist, r in sorted(prs.items()):
                print(f"   {dist}: {r['time_str']} ({r['pace_min_km']:.2f} min/km)")
        
        # Habits
        if habits:
            print(f"\n🔥 VANER")
            for name, s in habits.items():
                print(f"   {name}: {s['current_streak']} dager (best: {s['longest_streak']})")
        
        # Mood
        if mood:
            print(f"\n😊 HUMØR")
            print(f"   Innslag: {mood.get('entries', 0)}")
            print(f"   Gj.sn: {mood.get('avg_mood', 0):.1f}/5")
        
        # Coaching tips
        if tips:
            print(f"\n💡 COACHING-TIPS")
            for tip in tips:
                print(f"   {tip}")
        
        print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description='RUNSTR Analytics - Lettversjon')
    parser.add_argument('--nsec', required=True, help='Din Nostr private key (nsec1...)')
    parser.add_argument('--days', type=int, default=30, help='Analyseperiode i dager')
    parser.add_argument('--insights', action='store_true', help='Generer forbedringstips')
    parser.add_argument('--format', default='terminal', choices=['terminal', 'json'])
    
    args = parser.parse_args()
    
    analytics = RunstrAnalyticsLight(args.nsec)
    
    if not analytics.decode_nsec():
        sys.exit(1)
    
    print(f"🔑 Laster nøkler for: {analytics.hex_pk[:16]}...")
    
    data = analytics.fetch_backup()
    if not data:
        sys.exit(1)
    
    analytics.parse_data(data)
    
    print(f"📊 Lastet: {len(analytics.workouts)} økter, {len(analytics.habits)} vaner, {len(analytics.journal)} dagbok-innslag")
    
    trends = analytics.analyze_trends(args.days)
    prs = analytics.analyze_personal_records()
    habits = analytics.analyze_habits()
    mood = analytics.analyze_mood_trends()
    
    tips = []
    if args.insights:
        tips = analytics.generate_coaching_tips(trends, prs, habits, mood)
    
    if args.format == 'terminal':
        analytics.print_report(trends, prs, habits, mood, tips)
    elif args.format == 'json':
        output = {
            'trends': trends,
            'personal_records': prs,
            'habits': habits,
            'mood': mood,
            'coaching_tips': tips
        }
        print(json.dumps(output, indent=2, default=str))
    
    print("\n✅ Analyse fullført!")


if __name__ == '__main__':
    main()
