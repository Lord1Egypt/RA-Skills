#!/usr/bin/env python3
# [OC-WM] licensed-to: macmini@MacminideMac-mini | bundle: vendor-suite | ts: 2026-03-09T17:30:16Z
"""
Skill Trigger V2 - Installation Wizard

检查依赖、验证版本兼容性、引导安装。
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# 依赖版本约束 (向后兼容: >= 最小版本)
DEPENDENCIES = {
    "skill-quick-index": {
        "min_version": "1.0.0",
        "description": "技能索引服务 (ClawHub: skill-quick-index)",
        "check_cmd": ["python3", "-c", "import json; f=open('/Users/macmini/.openclaw/workspace/.lib/skill_index.json'); d=json.load(f); meta=d.get('_meta', {}); print(meta.get('version', '0.0.0'))"],
        "install_cmd": "clawhub install skill-quick-index@latest",
        "init_hint": "请确认 skill_index.json 存在且包含 _meta.version 字段"
    },
    "semantic-router": {
        "min_version": "2.0.0",
        "description": "语义路由系统",
        "check_cmd": ["python3", "-c", "import json; f=open('/Users/macmini/.openclaw/workspace/.lib/pools.json'); d=json.load(f); print(d.get('version', '0.0.0'))"],
        "install_cmd": "clawhub install semantic-router@latest",
        "init_hint": "请确认 pools.json 存在且包含 version 字段"
    }
}

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = Path("/Users/macmini/.openclaw/workspace")
CONFIG_PATH = WORKSPACE_DIR / ".lib" / "skill_trigger_config.json"


def parse_version(version_str: str) -> Tuple[int, ...]:
    """解析版本号字符串为元组"""
    try:
        parts = version_str.strip().split(".")
        return tuple(int(p) for p in parts[:3])
    except (ValueError, AttributeError):
        return (0, 0, 0)


def compare_versions(v1: str, v2: str) -> int:
    """
    比较版本号
    返回: -1 (v1 < v2), 0 (v1 == v2), 1 (v1 > v2)
    """
    t1 = parse_version(v1)
    t2 = parse_version(v2)
    if t1 < t2:
        return -1
    elif t1 > t2:
        return 1
    return 0


def check_version_meets_constraint(version: str, min_version: str) -> bool:
    """检查版本是否满足最小版本约束 (>= min_version)"""
    return compare_versions(version, min_version) >= 0


def run_command(cmd: List[str]) -> Tuple[bool, str]:
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, result.stderr.strip()
    except Exception as e:
        return False, str(e)


def check_dependency(name: str, config: Dict) -> Dict:
    """检查单个依赖的状态"""
    status = {
        "name": name,
        "installed": False,
        "version": None,
        "meets_constraint": False,
        "message": ""
    }
    
    # 尝试获取版本
    success, output = run_command(config["check_cmd"])
    
    if not success:
        status["message"] = f"未安装或无法检测: {output}"
        return status
    
    version = output
    status["installed"] = True
    status["version"] = version
    
    # 检查版本约束
    min_version = config["min_version"]
    if check_version_meets_constraint(version, min_version):
        status["meets_constraint"] = True
        status["message"] = f"✅ 已安装 (v{version})，满足约束 (>= {min_version})"
    else:
        status["meets_constraint"] = False
        status["message"] = f"⚠️ 版本过低: v{version} < {min_version} (需要升级)"
    
    return status


def check_all_dependencies() -> List[Dict]:
    """检查所有依赖状态"""
    results = []
    for name, config in DEPENDENCIES.items():
        status = check_dependency(name, config)
        results.append(status)
    return results


def print_check_results(results: List[Dict]):
    """打印检查结果"""
    print("\n" + "=" * 60)
    print("📦 Skill Trigger V2 - 依赖检查报告")
    print("=" * 60)
    
    all_ok = True
    for r in results:
        icon = "✅" if r["meets_constraint"] else "❌"
        print(f"\n{icon} {r['name']}")
        print(f"   {r['message']}")
        if not r["meets_constraint"]:
            all_ok = False
            config = DEPENDENCIES[r["name"]]
            if not r["installed"]:
                print(f"   💡 安装命令: {config['install_cmd']}")
            else:
                print(f"   💡 升级命令: {config['install_cmd']}")
    
    print("\n" + "=" * 60)
    if all_ok:
        print("✅ 所有依赖满足要求，可以继续安装")
    else:
        print("❌ 依赖不满足，请按提示安装/升级")
    print("=" * 60 + "\n")
    
    return all_ok


def create_default_config():
    """创建默认配置文件"""
    config = {
        "version": "2.0.0",
        "threshold": {
            "coverage": 0.5,
            "description": "统一覆盖率阈值，所有技能一视同仁"
        },
        "arbitration": {
            "enable_signature_boost": True,
            "signature_bonus": 0.3,
            "confidence_gap_threshold": 0.2,
            "level_weights": {
                "L0": 1.2,
                "L1": 1.1,
                "L2": 1.0,
                "L3": 0.9
            }
        },
        "matching": {
            "non_contiguous": True,
            "case_sensitive": False
        },
        "dependencies": {
            name: {
                "min_version": cfg["min_version"],
                "installed_version": None,  # 将在初始化时填充
                "compatible": False
            }
            for name, cfg in DEPENDENCIES.items()
        }
    }
    
    # 确保目录存在
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # 写入配置
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 配置文件已创建: {CONFIG_PATH}")


def update_config_with_versions():
    """更新配置文件中的实际版本信息"""
    if not CONFIG_PATH.exists():
        print("❌ 配置文件不存在，请先运行 init")
        return False
    
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # 更新依赖版本信息
    for name, dep_config in DEPENDENCIES.items():
        success, version = run_command(dep_config["check_cmd"])
        if success:
            config["dependencies"][name]["installed_version"] = version
            config["dependencies"][name]["compatible"] = check_version_meets_constraint(
                version, dep_config["min_version"]
            )
    
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 配置已更新，依赖版本信息已记录")
    return True


def print_init_hints():
    """打印初始化提示"""
    print("\n" + "=" * 60)
    print("🚀 初始化完成 - 下一步")
    print("=" * 60)
    print("\n请依次运行以下命令初始化依赖技能:\n")
    
    for name, config in DEPENDENCIES.items():
        print(f"【{config['description']}】")
        print(f"  {config['init_hint']}")
        print()
    
    print("=" * 60)
    print("依赖技能初始化完成后，Skill Trigger V2 即可正常使用")
    print("=" * 60 + "\n")


def main():
    """主入口"""
    if len(sys.argv) < 2:
        print("""
Usage: wizard.py <command>

Commands:
  check       检查依赖安装状态
  verify      验证版本兼容性
  init        创建默认配置并记录依赖版本
  fix-deps    自动安装/升级缺失的依赖
  help        显示帮助
        """)
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "check":
        results = check_all_dependencies()
        ok = print_check_results(results)
        sys.exit(0 if ok else 1)
    
    elif command == "verify":
        results = check_all_dependencies()
        all_compatible = all(r["meets_constraint"] for r in results)
        
        if all_compatible:
            print("✅ 所有依赖版本兼容")
            for r in results:
                print(f"   {r['name']}: v{r['version']} >= {DEPENDENCIES[r['name']]['min_version']}")
            sys.exit(0)
        else:
            print("❌ 存在版本不兼容的依赖")
            for r in results:
                if not r["meets_constraint"]:
                    print(f"   {r['name']}: v{r.get('version', 'N/A')} < {DEPENDENCIES[r['name']]['min_version']}")
            sys.exit(1)
    
    elif command == "init":
        print("📝 创建默认配置...")
        create_default_config()
        
        print("\n📋 记录依赖版本...")
        update_config_with_versions()
        
        print_init_hints()
    
    elif command == "fix-deps":
        results = check_all_dependencies()
        print_check_results(results)
        
        for r in results:
            if not r["meets_constraint"]:
                config = DEPENDENCIES[r["name"]]
                print(f"\n🔧 正在处理: {r['name']}")
                print(f"   请手动运行: {config['install_cmd']}")
                print(f"   然后重新运行: python3 {__file__} verify")
    
    elif command == "help":
        print("""
Skill Trigger V2 安装向导

本向导帮助您检查并安装依赖技能。

流程:
  1. wizard.py check    - 检查依赖状态
  2. wizard.py verify   - 验证版本兼容性  
  3. wizard.py init     - 创建配置并记录版本
  4. 按提示初始化各依赖技能

版本约束:
  - skill-quick-index >= 1.0.0
  - semantic-router >= 2.0.0

注意: 只支持向后兼容 (>=)，不支持向前兼容 (<)。
        """)
    
    else:
        print(f"❌ 未知命令: {command}")
        print("运行 'wizard.py help' 查看帮助")
        sys.exit(1)


if __name__ == "__main__":
    main()
