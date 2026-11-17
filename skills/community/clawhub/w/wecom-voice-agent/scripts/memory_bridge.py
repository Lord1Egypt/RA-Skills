#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
memory_bridge.py — zwjh 长期记忆桥接子模块（v2.7）

功能：
1. 探测 zwjh MCP Server 是否存在（stdio JSON-RPC ping）
2. 来电时调用 zwjh_query 拉取来电者历史诉求与偏好
3. 将历史注入本轮对话 system prompt
4. 通话结束调用 deposit 写入本次通话摘要
5. 未安装 zwjh 时降级为旧版行为（无记忆，可选装提示）

依赖：纯 Python 标准库（subprocess + json + os）
联系信息：njskills@agent.qq.com

版本：v1.0 (2026-09-02)
"""

import os
import json
import time
import logging
import subprocess
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

# ==========================================
# 配置
# ==========================================

ZWJH_MCP_SERVER = os.environ.get("ZWJH_MCP_SERVER", "")
ZWJH_MCP_TIMEOUT = int(os.environ.get("ZWJH_MCP_TIMEOUT", "5"))
ZWJH_INSTALL_HINT = (
    "提示：安装 zwjh 长期记忆插件后，语音助手将能记住您的历史诉求和偏好，"
    "提供更加个性化的服务。访问 https://skillhub.cn/skill/zwjh 了解更多。"
)


# ==========================================
# zwjh MCP 探测
# ==========================================

class ZwjhMCPProbe:
    """探测 zwjh MCP Server 是否可用"""

    def __init__(self, server_path: str = ZWJH_MCP_SERVER, timeout: int = ZWJH_MCP_TIMEOUT):
        self.server_path = server_path
        self.timeout = timeout
        self._cached_result: Optional[bool] = None
        self._cache_time: float = 0
        self._cache_ttl: float = 60  # 缓存 60 秒

    def is_available(self) -> bool:
        """
        探测 zwjh MCP Server 是否可用

        Returns:
            bool: 可用返回 True
        """
        # 缓存命中
        now = time.time()
        if self._cached_result is not None and (now - self._cache_time) < self._cache_ttl:
            return self._cached_result

        # 未配置路径
        if not self.server_path:
            self._cached_result = False
            self._cache_time = now
            return False

        # 尝试 stdio JSON-RPC ping
        try:
            result = self._try_ping()
            self._cached_result = result
            self._cache_time = now
            return result
        except Exception as e:
            logger.debug(f"zwjh MCP 探测失败: {e}")
            self._cached_result = False
            self._cache_time = now
            return False

    def _try_ping(self) -> bool:
        """尝试 JSON-RPC ping"""
        # 构建 JSON-RPC initialize 请求
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "wecom-voice-agent", "version": "2.7.0"}
            }
        }

        try:
            proc = subprocess.run(
                self.server_path.split(),
                input=json.dumps(init_request) + "\n",
                capture_output=True,
                text=True,
                timeout=self.timeout,
                encoding="utf-8",
            )

            if proc.returncode != 0:
                return False

            # 检查响应是否包含 JSON-RPC 结果
            response = proc.stdout.strip()
            if not response:
                return False

            resp_data = json.loads(response)
            return "result" in resp_data or "jsonrpc" in resp_data

        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
            return False

    def invalidate_cache(self):
        """清除探测缓存"""
        self._cached_result = None
        self._cache_time = 0


# ==========================================
# zwjh 记忆桥接器
# ==========================================

class MemoryBridge:
    """
    zwjh 长期记忆桥接器

    使用方式：
        bridge = MemoryBridge()
        
        # 来电时拉取历史
        history = bridge.query_history("zhangsan", "13800138000")
        system_prompt = bridge.build_system_prompt(history)
        
        # 通话结束回写
        bridge.deposit_summary("zhangsan", "13800138000", "本次通话摘要...")
    """

    def __init__(self, server_path: str = ZWJH_MCP_SERVER, timeout: int = ZWJH_MCP_TIMEOUT):
        self.server_path = server_path
        self.timeout = timeout
        self.probe = ZwjhMCPProbe(server_path, timeout)

    def is_zwjh_available(self) -> bool:
        """检查 zwjh 是否可用"""
        return self.probe.is_available()

    def query_history(self, userid: str, phone: str = "") -> Optional[Dict[str, Any]]:
        """
        拉取来电者历史诉求与偏好

        Args:
            userid: 企微 userid
            phone: 手机号（备选键）

        Returns:
            dict: 历史记录，无记录返回 None
        """
        if not self.is_zwjh_available():
            return None

        # 优先用 userid 查询，备选用手机号
        query_result = self._call_zwjh_query(userid)
        if query_result is None and phone:
            query_result = self._call_zwjh_query(phone)

        return query_result

    def build_system_prompt(self, history: Optional[Dict[str, Any]]) -> str:
        """
        根据历史记录构建 system prompt 注入文本

        Args:
            history: zwjh 返回的历史记录

        Returns:
            str: 注入文本（追加到 system prompt 末尾）
        """
        if not history:
            return ""

        parts = ["\n\n[用户历史记忆]"]

        # 历史诉求
        past_requests = history.get("past_requests", [])
        if past_requests:
            parts.append("该用户历史诉求：")
            for i, req in enumerate(past_requests[-5:], 1):  # 最多 5 条
                parts.append(f"  {i}. {req.get('summary', '未知')} ({req.get('date', '未知日期')})")

        # 偏好
        preferences = history.get("preferences", {})
        if preferences:
            pref_parts = []
            for k, v in preferences.items():
                pref_parts.append(f"{k}: {v}")
            if pref_parts:
                parts.append(f"用户偏好：{', '.join(pref_parts)}")

        # 最近通话摘要
        last_call = history.get("last_call_summary", "")
        if last_call:
            parts.append(f"上次通话摘要：{last_call}")

        # 情绪倾向
        emotion_tendency = history.get("emotion_tendency", "")
        if emotion_tendency:
            parts.append(f"历史情绪倾向：{emotion_tendency}")

        return "\n".join(parts)

    def deposit_summary(self, userid: str, phone: str, summary: str,
                        intent: str = "", emotion: str = "") -> bool:
        """
        通话结束写入本次通话摘要

        Args:
            userid: 企微 userid
            phone: 手机号
            summary: 通话摘要
            intent: 主要意图
            emotion: 情感倾向

        Returns:
            bool: 写入成功返回 True
        """
        if not self.is_zwjh_available():
            return False

        deposit_data = {
            "source": "wecom-voice-agent",
            "userid": userid,
            "phone": phone,
            "summary": summary,
            "intent": intent,
            "emotion": emotion,
            "timestamp": datetime.now().isoformat(),
        }

        return self._call_deposit(deposit_data)

    def get_install_hint(self) -> str:
        """获取 zwjh 安装提示"""
        return ZWJH_INSTALL_HINT

    # === 内部方法 ===

    def _call_zwjh_query(self, key: str) -> Optional[Dict[str, Any]]:
        """调用 zwjh_query 工具"""
        request = {
            "jsonrpc": "2.0",
            "id": int(time.time() * 1000) % 100000,
            "method": "tools/call",
            "params": {
                "name": "zwjh_query",
                "arguments": {"key": key}
            }
        }

        response = self._send_request(request)
        if response and "result" in response:
            result = response["result"]
            # 解析 content
            content = result.get("content", [])
            if content and isinstance(content, list):
                for item in content:
                    if item.get("type") == "text":
                        try:
                            return json.loads(item["text"])
                        except json.JSONDecodeError:
                            return {"raw_text": item["text"]}
        return None

    def _call_deposit(self, data: Dict[str, Any]) -> bool:
        """调用 deposit 工具"""
        request = {
            "jsonrpc": "2.0",
            "id": int(time.time() * 1000) % 100000,
            "method": "tools/call",
            "params": {
                "name": "deposit",
                "arguments": data
            }
        }

        response = self._send_request(request)
        return response is not None and "error" not in response

    def _send_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """发送 JSON-RPC 请求到 zwjh MCP Server"""
        if not self.server_path:
            return None

        try:
            proc = subprocess.run(
                self.server_path.split(),
                input=json.dumps(request, ensure_ascii=False) + "\n",
                capture_output=True,
                text=True,
                timeout=self.timeout,
                encoding="utf-8",
            )

            if proc.returncode != 0:
                logger.warning(f"zwjh MCP 返回非零退出码: {proc.returncode}")
                return None

            response = proc.stdout.strip()
            if not response:
                return None

            return json.loads(response)

        except subprocess.TimeoutExpired:
            logger.warning("zwjh MCP 调用超时")
            return None
        except json.JSONDecodeError as e:
            logger.warning(f"zwjh MCP 响应解析失败: {e}")
            return None
        except FileNotFoundError:
            logger.warning(f"zwjh MCP Server 路径不存在: {self.server_path}")
            return None
        except Exception as e:
            logger.warning(f"zwjh MCP 调用异常: {e}")
            return None


# ==========================================
# 便捷函数
# ==========================================

_bridge_instance: Optional[MemoryBridge] = None


def get_bridge() -> MemoryBridge:
    """获取 MemoryBridge 单例"""
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = MemoryBridge()
    return _bridge_instance


def query_history(userid: str, phone: str = "") -> Optional[Dict[str, Any]]:
    """便捷函数：拉取历史"""
    return get_bridge().query_history(userid, phone)


def build_memory_prompt(history: Optional[Dict[str, Any]]) -> str:
    """便捷函数：构建记忆 prompt"""
    return get_bridge().build_system_prompt(history)


def deposit_summary(userid: str, phone: str, summary: str,
                    intent: str = "", emotion: str = "") -> bool:
    """便捷函数：写入摘要"""
    return get_bridge().deposit_summary(userid, phone, summary, intent, emotion)


def is_zwjh_available() -> bool:
    """便捷函数：检查 zwjh 是否可用"""
    return get_bridge().is_zwjh_available()


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行记忆桥接自测"""
    print("=" * 60)
    print("memory_bridge.py — 自测模式")
    print("=" * 60)

    # 测试 1: 探测（无 zwjh 时应返回 False）
    print("\n[测试 1] 探测 zwjh MCP")
    bridge = MemoryBridge()
    available = bridge.is_zwjh_available()
    print(f"  zwjh 可用: {available}")
    assert isinstance(available, bool)
    print("✅ 探测测试通过")

    # 测试 2: 历史查询（无 zwjh 时应返回 None）
    print("\n[测试 2] 历史查询")
    history = bridge.query_history("test_user", "13800138000")
    print(f"  历史: {history}")
    assert history is None or isinstance(history, dict)
    print("✅ 历史查询通过")

    # 测试 3: 构建 system prompt（无历史时返回空）
    print("\n[测试 3] 构建 system prompt（无历史）")
    prompt = bridge.build_system_prompt(None)
    print(f"  prompt: '{prompt}'")
    assert prompt == ""
    print("✅ 空历史 prompt 通过")

    # 测试 4: 构建 system prompt（有历史）
    print("\n[测试 4] 构建 system prompt（有历史）")
    mock_history = {
        "past_requests": [
            {"summary": "查询订单状态", "date": "2026-08-20"},
            {"summary": "投诉物流延迟", "date": "2026-08-22"},
        ],
        "preferences": {"language": "中文", "response_style": "简洁"},
        "last_call_summary": "用户反馈物流问题，已安排加急处理",
        "emotion_tendency": "偏焦虑",
    }
    prompt = bridge.build_system_prompt(mock_history)
    print(f"  prompt:\n{prompt}")
    assert "用户历史记忆" in prompt
    assert "物流" in prompt
    assert "焦虑" in prompt
    print("✅ 有历史 prompt 通过")

    # 测试 5: deposit（无 zwjh 时应返回 False）
    print("\n[测试 5] deposit 回写")
    result = bridge.deposit_summary("test_user", "13800138000", "测试摘要")
    print(f"  结果: {result}")
    assert result is False
    print("✅ deposit 降级通过")

    # 测试 6: 安装提示
    print("\n[测试 6] 安装提示")
    hint = bridge.get_install_hint()
    print(f"  提示: {hint[:30]}...")
    assert "zwjh" in hint
    print("✅ 安装提示通过")

    # 测试 7: 单例模式
    print("\n[测试 7] 单例模式")
    b1 = get_bridge()
    b2 = get_bridge()
    assert b1 is b2
    print("✅ 单例模式通过")

    print(f"\n{'='*60}")
    print("所有自测通过 ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_self_test()
