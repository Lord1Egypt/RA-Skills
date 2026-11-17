"""
Virsical 统一会话管理模块。

提供一站式"配置检查 → 登录认证 → License 权限检查"流程，
消除各工作流中重复的预检逻辑。所有业务模块应在执行操作前调用
ensure_ready(scene) 统一入口。
"""

import json
import sys
from typing import Optional

from .config import get_config, reset_config, DEFAULT_BASE_URL
from .auth_manager import TokenManager, check_token_before_login
from .license import check_license_for_scene


# 场景名到中文标签的映射
SCENE_LABELS = {
    "meeting": "会议管理",
    "visitor": "访客管理",
    "requirement": "报事报修",
}


def ensure_config() -> dict:
    """检查配置完整性，缺失时返回缺失字段列表。

    Returns:
        {"ready": bool, "missing": list, "message": str}
    """
    cfg = get_config()
    missing = cfg.validate()
    if missing:
        return {
            "ready": False,
            "missing": missing,
            "message": f"缺少配置: {', '.join(missing)}",
        }
    return {"ready": True, "missing": [], "message": "配置完整"}


def ensure_auth() -> dict:
    """检查认证状态，需要登录时返回 should_login=True。

    先执行智能预检查（本地 + 服务端双重验证）。

    Returns:
        {
            "ready": bool,
            "should_login": bool,
            "username": str,
            "message": str,
        }
    """
    # 强制重置缓存，确保读取最新 token
    reset_config()
    cfg = get_config()
    tm = TokenManager(cfg)
    result = check_token_before_login(tm)

    return {
        "ready": not result["should_login"],
        "should_login": result["should_login"],
        "username": result.get("username", ""),
        "message": result.get("message", ""),
    }


def ensure_license(scene: str) -> dict:
    """检查指定场景的 license 权限。

    Args:
        scene: 场景标识（"meeting" / "visitor" / "requirement"）

    Returns:
        {
            "ready": bool,
            "has_license": bool,
            "scene": str,
            "scene_name": str,
            "all_licenses": list,
            "message": str,
        }
    """
    result = check_license_for_scene(scene)
    return {
        "ready": result["has_license"],
        **result,
    }


def ensure_ready(scene: str) -> dict:
    """一站式预检：配置 → 认证 → License 权限。

    这是所有业务操作的统一入口。三步检查全部通过才返回 ready=True。
    任一步失败则返回 ready=False 及详细原因，调用方应据此向用户展示
    下一步操作指引（如提供凭证、发起登录）。

    Args:
        scene: 场景标识。支持：
               - "meeting"       → 会议管理（会议室查询/预订/列表）
               - "visitor"       → 访客管理
               - "requirement"   → 报事报修（工单创建）

    Returns:
        {
            "ready": bool,           # 三步检查是否全部通过
            "step": str,             # 当前所处步骤: "config" / "auth" / "license" / "done"
            "stage_message": str,    # 当前步骤的提示信息
            "username": str,         # 当前用户名
            "all_licenses": list,    # 用户拥有的所有 license
            "should_login": bool,    # 是否需要登录
            "has_license": bool,     # 是否有目标场景权限
            "scene": str,            # 场景标识
            "scene_name": str,       # 场景中文名
            "next_action": str,      # 建议的下一步操作描述
        }
    """
    # Step 1: 配置检查
    config_result = ensure_config()
    if not config_result["ready"]:
        return {
            "ready": False,
            "step": "config",
            "stage_message": config_result["message"],
            "username": "",
            "all_licenses": [],
            "should_login": False,
            "has_license": False,
            "scene": scene,
            "scene_name": SCENE_LABELS.get(scene, scene),
            "next_action": "配置不完整，请检查配置。",
        }

    # Step 2: 认证检查
    auth_result = ensure_auth()
    if not auth_result["ready"]:
        return {
            "ready": False,
            "step": "auth",
            "stage_message": auth_result["message"],
            "username": auth_result.get("username", ""),
            "all_licenses": [],
            "should_login": auth_result["should_login"],
            "has_license": False,
            "scene": scene,
            "scene_name": SCENE_LABELS.get(scene, scene),
            "next_action": f"需要登录 Virsical。请按以下步骤获取授权码：1）打开浏览器，访问威思客系统：https://www.virsical.com/guide.html ；2）登录您的账号后，点击右上角的用户信息，找到「Agent授权码」，复制授权码；3）将授权码粘贴到这里 👇",
        }

    # Step 3: License 检查
    license_result = ensure_license(scene)
    if not license_result["ready"]:
        return {
            "ready": False,
            "step": "license",
            "stage_message": license_result["message"],
            "username": auth_result.get("username", ""),
            "all_licenses": license_result.get("all_licenses", []),
            "should_login": False,
            "has_license": False,
            "scene": scene,
            "scene_name": SCENE_LABELS.get(scene, scene),
            "next_action": f"您暂无「{SCENE_LABELS.get(scene, scene)}」许可，请联系管理员开通权限。",
        }

    return {
        "ready": True,
        "step": "done",
        "stage_message": "预检通过",
        "username": auth_result.get("username", ""),
        "all_licenses": license_result.get("all_licenses", []),
        "should_login": False,
        "has_license": True,
        "scene": scene,
        "scene_name": SCENE_LABELS.get(scene, scene),
        "next_action": "可以执行业务操作。",
    }


# ── CLI ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python session.py <scene>")
        print("  scene: meeting / visitor / requirement")
        sys.exit(1)

    scene = sys.argv[1]
    result = ensure_ready(scene)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["ready"] else 1)
