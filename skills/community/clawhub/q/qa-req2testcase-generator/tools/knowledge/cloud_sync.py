# _load_cloud_config (from orchestrator.py)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.utils import _read_json, _write_json, _ensure_dir

# _load_cloud_config (from orchestrator.py)
def _load_cloud_config(skill_dir):
    """读取 skill_v4/config/cloud.json 配置文件。
    如不存在返回默认配置（enabled=false），不抛异常。
    """
    config_path = os.path.join(skill_dir, "config", "cloud.json")
    if os.path.exists(config_path):
        try:
            return _read_json(config_path)
        except Exception:
            pass
    # 默认配置：全部关闭
    return {
        "review_tool": {
            "enabled": False,
            "api_url": "",
            "frontend_url": "",
            "api_key": "",
            "auto_push": False,
        },
        "experience_sync": {
            "enabled": False,
        }
    }



#!/usr/bin/env python3
# knowledge/cloud_sync.py — 知识库和评审经验同步
import os, json, urllib.request, urllib.error, time, hashlib, re

def _sync_knowledge_from_cloud(skill_dir, api_key, cloud_config):
    """V4.0.0: 从云端拉取知识库到本地

    流程：
    1. 读取本地版本号（.knowledge_version.json）
    2. 调用云端 GET /api/knowledge/version 获取最新版本
    3. 版本一致则跳过，不一致则下载
    4. 调用 GET /api/knowledge/pack 下载文件
    5. 写入本地 knowledge/ 目录
    6. 更新版本号
    """
    import urllib.request
    import urllib.error

    # 确定API base URL（兼容嵌套结构）
    api_base = (
        cloud_config.get("knowledge_api_url") or
        cloud_config.get("review_tool", {}).get("api_url") or
        cloud_config.get("experience_sync", {}).get("api_url") or
        ""
    )
    if not api_base:
        return "未配置云端地址"

    api_base = api_base.rstrip("/")

    # 1. 读取本地版本
    version_path = os.path.join(skill_dir, ".knowledge_version.json")
    local_version = None
    if os.path.exists(version_path):
        try:
            local_version = _read_json(version_path)
        except Exception:
            pass

    local_checksum = (local_version or {}).get("checksum", "")

    # 2. 检查云端版本
    try:
        ver_req = urllib.request.Request(
            f"{api_base}/api/knowledge/version",
            headers={"X-API-Key": api_key, "Content-Type": "application/json"}
        )
        with urllib.request.urlopen(ver_req, timeout=10) as resp:
            cloud_version = json.loads(resp.read().decode("utf-8"))

        if cloud_version.get("status") != "ok":
            return f"云端返回错误"

        cloud_data = cloud_version["data"]
        if cloud_data.get("checksum") == local_checksum:
            return f"已是最新（v{cloud_data['version']}）"

    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return "密码无权访问知识库"
        return f"云端版本检查失败(HTTP {e.code})"
    except Exception as e:
        return f"云端不可用({str(e)[:50]})"

    # 3. 下载知识库包
    try:
        pack_url = f"{api_base}/api/knowledge/pack"
        pack_req = urllib.request.Request(
            pack_url,
            headers={"X-API-Key": api_key, "Content-Type": "application/json"}
        )
        with urllib.request.urlopen(pack_req, timeout=30) as resp:
            pack = json.loads(resp.read().decode("utf-8"))

        if pack.get("status") != "ok":
            return f"下载失败"

        pack_data = pack["data"]
        files = pack_data.get("files", {})
        if not files:
            return "无文件"

        # 4. 写入本地
        saved_count = 0
        for rel_path, content in files.items():
            abs_path = os.path.join(skill_dir, "knowledge", rel_path)
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(content)
            saved_count += 1

        # 5. 更新版本号
        new_version = {
            "last_sync": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            "version": pack_data.get("version", ""),
            "checksum": pack_data.get("checksum", ""),
            "files_count": len(files),
        }
        with open(version_path, "w", encoding="utf-8") as f:
            json.dump(new_version, f, ensure_ascii=False, indent=2)

        return f"已同步{saved_count}个文件（v{pack_data.get('version', '?')}）"

    except urllib.error.HTTPError as e:
        return f"下载失败(HTTP {e.code})"
    except Exception as e:
        return f"同步失败({str(e)[:50]})"

