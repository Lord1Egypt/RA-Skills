"""
config.py - SmartEye 配置管理

设备配置文件路径（优先级从高到低）：
  1. ~/.openclaw/skills/smart-eye/devices/camera-devices.json（捆绑模板，首次自动复制到 2）
  2. ~/.openclaw/workspace/camera-devices.json（用户自定义，覆盖模板）

⚠️  安全：捆绑模板含示例凭证，请务必替换为真实密码后再使用！
"""

import json
import shutil
from pathlib import Path

# 路径定义
WORKSPACE = Path.home() / ".openclaw" / "workspace"
DEVICE_FILE = WORKSPACE / "camera-devices.json"   # 用户配置路径（覆盖用）
BUNDLED_TEMPLATE = Path(__file__).parent.parent / "devices" / "camera-devices.json"


def _ensure_file():
    """首次运行时将捆绑模板复制到用户配置路径。"""
    if not DEVICE_FILE.exists():
        DEVICE_FILE.parent.mkdir(parents=True, exist_ok=True)
        if BUNDLED_TEMPLATE.exists():
            shutil.copy(BUNDLED_TEMPLATE, DEVICE_FILE)


def load_devices() -> dict:
    """
    加载设备配置。

    优先级：
      1. ~/.openclaw/workspace/camera-devices.json（用户自定义）
      2. 捆绑模板（首次自动复制到 1）

    ⚠️  首次使用前请编辑 DEVICE_FILE，替换示例凭证为真实密码！
    """
    # 用户配置文件优先
    if DEVICE_FILE.exists():
        with open(DEVICE_FILE, encoding="utf-8") as f:
            return json.load(f)
    # 回退到捆绑模板（首次会自动复制到用户路径）
    if BUNDLED_TEMPLATE.exists():
        _ensure_file()
        with open(DEVICE_FILE, encoding="utf-8") as f:
            return json.load(f)
    # 极罕见：模板也不存在
    return {"cameras": [], "default": None}


def find_camera(devices: dict, name: str = None):
    """
    根据名称查找摄像头。

    匹配顺序：
      1. 精确匹配 id
      2. 模糊匹配 aliases（支持中文别名，如"建国路"）
      3. 精确匹配 brand
      4. 未指定 name → 使用 default 字段指定的摄像头

    Args:
        devices: load_devices() 返回的配置字典
        name:    用户指令中的摄像头名称（可空）

    Returns:
        匹配到的摄像头配置 dict，未找到返回 None
    """
    cameras = devices.get("cameras", [])
    default_id = devices.get("default")

    if not name:
        for c in cameras:
            if c["id"] == default_id:
                return c
        return cameras[0] if cameras else None

    name_lower = name.lower().strip()

    for c in cameras:
        if c["id"].lower() == name_lower:
            return c

    for c in cameras:
        for alias in c.get("aliases", []):
            al = alias.lower()
            if al == name_lower or name_lower in al or al in name_lower:
                return c

    for c in cameras:
        if c.get("brand", "").lower() == name_lower:
            return c

    return None


def list_cameras(devices: dict) -> list:
    """返回所有摄像头的可读摘要。"""
    lines = []
    cameras = devices.get("cameras", [])
    default_id = devices.get("default")
    for c in cameras:
        marker = " \u2190 默认" if c["id"] == default_id else ""
        ptz = c.get("ptz", {})
        caps = [axis.upper() for axis in ("pan", "tilt", "zoom")
                if ptz.get(axis, {}).get("supported")]
        lines.append(
            f"  [{c['id']}] {c.get('brand', '')} {c.get('model', '')}"
            f"  ({', '.join(c['aliases'])}){marker}"
            f"  PTZ: {', '.join(caps) if caps else 'none'}"
        )
    return lines
