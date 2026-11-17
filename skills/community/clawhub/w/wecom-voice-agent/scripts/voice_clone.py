#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
voice_clone.py — 语音克隆外呼（品牌音色）（v2.8）

功能：
1. 可选接入豆包 / MiniMax 语音克隆 API（环境变量配置，未配置时模块完全隐藏）
2. 内置授权确认文本（朗读 + 签署留痕），授权记录本地 SQLite 留存
3. 合规红线校验：仅限本人或已获书面授权的音色，未授权一律拒绝克隆
4. 克隆音色仅用于主动外呼场景（IVR 接听等场景禁用）
5. 完全隐藏（规则 9）：未配置 API Key / 授权时，克隆入口不出现、不报错，
   外呼主流程零影响

合规设计：
- 授权记录包含：声权人姓名、与使用者关系、授权时间、样本 SHA256 哈希、
  授权文本快照、授权范围（仅限本人外呼场景使用）
- 禁止模拟他人声音外呼；书面授权需使用者显式确认（written_authorized=True）

无 Key 原则（规则 16）：克隆为可选增强能力，不配置任何 Key 时主流程完整可用。

依赖：纯 Python 标准库（sqlite3 + hashlib + urllib）
联系信息：njskills@agent.qq.com

版本：v1.0 (2026-09-20)
"""

import os
import json
import hashlib
import sqlite3
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple

logger = logging.getLogger(__name__)

# ==========================================
# 配置
# ==========================================

DB_PATH = os.path.join(os.path.expanduser("~"), ".wecom_voice", "voice_auth.db")

# 克隆服务商：doubao（豆包）/ minimax（MiniMax），环境变量配置
CLONE_PROVIDER = os.environ.get("CLONE_PROVIDER", "")          # doubao / minimax / 空
CLONE_API_KEY = os.environ.get("CLONE_API_KEY", "")
CLONE_API_URL = os.environ.get("CLONE_API_URL", "")            # 可选，默认按服务商推导
# 干跑模式（测试用）：CLONE_API_DRY_RUN=1 时不发网络请求，返回模拟音色 ID
CLONE_API_DRY_RUN = os.environ.get("CLONE_API_DRY_RUN", "") == "1"

# 内置授权确认文本（朗读 + 签署留痕，不可跳过）
AUTHORIZATION_TEMPLATE = (
    "语音克隆授权确认：本人{owner}已知晓并同意，将本人语音样本用于生成克隆音色，"
    "该音色仅限{user}本人用于企业外呼场景，不得用于任何其他用途或转移给第三方。"
    "授权时间：{time}。如不同意，请终止克隆流程。"
)

# 克隆音色允许使用的场景（仅主动外呼）
CLONE_ALLOWED_SCENES = ("outbound",)

# 默认 API 端点（按服务商推导，可被 CLONE_API_URL 覆盖）
DEFAULT_API_URLS = {
    "doubao": "https://api.coze.cn/v1/audio/voices/clone",
    "minimax": "https://api.minimax.chat/v1/voice_clone",
}


# ==========================================
# 语音克隆模块
# ==========================================

class VoiceCloneModule:
    """
    语音克隆外呼模块

    使用方式：
        clone = VoiceCloneModule()

        # 1. 检查模块是否可见（未配置时完全隐藏）
        status = clone.module_status()
        if not status["visible"]:
            ...  # 不展示克隆入口

        # 2. 登记授权（本人或书面授权）
        auth_id = clone.register_authorization("张三", "self", sample_path)

        # 3. 合规校验通过后创建克隆音色
        voice = clone.create_clone_voice("品牌音色-张三", auth_id)

        # 4. 仅外呼场景可用
        clone.is_allowed_in_scene("outbound")  # True
        clone.is_allowed_in_scene("ivr")       # False
    """

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._db_ok = True
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self._init_db()
        except Exception as e:
            # 降级：数据库不可用时模块保持隐藏，不阻断外呼主流程（规则 9）
            self._db_ok = False
            logger.warning(f"克隆授权数据库初始化失败，模块降级为不可用: {e}")

    # ---------- 数据库 ----------

    def _init_db(self):
        """初始化授权与克隆音色表"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS voice_authorizations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    auth_id TEXT NOT NULL UNIQUE,
                    owner_name TEXT NOT NULL,
                    relation TEXT NOT NULL,
                    sample_path TEXT DEFAULT '',
                    sample_sha256 TEXT DEFAULT '',
                    consent_text TEXT DEFAULT '',
                    written_authorized INTEGER DEFAULT 0,
                    scope TEXT DEFAULT 'outbound_only',
                    created_at TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS clone_voices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    voice_id TEXT NOT NULL UNIQUE,
                    display_name TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    owner_auth_id TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'active',
                    created_at TEXT NOT NULL
                )
            """)

    # ---------- 模块可见性（规则 9：未配置完全隐藏） ----------

    def is_enabled(self) -> bool:
        """是否配置了克隆能力（服务商 + API Key 均就绪）"""
        return bool(CLONE_PROVIDER) and bool(CLONE_API_KEY)

    def module_status(self) -> Dict[str, Any]:
        """
        模块状态：未配置时 visible=False，调用方应完全隐藏克隆入口

        Returns:
            {"visible": bool, "provider": str, "reason": str}
        """
        if not self._db_ok:
            return {"visible": False, "provider": CLONE_PROVIDER, "reason": "授权数据库不可用，模块已降级"}
        if not CLONE_PROVIDER:
            return {"visible": False, "provider": "", "reason": "未配置 CLONE_PROVIDER（doubao/minimax）"}
        if not CLONE_API_KEY:
            return {"visible": False, "provider": CLONE_PROVIDER, "reason": "未配置 CLONE_API_KEY"}
        return {"visible": True, "provider": CLONE_PROVIDER, "reason": "克隆能力已就绪"}

    # ---------- 授权登记与合规校验 ----------

    def register_authorization(self, owner_name: str, relation: str, sample_path: str = "",
                               written_authorized: bool = False) -> str:
        """
        登记语音克隆授权（内置授权确认文本留痕）

        Args:
            owner_name: 声权人姓名
            relation: 与使用者关系（self=本人 / colleague=同事 / other=其他）
            sample_path: 录音样本路径（用于计算 SHA256 防篡改）
            written_authorized: 是否已获书面授权（非本人必须为 True 才通过合规）

        Returns:
            auth_id
        """
        auth_id = f"AUTH{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        if not self._db_ok:
            logger.warning("授权数据库不可用，无法登记授权")
            return ""
        sample_sha256 = self._sha256_file(sample_path) if sample_path else ""
        consent_text = AUTHORIZATION_TEMPLATE.format(
            owner=owner_name,
            user="本技能使用者",
            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO voice_authorizations
                (auth_id, owner_name, relation, sample_path, sample_sha256,
                 consent_text, written_authorized, scope, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (auth_id, owner_name, relation, sample_path, sample_sha256,
                  consent_text, 1 if written_authorized else 0,
                  "outbound_only", datetime.now().isoformat()))
        logger.info(f"授权登记完成: {auth_id}（声权人: {owner_name}, 关系: {relation}）")
        return auth_id

    def get_authorization(self, auth_id: str) -> Optional[Dict[str, Any]]:
        """查询授权记录"""
        if not self._db_ok:
            return None
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                row = conn.execute(
                    "SELECT * FROM voice_authorizations WHERE auth_id = ?", (auth_id,)
                ).fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.warning(f"查询授权记录失败: {e}")
            return None

    def check_compliance(self, auth_id: str) -> Tuple[bool, str]:
        """
        合规红线校验：仅限本人或已获书面授权的音色

        Returns:
            (是否通过, 原因)
        """
        record = self.get_authorization(auth_id)
        if not record:
            return False, "授权记录不存在"
        if record["relation"] == "self":
            return True, "本人授权，合规"
        if record["written_authorized"] == 1:
            return True, "已获书面授权，合规"
        return False, (
            f"拒绝克隆：声权人「{record['owner_name']}」非本人且无书面授权。"
            "仅限克隆本人或已获书面授权的音色，禁止模拟他人声音外呼。"
        )

    @staticmethod
    def _sha256_file(path: str) -> str:
        """计算样本文件 SHA256（防篡改留痕）；读取失败时降级为空串并告警"""
        try:
            h = hashlib.sha256()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    h.update(chunk)
            return h.hexdigest()
        except Exception as e:
            logger.warning(f"样本文件读取失败，SHA256 留痕跳过: {e}")
            return ""

    # ---------- 克隆音色创建 ----------

    def create_clone_voice(self, display_name: str, auth_id: str) -> Dict[str, Any]:
        """
        创建克隆音色（合规校验通过 + 模块已启用 才执行）

        Returns:
            {"ok": True, "voice_id": ..., "display_name": ..., "provider": ...}
            或 {"ok": False, "reason": ...}（任何失败均不抛出）
        """
        # 1. 模块启用检查（规则 9）
        status = self.module_status()
        if not status["visible"]:
            return {"ok": False, "reason": f"克隆模块未启用：{status['reason']}"}

        # 2. 合规红线检查
        ok, reason = self.check_compliance(auth_id)
        if not ok:
            logger.warning(f"克隆被合规拒绝: {reason}")
            return {"ok": False, "reason": reason}

        # 3. 调用克隆 API（干跑模式跳过网络）
        if CLONE_API_DRY_RUN:
            voice_id = f"clone_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            api_result = {"ok": True, "voice_id": voice_id}
        else:
            api_result = self._call_clone_api(display_name, auth_id)
        if not api_result.get("ok"):
            return {"ok": False, "reason": api_result.get("reason", "克隆 API 调用失败")}

        # 4. 登记克隆音色
        voice_id = api_result["voice_id"]
        if not self._db_ok:
            return {"ok": False, "reason": "授权数据库不可用，无法登记克隆音色"}
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO clone_voices
                (voice_id, display_name, provider, owner_auth_id, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (voice_id, display_name, CLONE_PROVIDER, auth_id, "active",
                  datetime.now().isoformat()))
        logger.info(f"克隆音色创建成功: {voice_id}（{display_name}）")
        return {"ok": True, "voice_id": voice_id, "display_name": display_name,
                "provider": CLONE_PROVIDER, "auth_id": auth_id}

    def _call_clone_api(self, display_name: str, auth_id: str) -> Dict[str, Any]:
        """
        调用克隆服务商 API（豆包 / MiniMax）

        任何网络/协议异常均降级为 {"ok": False, "reason": ...}，不抛出。
        """
        try:
            from urllib.request import Request, urlopen
            import ssl

            record = self.get_authorization(auth_id) or {}
            url = CLONE_API_URL or DEFAULT_API_URLS.get(CLONE_PROVIDER, "")
            if not url:
                return {"ok": False, "reason": f"未知克隆服务商: {CLONE_PROVIDER}"}

            payload = {
                "voice_name": display_name,
                "provider": CLONE_PROVIDER,
                "authorization": {
                    "auth_id": auth_id,
                    "owner_name": record.get("owner_name", ""),
                    "relation": record.get("relation", ""),
                    "sample_sha256": record.get("sample_sha256", ""),
                    "written_authorized": bool(record.get("written_authorized")),
                },
            }
            req = Request(url, data=json.dumps(payload).encode("utf-8"),
                          headers={"Content-Type": "application/json",
                                   "Authorization": f"Bearer {CLONE_API_KEY}"})
            ctx = ssl.create_default_context()
            with urlopen(req, timeout=15, context=ctx) as resp:
                body = json.loads(resp.read().decode("utf-8"))

            # 兼容常见响应字段
            data = body.get("data", body)
            voice_id = (data.get("voice_id") or data.get("id")
                        or data.get("voiceID") or "")
            if voice_id:
                return {"ok": True, "voice_id": voice_id}
            return {"ok": False, "reason": f"克隆 API 响应缺少 voice_id: {body}"}
        except Exception as e:
            logger.warning(f"克隆 API 调用失败: {e}")
            return {"ok": False, "reason": f"克隆 API 调用失败: {e}"}

    # ---------- 克隆音色管理 ----------

    def list_clone_voices(self) -> List[Dict[str, Any]]:
        """列出已登记的克隆音色"""
        if not self._db_ok:
            return []
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    "SELECT * FROM clone_voices WHERE status = 'active' ORDER BY created_at DESC"
                ).fetchall()
            return [dict(r) for r in rows]
        except Exception as e:
            logger.warning(f"查询克隆音色失败: {e}")
            return []

    def delete_clone_voice(self, voice_id: str) -> bool:
        """注销克隆音色（软删除）"""
        if not self._db_ok:
            return False
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.execute(
                    "UPDATE clone_voices SET status = 'deleted' WHERE voice_id = ?", (voice_id,)
                )
                return cur.rowcount > 0
        except Exception as e:
            logger.warning(f"注销克隆音色失败: {e}")
            return False

    # ---------- 场景限制（仅主动外呼） ----------

    def is_allowed_in_scene(self, scene: str) -> bool:
        """克隆音色仅允许用于主动外呼场景"""
        return scene in CLONE_ALLOWED_SCENES

    def scene_refusal_reason(self, scene: str) -> str:
        """场景拒绝原因（中文）"""
        return f"克隆音色仅用于主动外呼场景，当前场景「{scene or '(未指定)'}」已自动切换为预设音色。"


# ==========================================
# 便捷函数
# ==========================================

_clone_instance: Optional[VoiceCloneModule] = None


def get_clone_module() -> VoiceCloneModule:
    """获取克隆模块单例"""
    global _clone_instance
    if _clone_instance is None:
        _clone_instance = VoiceCloneModule()
    return _clone_instance


def module_status() -> Dict[str, Any]:
    """便捷函数：模块可见性（未配置时完全隐藏）"""
    return get_clone_module().module_status()


# ==========================================
# 命令行入口
# ==========================================

def _print_encoding_safe(text: str):
    """GBK 终端安全输出"""
    try:
        import sys
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    print(text)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="语音克隆外呼（v2.8）")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="查看模块状态（未配置时完全隐藏）")
    sub.add_parser("list", help="列出已登记克隆音色")
    sub.add_parser("selftest", help="运行自测")

    args = parser.parse_args()
    clone = get_clone_module()

    if args.command == "status":
        status = clone.module_status()
        _print_encoding_safe(f"克隆模块可见: {status['visible']}")
        _print_encoding_safe(f"服务商: {status['provider'] or '(未配置)'}")
        _print_encoding_safe(f"状态: {status['reason']}")
    elif args.command == "list":
        voices = clone.list_clone_voices()
        if not voices:
            _print_encoding_safe("暂无已登记的克隆音色。")
        for v in voices:
            _print_encoding_safe(f"  {v['display_name']}（{v['voice_id']}） 服务商: {v['provider']}")
    elif args.command == "selftest":
        run_self_test()
    else:
        parser.print_help()


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行语音克隆自测（使用临时数据库与临时样本，不触碰真实数据）"""
    import tempfile

    _print_encoding_safe("=" * 60)
    _print_encoding_safe("voice_clone.py — 自测模式")
    _print_encoding_safe("=" * 60)

    tmp_dir = tempfile.mkdtemp(prefix="voice_clone_test_")
    tmp_db = os.path.join(tmp_dir, "test_voice_auth.db")
    # 构造假样本文件
    sample_path = os.path.join(tmp_dir, "sample.wav")
    with open(sample_path, "wb") as f:
        f.write(b"RIFFfake_wav_data_for_sha256_test")

    clone = VoiceCloneModule(db_path=tmp_db)

    # 测试 1: 模块可见性（沙箱未配置 → 完全隐藏）
    _print_encoding_safe("\n[测试 1] 模块可见性（未配置时隐藏）")
    status = clone.module_status()
    _print_encoding_safe(f"  visible={status['visible']}  原因: {status['reason']}")
    if not status["visible"]:
        assert "未配置" in status["reason"]
        _print_encoding_safe("  未配置 → 模块完全隐藏 ✅")
    else:
        _print_encoding_safe("  当前环境已配置克隆能力（跳过隐藏断言）✅")

    # 测试 2: 授权登记（本人）+ SHA256 留痕
    _print_encoding_safe("\n[测试 2] 授权登记（本人）")
    auth_id = clone.register_authorization("张三", "self", sample_path)
    record = clone.get_authorization(auth_id)
    assert record is not None
    assert record["owner_name"] == "张三"
    assert len(record["sample_sha256"]) == 64, "SHA256 应为 64 位十六进制"
    assert "授权确认" in record["consent_text"]
    _print_encoding_safe(f"  auth_id={auth_id}  sha256={record['sample_sha256'][:16]}... ✅")

    # 测试 3: 合规校验（本人通过 / 他人无书面授权拒绝 / 他人有书面授权通过）
    _print_encoding_safe("\n[测试 3] 合规红线校验")
    ok, reason = clone.check_compliance(auth_id)
    assert ok is True
    _print_encoding_safe(f"  本人授权: {reason} ✅")

    auth_other = clone.register_authorization("李四", "other", sample_path, written_authorized=False)
    ok2, reason2 = clone.check_compliance(auth_other)
    assert ok2 is False and "书面授权" in reason2
    _print_encoding_safe(f"  他人无书面授权: 已拒绝 ✅")

    auth_written = clone.register_authorization("王五", "colleague", sample_path, written_authorized=True)
    ok3, reason3 = clone.check_compliance(auth_written)
    assert ok3 is True
    _print_encoding_safe(f"  他人有书面授权: {reason3} ✅")

    # 测试 4: 未启用时创建克隆被拒绝（规则 9）
    _print_encoding_safe("\n[测试 4] 未启用时拒绝创建")
    result = clone.create_clone_voice("测试音色", auth_id)
    if not clone.is_enabled():
        assert result["ok"] is False and "未启用" in result["reason"]
        _print_encoding_safe(f"  拒绝原因: {result['reason']} ✅")
    else:
        _print_encoding_safe("  当前环境已配置，跳过（干跑模式下见测试 5）✅")

    # 测试 5: 干跑模式全流程（模拟已配置环境）
    _print_encoding_safe("\n[测试 5] 干跑模式全流程")
    global CLONE_PROVIDER, CLONE_API_KEY, CLONE_API_DRY_RUN
    old_provider, old_key, old_dry = CLONE_PROVIDER, CLONE_API_KEY, CLONE_API_DRY_RUN
    try:
        CLONE_PROVIDER, CLONE_API_KEY, CLONE_API_DRY_RUN = "doubao", "test_key_xxx", True
        status5 = clone.module_status()
        assert status5["visible"] is True
        r5 = clone.create_clone_voice("品牌音色-张三", auth_id)
        assert r5["ok"] is True, r5
        assert r5["voice_id"].startswith("clone_")
        _print_encoding_safe(f"  创建成功: {r5['voice_id']} ✅")

        # 合规拒绝仍优先于模块启用
        r5b = clone.create_clone_voice("违规音色", auth_other)
        assert r5b["ok"] is False and "书面授权" in r5b["reason"]
        _print_encoding_safe("  合规红线优先于创建 ✅")

        voices = clone.list_clone_voices()
        assert len(voices) == 1
        _print_encoding_safe(f"  克隆音色列表: {len(voices)} 条 ✅")

        assert clone.delete_clone_voice(r5["voice_id"]) is True
        assert len(clone.list_clone_voices()) == 0
        _print_encoding_safe("  注销克隆音色 ✅")
    finally:
        CLONE_PROVIDER, CLONE_API_KEY, CLONE_API_DRY_RUN = old_provider, old_key, old_dry

    # 测试 6: 场景限制（仅主动外呼）
    _print_encoding_safe("\n[测试 6] 场景限制")
    assert clone.is_allowed_in_scene("outbound") is True
    for scene in ("ivr", "inbound", "system_notice"):
        assert clone.is_allowed_in_scene(scene) is False
    reason = clone.scene_refusal_reason("ivr")
    assert "仅用于主动外呼" in reason
    _print_encoding_safe(f"  outbound=允许  ivr/inbound=禁止 ✅")

    # 测试 7: 数据库不可用降级（规则 9）
    _print_encoding_safe("\n[测试 7] 数据库不可用降级")
    blocker = os.path.join(tmp_dir, "blocker")  # 用文件占用目录名，使 makedirs 必然失败
    with open(blocker, "w", encoding="utf-8") as f:
        f.write("x")
    bad_db = os.path.join(blocker, "sub", "voice_auth.db")
    clone_bad = VoiceCloneModule(db_path=bad_db)
    assert clone_bad._db_ok is False
    assert clone_bad.module_status()["visible"] is False
    assert clone_bad.register_authorization("张三", "self", sample_path) == ""
    assert clone_bad.get_authorization("whatever") is None
    assert clone_bad.list_clone_voices() == []
    assert clone_bad.delete_clone_voice("x") is False
    r7 = clone_bad.create_clone_voice("测试音色", "whatever")
    assert r7["ok"] is False
    _print_encoding_safe("  构造不抛异常、模块隐藏、写操作安全拒绝 ✅")

    # 清理临时目录
    import shutil
    shutil.rmtree(tmp_dir, ignore_errors=True)

    _print_encoding_safe(f"\n{'='*60}")
    _print_encoding_safe("所有自测通过 ✓")
    _print_encoding_safe("=" * 60)


if __name__ == "__main__":
    main()
