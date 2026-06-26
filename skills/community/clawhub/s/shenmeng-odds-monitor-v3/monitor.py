#!/usr/bin/env python3
"""
盘口变化监控器 - 主监控脚本
实时监控体育博彩盘口变化
"""

import asyncio
import json
import os
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False
    print("警告: aiohttp 未安装，仅支持同步模式")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


@dataclass
class OddsSnapshot:
    """赔率快照"""
    timestamp: str
    match_id: str
    home_team: str
    away_team: str
    bookmaker: str
    market: str
    outcome: str
    odds: float
    point: Optional[float] = None  # 让分/大小球盘口
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class OddsChange:
    """赔率变化记录"""
    match_id: str
    bookmaker: str
    market: str
    outcome: str
    old_odds: float
    new_odds: float
    change_pct: float
    timestamp: str
    change_type: str  # 'significant', 'major', 'minor'
    signal: Optional[str] = None  # 检测到的信号


class DataStorage:
    """数据存储管理"""
    
    def __init__(self, db_path: str = "odds_data.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 赔率快照表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS odds_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                match_id TEXT,
                home_team TEXT,
                away_team TEXT,
                bookmaker TEXT,
                market TEXT,
                outcome TEXT,
                odds REAL,
                point REAL
            )
        ''')
        
        # 变化记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS odds_changes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id TEXT,
                bookmaker TEXT,
                market TEXT,
                outcome TEXT,
                old_odds REAL,
                new_odds REAL,
                change_pct REAL,
                timestamp TEXT,
                change_type TEXT,
                signal TEXT
            )
        ''')
        
        # 监控配置表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monitoring_config (
                match_id TEXT PRIMARY KEY,
                home_team TEXT,
                away_team TEXT,
                is_active INTEGER,
                alert_threshold REAL,
                created_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_snapshot(self, snapshot: OddsSnapshot):
        """保存赔率快照"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO odds_snapshots 
            (timestamp, match_id, home_team, away_team, bookmaker, market, outcome, odds, point)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            snapshot.timestamp, snapshot.match_id, snapshot.home_team,
            snapshot.away_team, snapshot.bookmaker, snapshot.market,
            snapshot.outcome, snapshot.odds, snapshot.point
        ))
        conn.commit()
        conn.close()
    
    def save_change(self, change: OddsChange):
        """保存变化记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO odds_changes 
            (match_id, bookmaker, market, outcome, old_odds, new_odds, 
             change_pct, timestamp, change_type, signal)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            change.match_id, change.bookmaker, change.market, change.outcome,
            change.old_odds, change.new_odds, change.change_pct,
            change.timestamp, change.change_type, change.signal
        ))
        conn.commit()
        conn.close()
    
    def get_latest_snapshot(self, match_id: str, bookmaker: str, market: str, outcome: str) -> Optional[Dict]:
        """获取最新快照"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM odds_snapshots 
            WHERE match_id = ? AND bookmaker = ? AND market = ? AND outcome = ?
            ORDER BY timestamp DESC LIMIT 1
        ''', (match_id, bookmaker, market, outcome))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0], "timestamp": row[1], "match_id": row[2],
                "home_team": row[3], "away_team": row[4], "bookmaker": row[5],
                "market": row[6], "outcome": row[7], "odds": row[8], "point": row[9]
            }
        return None
    
    def get_changes_history(self, match_id: Optional[str] = None, hours: int = 24) -> List[Dict]:
        """获取变化历史"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        since = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        if match_id:
            cursor.execute('''
                SELECT * FROM odds_changes 
                WHERE match_id = ? AND timestamp > ?
                ORDER BY timestamp DESC
            ''', (match_id, since))
        else:
            cursor.execute('''
                SELECT * FROM odds_changes 
                WHERE timestamp > ?
                ORDER BY timestamp DESC
            ''', (since,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            "id": row[0], "match_id": row[1], "bookmaker": row[2],
            "market": row[3], "outcome": row[4], "old_odds": row[5],
            "new_odds": row[6], "change_pct": row[7], "timestamp": row[8],
            "change_type": row[9], "signal": row[10]
        } for row in rows]


class OddsFetcher:
    """赔率数据获取器"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ODDS_API_KEY")
        self.base_url = "https://api.the-odds-api.com/v4"
    
    async def fetch_sports(self) -> List[Dict]:
        """获取支持的体育项目"""
        if not AIOHTTP_AVAILABLE:
            return []
        
        url = f"{self.base_url}/sports"
        params = {"apiKey": self.api_key} if self.api_key else {}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                return []
    
    async def fetch_odds(
        self, 
        sport: str = "soccer", 
        regions: str = "eu",
        markets: str = "h2h,spreads,totals"
    ) -> List[Dict]:
        """获取赔率数据"""
        if not AIOHTTP_AVAILABLE:
            return []
        
        url = f"{self.base_url}/sports/{sport}/odds"
        params = {
            "apiKey": self.api_key,
            "regions": regions,
            "markets": markets,
            "oddsFormat": "decimal"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                print(f"获取赔率失败: {response.status}")
                return []
    
    def parse_odds_to_snapshots(self, odds_data: List[Dict]) -> List[OddsSnapshot]:
        """解析赔率数据为快照列表"""
        snapshots = []
        timestamp = datetime.now().isoformat()
        
        for match in odds_data:
            match_id = match.get("id")
            home_team = match.get("home_team")
            away_team = match.get("away_team")
            
            for bookmaker in match.get("bookmakers", []):
                bookmaker_name = bookmaker.get("title")
                
                for market in bookmaker.get("markets", []):
                    market_key = market.get("key")
                    
                    for outcome in market.get("outcomes", []):
                        snapshot = OddsSnapshot(
                            timestamp=timestamp,
                            match_id=match_id,
                            home_team=home_team,
                            away_team=away_team,
                            bookmaker=bookmaker_name,
                            market=market_key,
                            outcome=outcome.get("name"),
                            odds=outcome.get("price"),
                            point=outcome.get("point")
                        )
                        snapshots.append(snapshot)
        
        return snapshots


class ChangeDetector:
    """变化检测器"""
    
    def __init__(self, storage: DataStorage):
        self.storage = storage
        self.significant_threshold = 0.15  # 15% 为显著变化
        self.major_threshold = 0.25        # 25% 为重大变化
    
    def detect_changes(self, new_snapshot: OddsSnapshot) -> Optional[OddsChange]:
        """检测变化"""
        # 获取上一次快照
        old = self.storage.get_latest_snapshot(
            new_snapshot.match_id,
            new_snapshot.bookmaker,
            new_snapshot.market,
            new_snapshot.outcome
        )
        
        if not old:
            return None
        
        old_odds = old["odds"]
        new_odds = new_snapshot.odds
        
        if old_odds == new_odds:
            return None
        
        # 计算变化百分比
        change_pct = abs(new_odds - old_odds) / old_odds
        
        # 确定变化类型
        if change_pct >= self.major_threshold:
            change_type = "major"
        elif change_pct >= self.significant_threshold:
            change_type = "significant"
        else:
            change_type = "minor"
        
        # 检测信号
        signal = self._detect_signal(old_odds, new_odds, new_snapshot)
        
        return OddsChange(
            match_id=new_snapshot.match_id,
            bookmaker=new_snapshot.bookmaker,
            market=new_snapshot.market,
            outcome=new_snapshot.outcome,
            old_odds=old_odds,
            new_odds=new_odds,
            change_pct=change_pct,
            timestamp=new_snapshot.timestamp,
            change_type=change_type,
            signal=signal
        )
    
    def _detect_signal(self, old_odds: float, new_odds: float, snapshot: OddsSnapshot) -> Optional[str]:
        """检测异常信号"""
        change_pct = abs(new_odds - old_odds) / old_odds
        
        # 大额注单信号: 短时间内水位急剧下降
        if change_pct > 0.20 and new_odds < old_odds:
            return "heavy_betting"  # 大额注单
        
        # 诱盘信号: 赔率与盘口背离
        if snapshot.market == "spreads" and change_pct > 0.15:
            return "trap_suspected"  # 疑似诱盘
        
        # 临场变盘信号
        if change_pct > 0.10:
            return "late_movement"  # 临场变盘
        
        return None


class AlertManager:
    """预警管理器"""
    
    def __init__(self):
        self.alert_history: Dict[str, datetime] = {}
        self.cooldown_minutes = 15
    
    def should_alert(self, change: OddsChange) -> bool:
        """检查是否应该发送预警"""
        key = f"{change.match_id}:{change.bookmaker}:{change.market}:{change.outcome}"
        now = datetime.now()
        
        if key in self.alert_history:
            last_alert = self.alert_history[key]
            if now - last_alert < timedelta(minutes=self.cooldown_minutes):
                return False
        
        # 只预警显著和重大变化
        if change.change_type not in ["significant", "major"]:
            return False
        
        self.alert_history[key] = now
        return True
    
    def format_alert(self, change: OddsChange, match_info: Dict) -> str:
        """格式化预警消息"""
        direction = "📉 降" if change.new_odds < change.old_odds else "📈 升"
        
        lines = [
            f"🚨 盘口变化预警",
            f"",
            f"⚽ {match_info.get('home_team')} vs {match_info.get('away_team')}",
            f"🏢 {change.bookmaker}",
            f"📊 {change.market} - {change.outcome}",
            f"",
            f"{direction} {change.change_pct*100:.1f}%",
            f"   {change.old_odds:.2f} → {change.new_odds:.2f}",
            f"",
            f"⏰ {change.timestamp[11:16]}",
        ]
        
        if change.signal:
            signal_map = {
                "heavy_betting": "🔥 大额注单信号",
                "trap_suspected": "⚠️ 疑似诱盘",
                "late_movement": "⏰ 临场变盘"
            }
            lines.append(f"\n💡 {signal_map.get(change.signal, change.signal)}")
        
        return "\n".join(lines)
    
    def print_alert(self, change: OddsChange, match_info: Dict):
        """打印预警"""
        print("\n" + "=" * 50)
        print(self.format_alert(change, match_info))
        print("=" * 50 + "\n")


class OddsMovementMonitor:
    """盘口变化监控主类"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ODDS_API_KEY")
        self.storage = DataStorage()
        self.fetcher = OddsFetcher(self.api_key)
        self.detector = ChangeDetector(self.storage)
        self.alerts = AlertManager()
        self.is_running = False
    
    async def scan_once(self, sport: str = "soccer"):
        """执行一次扫描"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 开始扫描 {sport} 盘口数据...")
        
        # 获取赔率数据
        odds_data = await self.fetcher.fetch_odds(sport)
        
        if not odds_data:
            print("未获取到数据，请检查 API Key")
            return
        
        # 解析为快照
        snapshots = self.fetcher.parse_odds_to_snapshots(odds_data)
        print(f"获取到 {len(snapshots)} 条赔率数据")
        
        # 检测变化
        changes_detected = 0
        for snapshot in snapshots:
            # 保存快照
            self.storage.save_snapshot(snapshot)
            
            # 检测变化
            change = self.detector.detect_changes(snapshot)
            if change:
                self.storage.save_change(change)
                changes_detected += 1
                
                # 发送预警
                if self.alerts.should_alert(change):
                    match_info = {
                        "home_team": snapshot.home_team,
                        "away_team": snapshot.away_team
                    }
                    self.alerts.print_alert(change, match_info)
        
        print(f"检测到 {changes_detected} 处变化")
    
    async def start_monitoring(self, sport: str = "soccer", interval: int = 60):
        """开始持续监控"""
        self.is_running = True
        print(f"🟢 启动盘口监控: {sport}")
        print(f"   扫描间隔: {interval}秒")
        print(f"   按 Ctrl+C 停止\n")
        
        try:
            while self.is_running:
                await self.scan_once(sport)
                await asyncio.sleep(interval)
        except KeyboardInterrupt:
            print("\n🛑 监控已停止")
            self.is_running = False
    
    def get_monitoring_report(self, match_id: Optional[str] = None, hours: int = 24) -> str:
        """生成监控报告"""
        changes = self.storage.get_changes_history(match_id, hours)
        
        if not changes:
            return f"过去 {hours} 小时内无盘口变化记录"
        
        lines = [
            f"\n📊 盘口变化报告 (过去 {hours} 小时)",
            "=" * 60,
            f"共检测到 {len(changes)} 处变化\n"
        ]
        
        # 按变化类型统计
        major = len([c for c in changes if c["change_type"] == "major"])
        significant = len([c for c in changes if c["change_type"] == "significant"])
        minor = len([c for c in changes if c["change_type"] == "minor"])
        
        lines.extend([
            f"🔴 重大变化: {major}",
            f"🟡 显著变化: {significant}",
            f"🟢 轻微变化: {minor}",
            ""
        ])
        
        # 最近变化
        lines.append("最近变化:")
        for change in changes[:10]:
            direction = "↓" if change["new_odds"] < change["old_odds"] else "↑"
            lines.append(
                f"  [{change['timestamp'][11:16]}] "
                f"{change['bookmaker'][:10]:10} "
                f"{change['market']:8} "
                f"{direction} {change['change_pct']*100:5.1f}% "
                f"({change['old_odds']:.2f}→{change['new_odds']:.2f})"
            )
        
        lines.append("=" * 60)
        return "\n".join(lines)


def demo_monitoring():
    """演示监控功能"""
    print("=" * 60)
    print("Odds Movement Monitor 盘口变化监控器 v1.0")
    print("=" * 60)
    
    print("\n💡 使用说明:")
    print("  1. 设置 API Key: export ODDS_API_KEY='your_key'")
    print("     获取地址: https://the-odds-api.com/")
    print("  2. 启动监控: python monitor.py --monitor")
    print("  3. 查看报告: python monitor.py --report")
    
    print("\n📊 演示模式 (模拟数据):")
    print("-" * 60)
    
    # 模拟变化检测
    storage = DataStorage()
    detector = ChangeDetector(storage)
    alerts = AlertManager()
    
    # 模拟数据
    old_snapshot = OddsSnapshot(
        timestamp=(datetime.now() - timedelta(minutes=10)).isoformat(),
        match_id="match_001",
        home_team="曼城",
        away_team="阿森纳",
        bookmaker="Bet365",
        market="h2h",
        outcome="Home",
        odds=1.75,
        point=None
    )
    storage.save_snapshot(old_snapshot)
    
    # 模拟新数据（赔率下降，大额注单信号）
    new_snapshot = OddsSnapshot(
        timestamp=datetime.now().isoformat(),
        match_id="match_001",
        home_team="曼城",
        away_team="阿森纳",
        bookmaker="Bet365",
        market="h2h",
        outcome="Home",
        odds=1.55,
        point=None
    )
    
    change = detector.detect_changes(new_snapshot)
    if change:
        storage.save_change(change)
        
        match_info = {"home_team": "曼城", "away_team": "阿森纳"}
        alerts.print_alert(change, match_info)
    
    print("\n" + "=" * 60)
    print("监控演示完成")
    print("=" * 60)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="盘口变化监控器")
    parser.add_argument("--monitor", action="store_true", help="启动持续监控")
    parser.add_argument("--sport", default="soccer", help="体育项目 (默认: soccer)")
    parser.add_argument("--interval", type=int, default=60, help="扫描间隔秒数 (默认: 60)")
    parser.add_argument("--report", action="store_true", help="查看监控报告")
    parser.add_argument("--demo", action="store_true", help="运行演示")
    
    args = parser.parse_args()
    
    if args.demo or (not args.monitor and not args.report):
        demo_monitoring()
    elif args.monitor:
        monitor = OddsMovementMonitor()
        asyncio.run(monitor.start_monitoring(args.sport, args.interval))
    elif args.report:
        monitor = OddsMovementMonitor()
        print(monitor.get_monitoring_report())
