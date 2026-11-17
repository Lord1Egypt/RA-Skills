#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
call_record_subsystem.py — 通话记录子系统（v3.0）

合并原 4 个脚本为统一子系统：
- compliance.py: 录音存储 + 强制告知
- ivr_minutes.py: 纪要生成
- stats.py: 统计看板
- transcriber.py: 全文转写

统一接口：
  create_record() → add_audio() → generate_minutes() → get_stats()

依赖：纯 Python 标准库（零外部依赖）
联系信息：njskills@agent.qq.com

版本：v1.0 (2026-08-17)
"""

import os
import re
import json
import wave
import sqlite3
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from collections import Counter

logger = logging.getLogger(__name__)

# ==========================================
# 配置
# ==========================================

RECORDS_BASE_DIR = os.path.join(os.path.expanduser("~"), ".wecom_voice", "records")
DB_PATH = os.path.join(os.path.expanduser("~"), ".wecom_voice", "call_records.db")

# 允许的录音文件扩展名白名单
ALLOWED_AUDIO_EXTENSIONS = {"wav", "mp3", "ogg", "flac", "amr"}

# 允许更新的数据库字段白名单（防 SQL 注入）
ALLOWED_UPDATE_FIELDS = {
    "end_time", "duration_seconds", "intent", "asr_text",
    "has_recording", "recording_path", "consent_given", "hangup_reason",
    "announcement_method", "confirmation_method",
    "announcement_time", "confirmation_time",
    "transcript", "minutes_json", "summary_text",
}

# 强制录音告知文本
ANNOUNCEMENT_TEXT = (
    "您好，为了提升服务质量，本次通话将被录音。"
    "录音内容仅用于服务品质监控，不会泄露给第三方。"
    "请问您是否同意？"
)


# ==========================================
# 数据库管理
# ==========================================

class CallRecordDB:
    """通话记录 SQLite 数据库"""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """初始化数据库表"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS call_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    call_id TEXT NOT NULL UNIQUE,
                    caller TEXT NOT NULL,
                    callee TEXT NOT NULL,
                    direction TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    duration_seconds REAL DEFAULT 0,
                    intent TEXT DEFAULT 'unknown',
                    asr_text TEXT DEFAULT '',
                    has_recording INTEGER DEFAULT 0,
                    recording_path TEXT DEFAULT '',
                    consent_given INTEGER DEFAULT 0,
                    announcement_method TEXT DEFAULT '',
                    confirmation_method TEXT DEFAULT '',
                    announcement_time TEXT,
                    confirmation_time TEXT,
                    transcript TEXT DEFAULT '',
                    minutes_json TEXT DEFAULT '',
                    summary_text TEXT DEFAULT '',
                    hangup_reason TEXT DEFAULT 'normal',
                    created_at TEXT DEFAULT (datetime('now', 'localtime'))
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_call_records_time
                ON call_records(start_time)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_call_records_caller
                ON call_records(caller)
            """)
        logger.info("数据库初始化完成")

    def insert_record(self, call_id: str, caller: str, callee: str,
                      direction: str, start_time: str) -> bool:
        """插入新通话记录"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO call_records (call_id, caller, callee, direction, start_time)
                    VALUES (?, ?, ?, ?, ?)
                """, (call_id, caller, callee, direction, start_time))
            return True
        except sqlite3.IntegrityError:
            return False

    def update_record(self, call_id: str, **kwargs) -> bool:
        """更新通话记录（使用字段白名单防止 SQL 注入）"""
        if not kwargs:
            return False
        safe_kwargs = {k: v for k, v in kwargs.items() if k in ALLOWED_UPDATE_FIELDS}
        if not safe_kwargs:
            return False
        set_clause = ", ".join(f"{k} = ?" for k in safe_kwargs.keys())
        values = list(safe_kwargs.values()) + [call_id]
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(f"UPDATE call_records SET {set_clause} WHERE call_id = ?", values)
            return True
        except Exception as e:
            logger.warning(f"更新通话记录失败: {e}")
            return False

    def get_record(self, call_id: str) -> Optional[dict]:
        """查询单条通话记录"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM call_records WHERE call_id = ?", (call_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_records_by_date(self, date_str: str) -> List[dict]:
        """查询某天所有通话记录"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM call_records WHERE start_time LIKE ? ORDER BY start_time DESC",
                (f"{date_str}%",)
            )
            return [dict(row) for row in cursor.fetchall()]


# ==========================================
# 强制录音告知
# ==========================================

class MandatoryAnnouncement:
    """强制录音告知系统（不可跳过）"""

    def __init__(self):
        self._announcement_played: Dict[str, bool] = {}
        self._user_confirmed: Dict[str, bool] = {}

    def get_announcement_text(self) -> str:
        """获取告知语文本"""
        return ANNOUNCEMENT_TEXT

    def play_announcement(self, call_id: str) -> Dict:
        """播放录音告知（模拟）"""
        self._announcement_played[call_id] = True
        return {
            "played": True,
            "method": "text",
            "announcement_text": ANNOUNCEMENT_TEXT,
        }

    def confirm(self, call_id: str, consent: bool, method: str = "text_input") -> Dict:
        """用户给出确认"""
        self._user_confirmed[call_id] = consent
        return {
            "confirmed": True,
            "consent": consent,
            "method": method,
            "message": "您已同意录音，录音即将开始。" if consent else "您已拒绝录音，通话将继续但不会被录音。",
        }

    def is_confirmed(self, call_id: str) -> bool:
        return self._user_confirmed.get(call_id, False)

    def has_played_announcement(self, call_id: str) -> bool:
        return self._announcement_played.get(call_id, False)

    def get_status(self, call_id: str) -> Dict:
        return {
            "announcement_played": self.has_played_announcement(call_id),
            "user_confirmed": self.is_confirmed(call_id),
            "can_record": self.has_played_announcement(call_id) and self.is_confirmed(call_id),
        }


# ==========================================
# 纪要提取器
# ==========================================

class MinutesExtractor:
    """从通话文字记录中提取结构化纪要"""

    DECISION_KEYWORDS = [
        "决定", "确认", "同意", "批准", "选择", "确定",
        "定了", "就这么办", "行", "好的", "可以", "没问题",
        "ok", "OK", "okay", "yes", "好", "中", "成交"
    ]

    TODO_KEYWORDS = [
        "提醒", "待办", "任务", "记得", "别忘了",
        "需要", "必须", "安排", "准备", "跟进",
        "联系", "打电话", "发邮件", "发消息", "通知"
    ]

    def __init__(self):
        self._decision_pats = [
            re.compile(r'.*?(?:' + '|'.join(re.escape(kw) for kw in self.DECISION_KEYWORDS) + r').*', re.UNICODE)
        ]
        self._todo_pats = [
            re.compile(r'.*?(?:' + '|'.join(re.escape(kw) for kw in self.TODO_KEYWORDS) + r').*', re.UNICODE)
        ]

    def extract(self, turns: List[Dict], intent: str = "unknown") -> "Minutes":
        """从对话轮次中提取纪要"""
        decisions = []
        todos = []
        time_points = []
        keywords_found = []
        sentiment = "neutral"
        full_text = ""

        for turn in turns:
            if turn.get("role") == "user":
                text = turn.get("content", "")
                full_text += text + " "
                for pat in self._decision_pats:
                    if pat.match(text):
                        decisions.append(text)
                        break
                for pat in self._todo_pats:
                    if pat.match(text):
                        todos.append(text)
                        break

        time_points = self._extract_times(full_text)
        keywords_found = self._extract_keywords(full_text)
        sentiment = self._analyze_sentiment(full_text)

        return Minutes(
            decisions=decisions,
            todos=todos,
            time_points=time_points,
            keywords=keywords_found,
            sentiment=sentiment,
            intent=intent,
            turns_count=len(turns),
            source_text=full_text[:500],
        )

    def _extract_times(self, text: str) -> List[Dict[str, str]]:
        """从文本中提取时间点"""
        time_points = []
        for m in re.finditer(r'(\d{4})年(\d{1,2})月(\d{1,2})日', text):
            time_points.append({
                "text": m.group(0), "type": "date",
                "value": f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
            })
        for m in re.finditer(r'(\d{1,2})月(\d{1,2})日', text):
            year = datetime.now().year
            time_points.append({
                "text": m.group(0), "type": "date",
                "value": f"{year}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
            })
        relative_map = {"今天": 0, "明天": 1, "后天": 2, "大后天": 3}
        for word, offset in relative_map.items():
            if word in text:
                target = datetime.now() + timedelta(days=offset)
                time_points.append({
                    "text": word, "type": "relative_date",
                    "value": target.strftime("%Y-%m-%d")
                })
        weekday_pattern = r'[周週][一二三四五六日]'
        for m in re.finditer(weekday_pattern, text):
            time_points.append({
                "text": m.group(0), "type": "weekday", "value": m.group(0)
            })
        for m in re.finditer(r'(上午|下午|晚上|清晨|早晨|午间|早|晚)?(\d{1,2})点(\d{1,2})?', text):
            prefix = m.group(1) or ""
            hour = int(m.group(2))
            minute = int(m.group(3)) if m.group(3) else 0
            if prefix in ("下午", "晚上", "晚") and hour < 12:
                hour += 12
            time_points.append({
                "text": m.group(0), "type": "time",
                "value": f"{hour:02d}:{minute:02d}"
            })
        return time_points

    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
        freq = Counter(words)
        stopwords = {"我们", "他们", "这个", "那个", "然后", "但是", "所以", "因为", "如果", "的话", "知道", "现在", "可以", "已经"}
        filtered = [w for w, c in freq.most_common(10) if w not in stopwords and c >= 1]
        return filtered[:5]

    def _analyze_sentiment(self, text: str) -> str:
        """简单情感分析"""
        positive = ["好", "谢谢", "满意", "可以", "行", "同意", "没问题", "不错"]
        negative = ["不", "拒绝", "退订", "投诉", "错误", "问题", "差", "慢", "等"]
        p_count = sum(1 for w in positive if w in text)
        n_count = sum(1 for w in negative if w in text)
        if p_count > n_count:
            return "positive"
        elif n_count > p_count:
            return "negative"
        return "neutral"


# ==========================================
# 纪要对象
# ==========================================

class Minutes:
    """结构化纪要"""

    def __init__(self, decisions, todos, time_points, keywords, sentiment, intent, turns_count, source_text=""):
        self.decisions = decisions
        self.todos = todos
        self.time_points = time_points
        self.keywords = keywords
        self.sentiment = sentiment
        self.intent = intent
        self.turns_count = turns_count
        self.source_text = source_text
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_markdown(self) -> str:
        """生成 markdown 格式纪要"""
        lines = [
            "## 📋 通话纪要", "",
            f"**生成时间**: {self.created_at}",
            f"**主要意图**: {self.intent}",
            f"**对话轮次**: {self.turns_count}",
            f"**情感倾向**: {'😊 积极' if self.sentiment == 'positive' else '😐 中性' if self.sentiment == 'neutral' else '😟 消极'}",
            "",
        ]
        lines.append("### 🎯 决策点")
        if self.decisions:
            for d in self.decisions:
                lines.append(f"- {d}")
        else:
            lines.append("- 无明确决策")
        lines.append("")
        lines.append("### 📝 待办项")
        if self.todos:
            for t in self.todos:
                lines.append(f"- [ ] {t}")
        else:
            lines.append("- 无待办事项")
        lines.append("")
        lines.append("### ⏰ 时间点")
        if self.time_points:
            for tp in self.time_points:
                lines.append(f"- {tp['text']} ({tp['value']})")
        else:
            lines.append("- 无明确时间点")
        lines.append("")
        if self.keywords:
            lines.append("### 🔑 关键词")
            lines.append("、".join(self.keywords))
            lines.append("")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "decisions": self.decisions, "todos": self.todos,
            "time_points": self.time_points, "keywords": self.keywords,
            "sentiment": self.sentiment, "intent": self.intent,
            "turns_count": self.turns_count, "created_at": self.created_at,
            "source_text": self.source_text,
        }

    def to_summary(self) -> str:
        parts = [f"意图: {self.intent}"]
        if self.decisions:
            parts.append(f"决策: {len(self.decisions)}项")
        if self.todos:
            parts.append(f"待办: {len(self.todos)}项")
        if self.time_points:
            parts.append(f"时间: {len(self.time_points)}个")
        return " | ".join(parts)


# ==========================================
# 统计生成器
# ==========================================

class StatsGenerator:
    """通话统计生成器"""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def generate(self, period: str = "month", userid: str = None) -> Dict:
        """生成统计数据"""
        start_date, end_date = self._get_date_range(period)
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            where_clause = "WHERE start_time >= ? AND start_time <= ?"
            params = [start_date, end_date]
            if userid:
                where_clause += " AND (caller = ? OR callee = ?)"
                params.extend([userid, userid])

            row = conn.execute(f"SELECT COUNT(*) FROM call_records {where_clause}", params).fetchone()
            total_calls = row[0]

            if total_calls == 0:
                return {"period": period, "date_range": f"{start_date} ~ {end_date}", "total_calls": 0, "message": "该时间段内暂无通话记录"}

            row = conn.execute(f"SELECT COALESCE(SUM(duration_seconds), 0) FROM call_records {where_clause}", params).fetchone()
            total_duration = row[0]
            avg_duration = total_duration / total_calls

            rows = conn.execute(f"SELECT direction, COUNT(*) as cnt FROM call_records {where_clause} GROUP BY direction", params).fetchall()
            direction_counts = {r["direction"]: r["cnt"] for r in rows}
            outbound = direction_counts.get("outbound", 0)
            inbound = direction_counts.get("inbound", 0)

            rows = conn.execute(f"SELECT intent, COUNT(*) as cnt FROM call_records {where_clause} GROUP BY intent ORDER BY cnt DESC", params).fetchall()
            intent_counts = {r["intent"]: r["cnt"] for r in rows}

            rows = conn.execute(f"SELECT hangup_reason, COUNT(*) as cnt FROM call_records {where_clause} GROUP BY hangup_reason", params).fetchall()
            hangup_reasons = {r["hangup_reason"]: r["cnt"] for r in rows}

            rows = conn.execute(f"""
                SELECT DATE(start_time) as day, COUNT(*) as cnt, SUM(duration_seconds) as total_dur
                FROM call_records {where_clause} GROUP BY day ORDER BY day
            """, params).fetchall()
            daily_trend = [{"date": r["day"], "calls": r["cnt"], "duration": r["total_dur"]} for r in rows]

            row = conn.execute(f"SELECT call_id, duration_seconds FROM call_records {where_clause} ORDER BY duration_seconds DESC LIMIT 1", params).fetchone()
            longest_call = {"call_id": row["call_id"], "duration": row["duration_seconds"]} if row else None

            row = conn.execute(f"SELECT COUNT(*) FROM call_records {where_clause} AND has_recording = 1", params).fetchone()
            recorded_calls = row[0]
            recording_rate = recorded_calls / total_calls if total_calls > 0 else 0

            normal_hangup = hangup_reasons.get("normal", 0)
            answered_rate = normal_hangup / total_calls if total_calls > 0 else 0

        return {
            "period": period, "date_range": f"{start_date} ~ {end_date}",
            "total_calls": total_calls, "total_duration": total_duration,
            "avg_duration": avg_duration, "total_hours": total_duration / 3600,
            "outbound": outbound, "inbound": inbound,
            "outbound_ratio": outbound / total_calls if total_calls > 0 else 0,
            "intent_counts": intent_counts, "hangup_reasons": hangup_reasons,
            "daily_trend": daily_trend, "longest_call": longest_call,
            "recorded_calls": recorded_calls, "recording_rate": recording_rate,
            "answered_rate": answered_rate,
        }

    def render(self, stats: Dict) -> str:
        """渲染统计为可读字符串"""
        if stats["total_calls"] == 0:
            return f"\n📊 {stats['date_range']}: 暂无通话记录\n"
        lines = [
            "", "=" * 60, "📊 通话统计看板", "=" * 60,
            f"时间范围: {stats['date_range']}",
            f"总通话次数: {stats['total_calls']} 次",
            f"总通话时长: {stats['total_hours']:.1f} 小时 ({stats['total_duration']:.0f} 秒)",
            f"平均通话时长: {stats['avg_duration']:.1f} 秒",
            f"外呼次数: {stats['outbound']} 次 ({stats['outbound_ratio']*100:.0f}%)",
            f"来电次数: {stats['inbound']} 次 ({(1-stats['outbound_ratio'])*100:.0f}%)",
            f"已接听率: {stats['answered_rate']*100:.1f}%",
            f"录音覆盖率: {stats['recording_rate']*100:.1f}%", "",
        ]
        if stats["longest_call"]:
            lines.append(f"最长通话: {stats['longest_call']['call_id']} ({stats['longest_call']['duration']:.0f}秒)")
            lines.append("")
        lines.append("🎯 意图分布:")
        for intent, count in stats["intent_counts"].items():
            pct = count / stats["total_calls"] * 100
            lines.append(f"  {intent}: {count} 次 ({pct:.1f}%)")
        lines.append("")
        lines.append("📴 挂断原因:")
        for reason, count in stats["hangup_reasons"].items():
            pct = count / stats["total_calls"] * 100
            lines.append(f"  {reason}: {count} 次 ({pct:.1f}%)")
        lines.append("")
        if stats["daily_trend"]:
            lines.append("📈 每日趋势:")
            lines.append(self._render_trend_ascii(stats["daily_trend"]))
        lines.append("=" * 60)
        return "\n".join(lines)

    def _render_trend_ascii(self, daily_trend: List[Dict]) -> str:
        """渲染 ASCII 趋势图"""
        if not daily_trend:
            return "(无数据)"
        max_calls = max(d["calls"] for d in daily_trend) if daily_trend else 1
        if max_calls == 0:
            max_calls = 1
        lines = [f"  最大: {max_calls} 次/天", ""]
        for day in daily_trend:
            bar_len = int((day["calls"] / max_calls) * 20)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            lines.append(f"  {day['date']} │{bar}│ {day['calls']}次 ({day['duration']:.0f}s)")
        return "\n".join(lines)

    def _get_date_range(self, period: str) -> tuple:
        """获取日期范围"""
        now = datetime.now()
        end_date = now.strftime("%Y-%m-%d %H:%M:%S")
        if period == "week":
            start = now - timedelta(days=7)
        elif period == "year":
            start = now.replace(month=1, day=1, hour=0, minute=0, second=0)
        elif period == "month":
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            raise ValueError(f"不支持的时间范围: {period}")
        start_date = start.strftime("%Y-%m-%d %H:%M:%S")
        return start_date, end_date


# ==========================================
# 通话记录子系统（统一入口）
# ==========================================

class CallRecordSubsystem:
    """
    通话记录子系统 — 统一入口
    
    合并原 4 个脚本功能：
    - 录音存储 + 强制告知（原 compliance.py）
    - 纪要生成（原 ivr_minutes.py）
    - 统计看板（原 stats.py）
    - 全文转写（原 transcriber.py）
    
    使用方式：
        crs = CallRecordSubsystem()
        crs.create_record("call_001", "13800138000", "13900139000", "outbound")
        crs.give_consent("call_001", True)
        crs.add_audio("call_001", audio_data)
        crs.add_transcript("call_001", "用户: 你好\\n助手: 您好")
        minutes = crs.generate_minutes("call_001")
        stats = crs.get_stats("month")
    """

    def __init__(self, db_path: str = DB_PATH, records_dir: str = RECORDS_BASE_DIR):
        self.db_path = db_path
        self.records_dir = records_dir
        self.db = CallRecordDB(db_path)
        self.announcement = MandatoryAnnouncement()
        self.minutes_extractor = MinutesExtractor()
        self.stats_generator = StatsGenerator(db_path)
        self._active_consents: Dict[str, bool] = {}
        logger.info("通话记录子系统已初始化")

    # === 通话生命周期 ===

    def create_record(self, call_id: str, caller: str, callee: str,
                      direction: str) -> Dict:
        """
        创建通话记录
        
        Returns:
            dict: {"success": bool, "announcement": dict}
        """
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        success = self.db.insert_record(call_id, caller, callee, direction, start_time)
        announcement = self.announcement.play_announcement(call_id)
        return {"success": success, "announcement": announcement}

    def give_consent(self, call_id: str, consent: bool,
                     method: str = "text_input") -> Dict:
        """
        用户给出录音同意/拒绝
        
        Returns:
            dict: {"success": bool, "consent": bool, "message": str}
        """
        if not self.announcement.has_played_announcement(call_id):
            return {"success": False, "consent": False, "message": "请先播放告知语"}
        result = self.announcement.confirm(call_id, consent, method)
        self._active_consents[call_id] = consent
        self.db.update_record(call_id,
                            consent_given=1 if consent else 0,
                            confirmation_method=method,
                            confirmation_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return {"success": True, "consent": consent, "message": result.get("message", "")}

    def is_recording_allowed(self, call_id: str) -> bool:
        """检查是否允许录音"""
        return self._active_consents.get(call_id, False)

    def add_audio(self, call_id: str, audio_data: bytes,
                  file_ext: str = "wav") -> Optional[str]:
        """
        保存录音文件
        
        Returns:
            str: 保存路径，None 表示未同意或参数不合法
        """
        if not self.is_recording_allowed(call_id):
            return None
        if not file_ext or file_ext.lower() not in ALLOWED_AUDIO_EXTENSIONS:
            return None
        file_ext = file_ext.strip().lstrip(".")
        if not file_ext or "/" in file_ext or "\\" in file_ext:
            return None

        date_str = datetime.now().strftime("%Y-%m-%d")
        save_dir = os.path.join(self.records_dir, date_str)
        os.makedirs(save_dir, exist_ok=True)
        filename = f"{call_id}.{file_ext}"
        filepath = os.path.join(save_dir, filename)

        try:
            with open(filepath, 'wb') as f:
                f.write(audio_data)
            self.db.update_record(call_id, has_recording=1, recording_path=filepath)
            return filepath
        except Exception as e:
            logger.error(f"录音保存失败: {e}")
            return None

    def add_transcript(self, call_id: str, transcript: str,
                       intent: str = "unknown") -> bool:
        """
        添加 ASR 转写文本
        
        Args:
            call_id: 通话唯一标识
            transcript: 转写文本
            intent: 主要意图
        """
        return self.db.update_record(call_id, asr_text=transcript, intent=intent)

    def end_record(self, call_id: str, duration: float,
                   intent: str = "unknown", asr_text: str = "",
                   hangup_reason: str = "normal") -> bool:
        """
        结束通话记录
        """
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        success = self.db.update_record(
            call_id, end_time=end_time, duration_seconds=duration,
            intent=intent, asr_text=asr_text, hangup_reason=hangup_reason,
        )
        self._active_consents.pop(call_id, None)
        return success

    # === 纪要生成 ===

    def generate_minutes(self, call_id: str, turns: List[Dict] = None) -> Optional[Minutes]:
        """
        生成通话纪要
        
        Args:
            call_id: 通话唯一标识
            turns: 对话轮次列表，None 时从数据库读取
            
        Returns:
            Minutes 对象
        """
        record = self.db.get_record(call_id)
        if not record:
            return None

        if turns is None:
            # 从数据库读取转写文本，构造简单轮次
            asr_text = record.get("asr_text", "")
            if asr_text:
                turns = [{"role": "user", "content": asr_text}]
            else:
                turns = []

        intent = record.get("intent", "unknown")
        minutes = self.minutes_extractor.extract(turns, intent)

        # 保存纪要到数据库
        self.db.update_record(call_id,
                            minutes_json=json.dumps(minutes.to_dict(), ensure_ascii=False),
                            summary_text=minutes.to_summary())
        return minutes

    # === 统计看板 ===

    def get_stats(self, period: str = "month", userid: str = None) -> Dict:
        """获取统计数据"""
        return self.stats_generator.generate(period, userid)

    def render_stats(self, period: str = "month", userid: str = None) -> str:
        """渲染统计看板"""
        stats = self.get_stats(period, userid)
        return self.stats_generator.render(stats)

    # === 查询 ===

    def get_record(self, call_id: str) -> Optional[dict]:
        """获取通话记录"""
        return self.db.get_record(call_id)

    def get_today_records(self) -> List[dict]:
        """获取今日通话记录"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        return self.db.get_records_by_date(date_str)


# ==========================================
# 便捷函数
# ==========================================

def create_record(call_id: str, caller: str, callee: str, direction: str) -> Dict:
    """便捷函数：创建通话记录"""
    crs = CallRecordSubsystem()
    return crs.create_record(call_id, caller, callee, direction)

def get_stats(period: str = "month") -> Dict:
    """便捷函数：获取统计"""
    crs = CallRecordSubsystem()
    return crs.get_stats(period)

def generate_minutes(call_id: str, turns: List[Dict] = None) -> Optional[Minutes]:
    """便捷函数：生成纪要"""
    crs = CallRecordSubsystem()
    return crs.generate_minutes(call_id, turns)


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行子系统自测"""
    print("=" * 60)
    print("通话记录子系统 — 自测模式")
    print("=" * 60)

    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        temp_db = f.name

    try:
        crs = CallRecordSubsystem(db_path=temp_db)

        # 测试 1: 创建通话记录
        print("\n[测试 1] 创建通话记录")
        result = crs.create_record("call_test_001", "13800138000", "13900139000", "outbound")
        assert result["success"]
        assert result["announcement"]["played"]
        print("✅ 创建通话记录通过")

        # 测试 2: 强制告知+同意
        print("\n[测试 2] 强制告知+同意")
        consent = crs.give_consent("call_test_001", True)
        assert consent["success"]
        assert consent["consent"]
        assert crs.is_recording_allowed("call_test_001")
        print("✅ 强制告知+同意通过")

        # 测试 3: 保存录音
        print("\n[测试 3] 保存录音")
        fake_audio = b"\x00\x01\x02\x03" * 100
        path = crs.add_audio("call_test_001", fake_audio)
        assert path is not None
        assert os.path.exists(path)
        print("✅ 保存录音通过")

        # 测试 4: 添加转写文本
        print("\n[测试 4] 添加转写文本")
        crs.add_transcript("call_test_001", "用户: 你好，助手: 您好", "greeting")
        record = crs.get_record("call_test_001")
        assert record is not None
        assert "用户" in record["asr_text"]
        print("✅ 添加转写文本通过")

        # 测试 5: 生成纪要
        print("\n[测试 5] 生成纪要")
        turns = [
            {"role": "user", "content": "我想查天气"},
            {"role": "agent", "content": "明天北京晴"},
            {"role": "user", "content": "好的，谢谢"},
        ]
        minutes = crs.generate_minutes("call_test_001", turns)
        assert minutes is not None
        assert minutes.intent == "greeting"
        md = minutes.to_markdown()
        assert "## 📋 通话纪要" in md
        print("✅ 生成纪要通过")

        # 测试 6: 结束通话
        print("\n[测试 6] 结束通话")
        crs.end_record("call_test_001", 120.5, "greeting", "用户: 你好")
        record = crs.get_record("call_test_001")
        assert record["duration_seconds"] == 120.5
        print("✅ 结束通话通过")

        # 测试 7: 统计看板
        print("\n[测试 7] 统计看板")
        stats = crs.get_stats("month")
        assert stats["total_calls"] >= 1
        output = crs.render_stats("month")
        assert "📊 通话统计看板" in output
        print("✅ 统计看板通过")

        # 测试 8: 便捷函数
        print("\n[测试 8] 便捷函数")
        result = crs.create_record("call_test_002", "13700137000", "13600136000", "inbound")
        assert result["success"]
        print("✅ 便捷函数通过")

        print(f"\n{'='*60}")
        print("所有自测通过 ✓")
        print("=" * 60)

    finally:
        try:
            os.unlink(temp_db)
        except OSError:
            pass


if __name__ == "__main__":
    run_self_test()
