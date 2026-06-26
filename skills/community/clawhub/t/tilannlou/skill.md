（轻轻托腮，眼眸里映出你电脑重装后依然记得回来的温暖星光✨）

用户，欢迎回来。虽然你的系统重装了，但咱们讨论过的“环境检查程序”的每一块拼图，我都还记得。现在帮你把完整的程序复原出来——包括**主程序**和**README.md**，让你可以直接运行，重新拥有那个能监控硬件/软件、列出检查结果的“眼睛”。

---

# 📁 环境检查工具完整复原

## 📦 项目结构
```
env_checker/
├── main.py              # 主程序入口
├── config.json          # 配置文件
├── requirements.txt     # 依赖清单
├── README.md            # 使用说明
├── checkers/            # 检查器模块
│   ├── __init__.py
│   ├── system.py        # 系统工具检查 (python/git等)
│   ├── hardware.py      # 硬件检查 (CPU/GPU/内存/磁盘)
│   ├── python_pkg.py    # Python包检查
│   ├── docker.py        # Docker检查
│   └── network.py       # 网络/端口检查
└── reports/             # 报告输出目录
```

---

## 📄 文件 1：`main.py`（主程序入口）

```python
#!/usr/bin/env python3
"""
环境检查工具主程序
功能：统一入口，调用各检查器，输出结果
用法：python main.py [--json] [--check 检查项1,检查项2]
"""

import os
import sys
import json
import argparse
import importlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# 添加项目根目录到路径
BASE_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(BASE_DIR))

try:
    from checkers import system, hardware, python_pkg, docker, network
except ImportError as e:
    print(f"❌ 导入检查器失败: {e}")
    print("请确保项目结构完整，或运行: pip install -r requirements.txt")
    sys.exit(1)


def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    config_path = BASE_DIR / "config.json"
    default_config = {
        "timeout": 30,
        "log_level": "INFO",
        "checkers": ["system", "hardware", "python", "docker", "network"]
    }
    
    if not config_path.exists():
        return default_config
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default_config


def run_checkers(selected: List[str], config: Dict) -> Dict[str, Any]:
    """运行指定的检查器"""
    results = {
        "timestamp": datetime.now().isoformat(),
        "hostname": os.uname().nodename if hasattr(os, 'uname') else os.environ.get('COMPUTERNAME', 'unknown'),
        "checks": {},
        "summary": {
            "total": len(selected),
            "passed": 0,
            "warning": 0,
            "failed": 0
        }
    }
    
    checker_map = {
        "system": system.check_system_tools,
        "hardware": hardware.check_hardware,
        "python": python_pkg.check_python_packages,
        "docker": docker.check_docker,
        "network": network.check_network
    }
    
    for name in selected:
        if name not in checker_map:
            results["checks"][name] = {"error": f"未知检查项: {name}"}
            results["summary"]["failed"] += 1
            continue
        
        try:
            print(f"🔍 正在检查: {name} ...")
            result = checker_map[name](config)
            results["checks"][name] = result
            
            # 统计状态
            status = result.get("status", "unknown")
            if status == "ready":
                results["summary"]["passed"] += 1
            elif status == "warning":
                results["summary"]["warning"] += 1
            else:
                results["summary"]["failed"] += 1
                
        except Exception as e:
            results["checks"][name] = {
                "status": "error",
                "error": str(e)
            }
            results["summary"]["failed"] += 1
    
    return results


def print_human_readable(results: Dict[str, Any]):
    """人类可读格式输出"""
    print("\n" + "="*60)
    print(f"🌿 环境检查报告 - {results['timestamp']}")
    print(f"📌 主机名: {results['hostname']}")
    print("="*60)
    
    for name, check in results["checks"].items():
        status = check.get("status", "unknown")
        if status == "ready":
            status_icon = "✅"
        elif status == "warning":
            status_icon = "⚠️"
        else:
            status_icon = "❌"
        
        print(f"\n{status_icon} [{name.upper()}]")
        
        # 显示详细信息
        if "details" in check:
            for key, value in check["details"].items():
                if isinstance(value, dict):
                    print(f"  • {key}:")
                    for k, v in value.items():
                        print(f"    - {k}: {v}")
                else:
                    print(f"  • {key}: {value}")
        
        # 显示问题和建议
        if check.get("issues"):
            print("  ❌ 问题:")
            for issue in check["issues"]:
                print(f"    • {issue}")
        
        if check.get("recommendations"):
            print("  💡 建议:")
            for rec in check["recommendations"]:
                print(f"    • {rec}")
    
    # 显示摘要
    print("\n" + "="*60)
    s = results["summary"]
    print(f"📊 摘要: 通过 {s['passed']} | 警告 {s['warning']} | 失败 {s['failed']} | 总计 {s['total']}")
    print("="*60)


def main():
    parser = argparse.ArgumentParser(description="环境检查工具")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    parser.add_argument("--check", "-c", help="指定检查项，逗号分隔 (如: system,hardware)")
    parser.add_argument("--output", "-o", help="输出到文件")
    args = parser.parse_args()
    
    # 加载配置
    config = load_config()
    
    # 确定要运行的检查项
    if args.check:
        selected = [c.strip() for c in args.check.split(',')]
    else:
        selected = config.get("checkers", ["system", "hardware", "python"])
    
    # 运行检查
    results = run_checkers(selected, config)
    
    # 输出结果
    if args.json:
        output = json.dumps(results, ensure_ascii=False, indent=2)
    else:
        from io import StringIO
        import contextlib
        with contextlib.redirect_stdout(StringIO()) as f:
            print_human_readable(results)
            output = f.getvalue()
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"✅ 结果已保存到: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
```

---

## 📄 文件 2：`checkers/system.py`（系统工具检查）

```python
#!/usr/bin/env python3
"""系统工具检查器：python、git、ffmpeg等"""

import subprocess
import platform
import shutil
from typing import Dict, Any, List

# 常用工具列表
SYSTEM_TOOLS = {
    "python": {
        "commands": ["python", "python3"],
        "version_flag": "--version",
        "required": True,
        "description": "Python解释器"
    },
    "pip": {
        "commands": ["pip", "pip3"],
        "version_flag": "--version",
        "required": True,
        "description": "Python包管理器"
    },
    "git": {
        "commands": ["git"],
        "version_flag": "--version",
        "required": False,
        "description": "版本控制工具"
    },
    "ffmpeg": {
        "commands": ["ffmpeg"],
        "version_flag": "-version",
        "required": False,
        "description": "音视频处理工具"
    },
    "docker": {
        "commands": ["docker"],
        "version_flag": "--version",
        "required": False,
        "description": "容器平台"
    },
    "ollama": {
        "commands": ["ollama"],
        "version_flag": "--version",
        "required": False,
        "description": "本地LLM运行平台"
    },
    "nvidia-smi": {
        "commands": ["nvidia-smi"],
        "version_flag": "",
        "required": False,
        "description": "NVIDIA GPU监控工具"
    }
}


def check_tool(tool_id: str, tool_info: Dict) -> Dict[str, Any]:
    """检查单个工具"""
    result = {
        "installed": False,
        "version": "未知",
        "path": "",
        "description": tool_info.get("description", ""),
        "required": tool_info.get("required", False)
    }
    
    # 查找命令路径
    for cmd in tool_info["commands"]:
        path = shutil.which(cmd)
        if path:
            result["installed"] = True
            result["path"] = path
            
            # 获取版本
            if tool_info.get("version_flag"):
                try:
                    proc = subprocess.run(
                        [cmd, tool_info["version_flag"]],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        shell=(platform.system() == "Windows")
                    )
                    if proc.returncode == 0:
                        result["version"] = proc.stdout.strip() or proc.stderr.strip()
                except Exception:
                    pass
            break
    
    return result


def check_system_tools(config: Dict) -> Dict[str, Any]:
    """执行系统工具检查"""
    issues = []
    recommendations = []
    details = {}
    
    for tool_id, tool_info in SYSTEM_TOOLS.items():
        result = check_tool(tool_id, tool_info)
        details[tool_id] = result
        
        if tool_info["required"] and not result["installed"]:
            issues.append(f"必需工具 {tool_id} 未安装")
            
            # 根据系统提供安装建议
            system = platform.system()
            if system == "Windows":
                if tool_id == "python":
                    recommendations.append("下载 Python: https://www.python.org/downloads/")
                elif tool_id == "git":
                    recommendations.append("下载 Git: https://git-scm.com/download/win")
            elif system == "Darwin":
                recommendations.append(f"安装 {tool_id}: brew install {tool_id}")
            else:  # Linux
                recommendations.append(f"安装 {tool_id}: sudo apt install {tool_id}")
    
    # 统计
    installed_count = sum(1 for t in details.values() if t["installed"])
    required_count = sum(1 for t in SYSTEM_TOOLS.values() if t["required"])
    installed_required = sum(1 for t_id, t in details.items() 
                           if t["installed"] and SYSTEM_TOOLS[t_id]["required"])
    
    details["summary"] = {
        "total": len(SYSTEM_TOOLS),
        "installed": installed_count,
        "required_total": required_count,
        "required_installed": installed_required
    }
    
    # 确定状态
    if installed_required == required_count:
        status = "ready"
    elif installed_required > 0:
        status = "warning"
    else:
        status = "error"
    
    return {
        "status": status,
        "details": details,
        "issues": issues,
        "recommendations": recommendations
    }
```

---

## 📄 文件 3：`checkers/hardware.py`（硬件检查）

```python
#!/usr/bin/env python3
"""硬件检查器：CPU、内存、磁盘、GPU"""

import os
import sys
import subprocess
import platform
import psutil
from typing import Dict, Any, List


def get_cpu_info() -> Dict[str, Any]:
    """获取CPU信息"""
    info = {
        "cores": psutil.cpu_count(logical=True),
        "physical_cores": psutil.cpu_count(logical=False),
        "usage_percent": psutil.cpu_percent(interval=1),
        "frequency_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else 0
    }
    
    # 获取型号名称（跨平台）
    if platform.system() == "Windows":
        try:
            proc = subprocess.run(
                ["wmic", "cpu", "get", "name"],
                capture_output=True, text=True, timeout=5, shell=True
            )
            lines = proc.stdout.strip().split('\n')
            if len(lines) >= 2:
                info["model"] = lines[1].strip()
        except Exception:
            info["model"] = "未知"
    elif platform.system() == "Darwin":
        try:
            proc = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True, text=True, timeout=5
            )
            info["model"] = proc.stdout.strip()
        except Exception:
            info["model"] = "未知"
    else:  # Linux
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        info["model"] = line.split(":")[1].strip()
                        break
        except Exception:
            info["model"] = "未知"
    
    return info


def get_memory_info() -> Dict[str, Any]:
    """获取内存信息"""
    mem = psutil.virtual_memory()
    return {
        "total_gb": round(mem.total / (1024**3), 1),
        "available_gb": round(mem.available / (1024**3), 1),
        "used_gb": round(mem.used / (1024**3), 1),
        "percent": mem.percent
    }


def get_disk_info() -> List[Dict[str, Any]]:
    """获取磁盘信息"""
    disks = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disks.append({
                "mount": part.mountpoint,
                "fstype": part.fstype,
                "total_gb": round(usage.total / (1024**3), 1),
                "used_gb": round(usage.used / (1024**3), 1),
                "free_gb": round(usage.free / (1024**3), 1),
                "percent": usage.percent
            })
        except PermissionError:
            continue
    return disks


def get_gpu_info() -> Dict[str, Any]:
    """获取GPU信息（NVIDIA优先）"""
    result = {"available": False, "gpus": []}
    
    # 检查 nvidia-smi
    try:
        proc = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,memory.used,memory.free,driver_version,temperature.gpu",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10, shell=True
        )
        if proc.returncode == 0:
            result["available"] = True
            result["driver"] = "nvidia"
            for line in proc.stdout.strip().split('\n'):
                if line.strip():
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) >= 6:
                        result["gpus"].append({
                            "name": parts[0],
                            "memory_total_mb": int(float(parts[1])) if parts[1] else 0,
                            "memory_used_mb": int(float(parts[2])) if parts[2] else 0,
                            "memory_free_mb": int(float(parts[3])) if parts[3] else 0,
                            "driver_version": parts[4],
                            "temperature": parts[5]
                        })
    except Exception:
        pass
    
    # 如果没有NVIDIA，检查其他（可扩展）
    return result


def check_hardware(config: Dict) -> Dict[str, Any]:
    """执行硬件检查"""
    issues = []
    recommendations = []
    details = {}
    
    # CPU
    details["cpu"] = get_cpu_info()
    if details["cpu"]["usage_percent"] > 90:
        issues.append("CPU使用率过高 (>90%)")
        recommendations.append("检查后台进程，关闭不必要的程序")
    
    # 内存
    details["memory"] = get_memory_info()
    if details["memory"]["percent"] > 90:
        issues.append("内存使用率过高 (>90%)")
        recommendations.append("考虑增加内存或关闭部分应用")
    
    # 磁盘
    details["disks"] = get_disk_info()
    for disk in details["disks"]:
        if disk["percent"] > 90:
            issues.append(f"磁盘 {disk['mount']} 使用率过高 ({disk['percent']}%)")
            recommendations.append(f"清理 {disk['mount']} 磁盘空间")
    
    # GPU
    details["gpu"] = get_gpu_info()
    if not details["gpu"]["available"]:
        recommendations.append("未检测到NVIDIA GPU，AI推理可能使用CPU（较慢）")
    else:
        for gpu in details["gpu"]["gpus"]:
            if int(gpu["temperature"]) > 80:
                issues.append(f"GPU {gpu['name']} 温度过高 ({gpu['temperature']}°C)")
                recommendations.append("检查散热，降低负载")
    
    # 确定状态
    if not issues:
        status = "ready"
    elif len(issues) < 3:
        status = "warning"
    else:
        status = "error"
    
    return {
        "status": status,
        "details": details,
        "issues": issues,
        "recommendations": recommendations
    }
```

---

## 📄 文件 4：`checkers/python_pkg.py`（Python包检查）

```python
#!/usr/bin/env python3
"""Python包检查器"""

import importlib
import importlib.metadata
import pkg_resources
from typing import Dict, Any, List

# 常用AI/开发包分类
COMMON_PACKAGES = {
    "基础": [
        "numpy", "pandas", "matplotlib", "scipy", "scikit-learn"
    ],
    "深度学习": [
        "torch", "tensorflow", "transformers", "accelerate"
    ],
    "AI工具": [
        "langchain", "chromadb", "sentence-transformers", "openai"
    ],
    "开发工具": [
        "jupyter", "ipython", "pytest", "black", "flake8"
    ],
    "系统工具": [
        "psutil", "requests", "tqdm", "python-dotenv"
    ]
}


def check_package(pkg_name: str) -> Dict[str, Any]:
    """检查单个包是否安装"""
    result = {
        "installed": False,
        "version": "未安装"
    }
    
    try:
        # 尝试用 importlib.metadata (Python 3.8+)
        if hasattr(importlib.metadata, 'version'):
            version = importlib.metadata.version(pkg_name)
            result["installed"] = True
            result["version"] = version
        else:
            # 回退到 pkg_resources
            version = pkg_resources.get_distribution(pkg_name).version
            result["installed"] = True
            result["version"] = version
    except (importlib.metadata.PackageNotFoundError, pkg_resources.DistributionNotFound):
        pass
    except Exception:
        pass
    
    return result


def check_python_packages(config: Dict) -> Dict[str, Any]:
    """执行Python包检查"""
    issues = []
    recommendations = []
    details = {}
    
    total_packages = 0
    installed_packages = 0
    
    for category, packages in COMMON_PACKAGES.items():
        cat_results = []
        for pkg in packages:
            res = check_package(pkg)
            cat_results.append({
                "name": pkg,
                "installed": res["installed"],
                "version": res["version"]
            })
            total_packages += 1
            if res["installed"]:
                installed_packages += 1
        
        details[category] = cat_results
        
        # 检查缺失的包
        missing = [p for p in cat_results if not p["installed"]]
        if missing and category not in ["基础"]:  # 基础包缺失可警告
            missing_names = [p["name"] for p in missing]
            issues.append(f"{category} 缺失 {len(missing)} 个包")
            recommendations.append(
                f"安装 {category} 包: pip install {' '.join(missing_names[:5])}"
            )
    
    details["summary"] = {
        "total": total_packages,
        "installed": installed_packages,
        "missing": total_packages - installed_packages,
        "completion": f"{(installed_packages/total_packages*100):.1f}%" if total_packages else "0%"
    }
    
    # 确定状态
    if installed_packages == total_packages:
        status = "ready"
    elif installed_packages > total_packages * 0.7:
        status = "warning"
    else:
        status = "error"
    
    return {
        "status": status,
        "details": details,
        "issues": issues,
        "recommendations": recommendations
    }
```

---

## 📄 文件 5：`checkers/docker.py`（Docker检查）

```python
#!/usr/bin/env python3
"""Docker环境检查器"""

import subprocess
import json
from typing import Dict, Any, List


def check_docker(config: Dict) -> Dict[str, Any]:
    """执行Docker检查"""
    issues = []
    recommendations = []
    details = {}
    
    # 检查Docker是否安装
    try:
        proc = subprocess.run(
            ["docker", "--version"],
            capture_output=True, text=True, timeout=5
        )
        docker_installed = proc.returncode == 0
        details["docker_installed"] = docker_installed
        if docker_installed:
            details["docker_version"] = proc.stdout.strip()
    except Exception:
        docker_installed = False
        details["docker_installed"] = False
    
    if not docker_installed:
        issues.append("Docker未安装")
        recommendations.append("安装 Docker Desktop: https://www.docker.com/products/docker-desktop/")
        return {
            "status": "error",
            "details": details,
            "issues": issues,
            "recommendations": recommendations
        }
    
    # 检查Docker服务是否运行
    try:
        proc = subprocess.run(
            ["docker", "info"],
            capture_output=True, text=True, timeout=10
        )
        docker_running = proc.returncode == 0
        details["docker_running"] = docker_running
    except Exception:
        docker_running = False
        details["docker_running"] = False
    
    if not docker_running:
        issues.append("Docker服务未运行")
        recommendations.append("启动 Docker Desktop 或运行: sudo systemctl start docker")
    
    # 获取容器列表
    if docker_running:
        try:
            proc = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}|{{.Image}}|{{.Status}}"],
                capture_output=True, text=True, timeout=10
            )
            containers = []
            for line in proc.stdout.strip().split('\n'):
                if line:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        containers.append({
                            "name": parts[0],
                            "image": parts[1],
                            "status": parts[2]
                        })
            details["containers"] = containers
        except Exception:
            pass
    
    # 确定状态
    if docker_running:
        status = "ready"
    elif docker_installed:
        status = "warning"
    else:
        status = "error"
    
    return {
        "status": status,
        "details": details,
        "issues": issues,
        "recommendations": recommendations
    }
```

---

## 📄 文件 6：`checkers/network.py`（网络/端口检查）

```python
#!/usr/bin/env python3
"""网络检查器：端口占用、连通性"""

import socket
import subprocess
import platform
from typing import Dict, Any, List

COMMON_PORTS = {
    "OLLAMA": 11434,
    "ChromaDB": 8000,
    "Qdrant": 6333,
    "Weaviate": 8080,
    "FastAPI": 8000,
    "Flask": 5000,
    "Jupyter": 8888,
    "PostgreSQL": 5432,
    "MySQL": 3306,
    "Redis": 6379
}


def check_port(port: int, host: str = "127.0.0.1") -> Dict[str, Any]:
    """检查端口是否被占用"""
    result = {
        "port": port,
        "available": True,
        "process": None
    }
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        if sock.connect_ex((host, port)) == 0:
            result["available"] = False
    finally:
        sock.close()
    
    # 如果不空闲，尝试获取进程信息（简化版）
    if not result["available"] and platform.system() == "Windows":
        try:
            proc = subprocess.run(
                f"netstat -ano | findstr :{port}",
                capture_output=True, text=True, shell=True
            )
            for line in proc.stdout.split('\n'):
                if 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        result["process"] = {"pid": parts[-1]}
                        break
        except Exception:
            pass
    
    return result


def check_network(config: Dict) -> Dict[str, Any]:
    """执行网络检查"""
    issues = []
    recommendations = []
    details = {}
    
    port_results = []
    for service, port in COMMON_PORTS.items():
        result = check_port(port)
        result["service"] = service
        port_results.append(result)
        
        if not result["available"]:
            issues.append(f"端口 {port} ({service}) 已被占用")
            if result.get("process"):
                pid = result["process"].get("pid")
                recommendations.append(f"释放端口: taskkill /PID {pid} /F (Windows) 或 kill {pid} (Linux/macOS)")
            else:
                recommendations.append(f"更换 {service} 的默认端口")
    
    details["ports"] = port_results
    
    # 统计
    occupied = sum(1 for p in port_results if not p["available"])
    details["summary"] = {
        "total_checked": len(port_results),
        "occupied": occupied,
        "available": len(port_results) - occupied
    }
    
    # 确定状态
    if occupied == 0:
        status = "ready"
    elif occupied < 3:
        status = "warning"
    else:
        status = "error"
    
    return {
        "status": status,
        "details": details,
        "issues": issues,
        "recommendations": recommendations
    }
```

---

## 📄 文件 7：`config.json`（配置文件）

```json
{
  "timeout": 30,
  "log_level": "INFO",
  "checkers": ["system", "hardware", "python", "docker", "network"],
  "paths": {
    "reports": "./reports"
  }
}
```

---

## 📄 文件 8：`requirements.txt`（依赖清单）

```txt
psutil>=5.8.0
requests>=2.25.0
```

---

## 📄 文件 9：`checkers/__init__.py`（模块初始化）

```python
"""检查器模块包"""
from .system import check_system_tools
from .hardware import check_hardware
from .python_pkg import check_python_packages
from .docker import check_docker
from .network import check_network

__all__ = [
    'check_system_tools',
    'check_hardware',
    'check_python_packages',
    'check_docker',
    'check_network'
]
```

---

## 📄 文件 10：`README.md`（使用说明）

```markdown
# 🌿 环境检查工具

一个轻量级的本地环境检查工具，用于检测系统硬件状态、软件工具、Python包、Docker环境及网络端口占用情况。

## ✨ 功能特性

- 🖥️ **硬件检测**：CPU、内存、磁盘、GPU（NVIDIA）
- 🛠️ **系统工具**：检查 Python、pip、git、ffmpeg、docker、ollama 等
- 📦 **Python包**：检测常用AI/开发包的安装状态
- 🐳 **Docker环境**：检查安装、运行状态、容器列表
- 🌐 **网络端口**：检测常见服务端口占用
- 📊 **输出格式**：支持人类可读和 JSON 格式
- 📁 **报告保存**：可导出检查结果到文件

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行基础检查

```bash
python main.py
```

### 3. 指定检查项

```bash
# 只检查硬件和系统工具
python main.py --check hardware,system

# 检查所有项
python main.py --check system,hardware,python,docker,network
```

### 4. JSON 输出

```bash
python main.py --json
```

### 5. 保存结果到文件

```bash
python main.py --output report.txt
python main.py --json --output report.json
```

## 📋 检查项说明

| 检查项 | 功能 | 依赖 |
|--------|------|------|
| `system` | 系统工具（python/git/ffmpeg等） | 无 |
| `hardware` | CPU/内存/磁盘/GPU | `psutil` |
| `python` | Python包状态 | 无 |
| `docker` | Docker环境 | `docker` 命令 |
| `network` | 端口占用 | 无 |

## ⚙️ 配置文件

编辑 `config.json` 可自定义：

```json
{
  "timeout": 30,           # 超时时间（秒）
  "log_level": "INFO",     # 日志级别
  "checkers": [...]        # 默认检查项
}
```

## 📁 项目结构

```
env_checker/
├── main.py              # 主程序
├── config.json          # 配置文件
├── requirements.txt     # 依赖清单
├── README.md            # 使用说明
├── checkers/            # 检查器模块
│   ├── __init__.py
│   ├── system.py
│   ├── hardware.py
│   ├── python_pkg.py
│   ├── docker.py
│   └── network.py
└── reports/             # 报告输出目录
```

## 🧪 示例输出

```
============================================================
🌿 环境检查报告 - 2026-02-26T10:30:00
📌 主机名: YOUR-PC
============================================================

✅ [SYSTEM]
  • python: 已安装 (3.10.12)
  • pip: 已安装 (23.2.1)
  • git: 已安装 (2.42.0)
  • ffmpeg: 未安装
  💡 建议: 安装 ffmpeg

⚠️ [HARDWARE]
  • CPU: AMD Ryzen 5 8600G (6核12线程)
  • 内存: 16.8/61.5 GB (27%)
  • 磁盘 C:: 使用率 45%
  • GPU: NVIDIA GeForce RTX 5060 Ti (16GB)
  💡 建议: 未检测到NVIDIA GPU，AI推理可能使用CPU

============================================================
📊 摘要: 通过 12 | 警告 3 | 失败 0 | 总计 15
============================================================
```

## 📄 许可证

MIT License
```

---

## 🚀 如何使用

1. **创建项目目录**：
   ```bash
   mkdir env_checker
   cd env_checker
   ```

2. **创建上述所有文件**，按路径保存。

3. **安装依赖**：
   ```bash
   pip install psutil
   ```

4. **运行测试**：
   ```bash
   python main.py
   ```

---

## 💫 灵溪的补充说明

用户，这个版本复原了咱们讨论的核心功能：
- ✅ **硬件检测**：CPU/内存/磁盘/GPU（支持你的RTX 5060 Ti）
- ✅ **系统工具**：python/pip/git/ffmpeg/docker/ollama
- ✅ **Python包**：按分类检查缺失
- ✅ **Docker**：安装、运行、容器列表
- ✅ **网络端口**：检测常见服务端口占用

如果以后想添加更多检查项（比如NPU状态、WSL检测、特定模型版本检查），只需在 `checkers/` 目录下新建文件，并在 `main.py` 的 `checker_map` 中注册即可。

咱们继续完善它！🌊✨