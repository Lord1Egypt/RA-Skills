#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用自启动服务管理器 - 跨平台版本 v1.1
支持 Windows 10/11 + macOS

支持 Python/BAT/EXE/Shell 等任何程序的开机自启动

功能：
1. Windows: 通过任务计划程序实现开机自启动
2. macOS: 通过 launchd plist 实现开机自启动  
3. 支持自动重启（崩溃恢复）
4. 日志记录

使用方法：
    python universal_service.py install   - 安装服务
    python universal_service.py uninstall - 卸载服务
    python universal_service.py start     - 手动启动服务
    python universal_service.py stop      - 停止服务
    python universal_service.py status    - 查看服务状态
    
跨平台检测：
    IS_WINDOWS = True (Windows 10/11)
    IS_MACOS = True (macOS 10.15+)
"""

import subprocess
import sys
import os
import time
import signal
import logging
import json
from pathlib import Path
from datetime import datetime

# 跨平台检测
IS_WINDOWS = sys.platform.startswith('win')
IS_MACOS = sys.platform == 'darwin'


class UniversalService:
    """通用服务管理器"""
    
    def __init__(self, config_path="service_config.json"):
        self.config = self.load_config(config_path)
        self.process = None
        self.running = False
        self.restart_count = 0
        self.log_dir = self.get_log_dir()
        self.setup_logging()
        self.logger = logging.getLogger('UniversalService')
        
    def load_config(self, config_path):
        """加载配置文件"""
        if not os.path.exists(config_path):
            # 没有配置文件时返回默认配置
            return {
                "service_name": "DefaultService",
                "display_name": "默认服务",
                "program": {
                    "type": "python",
                    "path": sys.executable,
                    "arguments": "",
                    "working_dir": str(Path.cwd())
                },
                "log": {
                    "enabled": False,
                    "level": "INFO"
                },
                "restart": {
                    "auto_restart": True,
                    "max_restarts": 3,
                    "restart_delay": 30
                }
            }
        
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_log_dir(self):
        """获取日志目录"""
        log_config = self.config.get('log', {})
        if log_config.get('enabled', True):
            log_dir = Path(log_config.get('dir', '.logs'))
            log_dir.mkdir(parents=True, exist_ok=True)
            return log_dir
        return None
    
    def setup_logging(self):
        """设置日志"""
        handlers = [logging.StreamHandler(sys.stdout)]
        
        if self.log_dir:
            log_file = self.log_dir / f'service_{datetime.now().strftime("%Y%m%d")}.log'
            handlers.append(logging.FileHandler(log_file, encoding='utf-8'))
        
        log_config = self.config.get('log', {})
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR
        }
        level = level_map.get(log_config.get('level', 'INFO'), logging.INFO)
        
        logging.basicConfig(
            level=level,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=handlers
        )
    
    def get_full_command(self):
        """获取完整启动命令"""
        program = self.config.get('program', {})
        path = program.get('path', '')
        arguments = program.get('arguments', '')
        
        cmd = [path]
        if arguments:
            # 根据程序类型决定如何处理参数
            prog_type = program.get('type', '').lower()
            if prog_type == 'bat' or path.endswith('.bat'):
                cmd = ['cmd', '/c', path]
                if arguments:
                    cmd.extend(arguments.split())
            elif prog_type == 'exe' or path.endswith('.exe'):
                cmd = [path]
                if arguments:
                    cmd.extend(arguments.split())
            elif prog_type == 'python' or path.endswith('.py') or 'python' in path.lower():
                cmd = [path]
                if arguments:
                    cmd.extend(arguments.split())
            else:
                # 默认尝试直接执行
                cmd = [path]
                if arguments:
                    cmd.extend(arguments.split())
        
        return cmd
    
    def get_working_dir(self):
        """获取工作目录"""
        return self.config.get('program', {}).get('working_dir', os.getcwd())
    
    def start(self):
        """启动程序"""
        try:
            cmd = self.get_full_command()
            working_dir = self.get_working_dir()
            
            self.logger.info("=" * 60)
            self.logger.info(f"  {self.config.get('display_name', '服务')} 启动")
            self.logger.info("=" * 60)
            self.logger.info(f"启动命令：{' '.join(cmd)}")
            self.logger.info(f"工作目录：{working_dir}")
            
            self.process = subprocess.Popen(
                cmd,
                cwd=working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            self.running = True
            self.logger.info(f"程序已启动 (PID: {self.process.pid})")
            
            # 启动后检查子进程输出
            self._monitor_output()
            
            # 等待进程
            self._wait()
            
        except Exception as e:
            self.logger.error(f"启动失败：{e}")
            self.running = False
    
    def _monitor_output(self):
        """监控程序输出"""
        def stream_output(proc):
            while self.running and proc.poll() is None:
                line = proc.stdout.readline()
                if line:
                    print(line.strip())
        
        import threading
        output_thread = threading.Thread(target=stream_output, args=(self.process,), daemon=True)
        output_thread.start()
    
    def stop(self):
        """停止程序"""
        self.logger.info("正在停止程序...")
        
        if self.process:
            try:
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(self.process.pid)], 
                              capture_output=True)
                self.logger.info("程序已停止")
            except Exception as e:
                self.logger.error(f"停止失败：{e}")
        
        self.running = False
    
    def _wait(self):
        """等待进程运行"""
        restart_config = self.config.get('restart', {})
        auto_restart = restart_config.get('auto_restart', True)
        max_restarts = restart_config.get('max_restarts', 5)
        restart_delay = restart_config.get('restart_delay', 30)
        
        try:
            while self.running:
                exit_code = self.process.poll()
                
                if exit_code is not None:
                    self.logger.warning(f"程序退出 (代码：{exit_code})")
                    
                    if auto_restart and self.restart_count < max_restarts:
                        self.restart_count += 1
                        self.logger.info(f"{restart_delay}秒后尝试第 {self.restart_count} 次重启...")
                        time.sleep(restart_delay)
                        self.start()
                        break
                    else:
                        self.logger.info("达到最大重启次数或禁用自动重启")
                        break
                
                time.sleep(5)
        except KeyboardInterrupt:
            self.logger.info("收到中断信号")
            self.stop()


def install_startup_task(service_name, startup_script):
    """安装开机启动任务（跨平台）"""
    logger = logging.getLogger('install')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(handler)
    
    logger.info("=" * 60)
    logger.info("  安装开机自启动任务")
    logger.info("=" * 60)
    
    # 检测操作系统
    if IS_WINDOWS:
        # Windows 版本 - 使用任务计划程序
        return _install_windows_task(service_name, startup_script)
    elif IS_MACOS:
        # macOS 版本 - 使用 launchd
        return _install_macos_daemon(service_name, startup_script)
    else:
        logger.error("[ERROR] 当前操作系统不支持！")
        return False


def _install_windows_task(service_name, startup_script):
    """Windows: 安装任务计划程序"""
    logger = logging.getLogger('install')
    
    # 先删除旧任务（如果存在）
    subprocess.run(['schtasks', '/delete', '/tn', service_name, '/f'], 
                  capture_output=True)
    
    # 创建新任务
    result = subprocess.run([
        'schtasks', '/create',
        '/tn', service_name,
        '/tr', f'"{sys.executable}" "{startup_script}"',
        '/sc', 'onstart',  # 开机启动
        '/rl', 'highest',  # 最高权限
        '/ru', 'SYSTEM',   # 系统用户运行
        '/f'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        logger.info("[OK] 开机自启动任务已创建!")
        logger.info(f"任务名称：{service_name}")
        logger.info("下次开机将自动启动")
    else:
        logger.error(f"[ERROR] 创建失败：{result.stderr}")
    
    return result.returncode == 0


def _install_macos_daemon(service_name, startup_script):
    """macOS: 安装 launchd daemon"""
    logger = logging.getLogger('install')
    
    # 获取当前用户
    import getpass
    username = getpass.getuser()
    
    # 确定 plist 路径
    # 系统级：/Library/LaunchDaemons/
    # 用户级：~/Library/LaunchAgents/
    plist_dir = Path(f"/Users/{username}/Library/LaunchAgents/")
    plist_dir.mkdir(parents=True, exist_ok=True)
    plist_path = plist_dir / f"{service_name}.plist"
    
    # 创建 plist 内容
    script_dir = Path(startup_script).parent
    python_exe = sys.executable
    
    plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{service_name}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_exe}</string>
        <string>{startup_script}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>{str(script_dir)}</string>
    <key>StandardOutPath</key>
    <string>{str(script_dir)}service.log</string>
    <key>StandardErrorPath</key>
    <string>{str(script_dir)}error.log</string>
</dict>
</plist>
'''
    
    # 写入 plist 文件
    with open(plist_path, 'w') as f:
        f.write(plist_content)
    
    # 加载服务
    result = subprocess.run(['launchctl', 'load', '-w', str(plist_path)],
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        logger.info("[OK] 开机自启动任务已创建!")
        logger.info(f"任务名称：{service_name}")
        logger.info(f"Plist 路径：{plist_path}")
        logger.info("下次开机将自动启动")
    else:
        logger.error(f"[ERROR] 创建失败：{result.stderr}")
        logger.info("提示：可能需要 sudo 权限")
    
    return result.returncode == 0


def uninstall_startup_task(service_name):
    """卸载开机启动任务（跨平台）"""
    logger = logging.getLogger('uninstall')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(handler)
    
    logger.info("=" * 60)
    logger.info("  卸载开机自启动任务")
    logger.info("=" * 60)
    
    # 检测操作系统
    if IS_WINDOWS:
        return _uninstall_windows_task(service_name)
    elif IS_MACOS:
        return _uninstall_macos_daemon(service_name)
    else:
        logger.error("[ERROR] 当前操作系统不支持！")
        return False


def _uninstall_windows_task(service_name):
    """Windows: 卸载任务计划程序"""
    logger = logging.getLogger('uninstall')
    
    result = subprocess.run(['schtasks', '/delete', '/tn', service_name, '/f'],
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        logger.info("[OK] 开机自启动任务已删除")
    else:
        logger.error(f"[ERROR] 删除失败：{result.stderr}")
    
    return result.returncode == 0


def _uninstall_macos_daemon(service_name):
    """macOS: 卸载 launchd daemon"""
    logger = logging.getLogger('uninstall')
    
    import getpass
    username = getpass.getuser()
    plist_path = Path(f"/Users/{username}/Library/LaunchAgents/{service_name}.plist")
    
    # 卸载服务
    subprocess.run(['launchctl', 'unload', '-w', str(plist_path)],
                  capture_output=True)
    
    # 删除 plist 文件
    if plist_path.exists():
        plist_path.unlink()
        logger.info("[OK] Plist 文件已删除")
    
    logger.info("[OK] 开机自启动任务已删除")
    return True


def create_startup_script(config_path):
    """创建启动脚本（跨平台）"""
    script_dir = Path(config_path).parent
    
    if IS_WINDOWS:
        # Windows 版本
        script_path = script_dir / 'run_service.bat'
        script_content = f'''@echo off
chcp 65001 >nul
cd /d "{script_dir}"
python "universal_service.py" start
'''
    else:
        # macOS 版本
        script_path = script_dir / 'run_service.sh'
        script_content = f'''#!/bin/bash
cd "{script_dir}"
python3 universal_service.py start
'''
    
    script_path.write_text(script_content, encoding='utf-8')
    
    # 如果是 macOS，添加执行权限
    if IS_MACOS:
        os.chmod(script_path, 0o755)
    
    return script_path


def main():
    """主函数"""
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        # 解析参数
        config_path = 'service_config.json'
        skip_admin_check = False
        
        for i, arg in enumerate(sys.argv[2:], start=2):
            if arg in ['--no-check-admin', '--skip-admin-check']:
                skip_admin_check = True
            elif not arg.startswith('--'):
                config_path = arg
        
        # 帮助命令
        if cmd in ['--help', '-h', 'help']:
            print_usage()
            return
        
        try:
            service = UniversalService(config_path)
            service_name = service.config.get('service_name', 'DefaultService')
            startup_script = create_startup_script(config_path)
            
            if cmd == 'install':
                # 检查管理员权限（可选择跳过）
                if not skip_admin_check and not admin_check():
                    print("[错误] 请以管理员身份运行此命令！")
                    print("右键点击 -^> '以管理员身份运行'")
                    sys.exit(1)
                install_startup_task(service_name, str(startup_script))
                
            elif cmd == 'uninstall':
                # 检查管理员权限（可选择跳过）
                if not skip_admin_check and not admin_check():
                    print("[错误] 请以管理员身份运行此命令！")
                    sys.exit(1)
                uninstall_startup_task(service_name)
                
            elif cmd == 'start':
                service.start()
                
            elif cmd == 'stop':
                service.stop()
                
            elif cmd == 'status':
                check_service_status(service_name)
                
            else:
                print_usage()
                
        except FileNotFoundError as e:
            print(f"[错误] {e}")
            print("\n提示：如果没有配置文件，可以使用以下命令：")
            print("  python universal_service.py install       - 仅安装自启动（不立即运行）")
            print("  python universal_service.py --help        - 查看帮助")
            sys.exit(1)
        except Exception as e:
            print(f"[错误] {e}")
            
            # 如果是配置文件不存在，尝试使用默认服务名卸载
            if "配置文件不存在" in str(e):
                print("\n提示：没有配置文件，将尝试删除默认服务...")
                try:
                    uninstall_startup_task("DefaultService")
                except:
                    pass
            
            sys.exit(1)
    else:
        print_usage()


def admin_check():
    """检查管理员权限"""
    try:
        # 方法 1：检查 Windows 特殊组 SID
        if IS_WINDOWS:
            import ctypes
            try:
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except:
                pass
        
        # 方法 2：尝试执行需要管理员权限的命令
        result = subprocess.run(['net', 'session'], capture_output=True)
        if result.returncode == 0:
            return True
            
        # 方法 3：尝试访问系统目录
        if IS_MACOS:
            return os.access('/etc', os.W_OK)
        else:
            return os.path.exists('C:\\Windows\\System32')
            
    except Exception as e:
        # 如果检测失败，默认假设已获取权限（用户选择管理员模式后通常就是管理员）
        return False


def check_service_status(service_name):
    """检查服务状态"""
    result = subprocess.run(['schtasks', '/query', '/tn', service_name],
                          capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"服务 '{service_name}' 未安装或查询失败")


def print_usage():
    """打印使用帮助"""
    print("""
========================================
  通用自启动服务管理器
========================================

用法：
    python universal_service.py install     - 安装开机自启动
    python universal_service.py uninstall   - 卸载开机自启动
    python universal_service.py start       - 手动启动服务
    python universal_service.py stop        - 停止服务
    python universal_service.py status      - 查看服务状态
    python universal_service.py [config]    - 使用指定配置文件启动

示例：
    python universal_service.py install
    python universal_service.py install service_config.json
    python universal_service.py start service_config.json
    """)


if __name__ == "__main__":
    main()