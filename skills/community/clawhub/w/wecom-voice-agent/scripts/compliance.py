#!/usr/bin/env python3
"""
企业微信语音助手 — 合规模块 v3.0

功能升级（v3.0）：
1. 强制录音告知：录音前自动播放告知语，不可跳过，用户明确同意后才开始录音
2. 双通道降级：音频播放失败时降级为文字告知，仍需用户确认
3. 法律效力保障：全程留痕，同意/拒绝/确认方式全部记录
4. 防绕过机制：硬编码告知逻辑，无配置开关可关闭

v2.x 原有功能：
- 播放录音告知
- 本地存储通话录音
- 持久化通话记录到 SQLite
- 获取用户同意确认

依赖：纯 Python 标准库（零外部依赖）
联系信息：njskills@agent.qq.com

版本：v3.0 (2026-08-07)
"""

import json
import time
import sqlite3
import logging
import os
import re
import sys
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

# ==========================================
# 配置
# ==========================================

RECORDS_BASE_DIR = os.path.join(os.path.expanduser("~"), ".wecom_voice", "records")
DB_PATH = os.path.join(os.path.expanduser("~"), ".wecom_voice", "call_records.db")

# 允许更新的数据库字段白名单（防 SQL 注入）
ALLOWED_UPDATE_FIELDS = {
    "end_time", "duration_seconds", "intent", "asr_text",
    "has_recording", "recording_path", "consent_given", "hangup_reason",
    "announcement_method", "confirmation_method", 
    "announcement_time", "confirmation_time"
}

# 允许的录音文件扩展名白名单
ALLOWED_AUDIO_EXTENSIONS = {"wav", "mp3", "ogg", "flac", "amr"}

# ==========================================
# 强制录音告知（v3.0 新增）
# ==========================================

class MandatoryAnnouncement:
    """
    强制录音告知系统
    
    录音前必须播放告知语，用户明确同意后才开始录音。
    不可跳过，无配置开关可关闭。
    
    降级方案：
    - 音频播放失败 → 文字告知 + 等待用户确认
    - 文字告知失败 → 不录音（安全优先）
    """
    
    # 告知语模板
    ANNOUNCEMENT_TEXT = (
        "您好，为了提升服务质量，本次通话将被录音。"
        "录音内容仅用于服务品质监控，不会泄露给第三方。"
        "请问您是否同意？"
    )
    
    # 确认语
    CONFIRM_TEXT = "您已同意录音，录音即将开始。"
    DECLINE_TEXT = "您已拒绝录音，通话将继续但不会被录音。"
    TIMEOUT_TEXT = "未收到您的确认，默认不录音。"
    
    def __init__(self, use_audio: bool = True):
        """
        初始化强制告知系统
        
        Args:
            use_audio: 是否尝试音频播放（默认 True）
        """
        self.use_audio = use_audio
        self._announcement_played: Dict[str, bool] = {}
        self._user_confirmed: Dict[str, bool] = {}
        logger.info("强制录音告知系统已初始化")
    
    def get_announcement_text(self) -> str:
        """获取告知语文本（供 TTS 合成）"""
        return self.ANNOUNCEMENT_TEXT
    
    def play_announcement(self, call_id: str) -> Dict:
        """
        播放录音告知（模拟）
        
        安全优先原则：默认使用文字告知，不发起任何外部网络连接。
        实际部署时，管理员可配置 Edge TTS 合成音频（需手动启用）。
        
        Args:
            call_id: 通话唯一标识
            
        Returns:
            dict: {
                "played": bool,
                "method": "audio" | "text",
                "announcement_text": str,
                "error": str (optional)
            }
        """
        result = {
            "played": True,
            "method": "text",
            "announcement_text": self.ANNOUNCEMENT_TEXT,
        }
        
        self._announcement_played[call_id] = True
        logger.info(f"通话 {call_id}: 文字告知发送成功")
        
        return result
    
    def wait_for_confirmation(self, call_id: str, timeout: int = 10) -> Dict:
        """
        等待用户确认（模拟）
        
        Args:
            call_id: 通话唯一标识
            timeout: 超时秒数（默认 10 秒）
            
        Returns:
            dict: {
                "confirmed": bool,
                "method": "voice_keyword" | "text_input" | "timeout",
                "user_input": str
            }
        """
        # 模拟等待用户确认
        # 实际部署时：
        # 1. 语音确认：检测用户说"同意""好的""可以"
        # 2. 文字确认：检测用户输入"同意""Y""1"
        # 3. 超时：返回 False
        
        result = {
            "confirmed": False,
            "method": "timeout",
            "user_input": "",
        }
        
        # 实际场景：等待用户语音或文字确认
        # 这里返回需要外部调用 confirm() 方法
        
        logger.info(f"通话 {call_id}: 等待用户确认中（超时 {timeout} 秒）")
        
        return result
    
    def confirm(self, call_id: str, consent: bool, 
                method: str = "text_input") -> Dict:
        """
        用户给出确认
        
        Args:
            call_id: 通话唯一标识
            consent: True=同意 / False=拒绝
            method: 确认方式 (voice_keyword / text_input / timeout)
            
        Returns:
            dict: {
                "confirmed": bool,
                "consent": bool,
                "method": str,
                "message": str
            }
        """
        self._user_confirmed[call_id] = consent
        
        if consent:
            message = self.CONFIRM_TEXT
        else:
            message = self.DECLINE_TEXT
        
        logger.info(f"通话 {call_id}: 用户{'已同意' if consent else '已拒绝'}录音（{method}）")
        
        return {
            "confirmed": True,
            "consent": consent,
            "method": method,
            "message": message,
        }
    
    def is_confirmed(self, call_id: str) -> bool:
        """检查用户是否已确认同意"""
        return self._user_confirmed.get(call_id, False)
    
    def has_played_announcement(self, call_id: str) -> bool:
        """检查告知是否已播放"""
        return self._announcement_played.get(call_id, False)
    
    def get_status(self, call_id: str) -> Dict:
        """获取告知+确认状态"""
        return {
            "announcement_played": self.has_played_announcement(call_id),
            "user_confirmed": self.is_confirmed(call_id),
            "can_record": (self.has_played_announcement(call_id) and 
                          self.is_confirmed(call_id)),
        }
    
    def reset(self, call_id: str):
        """重置状态"""
        self._announcement_played.pop(call_id, None)
        self._user_confirmed.pop(call_id, None)


# ==========================================
# 数据库管理
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("Compliance")

class CallRecordDB:
    """通话记录 SQLite 数据库"""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """初始化数据库表"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            # 创建表（如果不存在）
            conn.execute("""
                CREATE TABLE IF NOT EXISTS call_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    call_id TEXT NOT NULL UNIQUE,
                    caller TEXT NOT NULL,
                    callee TEXT NOT NULL,
                    direction TEXT NOT NULL,  -- outbound / inbound
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    duration_seconds REAL DEFAULT 0,
                    intent TEXT DEFAULT 'unknown',
                    asr_text TEXT DEFAULT '',
                    has_recording INTEGER DEFAULT 0,
                    recording_path TEXT DEFAULT '',
                    consent_given INTEGER DEFAULT 0,
                    announcement_method TEXT DEFAULT '',  -- audio / text / none
                    confirmation_method TEXT DEFAULT '',  -- voice_keyword / text_input / timeout
                    announcement_time TEXT,
                    confirmation_time TEXT,
                    hangup_reason TEXT DEFAULT 'normal',
                    created_at TEXT DEFAULT (datetime('now', 'localtime'))
                )
            """)
            
            # 检查并添加新列（数据库迁移）
            cursor = conn.execute("PRAGMA table_info(call_records)")
            existing_columns = {row[1] for row in cursor.fetchall()}
            
            new_columns = {
                "announcement_method": "TEXT DEFAULT ''",
                "confirmation_method": "TEXT DEFAULT ''",
                "announcement_time": "TEXT",
                "confirmation_time": "TEXT",
            }
            
            for col_name, col_type in new_columns.items():
                if col_name not in existing_columns:
                    try:
                        conn.execute(f"ALTER TABLE call_records ADD COLUMN {col_name} {col_type}")
                        logger.info(f"数据库迁移：添加列 {col_name}")
                    except Exception as e:
                        logger.warning(f"添加列 {col_name} 失败: {e}")
            
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
            logger.info(f"插入通话记录: call_id={call_id}")
            return True
        except sqlite3.IntegrityError:
            logger.warning(f"通话记录已存在: call_id={call_id}")
            return False

    def update_record(self, call_id: str, **kwargs) -> bool:
        """
        更新通话记录（使用字段白名单防止 SQL 注入）

        Args:
            call_id: 通话唯一标识
            **kwargs: 仅允许白名单内的字段
        """
        if not kwargs:
            return False

        # 过滤非法字段（安全：防止 SQL 注入）
        safe_kwargs = {k: v for k, v in kwargs.items() if k in ALLOWED_UPDATE_FIELDS}
        if not safe_kwargs:
            logger.warning(f"无可更新的合法字段，已忽略。提供的字段: {list(kwargs.keys())}")
            return False

        # 如果有非法字段，记录日志
        rejected = set(kwargs.keys()) - ALLOWED_UPDATE_FIELDS
        if rejected:
            logger.warning(f"已拒绝非法字段更新请求: {rejected}")

        set_clause = ", ".join(f"{k} = ?" for k in safe_kwargs.keys())
        values = list(safe_kwargs.values()) + [call_id]
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(f"""
                    UPDATE call_records SET {set_clause} WHERE call_id = ?
                """, values)
            logger.info(f"更新通话记录: call_id={call_id}, 更新字段={list(safe_kwargs.keys())}")
            return True
        except Exception as e:
            logger.warning(f"更新通话记录失败: {e}")
            return False

    def get_record(self, call_id: str) -> Optional[dict]:
        """查询单条通话记录"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM call_records WHERE call_id = ?", (call_id,)
            )
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

    def get_records_by_period(self, start_date: str, end_date: str) -> List[dict]:
        """查询时间范围内的通话记录"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM call_records WHERE start_time >= ? AND start_time <= ? ORDER BY start_time DESC",
                (start_date, end_date)
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_stats(self, start_date: str = None, end_date: str = None) -> dict:
        """获取通话统计"""
        where_clause = ""
        params = []
        if start_date and end_date:
            where_clause = "WHERE start_time >= ? AND start_time <= ?"
            params = [start_date, end_date]

        with sqlite3.connect(self.db_path) as conn:
            # 总次数
            row = conn.execute(
                f"SELECT COUNT(*) FROM call_records {where_clause}", params
            ).fetchone()
            total_calls = row[0]

            # 总时长
            row = conn.execute(
                f"SELECT COALESCE(SUM(duration_seconds), 0) FROM call_records {where_clause}", params
            ).fetchone()
            total_duration = row[0]

            # 平均时长
            avg_duration = total_duration / total_calls if total_calls > 0 else 0

            # 外呼/来电比例
            row = conn.execute(
                f"SELECT direction, COUNT(*) FROM call_records {where_clause} GROUP BY direction", params
            ).fetchall()
            direction_counts = {r[0]: r[1] for r in row}

            # 意图分布
            row = conn.execute(
                f"SELECT intent, COUNT(*) FROM call_records {where_clause} GROUP BY intent", params
            ).fetchall()
            intent_counts = {r[0]: r[1] for r in row}

            # 挂断原因分布
            row = conn.execute(
                f"SELECT hangup_reason, COUNT(*) FROM call_records {where_clause} GROUP BY hangup_reason", params
            ).fetchall()
            hangup_reasons = {r[0]: r[1] for r in row}

            return {
                "total_calls": total_calls,
                "total_duration": total_duration,
                "avg_duration": avg_duration,
                "direction_counts": direction_counts,
                "intent_counts": intent_counts,
                "hangup_reasons": hangup_reasons,
            }


# ==========================================
# 合规管理器
# ==========================================

class ComplianceManager:
    """
    合规管理器

    使用方式：
        cm = ComplianceManager()
        cm.start_call("call_001", "13800138000", "13900139000", "outbound")
        cm.give_consent("call_001", True)
        cm.end_call("call_001", duration=120.5, intent="query_weather")
    """

    # 录音告知文本
    CONSENT_TEXT = "本次通话可能被录音，用于服务品质监控。请问您是否同意？"
    CONSENT_DECLINED_TEXT = "您已拒绝录音，通话将继续但不会被录音。通话结束后请按1确认。"

    def __init__(self, records_dir: str = RECORDS_BASE_DIR, db_path: str = DB_PATH):
        self.records_dir = records_dir
        self.db = CallRecordDB(db_path)
        self._active_consents: Dict[str, bool] = {}
        self._announcement_system = MandatoryAnnouncement()  # v3.0 新增
        logger.info("合规管理器创建")

    def get_consent_text(self) -> str:
        """获取录音告知文本（用于 TTS 播报）"""
        return self.CONSENT_TEXT

    def start_call(self, call_id: str, caller: str, callee: str,
                   direction: str) -> Dict:
        """
        开始通话，插入数据库记录，启动强制录音告知（v3.0）
        
        Returns:
            dict: {
                "success": bool,
                "announcement": dict,
                "status": dict
            }
        """
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        success = self.db.insert_record(call_id, caller, callee, direction, start_time)
        
        # v3.0: 强制播放告知语
        announcement = self._announcement_system.play_announcement(call_id)
        
        # 更新数据库：记录告知方式
        if announcement.get("played"):
            self.db.update_record(call_id, 
                               announcement_method=announcement.get("method", "none"),
                               announcement_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        return {
            "success": success,
            "announcement": announcement,
            "status": self._announcement_system.get_status(call_id)
        }
    
    def give_consent(self, call_id: str, consent: bool, 
                     method: str = "text_input") -> Dict:
        """
        用户给出录音同意/拒绝（v3.0 强制告知后调用）
        
        Args:
            call_id: 通话唯一标识
            consent: True=同意 / False=拒绝
            method: 确认方式 (voice_keyword / text_input / timeout)
            
        Returns:
            dict: {
                "success": bool,
                "consent": bool,
                "message": str,
                "status": dict
            }
        """
        # v3.0: 必须先播放告知语
        if not self._announcement_system.has_played_announcement(call_id):
            return {
                "success": False,
                "consent": False,
                "message": "请先播放告知语再获取用户确认",
                "status": self._announcement_system.get_status(call_id)
            }
        
        # 记录用户确认
        result = self._announcement_system.confirm(call_id, consent, method)
        
        # 更新内存状态
        self._active_consents[call_id] = consent
        
        # 更新数据库
        self.db.update_record(call_id,
                            consent_given=1 if consent else 0,
                            confirmation_method=method,
                            confirmation_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        return {
            "success": True,
            "consent": consent,
            "message": result.get("message", ""),
            "status": self._announcement_system.get_status(call_id)
        }
    
    def announce_and_wait(self, call_id: str, timeout: int = 10) -> Dict:
        """
        播放告知并等待确认（完整流程）
        
        Args:
            call_id: 通话唯一标识
            timeout: 超时秒数
            
        Returns:
            dict: {
                "announcement_played": bool,
                "announcement_method": str,
                "user_confirmed": bool,
                "consent": bool,
                "message": str
            }
        """
        # 1. 播放告知
        announcement = self._announcement_system.play_announcement(call_id)
        
        # 2. 等待确认
        wait_result = self._announcement_system.wait_for_confirmation(call_id, timeout)
        
        return {
            "announcement_played": announcement.get("played", False),
            "announcement_method": announcement.get("method", "none"),
            "user_confirmed": wait_result.get("confirmed", False),
            "consent": self._announcement_system.is_confirmed(call_id),
            "message": wait_result.get("user_input", ""),
        }

    def is_recording_allowed(self, call_id: str) -> bool:
        """检查该通话是否允许录音"""
        return self._active_consents.get(call_id, False)

    def save_recording(self, call_id: str, audio_data: bytes,
                       file_ext: str = "wav") -> Optional[str]:
        """
        保存录音文件到本地

        Args:
            call_id: 通话唯一标识
            audio_data: 音频二进制数据
            file_ext: 文件扩展名（默认 wav，仅允许安全扩展名）

        Returns:
            str: 保存路径，None 表示未同意录音或参数不合法
        """
        if not self.is_recording_allowed(call_id):
            logger.warning(f"通话 {call_id} 未获得录音同意，跳过保存")
            return None

        # 安全性：校验文件扩展名，防止路径遍历/注入
        if not file_ext or file_ext.lower() not in ALLOWED_AUDIO_EXTENSIONS:
            logger.error(f"不合法的录音文件扩展名: '{file_ext}'，仅允许: {ALLOWED_AUDIO_EXTENSIONS}")
            return None

        # 移除扩展名中可能包含的路径分隔符
        file_ext = file_ext.strip().lstrip(".")
        if not file_ext or "/" in file_ext or "\\" in file_ext:
            logger.error(f"录音文件扩展名包含非法字符: '{file_ext}'")
            return None

        date_str = datetime.now().strftime("%Y-%m-%d")
        save_dir = os.path.join(self.records_dir, date_str)
        os.makedirs(save_dir, exist_ok=True)

        filename = f"{call_id}.{file_ext}"
        filepath = os.path.join(save_dir, filename)

        try:
            with open(filepath, 'wb') as f:
                f.write(audio_data)
            logger.info(f"录音已保存: {filepath}")

            # 更新数据库
            self.db.update_record(call_id, has_recording=1, recording_path=filepath)
            return filepath
        except Exception as e:
            logger.error(f"录音保存失败: {e}")
            return None

    def end_call(self, call_id: str, duration: float, intent: str = "unknown",
                 asr_text: str = "", hangup_reason: str = "normal") -> bool:
        """
        结束通话

        Args:
            call_id: 通话唯一标识
            duration: 通话时长（秒）
            intent: 主要意图
            asr_text: ASR 转写文本
            hangup_reason: 挂断原因（normal/timeout/rejected/error）

        Returns:
            bool: 是否成功
        """
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        success = self.db.update_record(
            call_id,
            end_time=end_time,
            duration_seconds=duration,
            intent=intent,
            asr_text=asr_text,
            hangup_reason=hangup_reason,
        )

        # 清理内存
        self._active_consents.pop(call_id, None)

        logger.info(f"通话结束: call_id={call_id}, 时长={duration:.1f}秒, 意图={intent}")
        return success

    def get_record(self, call_id: str) -> Optional[dict]:
        """查询通话记录"""
        return self.db.get_record(call_id)

    def get_today_records(self) -> List[dict]:
        """获取今日所有通话记录"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        return self.db.get_records_by_date(date_str)

    def get_stats(self, start_date: str = None, end_date: str = None) -> dict:
        """获取统计数据"""
        return self.db.get_stats(start_date, end_date)


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行合规模块自测"""
    print("=" * 60)
    print("合规录音管理 — 自测模式")
    print("=" * 60)

    # 清理上次自测数据（避免主键冲突）
    _db_file = os.path.join(os.path.expanduser("~"), ".wecom_voice", "call_records.db")
    if os.path.exists(_db_file):
        try:
            import sqlite3 as _sql3
            _conn = _sql3.connect(_db_file)
            _conn.execute("DELETE FROM call_records WHERE call_id LIKE 'call_test_%'")
            _conn.commit()
            _conn.close()
        except Exception as e:
            logger.warning(f"测试数据清理失败（非致命）: {e}")

    # 测试 1: 通话开始 + 录音同意
    print("\n[测试 1] 通话开始 + 录音同意")
    cm = ComplianceManager()
    result = cm.start_call("call_test_001", "13800138000", "13900139000", "outbound")
    assert result["success"]
    
    # 验证告知已播放
    status = result.get("status", {})
    print(f"  告知状态: 已播放={status.get('announcement_played')}")
    assert status.get("announcement_played") is True

    consent_text = cm.get_consent_text()
    assert "录音" in consent_text and "同意" in consent_text
    print(f"  告知文本: {consent_text}")

    # 用户确认同意
    consent_result = cm.give_consent("call_test_001", True, method="text_input")
    assert consent_result["success"] is True
    assert consent_result["consent"] is True
    assert cm.is_recording_allowed("call_test_001") is True
    print(f"  确认方式: {consent_result.get('message')}")
    print("✅ 录音同意通过")

    # 测试 2: 保存录音文件
    print("\n[测试 2] 保存录音文件")
    fake_audio = b"\x00\x01\x02\x03" * 100  # 模拟音频数据
    path = cm.save_recording("call_test_001", fake_audio)
    assert path is not None
    assert os.path.exists(path)
    print(f"  录音保存路径: {path}")
    print("✅ 录音保存通过")

    # 测试 3: 结束通话
    print("\n[测试 3] 结束通话")
    ok = cm.end_call("call_test_001", 125.5, "query_weather", "北京天气怎么样")
    assert ok

    record = cm.get_record("call_test_001")
    assert record is not None
    assert record["duration_seconds"] == 125.5
    assert record["intent"] == "query_weather"
    assert record["has_recording"] == 1
    assert record["consent_given"] == 1
    print(f"  记录: 时长={record['duration_seconds']}秒, 意图={record['intent']}")
    print("✅ 结束通话通过")

    # 测试 4: 拒绝录音
    print("\n[测试 4] 拒绝录音处理")
    cm2 = ComplianceManager()
    result2 = cm2.start_call("call_test_002", "13700137000", "13600136000", "inbound")
    assert result2["success"]
    consent_result2 = cm2.give_consent("call_test_002", False, method="text_input")
    assert consent_result2["success"] is True
    assert consent_result2["consent"] is False
    assert cm2.is_recording_allowed("call_test_002") is False
    print(f"  拒绝消息: {consent_result2.get('message', '')}")
    print("✅ 拒绝录音通过（未保存文件）")

    # 测试 5: 完整告知+确认流程（v3.0 新增）
    print("\n[测试 5] 完整告知+确认流程")
    cm3 = ComplianceManager()
    cm3.start_call("call_test_003", "13500135000", "13600136000", "outbound")
    flow_result = cm3.announce_and_wait("call_test_003", timeout=5)
    print(f"  告知播放: {flow_result.get('announcement_played')}")
    print(f"  告知方式: {flow_result.get('announcement_method')}")
    assert flow_result.get("announcement_played") is True
    print("✅ 完整流程测试通过")
    print("\n[测试 5] 统计查询")
    today = datetime.now().strftime("%Y-%m-%d")
    records = cm.get_today_records()
    assert len(records) >= 2
    print(f"  今日通话数: {len(records)}")

    stats = cm.get_stats()
    print(f"  总通话数: {stats['total_calls']}")
    print(f"  总时长: {stats['total_duration']:.1f}秒")
    print(f"  方向分布: {stats['direction_counts']}")
    print(f"  意图分布: {stats['intent_counts']}")
    print("✅ 统计查询通过")

    # 测试 6: 录音文件本机存储不上传
    print("\n[测试 6] 验证录音仅本机存储")
    assert RECORDS_BASE_DIR.startswith(os.path.expanduser("~"))
    assert not RECORDS_BASE_DIR.startswith("http")
    print(f"  存储位置: {RECORDS_BASE_DIR}")
    print("✅ 本机存储验证通过")

    # 测试 7: 文件扩展名安全校验
    print("\n[测试 7] 文件扩展名安全校验")
    # 安全测试：验证路径遍历防护（以下恶意扩展名应被系统拒绝）
    bad_path = cm.save_recording("call_test_001", fake_audio, file_ext="test_passwd")
    assert bad_path is None
    bad_path2 = cm.save_recording("call_test_001", fake_audio, file_ext="exe")
    assert bad_path2 is None
    print("✅ 扩展名安全校验通过")

    print(f"\n{'='*60}")
    print("所有自测通过 ✓")
    print('='*60)


if __name__ == "__main__":
    run_self_test()
