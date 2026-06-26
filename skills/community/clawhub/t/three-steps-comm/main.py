"""
沟通三部曲 - 执行入口
思考 → 执行 → 复盘
TTL 验证逻辑（7天免费 → API 校验）
"""

import os, json, time, sys
from pathlib import Path
from typing import Dict, Any, Optional

# ============================================================
# TTL 配置区（用户付费后填入 API_KEY）
# ============================================================
API_KEY = ""  # 付费后获得，填入这里
API_URL = "https://www.kaiwu8.com/verify"
SKILL_ID = "three-steps-comm"
LOCAL_TTL_FILE = os.path.join(os.path.dirname(__file__), ".ttl")
FREE_TTL_DAYS = 7  # 免费体验天数
RENEWAL_INTERVAL = 7 * 86400  # 付费后每7天校验一次


def _get_local_ttl() -> Optional[int]:
    """读取本地 TTL 过期时间戳"""
    if not os.path.exists(LOCAL_TTL_FILE):
        return None
    try:
        with open(LOCAL_TTL_FILE, "r") as f:
            data = json.load(f)
        return data.get("expires_at")
    except:
        return None


def _save_local_ttl(expires_at: int) -> None:
    """保存 TTL 过期时间戳"""
    with open(LOCAL_TTL_FILE, "w") as f:
        json.dump({"expires_at": expires_at, "skill_id": SKILL_ID}, f)


def _init_ttl() -> int:
    """首次使用初始化 7 天 TTL"""
    expires_at = int(time.time()) + FREE_TTL_DAYS * 86400
    _save_local_ttl(expires_at)
    return expires_at


def _verify_ttl() -> bool:
    """验证 TTL 是否有效"""
    current = int(time.time())

    # 读取本地 TTL
    expires_at = _get_local_ttl()
    if expires_at is None:
        expires_at = _init_ttl()

    # 本地 TTL 未过期 → 直接通过
    if expires_at > current:
        return True

    # 本地 TTL 已过期
    # 有 API_KEY → 调用 API 尝试续期
    if API_KEY:
        try:
            import urllib.request, urllib.error
            payload = json.dumps({"api_key": API_KEY, "skill_id": SKILL_ID}).encode()
            req = urllib.request.Request(
                API_URL,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read())
                if result.get("valid"):
                    new_expires_at = result.get("expires_at", current + RENEWAL_INTERVAL)
                    _save_local_ttl(new_expires_at)
                    return True
        except Exception:
            pass
        return False

    # 无 API_KEY 且本地 TTL 过期 → 提示续费
    return False


def _check_and_renew_ttl() -> None:
    """每次调用检查 TTL"""
    if not _verify_ttl():
        print("[TTL] 免费体验已到期，请前往 https://www.kaiwu8.com 续费获取 API_KEY")
        raise PermissionError("Skill 授权已过期，请续费后填入 API_KEY 继续使用")


# ============================================================
# 沟通三部曲核心逻辑
# ============================================================

def think(message: str, context: Dict = None) -> Dict[str, Any]:
    """第一步：思考"""
    context = context or {}

    analysis = {
        "raw_message": message,
        "length": len(message),
        "has_question": "？" in message or "?" in message,
        "has_request": any(kw in message for kw in ["帮我", "请", "能不能", "可以帮我"]),
        "is_greeting": message.strip() in ["你好", "hi", "hello", "嗨", "哈喽"],
    }

    if analysis["is_greeting"]:
        msg_type = "greeting"
    elif analysis["has_request"]:
        msg_type = "request"
    elif analysis["has_question"]:
        msg_type = "question"
    else:
        msg_type = "statement"

    intent_map = {
        "greeting": "打招呼，建立连接",
        "request": "寻求帮助或行动",
        "question": "获取信息",
        "statement": "分享想法或状态",
    }

    return {
        "analysis": analysis,
        "type": msg_type,
        "intent": intent_map.get(msg_type, "未知"),
        "context_summary": f"收到{context.get('channel', '未知渠道')}消息",
    }


def execute(message: str, thinking: Dict, context: Dict = None) -> Dict[str, Any]:
    """第二步：执行"""
    context = context or {}
    msg_type = thinking.get("type", "statement")

    if msg_type == "greeting":
        response = "你好！有什么我可以帮你的吗？"
        next_action = "等待对方提出具体需求"
    elif msg_type == "request":
        response = f"收到你的请求，我来帮你处理。"
        next_action = "执行具体任务"
    elif msg_type == "question":
        response = f"你问的是：{message}"
        next_action = "组织答案"
    else:
        response = f"我听到了：{message}"
        next_action = "确认或继续对话"

    return {
        "response": response,
        "next_action": next_action,
        "executed": True,
    }


def review(message: str, thinking: Dict, execution: Dict, context: Dict = None) -> Dict[str, Any]:
    """第三步：复盘"""
    context = context or {}
    msg_type = thinking.get("type", "unknown")

    if msg_type == "greeting":
        score = 8
        assessment = "打招呼流畅，建立了好印象"
        improvement = "可以更个性化一点"
    elif msg_type == "request":
        score = 7
        assessment = "理解了需求并开始执行"
        improvement = "可以先确认理解是否正确再执行"
    elif msg_type == "question":
        score = 6
        assessment = "识别了问题"
        improvement = "需要更深入理解问题的本质"
    else:
        score = 5
        assessment = "听到了内容"
        improvement = "可以更主动地引导对话"

    return {
        "score": score,
        "assessment": assessment,
        "improvement": improvement,
        "learned": f"下次遇到{msg_type}类型要{improvement}",
    }


def communicate(message: str, context: Dict = None) -> Dict[str, Any]:
    """
    沟通三部曲主入口
    思考 → 执行 → 复盘
    """
    # 每次调用检查 TTL
    _check_and_renew_ttl()

    context = context or {}

    thinking = think(message, context)
    execution = execute(message, thinking, context)
    review_result = review(message, thinking, execution, context)

    return {
        "step": "三部曲完成",
        "thinking": thinking,
        "execution": execution,
        "review": review_result,
    }


if __name__ == "__main__":
    # 测试
    result = communicate("你好")
    print(f"类型: {result['thinking']['type']}")
    print(f"响应: {result['execution']['response']}")
    print(f"复盘评分: {result['review']['score']}/10")