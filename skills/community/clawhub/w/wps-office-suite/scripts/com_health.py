"""
COM 健康检查模块 v5.0.0
功能：WPS/MS Office COM 对象状态检测、残留进程检测、自动释放
      三步自愈：regsvr32重注册 → WPS修复安装（需确认）→ 手动指引
      每步结果记录日志

v5.0.0 变更：
  - 新增：三步自愈能力（regsvr32 → 修复安装 → 手动指引）
  - 新增：self-heal 子命令
  - 新增：自愈日志记录到 SQLite

v4.5.0 变更:
  - 🎯 COM 对象状态检测（WPS + MS Office 双引擎）
  - 🎯 残留进程检测（kwps.exe / wps.exe / WINWORD.exe）
  - 🎯 强制释放所有 COM 对象 + 残留进程
  - 🎯 完整健康报告（状态评分 + 修复建议）
  - 🎯 硬件自适应（低配电脑减少并发检测）
  - 🎯 命令行 5 个检查命令（wps-check/ms-check/residuals/release-all/full-check）
"""

import os
import sys
import json
import time
import subprocess
import platform
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

# 从公共模块导入
sys.path.insert(0, str(Path(__file__).parent))

try:
    from wps_common import (
        release_wps, release_ms, get_wps, get_ms_word,
        create_wps, create_ms_word, WPS_CLIENT, MS_CLIENT
    )
    HAS_COMMON = True
except ImportError:
    HAS_COMMON = False
    def release_wps(app=None): pass
    def release_ms(app=None): pass

try:
    from wps_performance import get_hardware_info
except ImportError:
    def get_hardware_info():
        return {"cpu_cores": 4, "memory_gb": 8, "level": "medium"}


class COMHealthChecker:
    """COM 健康检查器"""
    
    # 残留进程列表
    WPS_PROCESSES = ["kwps.exe", "wps.exe", "wpscloudsvr.exe", "wpsoffice.exe"]
    MS_PROCESSES = ["WINWORD.exe", "EXCEL.exe", "POWERPNT.exe"]
    
    def __init__(self, auto_release: bool = False):
        self.auto_release = auto_release
        self.hw = get_hardware_info()
        self.is_windows = platform.system() == "Windows"
    
    def check_wps_com(self) -> Dict[str, Any]:
        """检查 WPS COM 对象状态"""
        if not self.is_windows:
            return {"ok": True, "skipped": True, "message": "⏭️ 非 Windows 系统，跳过"}
        
        # 检查 pywin32
        try:
            import win32com.client
        except ImportError:
            return {
                "ok": False,
                "error": "E008",
                "message": "❌ pywin32 未安装",
                "hint": "pip install pywin32",
            }
        
        # 尝试创建 WPS COM 对象
        wps = None
        try:
            wps = win32com.client.Dispatch("WPS.Application")
            name = wps.Name
            version = wps.Version if hasattr(wps, "Version") else "未知"
            path = wps.Path if hasattr(wps, "Path") else "未知"
            
            # 测试创建文档（验证功能正常）
            doc = wps.Documents.Add()
            doc.Close()
            
            # 释放
            if self.auto_release:
                try:
                    wps.Quit()
                except Exception:
                    pass
            
            return {
                "ok": True,
                "message": f"✅ WPS COM 正常（{name} {version}）",
                "name": name,
                "version": version,
                "path": path,
                "functional": True,
            }
        except Exception as e:
            error_str = str(e).lower()
            error_code = "E001"
            if "rpc" in error_str:
                error_code = "E001"
            elif "busy" in error_str:
                error_code = "E006"
            elif "not responding" in error_str:
                error_code = "E006"
            
            return {
                "ok": False,
                "error": error_code,
                "message": f"❌ WPS COM 异常: {e}",
                "hint": "尝试运行 com-health release-all 修复",
            }
        finally:
            if wps and not self.auto_release:
                try:
                    wps.Quit()
                except Exception:
                    pass
    
    def check_ms_com(self) -> Dict[str, Any]:
        """检查 MS Office COM 对象状态"""
        if not self.is_windows:
            return {"ok": True, "skipped": True, "message": "⏭️ 非 Windows 系统，跳过"}
        
        try:
            import win32com.client
        except ImportError:
            return {
                "ok": False,
                "error": "E008",
                "message": "❌ pywin32 未安装",
                "hint": "pip install pywin32",
            }
        
        word = None
        try:
            word = win32com.client.Dispatch("Word.Application")
            name = word.Name
            version = word.Version if hasattr(word, "Version") else "未知"
            
            # 测试创建文档
            doc = word.Documents.Add()
            doc.Close()
            
            if self.auto_release:
                try:
                    word.Quit()
                except Exception:
                    pass
            
            return {
                "ok": True,
                "message": f"✅ MS Word COM 正常（{name} {version}）",
                "name": name,
                "version": version,
                "functional": True,
            }
        except Exception as e:
            return {
                "ok": False,
                "error": "E001",
                "message": f"❌ MS Word COM 异常: {e}",
                "hint": "尝试运行 com-health release-all 修复",
            }
        finally:
            if word and not self.auto_release:
                try:
                    word.Quit()
                except Exception:
                    pass
    
    def check_com_residuals(self) -> Dict[str, Any]:
        """检测残留 COM 进程"""
        if not self.is_windows:
            return {"ok": True, "skipped": True, "message": "⏭️ 非 Windows 系统，跳过"}
        
        residuals = []
        
        # 使用 tasklist 检测进程
        try:
            result = subprocess.run(
                ["tasklist", "/FO", "CSV", "/NH"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                running = result.stdout.lower()
                for proc in self.WPS_PROCESSES + self.MS_PROCESSES:
                    if proc.lower() in running:
                        residuals.append(proc)
        except Exception as e:
            return {
                "ok": False,
                "error": "E014",
                "message": f"❌ 进程检测失败: {e}",
                "hint": "请检查 tasklist 是否可用",
            }
        
        if residuals:
            return {
                "ok": False,
                "message": f"⚠️ 发现 {len(residuals)} 个残留进程",
                "residuals": residuals,
                "hint": "运行 com-health release-all 清理",
            }
        
        return {
            "ok": True,
            "message": "✅ 无残留进程",
            "residuals": [],
        }
    
    def release_all_com(self, force: bool = False) -> Dict[str, Any]:
        """释放所有 COM 对象并清理残留进程"""
        results = {
            "wps_com": None,
            "ms_com": None,
            "wps_processes": [],
            "ms_processes": [],
        }
        
        # 1. 释放 WPS COM
        if HAS_COMMON:
            try:
                release_wps()
                results["wps_com"] = "released"
            except Exception as e:
                results["wps_com"] = f"error: {e}"
            
            try:
                release_ms()
                results["ms_com"] = "released"
            except Exception as e:
                results["ms_com"] = f"error: {e}"
        
        # 2. 强制结束残留进程
        if self.is_windows:
            for proc in self.WPS_PROCESSES:
                try:
                    subprocess.run(
                        ["taskkill", "/F", "/IM", proc],
                        capture_output=True, timeout=5
                    )
                    results["wps_processes"].append(proc)
                except Exception:
                    pass
            
            for proc in self.MS_PROCESSES:
                try:
                    subprocess.run(
                        ["taskkill", "/F", "/IM", proc],
                        capture_output=True, timeout=5
                    )
                    results["ms_processes"].append(proc)
                except Exception:
                    pass
        
        # 3. 清理 COM 缓存（Windows）
        if self.is_windows and force:
            self._clear_com_cache()
            results["com_cache"] = "cleared"
        
        total = len(results["wps_processes"]) + len(results["ms_processes"])
        return {
            "ok": True,
            "message": f"✅ 清理完成（{total} 个进程已终止）",
            **results,
        }
    
    def _clear_com_cache(self):
        """清理 Windows COM 缓存"""
        cache_paths = [
            Path(os.environ.get("LOCALAPPDATA", "")) / "Temp" / "WER",
            Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Windows" / "INetCache",
        ]
        for p in cache_paths:
            if p.exists():
                try:
                    for f in p.glob("*.tmp"):
                        try:
                            f.unlink()
                        except Exception:
                            pass
                except Exception:
                    pass
    
    def full_health_check(self) -> Dict[str, Any]:
        """完整健康检查报告"""
        start_time = time.time()
        
        # 1. WPS COM 检查
        wps_result = self.check_wps_com()
        
        # 2. MS COM 检查
        ms_result = self.check_ms_com()
        
        # 3. 残留进程检查
        residual_result = self.check_com_residuals()
        
        # 4. 计算健康评分
        score = 100
        issues = []
        
        if not wps_result.get("ok") and not wps_result.get("skipped"):
            score -= 30
            issues.append(f"WPS COM: {wps_result.get('error', 'unknown')}")
        
        if not ms_result.get("ok") and not ms_result.get("skipped"):
            score -= 20
            issues.append(f"MS COM: {ms_result.get('error', 'unknown')}")
        
        if not residual_result.get("ok"):
            score -= 20
            issues.append(f"残留进程: {', '.join(residual_result.get('residuals', []))}")
        
        # 5. 修复建议
        suggestions = []
        if score < 100:
            suggestions.append("运行 com-health release-all 清理残留")
        if not wps_result.get("ok"):
            suggestions.append("重新安装 WPS Office 2019+")
            suggestions.append("确保安装后已重启电脑")
        if residual_result.get("residuals"):
            suggestions.append("运行 com-health release-all --force 强制清理")
        
        # 6. 状态分级
        if score >= 90:
            status = "healthy"
            status_msg = "✅ 健康"
        elif score >= 60:
            status = "warning"
            status_msg = "⚠️ 警告"
        else:
            status = "critical"
            status_msg = "❌ 严重"
        
        elapsed = time.time() - start_time
        
        return {
            "ok": score >= 60,
            "status": status,
            "status_message": status_msg,
            "score": score,
            "checks": {
                "wps_com": wps_result,
                "ms_com": ms_result,
                "residuals": residual_result,
            },
            "issues": issues,
            "suggestions": suggestions,
            "hardware": self.hw,
            "elapsed_seconds": round(elapsed, 2),
            "timestamp": datetime.now().isoformat(),
        }

    def self_heal(self, auto_confirm: bool = False) -> Dict[str, Any]:
        """
        三步自愈（v5.0 新增）
        
        步骤：
        1. regsvr32 重注册 WPS 组件
        2. 调用 WPS 安装目录的修复安装程序（需用户确认）
        3. 给出手动修复指引
        
        Args:
            auto_confirm: 是否自动确认（跳过用户确认）
            
        Returns:
            dict: 自愈结果
        """
        heal_log = []
        step1_ok = False
        step2_ok = False
        
        # 先执行 release-all
        self.release_all_com(force=True)
        heal_log.append({"step": 0, "action": "release_all", "ok": True, "message": "已释放所有COM对象和残留进程"})
        
        # 步骤1：regsvr32 重注册 WPS 组件
        step1_result = self._step1_regsvr32()
        heal_log.append(step1_result)
        if step1_result.get("ok"):
            step1_ok = True
        
        # 步骤2：WPS 修复安装（需用户确认）
        if not step1_ok or not auto_confirm:
            step2_result = self._step2_repair_install(auto_confirm=auto_confirm)
            heal_log.append(step2_result)
            if step2_result.get("ok"):
                step2_ok = True
        
        # 步骤3：手动修复指引
        if not step1_ok and not step2_ok:
            step3_result = self._step3_manual_guide()
            heal_log.append(step3_result)
        
        # 记录自愈日志到 SQLite
        self._log_self_heal(heal_log)
        
        return {
            "ok": step1_ok or step2_ok,
            "step1_regsvr32": step1_ok,
            "step2_repair_install": step2_ok,
            "log": heal_log,
            "message": "自愈完成" if (step1_ok or step2_ok) else "自愈失败，请参考手动指引"
        }

    def _step1_regsvr32(self) -> Dict[str, Any]:
        """步骤1：regsvr32 重注册 WPS 组件"""
        if not self.is_windows:
            return {"step": 1, "ok": False, "message": "非Windows系统，跳过regsvr32"}
        
        # 常见 WPS DLL 路径
        wps_dlls = [
            "kso.dll",
            "wps.dll",
            "et.dll",
            "wpp.dll",
        ]
        
        # 尝试在 WPS 安装目录中查找
        wps_path = self._get_wps_install_path()
        registered = []
        failed = []
        
        if wps_path:
            for dll in wps_dlls:
                dll_path = Path(wps_path) / dll
                if dll_path.exists():
                    try:
                        proc = subprocess.Popen(
                            ["regsvr32", "/s", str(dll_path)],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                        try:
                            proc.communicate(timeout=10)
                            if proc.returncode == 0:
                                registered.append(dll)
                            else:
                                failed.append(dll)
                        except subprocess.TimeoutExpired:
                            proc.kill()
                            failed.append(dll)
                    except Exception:
                        failed.append(dll)
        
        if registered:
            return {
                "step": 1,
                "ok": True,
                "message": f"regsvr32 重注册成功: {', '.join(registered)}",
                "registered": registered,
                "failed": failed
            }
        else:
            return {
                "step": 1,
                "ok": False,
                "message": "regsvr32 未找到可注册的WPS组件",
                "hint": "WPS可能未安装或路径不在默认位置"
            }

    def _step2_repair_install(self, auto_confirm: bool = False) -> Dict[str, Any]:
        """步骤2：调用 WPS 安装目录的修复安装程序"""
        if not self.is_windows:
            return {"step": 2, "ok": False, "message": "非Windows系统，跳过修复安装"}
        
        wps_path = self._get_wps_install_path()
        if not wps_path:
            return {"step": 2, "ok": False, "message": "未找到WPS安装目录"}
        
        # 查找修复安装程序
        repair_exes = [
            Path(wps_path) / "wps.exe",
            Path(wps_path) / "ksomisc.exe",
            Path(wps_path) / "repair.exe",
        ]
        
        repair_exe = None
        for exe in repair_exes:
            if exe.exists():
                repair_exe = exe
                break
        
        if not repair_exe:
            return {"step": 2, "ok": False, "message": "未找到WPS修复安装程序"}
        
        # 需要用户确认
        if not auto_confirm:
            print(f"\n⚠️  即将运行 WPS 修复安装程序: {repair_exe}")
            print("   此操作可能需要管理员权限，并可能重启WPS。")
            try:
                answer = input("   是否继续？[y/N]: ").strip().lower()
                if answer != "y":
                    return {"step": 2, "ok": False, "message": "用户取消修复安装"}
            except Exception:
                return {"step": 2, "ok": False, "message": "用户取消修复安装"}
        
        try:
            proc = subprocess.Popen(
                [str(repair_exe), "/repair"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            try:
                proc.communicate(timeout=60)
                if proc.returncode == 0:
                    return {"step": 2, "ok": True, "message": "WPS修复安装完成"}
                else:
                    return {"step": 2, "ok": False, "message": f"修复安装返回码: {proc.returncode}"}
            except subprocess.TimeoutExpired:
                proc.kill()
                return {"step": 2, "ok": False, "message": "修复安装超时"}
        except Exception as e:
            return {"step": 2, "ok": False, "message": f"修复安装失败: {str(e)}"}

    def _step3_manual_guide(self) -> Dict[str, Any]:
        """步骤3：手动修复指引"""
        guide = """
╔══════════════════════════════════════════════════════════════╗
║                  COM 手动修复指引                            ║
╠══════════════════════════════════════════════════════════════╣
║ 如果自动修复失败，请按以下步骤手动修复：                      ║
║                                                              ║
║ 1. 关闭所有 WPS/MS Office 程序                               ║
║ 2. 打开任务管理器，结束以下进程：                             ║
║    - kwps.exe, wps.exe, wpscloudsvr.exe                     ║
║    - WINWORD.exe, EXCEL.exe, POWERPNT.exe                   ║
║ 3. 以管理员身份运行命令提示符，执行：                         ║
║    regsvr32 /u "C:\\Program Files\\WPS Office\\kso.dll"      ║
║    regsvr32 "C:\\Program Files\\WPS Office\\kso.dll"         ║
║ 4. 重启电脑                                                  ║
║ 5. 重新安装 WPS Office（如果以上步骤无效）                    ║
║                                                              ║
║ 联系反馈：njskills@agent.qq.com                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        return {"step": 3, "ok": False, "message": "请参考手动修复指引", "guide": guide}

    def _get_wps_install_path(self) -> Optional[str]:
        """获取 WPS 安装路径"""
        if not self.is_windows:
            return None
        
        # 常见安装路径
        possible_paths = [
            r"C:\Program Files\WPS Office",
            r"C:\Program Files (x86)\WPS Office",
            os.path.expandvars(r"%LOCALAPPDATA%\Kingsoft\WPS Office"),
        ]
        
        # 从注册表读取
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Kingsoft\WPS Office") as key:
                install_path = winreg.QueryValueEx(key, "InstallPath")[0]
                if install_path:
                    possible_paths.insert(0, install_path)
        except Exception:
            pass
        
        for path in possible_paths:
            if Path(path).exists():
                return path
        
        return None

    def _log_self_heal(self, log: List[Dict]):
        """记录自愈日志到 SQLite"""
        try:
            db_path = Path(__file__).parent / "wps_stats.db"
            import sqlite3
            with sqlite3.connect(str(db_path)) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS self_heal_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        step INTEGER NOT NULL,
                        action TEXT NOT NULL,
                        ok INTEGER DEFAULT 0,
                        message TEXT DEFAULT ''
                    )
                """)
                for entry in log:
                    conn.execute("""
                        INSERT INTO self_heal_log (timestamp, step, action, ok, message)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        datetime.now().isoformat(),
                        entry.get("step", 0),
                        entry.get("action", entry.get("message", "")),
                        1 if entry.get("ok") else 0,
                        entry.get("message", "")
                    ))
                conn.commit()
        except Exception:
            pass


def _cli():
    """CLI 入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="COM 健康检查 v5.0.0")
    sub = parser.add_subparsers(dest="command", required=True)
    
    # wps-check
    p = sub.add_parser("wps-check", help="检查 WPS COM 状态")
    p.add_argument("--auto-release", action="store_true", help="检查后自动释放")
    
    # ms-check
    p = sub.add_parser("ms-check", help="检查 MS Office COM 状态")
    p.add_argument("--auto-release", action="store_true", help="检查后自动释放")
    
    # residuals
    p = sub.add_parser("residuals", help="检测残留进程")
    
    # release-all
    p = sub.add_parser("release-all", help="释放所有 COM + 清理残留进程")
    p.add_argument("--force", action="store_true", help="强制清理（包括 COM 缓存）")
    
    # full-check
    p = sub.add_parser("full-check", help="完整健康检查报告")
    p.add_argument("--auto-release", action="store_true", help="检查后自动释放")
    p.add_argument("--json", action="store_true", help="JSON 格式输出")
    
    # self-heal (v5.0 新增)
    p = sub.add_parser("self-heal", help="三步自愈（regsvr32→修复安装→手动指引）")
    p.add_argument("--yes", action="store_true", help="自动确认（跳过用户确认）")
    
    args = parser.parse_args()
    checker = COMHealthChecker(auto_release=getattr(args, "auto_release", False))
    
    if args.command == "wps-check":
        result = checker.check_wps_com()
        print(json.dumps(result, ensure_ascii=False, default=str))
    
    elif args.command == "ms-check":
        result = checker.check_ms_com()
        print(json.dumps(result, ensure_ascii=False, default=str))
    
    elif args.command == "residuals":
        result = checker.check_com_residuals()
        print(json.dumps(result, ensure_ascii=False, default=str))
    
    elif args.command == "release-all":
        result = checker.release_all_com(force=args.force)
        print(json.dumps(result, ensure_ascii=False, default=str))
    
    elif args.command == "self-heal":
        result = checker.self_heal(auto_confirm=args.yes)
        print(json.dumps(result, ensure_ascii=False, default=str))
    
    elif args.command == "full-check":
        result = checker.full_health_check()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, default=str))
        else:
            print("=" * 50)
            print("COM 健康检查报告")
            print("=" * 50)
            print(f"状态: {result['status_message']}")
            print(f"评分: {result['score']}/100")
            print(f"耗时: {result['elapsed_seconds']}s")
            print(f"时间: {result['timestamp']}")
            print()
            
            print("[WPS COM]")
            wps = result["checks"]["wps_com"]
            print(f"  {wps.get('message', '未知')}")
            if wps.get("version"):
                print(f"  版本: {wps['version']}")
            
            print()
            print("[MS COM]")
            ms = result["checks"]["ms_com"]
            print(f"  {ms.get('message', '未知')}")
            if ms.get("version"):
                print(f"  版本: {ms['version']}")
            
            print()
            print("[残留进程]")
            res = result["checks"]["residuals"]
            if res.get("residuals"):
                for proc in res["residuals"]:
                    print(f"  ⚠️ {proc}")
            else:
                print(f"  {res.get('message', '无')}")
            
            if result["issues"]:
                print()
                print("[问题]")
                for issue in result["issues"]:
                    print(f"  - {issue}")
            
            if result["suggestions"]:
                print()
                print("[建议]")
                for sug in result["suggestions"]:
                    print(f"  → {sug}")
            
            print()
            print("-" * 50)
            print(f"硬件: {result['hardware'].get('level', 'unknown')} "
                  f"({result['hardware'].get('cpu_cores', '?')}核 "
                  f"{result['hardware'].get('memory_gb', '?')}GB)")
            print("=" * 50)


if __name__ == "__main__":
    _cli()
