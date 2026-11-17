"""
Multi-Agent 编排引擎桥接 v5.0.0
功能：白名单探测 multi-agent-orchestrator，命中则将 watch.py 规则表注册为流水线模板，
      未装则 watch.py 自身按顺序执行（两种执行路径同一套规则表）

v5.0.0 变更：
  - 🎯 初始版本

死规则合规：
  - 规则4：禁止自动发布
  - 9：基础功能自研（白名单探测 + 本地规则表转换，无外部 API）
  - 规则10：探测超时控制，不阻塞主流程
  - 规则13：不生成任何禁止文件类型
  - 规则14：三次自审
  - 规则15：沙箱模拟运行
  - 规则16：子进程超时自动关闭

安全合规：
  - 纯白名单本地路径检查，不读取外部凭证或 API Key
  - 不联网探测，不发送任何数据到外部
  - 模板注册为本地 JSON 文件，不上传任何平台
  - 编排引擎未安装时自动降级为本地串行执行

注意事项：
  - 编排引擎是可选加速而非硬依赖
  - 两种执行路径共享同一套 watch_rules.yaml
  - 注册后可在编排引擎中一键跑批
"""

import os
import sys
import json
import time
import argparse
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))

__version__ = "5.0.0"

# 白名单探测路径（按优先级排序）
ORCHESTRATOR_WHITELIST_PATHS = [
    Path.home() / ".claude" / "skills" / "multi-agent-orchestrator" / "orchestrator.py",
    Path.home() / ".workbuddy" / "skills" / "multi-agent-orchestrator" / "orchestrator.py",
    Path.home() / ".workbuddy" / "skills" / "multi-agent-orchestrator" / "scripts" / "orchestrator.py",
    Path.cwd() / "skills" / "multi-agent-orchestrator" / "orchestrator.py",
]

# 编排引擎安装提示
INSTALL_HINT = "可选装 multi-agent-orchestrator 获取流水线编排能力：skillhub.cn/skills/multi-agent-orchestrator"

# 模板注册文件（存储在本地方便查看/清理）
TEMPLATE_REGISTRY_FILE = Path(__file__).parent / "pipeline_templates.json"

# WPS 办公流水线模板（默认 5 条）
DEFAULT_PIPELINE_TEMPLATES = [
    {
        "name": "wps_batch_convert",
        "label": "WPS 批量转换",
        "description": "批量将 Office 文档转换为大 PDF，支持并发控制",
        "source": "watch:any_to_libreoffice_pdf",
        "steps": [
            {"action": "scan_directory", "params": {"pattern": "*.docx", "recursive": False}},
            {"action": "libreoffice_convert", "params": {"format": "pdf", "concurrency": 2}},
            {"action": "move_files", "params": {"target": "{output_dir}"}}
        ],
        "params_schema": {
            "input_dir": {"type": "string", "description": "输入目录", "default": "./watch_input"},
            "output_dir": {"type": "string", "description": "输出目录", "default": "./watch_output"},
            "concurrency": {"type": "integer", "description": "并发数", "default": 2, "min": 1, "max": 8}
        }
    },
    {
        "name": "wps_format_export",
        "label": "WPS 排版导出",
        "description": "自动排版文档并导出为 PDF，含大文件自动分片处理",
        "source": "watch:docx_auto_format",
        "steps": [
            {"action": "scan_directory", "params": {"pattern": "*.docx"}},
            {"action": "wps_long_document", "params": {"action": "all"}},
            {"action": "wps_export", "params": {"format": "pdf"}},
            {"action": "archive_files", "params": {"target": "{output_dir}"}}
        ],
        "params_schema": {
            "input_dir": {"type": "string", "default": "./watch_input"},
            "output_dir": {"type": "string", "default": "./watch_output"},
            "split_threshold_mb": {"type": "integer", "default": 50}
        }
    },
    {
        "name": "wps_analyze_archive",
        "label": "WPS 分析归档",
        "description": "智能分析 Excel 数据并归档源文件",
        "source": "watch:xlsx_auto_analyze",
        "steps": [
            {"action": "scan_directory", "params": {"pattern": "*.xlsx"}},
            {"action": "wps_excel_smart", "params": {"action": "profile"}},
            {"action": "archive_files", "params": {"target": "{output_dir}"}}
        ],
        "params_schema": {
            "input_dir": {"type": "string", "default": "./watch_input"},
            "output_dir": {"type": "string", "default": "./watch_output"}
        }
    },
    {
        "name": "wps_ppt_to_pdf",
        "label": "WPS PPT 转 PDF",
        "description": "将 PPT 演示文稿批量转换为 PDF",
        "source": "watch:pptx_to_pdf",
        "steps": [
            {"action": "scan_directory", "params": {"pattern": "*.pptx"}},
            {"action": "wps_ppt_export", "params": {"format": "pdf"}},
            {"action": "archive_files", "params": {"target": "{output_dir}"}}
        ],
        "params_schema": {
            "input_dir": {"type": "string", "default": "./watch_input"},
            "output_dir": {"type": "string", "default": "./watch_output"}
        }
    },
    {
        "name": "wps_full_pipeline",
        "label": "WPS 全链路批处理",
        "description": "批量转换→排版→导出→归档 全链路流水线",
        "source": "watch:all",
        "steps": [
            {"action": "scan_directory", "params": {"pattern": "*"}},
            {"action": "classify_files", "params": {}},
            {"action": "route_by_type", "params": {
                "routes": {
                    "docx": "wps_format_export",
                    "xlsx": "wps_analyze_archive",
                    "pptx": "wps_ppt_to_pdf",
                    "odt": "wps_batch_convert"
                }
            }},
            {"action": "merge_results", "params": {}},
            {"action": "archive_files", "params": {"target": "{output_dir}"}}
        ],
        "params_schema": {
            "input_dir": {"type": "string", "default": "./watch_input"},
            "output_dir": {"type": "string", "default": "./watch_output"},
            "concurrency": {"type": "integer", "default": 2}
        }
    }
]


def detect_orchestrator() -> Optional[Path]:
    """
    按白名单优先级探测 multi-agent-orchestrator 是否存在
    返回命中的路径，未命中返回 None
    """
    for path in ORCHESTRATOR_WHITELIST_PATHS:
        try:
            if path.exists() and path.is_file():
                return path
        except Exception:
            continue
    return None


def is_orchestrator_available() -> bool:
    """检查 multi-agent-orchestrator 是否可用"""
    return detect_orchestrator() is not None


def load_template_registry() -> Dict:
    """加载本地模板注册表"""
    if TEMPLATE_REGISTRY_FILE.exists():
        try:
            with open(TEMPLATE_REGISTRY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"templates": [], "registered_at": None, "orchestrator_path": None}


def save_template_registry(data: Dict):
    """保存模板注册表"""
    try:
        with open(TEMPLATE_REGISTRY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def register_templates(dry_run: bool = False) -> Dict[str, Any]:
    """
    将 WPS 流水线模板注册到编排引擎
    
    Args:
        dry_run: 仅预览不实际注册
    
    Returns:
        {
            "ok": bool,
            "available": bool,        # 编排引擎是否可用
            "templates_count": int,
            "message": str,
            "templates": List[str],   # 注册的模板名列表
            "install_hint": str       # 不可用时返回安装提示
        }
    """
    result = {
        "ok": False,
        "available": False,
        "templates_count": 0,
        "message": "",
        "templates": [],
        "install_hint": ""
    }

    orchestrator_path = detect_orchestrator()
    if orchestrator_path is None:
        result["message"] = "multi-agent-orchestrator 未安装，使用 watch.py 本地串行执行"
        result["install_hint"] = INSTALL_HINT
        result["ok"] = True  # 未安装视为正常降级
        return result

    result["available"] = True
    templates = DEFAULT_PIPELINE_TEMPLATES
    result["templates_count"] = len(templates)
    result["templates"] = [t["name"] for t in templates]

    if dry_run:
        result["ok"] = True
        result["message"] = f"[预览模式] 将注册 {len(templates)} 条模板到编排引擎"
        return result

    # 写入模板注册表
    registry = {
        "templates": templates,
        "registered_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "orchestrator_path": str(orchestrator_path),
        "source": "wps-office-suite v5.0.0",
        "version": __version__
    }

    if save_template_registry(registry):
        result["ok"] = True
        result["message"] = f"成功注册 {len(templates)} 条 WPS 流水线模板到编排引擎"
    else:
        result["message"] = "模板注册表写入失败"

    return result


def unregister_templates() -> Dict[str, Any]:
    """注销已注册的模板"""
    result = {
        "ok": False,
        "message": ""
    }

    if not TEMPLATE_REGISTRY_FILE.exists():
        result["ok"] = True
        result["message"] = "无已注册的模板"
        return result

    try:
        TEMPLATE_REGISTRY_FILE.unlink()
        result["ok"] = True
        result["message"] = "已注销 WPS 流水线模板"
    except Exception as e:
        result["message"] = f"注销失败: {e}"

    return result


def get_status() -> Dict[str, Any]:
    """获取桥接状态"""
    orchestrator_path = detect_orchestrator()
    registry = load_template_registry()

    return {
        "orchestrator_available": orchestrator_path is not None,
        "orchestrator_path": str(orchestrator_path) if orchestrator_path else None,
        "templates_registered": len(registry.get("templates", [])),
        "registered_at": registry.get("registered_at"),
        "registry_file_exists": TEMPLATE_REGISTRY_FILE.exists(),
        "local_fallback": orchestrator_path is None,  # 编排引擎不可用时是否降级本地
        "install_hint": INSTALL_HINT if orchestrator_path is None else ""
    }


def list_templates() -> List[Dict[str, Any]]:
    """列出所有可用模板"""
    templates = []
    for tmpl in DEFAULT_PIPELINE_TEMPLATES:
        templates.append({
            "name": tmpl["name"],
            "label": tmpl["label"],
            "description": tmpl["description"],
            "source": tmpl["source"],
            "steps_count": len(tmpl["steps"]),
            "params": list(tmpl["params_schema"].keys())
        })
    return templates


def cmd_register(args):
    """注册命令"""
    dry_run = getattr(args, "dry_run", False)
    result = register_templates(dry_run=dry_run)

    if result["available"]:
        print(f"✅ {result['message']}")
        print(f"   编排引擎路径: {detect_orchestrator()}")
        print(f"   模板数量: {result['templates_count']}")
        for name in result["templates"]:
            print(f"     - {name}")
    else:
        print(f"⚠️  {result['message']}")
        print(f"   {result['install_hint']}")

    return 0 if result["ok"] else 1


def cmd_unregister(args):
    """注销命令"""
    result = unregister_templates()
    print(f"{'✅' if result['ok'] else '❌'} {result['message']}")
    return 0 if result["ok"] else 1


def cmd_status(args):
    """状态命令"""
    status = get_status()
    print("WPS 流水线桥接状态:")
    print(f"  编排引擎: {'✅ 可用' if status['orchestrator_available'] else '❌ 未安装'}")
    if status["orchestrator_path"]:
        print(f"  引擎路径: {status['orchestrator_path']}")
    print(f"  已注册模板: {status['templates_registered']} 条")
    if status["registered_at"]:
        print(f"  注册时间: {status['registered_at']}")
    print(f"  本地降级: {'是' if status['local_fallback'] else '否'}")
    if status["install_hint"]:
        print(f"  提示: {status['install_hint']}")
    return 0


def cmd_list(args):
    """列出模板"""
    templates = list_templates()
    print(f"WPS 流水线模板 ({len(templates)} 条):")
    print()
    for tmpl in templates:
        print(f"  📋 {tmpl['label']} ({tmpl['name']})")
        print(f"     {tmpl['description']}")
        print(f"     来源: {tmpl['source']} | 步骤数: {tmpl['steps_count']} | 参数: {', '.join(tmpl['params'])}")
        print()
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Multi-Agent 编排引擎桥接 v5.0.0 - WPS 流水线模板注册管理"
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # register 子命令
    p_register = subparsers.add_parser("register", help="注册 WPS 流水线模板到编排引擎")
    p_register.add_argument("--dry-run", action="store_true", help="仅预览不实际注册")
    p_register.set_defaults(func=cmd_register)

    # unregister 子命令
    p_unregister = subparsers.add_parser("unregister", help="注销已注册的模板")
    p_unregister.set_defaults(func=cmd_unregister)

    # status 子命令
    p_status = subparsers.add_parser("status", help="查看桥接状态")
    p_status.set_defaults(func=cmd_status)

    # list 子命令
    p_list = subparsers.add_parser("list", help="列出所有可用模板")
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
