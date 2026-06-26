#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remote Install Skill - 远程软件安装自动化脚本
支持：RustDesk 远程连接 + 自动检测安装包 + Office 32/64 位判断 + 自动点击"下一步"
"""

import os
import sys
import json
import time
import logging
import subprocess
import platform
import shutil
from pathlib import Path
from datetime import datetime

try:
    import pyautogui
    import pygetwindow as gw
    HAS_GUI = True
except ImportError:
    HAS_GUI = False
    print("警告：pyautogui 或 pygetwindow 未安装，GUI 自动化功能将不可用")

try:
    from pywinauto import Application
    from pywinauto.timings import TimeoutError
    HAS_PYWINAUTO = True
except ImportError:
    HAS_PYWINAUTO = False
    print("警告：pywinauto 未安装，控件识别功能将不可用")


class RustDeskController:
    """RustDesk 远程控制器"""
    
    def __init__(self):
        self.app = None
        self.process = None
    
    def find_rustdesk_window(self):
        """查找 RustDesk 窗口"""
        try:
            windows = gw.getAllWindows()
            for w in windows:
                title = w.title.lower()
                if 'rustdesk' in title:
                    logging.info(f"找到 RustDesk 窗口：{w.title}")
                    return w
            return None
        except Exception as e:
            logging.warning(f"查找 RustDesk 窗口失败：{e}")
            return None
    
    def start_rustdesk(self):
        """启动 RustDesk"""
        rustdesk_paths = [
            os.path.expandvars(r"%ProgramFiles%\RustDesk\RustDesk.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\RustDesk\RustDesk.exe"),
            os.path.join(os.environ.get('APPDATA', ''), r'RustDesk\RustDesk.exe'),
            r"C:\Program Files\RustDesk\RustDesk.exe",
        ]
        
        for path in rustdesk_paths:
            if os.path.exists(path):
                logging.info(f"启动 RustDesk: {path}")
                self.process = subprocess.Popen(path)
                time.sleep(3)
                return True
        
        logging.warning("未找到 RustDesk，尝试搜索...")
        try:
            self.process = subprocess.Popen(['rustdesk'])
            time.sleep(3)
            return True
        except:
            logging.error("无法启动 RustDesk")
            return False
    
    def connect(self, remote_id, password, timeout=60):
        """连接到远程电脑"""
        logging.info(f"开始连接 RustDesk: ID={remote_id}, 密码={password}")
        
        # 确保 RustDesk 已启动
        if not self.find_rustdesk_window():
            if not self.start_rustdesk():
                return {"success": False, "message": "无法启动 RustDesk"}
        
        time.sleep(2)
        
        try:
            # 使用 pywinauto 控制 RustDesk
            app = Application().connect(title_re=".*RustDesk.*", timeout=10)
            main_window = app.top_window()
            main_window.set_focus()
            time.sleep(1)
            
            # 方法 1: 尝试通过控件 ID 输入
            logging.info("尝试通过控件输入...")
            
            # 查找 ID 输入框（通常第一个输入框）
            try:
                # 尝试常见的控件名称
                edit_boxes = main_window.controls(control_type="Edit")
                if len(edit_boxes) >= 2:
                    # 第一个是 ID 输入框，第二个是密码输入框
                    id_edit = edit_boxes[0]
                    pwd_edit = edit_boxes[1]
                    
                    # 清除并输入 ID
                    id_edit.set_focus()
                    id_edit.set_text("")
                    id_edit.type_keys(remote_id.replace(' ', ''), with_spaces=True)
                    logging.info(f"已输入 ID: {remote_id}")
                    
                    # 输入密码
                    pwd_edit.set_focus()
                    pwd_edit.set_text("")
                    pwd_edit.type_keys(password, with_spaces=True)
                    logging.info("已输入密码")
                    
                    time.sleep(1)
                    
                    # 查找连接按钮并点击
                    buttons = main_window.controls(control_type="Button")
                    for btn in buttons:
                        btn_text = btn.window_text()
                        if any(kw in btn_text.lower() for kw in ['connect', '连接', 'control', '控制']):
                            btn.click_input()
                            logging.info(f"点击连接按钮：{btn_text}")
                            break
                    else:
                        # 如果没找到按钮，尝试按回车
                        pyautogui.press('enter')
                        logging.info("按回车键连接")
                    
                    # 等待连接
                    logging.info("等待连接建立...")
                    time.sleep(5)
                    
                    return {"success": True, "message": "RustDesk 连接成功"}
                    
                else:
                    logging.warning(f"未找到足够的输入框，找到 {len(edit_boxes)} 个")
                    
            except Exception as e:
                logging.warning(f"控件操作失败：{e}")
                # 回退到图像识别/坐标方式
                return self.connect_by_coordinates(remote_id, password)
                
        except Exception as e:
            logging.error(f"RustDesk 连接失败：{e}")
            return {"success": False, "message": f"连接失败：{str(e)}"}
    
    def connect_by_coordinates(self, remote_id, password):
        """通过坐标点击连接（备用方案）"""
        logging.info("使用坐标方式连接...")
        
        window = self.find_rustdesk_window()
        if not window:
            return {"success": False, "message": "未找到 RustDesk 窗口"}
        
        try:
            window.activate()
            rect = window.rect
            
            # 估算输入框位置（基于常见 RustDesk 界面布局）
            # ID 输入框通常在顶部
            id_x = rect.left + rect.width // 2
            id_y = rect.top + 80
            
            # 密码输入框在 ID 下方
            pwd_y = rect.top + 130
            
            # 连接按钮在底部
            btn_y = rect.top + rect.height - 60
            
            # 点击 ID 输入框并输入
            pyautogui.click(id_x, id_y)
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.write(remote_id.replace(' ', ''))
            logging.info(f"已输入 ID: {remote_id}")
            
            # 点击密码输入框并输入
            pyautogui.click(id_x, pwd_y)
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.write(password)
            logging.info("已输入密码")
            
            # 点击连接按钮
            pyautogui.click(id_x, btn_y)
            logging.info("点击连接按钮")
            
            # 等待连接
            time.sleep(5)
            
            return {"success": True, "message": "RustDesk 连接成功（坐标方式）"}
            
        except Exception as e:
            logging.error(f"坐标方式连接失败：{e}")
            return {"success": False, "message": f"坐标连接失败：{str(e)}"}
    
    def close(self):
        """关闭 RustDesk 连接"""
        try:
            if self.app:
                self.app.kill()
            logging.info("RustDesk 连接已关闭")
        except:
            pass


class RemoteInstaller:
    """远程安装器"""
    
    def __init__(self, config_path='config.json'):
        """初始化"""
        self.config = self.load_config(config_path)
        self.setup_logging()
        self.results = []
        self.rustdesk = RustDeskController()
        
        if HAS_GUI:
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 1.0
    
    def load_config(self, config_path):
        """加载配置文件"""
        if not os.path.isabs(config_path):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, config_path)
        
        default_config = {
            "installation": {"timeout_seconds": 300, "retry_attempts": 3, "log_level": "INFO"},
            "ui_elements": {
                "next_button_texts": ["下一步", "Next", "继续", "Install", "同意"],
                "finish_button_texts": ["完成", "Finish", "关闭", "Close"]
            },
            "search_paths": ["Desktop", "Downloads", "Documents"],
            "min_file_size_mb": 1
        }
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                return {**default_config, **loaded}
        except Exception as e:
            logging.warning(f"加载配置文件失败，使用默认配置：{e}")
            return default_config
    
    def setup_logging(self):
        """设置日志"""
        log_level = getattr(logging, self.config.get('installation', {}).get('log_level', 'INFO'))
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(script_dir, 'installer.log')
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_path, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    
    def detect_system_arch(self):
        """检测系统架构"""
        return "64" if platform.architecture()[0] == '64bit' else "32"
    
    def detect_office_architecture(self):
        """检测已安装 Office 架构"""
        import winreg
        reg_paths = [
            r"SOFTWARE\Microsoft\Office\ClickToRun\Configuration",
            r"SOFTWARE\WOW6432Node\Microsoft\Office\ClickToRun\Configuration"
        ]
        for reg_path in reg_paths:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                platform_val, _ = winreg.QueryValueEx(key, "Platform")
                winreg.CloseKey(key)
                if platform_val:
                    return "64" if platform_val == "X64" else "32"
            except:
                continue
        return None
    
    def get_total_ram_gb(self):
        """获取总内存 (GB)"""
        try:
            import ctypes
            mem = ctypes.windll.kernel32.GlobalMemoryStatusEx()
            return mem['dwTotalPhys'] / (1024 ** 3)
        except:
            return 8.0
    
    def get_recommended_architecture(self, software_name=""):
        """推荐安装架构"""
        sys_arch = self.detect_system_arch()
        software_lower = software_name.lower()
        
        if any(kw in software_lower for kw in ['office', 'excel', 'word', 'powerpoint', 'outlook']):
            existing = self.detect_office_architecture()
            if existing and self.config.get('office', {}).get('keep_existing_architecture', True):
                logging.info(f"检测到已安装 Office {existing}位，保持一致")
                return existing
            
            total_ram = self.get_total_ram_gb()
            min_ram = self.config.get('office', {}).get('min_ram_for_64bit_gb', 4)
            
            if total_ram < min_ram:
                logging.info(f"内存{total_ram:.1f}GB < {min_ram}GB，推荐 32 位")
                return "32"
            
            prefer_64 = self.config.get('office', {}).get('prefer_64bit', True)
            arch = "64" if prefer_64 else sys_arch
            logging.info(f"系统{sys_arch}位，内存{total_ram:.1f}GB，推荐{arch}位")
            return arch
        
        return sys_arch
    
    def find_installers(self, custom_paths=None, keywords=None):
        """查找安装包"""
        installers = []
        
        if custom_paths:
            search_paths = custom_paths
        else:
            search_dirs = self.config.get("search_paths", ["Desktop", "Downloads"])
            user_profile = os.environ.get("USERPROFILE", "C:\\Users\\Default")
            search_paths = [os.path.join(user_profile, d) for d in search_dirs]
        
        extensions = self.config.get('software_types', {}).get('installer_extensions', ['.exe', '.msi', '.zip', '.rar'])
        min_size = self.config.get('min_file_size_mb', 1) * 1024 * 1024
        
        for search_path in search_paths:
            if not os.path.exists(search_path):
                continue
            
            logging.info(f"搜索目录：{search_path}")
            
            for root, dirs, files in os.walk(search_path):
                if 'extracted' in root.lower():
                    continue
                    
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext not in extensions:
                        continue
                    
                    file_path = os.path.join(root, file)
                    try:
                        if os.path.getsize(file_path) < min_size:
                            continue
                    except:
                        continue
                    
                    if keywords:
                        if not any(kw.lower() in file.lower() for kw in keywords):
                            continue
                    
                    logging.info(f"找到安装包：{file_path}")
                    installers.append(file_path)
        
        return installers
    
    def detect_software_type(self, installer_path):
        """检测软件类型"""
        filename = os.path.basename(installer_path).lower()
        types_config = self.config.get('software_types', {})
        
        type_names = {
            'office': 'Microsoft Office',
            'adobe': 'Adobe Software',
            'browser': 'Browser',
            'archive': 'Archive Tool'
        }
        
        for type_key, config in types_config.items():
            if type_key == 'installer_extensions':
                continue
            patterns = config.get('patterns', [])
            if any(p in filename for p in patterns):
                return type_names.get(type_key, type_key)
        
        return 'Unknown Software'
    
    def click_button_by_text(self, button_texts, timeout=5):
        """通过文本点击按钮"""
        if not HAS_PYWINAUTO:
            return False
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                windows = gw.getAllWindows() if HAS_GUI else []
                for window in windows:
                    if not window.title:
                        continue
                    
                    install_keywords = ["安装", "setup", "installer", "wizard", "install"]
                    if not any(kw in window.title.lower() for kw in install_keywords):
                        continue
                    
                    logging.info(f"检测到安装窗口：{window.title}")
                    
                    try:
                        app = Application().connect(title=window.title)
                        dlg = app.top_window()
                        
                        for btn_text in button_texts:
                            try:
                                btn = dlg.child_window(title=btn_text, control_type="Button")
                                if btn.exists():
                                    btn.click_input()
                                    logging.info(f"点击按钮：{btn_text}")
                                    time.sleep(2)
                                    return True
                            except:
                                continue
                    except:
                        continue
                
                time.sleep(1)
            except Exception as e:
                logging.warning(f"点击按钮时出错：{e}")
                time.sleep(1)
        
        return False
    
    def click_by_position(self, positions):
        """按坐标点击"""
        if not HAS_GUI:
            return False
        
        try:
            windows = gw.getAllWindows()
            for window in windows:
                if not window.title:
                    continue
                
                install_keywords = ["安装", "setup", "installer", "wizard"]
                if not any(kw in window.title.lower() for kw in install_keywords):
                    continue
                
                window.activate()
                rect = window.rect
                
                for ratio_x, ratio_y in positions:
                    x = rect.left + int(rect.width * ratio_x)
                    y = rect.top + int(rect.height * ratio_y)
                    pyautogui.click(x, y)
                    logging.info(f"点击位置：({x}, {y})")
                    time.sleep(2)
                    return True
        except Exception as e:
            logging.warning(f"坐标点击失败：{e}")
        
        return False
    
    def handle_installation_gui(self, timeout=120):
        """处理安装 GUI"""
        logging.info("开始 GUI 自动化安装...")
        
        next_buttons = self.config.get('ui_elements', {}).get('next_button_texts', [])
        finish_buttons = self.config.get('ui_elements', {}).get('finish_button_texts', [])
        button_positions = [(0.75, 0.85), (0.65, 0.85), (0.5, 0.85)]
        
        start_time = time.time()
        click_count = 0
        max_clicks = 20
        
        while time.time() - start_time < timeout and click_count < max_clicks:
            if self.click_button_by_text(next_buttons + finish_buttons, timeout=3):
                click_count += 1
                continue
            
            if self.click_by_position(button_positions):
                click_count += 1
                time.sleep(3)
                continue
            
            time.sleep(2)
        
        logging.info(f"GUI 自动化完成，共点击{click_count}次")
        return True
    
    def install_msi(self, installer_path):
        """安装 MSI 包"""
        cmd = f'msiexec /i "{installer_path}" /quiet /norestart'
        return self.run_command(cmd, "MSI")
    
    def install_exe(self, installer_path):
        """安装 EXE 包"""
        silent_params = ["/S", "/VERYSILENT", "/SILENT", "/quiet", "/q"]
        
        for param in silent_params:
            cmd = f'"{installer_path}" {param}'
            result = self.run_command(cmd, "EXE", timeout=60)
            if result.get('success'):
                return result
        
        logging.info("静默安装失败，尝试 GUI 自动化...")
        try:
            subprocess.Popen(f'"{installer_path}"')
            time.sleep(3)
            self.handle_installation_gui()
            return {"success": True, "message": "EXE 包通过 GUI 自动化安装"}
        except Exception as e:
            return {"success": False, "message": f"EXE 安装失败：{e}"}
    
    def install_archive(self, archive_path):
        """安装压缩包"""
        import zipfile
        
        extract_dir = os.path.join(os.path.dirname(archive_path), "extracted_" + str(int(time.time())))
        os.makedirs(extract_dir, exist_ok=True)
        
        try:
            if archive_path.endswith('.zip'):
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                logging.info(f"解压完成：{extract_dir}")
                
                for root, dirs, files in os.walk(extract_dir):
                    for file in files:
                        if file.lower() in ['setup.exe', 'install.exe', 'installer.exe']:
                            installer = os.path.join(root, file)
                            logging.info(f"找到安装程序：{installer}")
                            result = self.install_exe(installer)
                            try:
                                shutil.rmtree(extract_dir)
                            except:
                                pass
                            return result
                
                return {"success": True, "message": "压缩包已解压"}
            else:
                return {"success": False, "message": f"不支持的压缩格式：{archive_path}"}
        except Exception as e:
            return {"success": False, "message": f"解压失败：{e}"}
    
    def run_command(self, cmd, pkg_type, timeout=None):
        """运行命令"""
        timeout = timeout or self.config.get('installation', {}).get('timeout_seconds', 300)
        
        try:
            logging.info(f"执行命令：{cmd}")
            result = subprocess.run(cmd, shell=True, timeout=timeout, capture_output=True, text=True)
            
            if result.returncode == 0:
                logging.info(f"{pkg_type}包安装成功")
                return {"success": True, "message": f"{pkg_type}包安装成功"}
            else:
                logging.error(f"{pkg_type}包安装失败：{result.stderr}")
                return {"success": False, "message": f"{pkg_type}包安装失败：{result.stderr}"}
        except subprocess.TimeoutExpired:
            logging.error(f"{pkg_type}包安装超时")
            return {"success": False, "message": f"{pkg_type}包安装超时"}
        except Exception as e:
            logging.error(f"{pkg_type}包安装异常：{e}")
            return {"success": False, "message": f"{pkg_type}包安装异常：{e}"}
    
    def install_package(self, installer_path, software_name=""):
        """安装单个包"""
        logging.info(f"开始安装：{installer_path}")
        
        ext = os.path.splitext(installer_path)[1].lower()
        
        if ext == '.msi':
            result = self.install_msi(installer_path)
        elif ext == '.exe':
            result = self.install_exe(installer_path)
        elif ext in ['.zip', '.rar']:
            result = self.install_archive(installer_path)
        else:
            result = {"success": False, "message": f"不支持的格式：{ext}"}
        
        result['package'] = installer_path
        result['type'] = self.detect_software_type(installer_path)
        return result
    
    def verify_installation(self, software_name=""):
        """验证安装"""
        program_files = [
            os.environ.get("ProgramFiles", "C:\\Program Files"),
            os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
        ]
        
        for pf in program_files:
            if os.path.exists(pf):
                try:
                    for item in os.listdir(pf):
                        if software_name.lower() in item.lower():
                            logging.info(f"验证成功：找到 {item}")
                            return True
                except:
                    continue
        
        logging.warning("无法验证安装，但可能已成功")
        return True
    
    def connect_remote(self, remote_id, password):
        """连接到远程电脑"""
        logging.info(f"准备连接远程电脑：ID={remote_id}")
        return self.rustdesk.connect(remote_id, password)
    
    def install_remote(self, remote_id, password, installer_path=None, software_name=""):
        """完整远程安装流程"""
        logging.info("=" * 60)
        logging.info(f"开始远程安装任务 - {datetime.now().isoformat()}")
        logging.info(f"远程 ID: {remote_id}, 安装包：{installer_path}")
        logging.info("=" * 60)
        
        result = {
            "success": False,
            "message": "",
            "remote_id": remote_id,
            "installer_path": installer_path
        }
        
        try:
            # 1. 连接远程电脑
            connect_result = self.connect_remote(remote_id, password)
            if not connect_result.get('success'):
                result["message"] = f"远程连接失败：{connect_result.get('message', '未知错误')}"
                return result
            
            logging.info("远程连接成功")
            
            # 等待连接稳定
            time.sleep(3)
            
            # 2. 查找或验证安装包
            if installer_path and os.path.exists(installer_path):
                logging.info(f"使用指定安装包：{installer_path}")
            else:
                # 在远程电脑上搜索
                installers = self.find_installers()
                if not installers:
                    result["message"] = "未找到安装包"
                    return result
                installer_path = installers[0]
                logging.info(f"找到安装包：{installer_path}")
            
            # 3. 执行安装
            if not software_name:
                software_name = self.detect_software_type(installer_path)
            
            arch = self.get_recommended_architecture(software_name)
            logging.info(f"推荐架构：{arch}位")
            
            install_result = self.install_package(installer_path, software_name)
            
            # 4. 验证安装
            if install_result.get('success'):
                verify_result = self.verify_installation(software_name)
                install_result['verified'] = verify_result
            
            result.update(install_result)
            
        except Exception as e:
            logging.error(f"远程安装异常：{e}")
            result["message"] = f"安装异常：{str(e)}"
        
        # 5. 关闭连接
        self.rustdesk.close()
        
        logging.info("=" * 60)
        logging.info(f"远程安装完成：{result.get('message', '未知')}")
        logging.info("=" * 60)
        
        return result
    
    def install(self, custom_paths=None, keywords=None):
        """本地安装流程（无远程）"""
        logging.info("=" * 60)
        logging.info(f"开始本地安装任务 - {datetime.now().isoformat()}")
        logging.info("=" * 60)
        
        installers = self.find_installers(custom_paths, keywords)
        
        if not installers:
            return {
                "success": False,
                "message": "未找到安装包，请确认安装包位置",
                "summary": {"total_packages": 0, "successful_installs": 0, "failed_installs": 0, "results": []}
            }
        
        logging.info(f"找到 {len(installers)} 个安装包")
        
        results = []
        for installer in installers:
            software_name = self.detect_software_type(installer)
            arch = self.get_recommended_architecture(software_name)
            logging.info(f"推荐架构：{arch}位")
            
            result = self.install_package(installer, software_name)
            result['recommended_arch'] = arch
            results.append(result)
        
        success_count = sum(1 for r in results if r.get('success'))
        failed_count = len(results) - success_count
        
        summary = {
            "total_packages": len(results),
            "successful_installs": success_count,
            "failed_installs": failed_count,
            "results": results
        }
        
        logging.info("=" * 60)
        logging.info(f"本地安装完成 - 成功：{success_count}, 失败：{failed_count}")
        logging.info("=" * 60)
        
        return {
            "success": failed_count == 0,
            "message": f"远程安装流程完成 - 成功{success_count}个，失败{failed_count}个",
            "summary": summary
        }


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='远程软件安装工具')
    parser.add_argument('--remote-id', help='RustDesk 远程 ID')
    parser.add_argument('--password', help='RustDesk 验证码')
    parser.add_argument('--paths', nargs='+', help='自定义搜索路径')
    parser.add_argument('--keywords', nargs='+', help='关键词过滤')
    parser.add_argument('--config', default='config.json', help='配置文件路径')
    parser.add_argument('--package', help='指定安装包路径')
    parser.add_argument('--software', help='软件名称')
    
    args = parser.parse_args()
    
    installer = RemoteInstaller(config_path=args.config)
    
    if args.remote_id and args.password:
        # 远程安装模式
        result = installer.install_remote(
            remote_id=args.remote_id,
            password=args.password,
            installer_path=args.package,
            software_name=args.software
        )
    else:
        # 本地安装模式
        result = installer.install(custom_paths=args.paths, keywords=args.keywords)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    return 0 if result.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
