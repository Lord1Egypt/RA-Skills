#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""
L1 Fast Check - 快速检查 (<200ms)

功能:
- 检查关键定义文件是否存在
- 检查文件大小是否合理
- 检查文件是否可读

使用方式:
    python scripts/l1_fast_check.py
    python scripts/l1_fast_check.py --json
"""

import json
import os
import sys
import time
from pathlib import Path

# 添加父目录到路径（用于导入 i18n）
sys.path.insert(0, str(Path(__file__).parent))
from i18n import get_i18n

# ============== 配置 ==============

DEFAULT_WORKSPACE = Path.home() / ".openclaw" / "workspace"
DEFAULT_CONFIG = Path.home() / ".openclaw" / "skills" / "system-healthcheck" / "config" / "default_config.yaml"

CRITICAL_FILES = [
    "SOUL.md",
    "IDENTITY.md",
    "AGENTS.md",
    "TOOLS.md",
    "MEMORY.md"
]

FILE_SIZE_LIMIT_KB = 50 * 1024  # 50KB


def load_config() -> dict:
    """加载配置文件"""
    config = {
        "workspace": DEFAULT_WORKSPACE,
        "critical_files": CRITICAL_FILES,
        "file_size_limit_kb": FILE_SIZE_LIMIT_KB,
    }
    
    config_file = Path(DEFAULT_CONFIG)
    if config_file.exists():
        try:
            import yaml
            with open(config_file, "r", encoding="utf-8") as f:
                full_config = yaml.safe_load(f) or {}
                l1_config = full_config.get("l1", {})
                if l1_config.get("critical_files"):
                    config["critical_files"] = l1_config["l1"]["critical_files"]
                if l1_config.get("timeout_ms"):
                    config["timeout_ms"] = l1_config["timeout_ms"]
        except ImportError:
            pass  # 无 yaml 库时使用默认配置
        except Exception:
            pass  # 配置加载失败时使用默认配置
    
    return config


def check_file_exists(file_path: Path) -> tuple:
    """检查文件是否存在
    
    Returns:
        (exists: bool, size_kb: int, readable: bool)
    """
    if not file_path.exists():
        return False, 0, False
    
    try:
        size = file_path.stat().st_size
        size_kb = size // 1024
        
        # 检查是否可读
        with open(file_path, "r", encoding="utf-8") as f:
            f.read(1024)  # 只读 1KB 测试
        
        return True, size_kb, True
    except PermissionError:
        return True, 0, False
    except Exception:
        return True, 0, False


def run_l1_check(workspace: Path, critical_files: list) -> dict:
    """执行 L1 检查
    
    Returns:
        {
            "success": bool,
            "missing": list,
            "details": list
        }
    """
    results = {
        "success": True,
        "missing": [],
        "details": []
    }
    
    for filename in critical_files:
        file_path = workspace / filename
        exists, size_kb, readable = check_file_exists(file_path)
        
        detail = {
            "file": filename,
            "exists": exists,
            "size_kb": size_kb,
            "readable": readable
        }
        
        if not exists:
            results["success"] = False
            results["missing"].append(filename)
            detail["status"] = "missing"
        elif not readable:
            results["success"] = False
            detail["status"] = "unreadable"
        else:
            detail["status"] = "ok"
        
        results["details"].append(detail)
    
    return results


def format_output(results: dict, duration_ms: float, colorful: bool = True) -> str:
    """格式化输出"""
    i18n = get_i18n()
    
    lines = []
    
    # 标题
    lines.append(f"{i18n.t('l1.title')} · {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    
    # 文件检查详情
    for detail in results["details"]:
        filename = detail["file"]
        status = detail["status"]
        
        if status == "ok":
            icon = i18n.t("status.ok")
            size_info = f" ({detail['size_kb']}KB)"
        elif status == "missing":
            icon = i18n.t("status.error")
            size_info = ""
        else:  # unreadable
            icon = i18n.t("status.error")
            size_info = ""
        
        lines.append(f"{icon} {filename}{size_info}")
    
    lines.append("")
    lines.append("━" * 40)
    
    # 总结
    if results["success"]:
        lines.append(f"{i18n.t('l1.ok')}")
    else:
        missing = ", ".join(results["missing"])
        lines.append(i18n.t("l1.error", files=missing))
    
    lines.append(f"{i18n.t('meta.duration', seconds=f'{duration_ms:.0f}ms')}")
    
    return "\n".join(lines)


def main():
    """主函数"""
    start = time.time()
    
    # 加载配置
    config = load_config()
    workspace = Path(config.get("workspace", DEFAULT_WORKSPACE))
    critical_files = config.get("critical_files", CRITICAL_FILES)
    
    # 解析命令行参数
    json_output = "--json" in sys.argv
    quiet = "--quiet" in sys.argv
    
    # 执行检查
    results = run_l1_check(workspace, critical_files)
    
    duration_ms = (time.time() - start) * 1000
    
    # 输出
    if json_output:
        results["duration_ms"] = duration_ms
        print(json.dumps(results, indent=2))
    elif quiet:
        # 静默模式：仅返回退出码
        sys.exit(0 if results["success"] else 1)
    else:
        print(format_output(results, duration_ms))
        sys.exit(0 if results["success"] else 1)


if __name__ == "__main__":
    main()
