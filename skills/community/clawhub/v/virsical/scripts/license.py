"""
Virsical License 检查模块。

在认证登录后检查用户是否有对应场景的 license 权限：
- vst: 访客管理
- fm: 报事报修（工单）
- smt: 会议管理

注意：cloud-oms 的 license 接口仅需 Bearer token，不需要 vsk-signature 签名。

使用方式：
    python -c "from scripts.license import check_license_for_scene; print(check_license_for_scene('meeting'))"
"""

import json
from typing import Optional, List
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from .config import get_config, VirsicalConfig
from .auth_manager import TokenManager

# 产品码与场景名称的映射
PRODUCT_CODE_MAP = {
    "vst": "访客管理",
    "fm": "报事报修",
    "smt": "会议管理",
    "cloud": "云平台",
    "common": "通用基础",
    "w": "办公空间",
}

# 场景标识 → 产品码
SCENE_CODE_MAP = {
    "visitor": "vst",        # 访客
    "requirement": "fm",     # 报事报修
    "meeting": "smt",        # 会议
}

# License 接口路径（cloud-oms 微服务，仅需 Bearer token，无需 vsk-signature）
LICENSE_API_PATH = "/vsk/cloud-oms/tenants/using/all/productCodes"


def _get_token() -> str:
    """获取当前有效的 access token（复用全局 TokenManager）。"""
    from .auth_manager import TokenManager
    cfg = get_config()
    tm = TokenManager(cfg)
    token = tm.get_access_token()
    if not token:
        raise Exception("Not authenticated. Please login first.")
    return token


def fetch_licenses() -> dict:
    """获取用户租户的所有产品许可列表。

    调用 GET /vsk/cloud-oms/tenants/using/all/productCodes 接口。
    该接口仅需 Bearer token，不需要 vsk-signature 签名头。

    Returns:
        {
            "success": bool,
            "licenses": list,   # 产品码列表，如 ["cloud", "common", "vst", "w", "fm", "smt"]
            "message": str,
        }
    """
    cfg = get_config()
    url = f"{cfg.base_url}{LICENSE_API_PATH}"

    try:
        token = _get_token()
    except Exception as e:
        return {
            "success": False,
            "licenses": [],
            "message": f"未登录: {e}",
        }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    try:
        req = Request(url, headers=headers, method="GET")
        with urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())

        if result.get("code") == 0:
            licenses = result.get("data", [])
            return {
                "success": True,
                "licenses": licenses,
                "message": f"获取到 {len(licenses)} 个产品许可",
            }
        else:
            return {
                "success": False,
                "licenses": [],
                "message": f"获取许可列表失败: {result.get('msg', '未知错误')}",
            }
    except HTTPError as e:
        try:
            body = json.loads(e.read().decode())
            msg = body.get("msg", e.reason)
        except Exception:
            msg = str(e.reason)
        return {
            "success": False,
            "licenses": [],
            "message": f"请求失败 (HTTP {e.code}): {msg}",
        }
    except URLError as e:
        return {
            "success": False,
            "licenses": [],
            "message": f"网络错误: {e.reason}",
        }
    except Exception as e:
        return {
            "success": False,
            "licenses": [],
            "message": f"获取许可列表异常: {e}",
        }


def check_license(scene: str,
                  licenses: Optional[List[str]] = None) -> dict:
    """检查用户是否拥有指定场景的 license。

    Args:
        scene: 场景标识。支持以下值：
               - "visitor" / "vst"       → 访客管理
               - "requirement" / "fm"    → 报事报修
               - "meeting" / "smt"       → 会议管理
        licenses: 已获取的 license 列表（可选，不传则自动调用 fetch_licenses）

    Returns:
        {
            "has_license": bool,
            "scene": str,        # 场景标识
            "scene_name": str,   # 场景中文名称
            "message": str,      # 结果描述
        }
    """
    # 将场景标识映射为产品码
    code = SCENE_CODE_MAP.get(scene, scene)
    scene_name = PRODUCT_CODE_MAP.get(code, code)

    # 获取 license 列表
    if licenses is None:
        result = fetch_licenses()
        if not result["success"]:
            return {
                "has_license": False,
                "scene": scene,
                "scene_name": scene_name,
                "message": f"无法检查许可: {result['message']}",
            }
        licenses = result["licenses"]

    has_license = code in licenses

    if has_license:
        return {
            "has_license": True,
            "scene": scene,
            "scene_name": scene_name,
            "message": f"已拥有「{scene_name}」许可",
        }
    else:
        return {
            "has_license": False,
            "scene": scene,
            "scene_name": scene_name,
            "message": f"您暂无「{scene_name}」许可，无法使用该功能。请联系管理员开通权限。",
        }


def check_license_for_scene(scene: str) -> dict:
    """一站式检查：自动获取 licenses 列表并检查指定场景的许可。

    这是最常用的入口函数，一次调用完成认证 → 获取许可 → 检查三步。

    Args:
        scene: 场景标识。支持：
               - "visitor" / "vst"       → 访客管理
               - "requirement" / "fm"    → 报事报修
               - "meeting" / "smt"       → 会议管理

    Returns:
        {
            "has_license": bool,
            "scene": str,
            "scene_name": str,
            "all_licenses": list,    # 完整的 license 列表
            "message": str,
        }
    """
    result = fetch_licenses()
    if not result["success"]:
        code = SCENE_CODE_MAP.get(scene, scene)
        return {
            "has_license": False,
            "scene": scene,
            "scene_name": PRODUCT_CODE_MAP.get(code, code),
            "all_licenses": [],
            "message": result["message"],
        }

    check = check_license(scene, result["licenses"])
    check["all_licenses"] = result["licenses"]
    return check


def format_license_list(licenses: List[str]) -> str:
    """格式化 license 列表为可读文本。

    Args:
        licenses: 产品码列表

    Returns:
        格式化的多行文本
    """
    lines = []
    for code in licenses:
        name = PRODUCT_CODE_MAP.get(code, code)
        lines.append(f"  - {code}（{name}）")
    return "\n".join(lines) if lines else "  （无许可）"


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法：python license.py <scene>")
        print("  scene: meeting / visitor / requirement")
        print("  或直接使用产品码: smt / vst / fm")
        sys.exit(1)

    scene = sys.argv[1]
    result = check_license_for_scene(scene)
    print(json.dumps(result, ensure_ascii=False, indent=2))
