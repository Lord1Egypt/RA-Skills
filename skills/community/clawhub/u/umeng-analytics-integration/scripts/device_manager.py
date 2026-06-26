#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设备管理模块
检测和管理Android设备(真机/模拟器)
"""

import os
import sys
import subprocess
import platform
from typing import List, Dict, Tuple


class DeviceManager:
    """Android设备管理器"""
    
    def __init__(self):
        self.devices = []
    
    def detect_devices(self) -> List[Dict]:
        """
        检测所有连接的设备
        
        Returns:
            设备列表,每个设备包含:
            - serial: 设备序列号
            - type: 设备类型(real_device/emulator)
            - name: 设备名称
            - state: 设备状态(device/offline/unauthorized)
        """
        print("\n📱 检测Android设备...\n")
        
        try:
            result = subprocess.run(
                ['adb', 'devices', '-l'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                print("  ❌ adb命令执行失败")
                print(f"  错误: {result.stderr}")
                return []
            
            # 解析输出
            lines = result.stdout.strip().split('\n')
            
            # 跳过第一行(List of devices attached)
            for line in lines[1:]:
                if not line.strip():
                    continue
                
                device = self._parse_device_line(line)
                if device:
                    self.devices.append(device)
            
            if not self.devices:
                print("  ⚠️  未检测到任何设备\n")
                return []
            
            # 打印设备列表
            print(f"  检测到 {len(self.devices)} 个设备:\n")
            for i, device in enumerate(self.devices, 1):
                type_icon = "📱" if device['type'] == 'real_device' else "💻"
                print(f"  {i}. {type_icon} {device['name']}")
                print(f"     序列号: {device['serial']}")
                print(f"     类型: {'真机' if device['type'] == 'real_device' else '模拟器'}")
                print(f"     状态: {device['state']}")
                print()
            
            return self.devices
            
        except FileNotFoundError:
            print("  ❌ 未找到adb工具")
            print("  💡 请安装Android SDK Platform-Tools\n")
            return []
        except subprocess.TimeoutExpired:
            print("  ❌ adb命令超时\n")
            return []
        except Exception as e:
            print(f"  ❌ 检测设备失败: {str(e)}\n")
            return []
    
    def _parse_device_line(self, line: str) -> Dict:
        """解析adb devices输出的一行"""
        parts = line.split()
        if len(parts) < 2:
            return None
        
        serial = parts[0]
        state = parts[1]
        
        # 跳过offline和unauthorized设备
        if state not in ['device']:
            return None
        
        # 判断设备类型
        device_type = 'emulator' if serial.startswith('emulator-') else 'real_device'
        
        # 提取设备名称
        name = self._extract_device_name(line, device_type)
        
        return {
            'serial': serial,
            'type': device_type,
            'name': name,
            'state': state
        }
    
    def _extract_device_name(self, line: str, device_type: str) -> str:
        """提取设备名称"""
        if device_type == 'emulator':
            # 模拟器: emulator-5554 device product:sdk_gphone64_x86_64 model:sdk_gphone64_x86_64 device:emulator64x86_64
            if 'model:' in line:
                try:
                    model_start = line.index('model:') + 6
                    model_end = line.index(' ', model_start) if ' ' in line[model_start:] else len(line)
                    return line[model_start:model_end]
                except:
                    pass
            return 'Android Emulator'
        else:
            # 真机: ABC123 device product:xxx model:xxx device:xxx
            if 'model:' in line:
                try:
                    model_start = line.index('model:') + 6
                    model_end = line.index(' ', model_start) if ' ' in line[model_start:] else len(line)
                    return line[model_start:model_end]
                except:
                    pass
            return 'Android Device'
    
    def get_available_device(self) -> Dict:
        """获取一个可用设备(优先真机,其次模拟器)"""
        if not self.devices:
            return None
        
        # 优先选择真机
        for device in self.devices:
            if device['type'] == 'real_device':
                return device
        
        # 其次选择模拟器
        for device in self.devices:
            if device['type'] == 'emulator':
                return device
        
        return None
    
    def handle_no_device(self) -> str:
        """
        处理无设备情况
        
        Returns:
            用户选择: 'emulator' / 'skip' / 'exit'
        """
        print("\n" + "=" * 60)
        print("未检测到可用的Android设备")
        print("=" * 60)
        print("\nSDK验证需要Android设备(真机或模拟器)来运行应用并检查日志。")
        print("\n请选择:")
        print("  [1] 引导配置模拟器")
        print("  [2] 跳过设备测试(仅集成代码)")
        print("  [3] 退出")
        print()
        
        while True:
            choice = input("请选择 (1/2/3, 默认2): ").strip()
            
            if choice == '1' or not choice:
                return 'emulator'
            elif choice == '2':
                return 'skip'
            elif choice == '3':
                return 'exit'
            else:
                print("无效选择,请重新输入")
    
    def provide_emulator_guide(self):
        """提供模拟器配置指引"""
        print("\n" + "=" * 60)
        print("Android模拟器配置指引")
        print("=" * 60)
        
        system = platform.system()
        
        print("\n方法1: 使用Android Studio创建模拟器(推荐)\n")
        print("  1. 打开Android Studio")
        print("  2. 点击 Tools -> Device Manager")
        print("  3. 点击 Create Device")
        print("  4. 选择设备型号(如: Pixel 6)")
        print("  5. 选择系统镜像(推荐: API 34)")
        print("  6. 点击 Finish 完成创建")
        print("  7. 点击 ▶️ 启动模拟器")
        
        print("\n方法2: 使用命令行创建模拟器\n")
        print("  # 列出可用的系统镜像")
        print("  sdkmanager --list | grep system-images")
        print()
        print("  # 安装系统镜像")
        print("  sdkmanager \"system-images;android-34;google_apis;x86_64\"")
        print()
        print("  # 创建AVD")
        print("  avdmanager create avd -n my_emulator -k \"system-images;android-34;google_apis;x86_64\"")
        print()
        print("  # 启动模拟器")
        print("  emulator -avd my_emulator")
        
        print("\n方法3: 使用第三方模拟器\n")
        print("  - Genymotion: https://www.genymotion.com/")
        print("  - 网易MuMu: https://mumu.163.com/")
        print("  - 雷电模拟器: https://www.ldmnq.com/")
        
        print("\n" + "=" * 60)
        print("\n创建并启动模拟器后,请重新运行SDK集成工具进行验证。\n")
    
    def install_apk(self, device_serial: str, apk_path: str) -> bool:
        """
        安装APK到指定设备
        
        Args:
            device_serial: 设备序列号
            apk_path: APK文件路径
        
        Returns:
            是否安装成功
        """
        print(f"\n📦 安装APK到设备 {device_serial}...")
        print(f"  APK路径: {apk_path}\n")
        
        try:
            result = subprocess.run(
                ['adb', '-s', device_serial, 'install', '-r', apk_path],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                print("  ✅ APK安装成功\n")
                return True
            else:
                print("  ❌ APK安装失败")
                print(f"  错误: {result.stderr}")
                print()
                return False
                
        except subprocess.TimeoutExpired:
            print("  ❌ 安装超时(超过2分钟)\n")
            return False
        except Exception as e:
            print(f"  ❌ 安装失败: {str(e)}\n")
            return False
    
    def launch_app(self, device_serial: str, package_name: str) -> bool:
        """
        启动应用
        
        Args:
            device_serial: 设备序列号
            package_name: 应用包名
        
        Returns:
            是否启动成功
        """
        print(f"\n🚀 启动应用 {package_name}...")
        
        try:
            # 获取启动Activity
            result = subprocess.run(
                ['adb', '-s', device_serial, 'shell', 'cmd', 'package', 'resolve-activity', '--brief', package_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0 and result.stdout.strip():
                # 提取Activity名称
                lines = result.stdout.strip().split('\n')
                activity = lines[-1]  # 最后一行是Activity
                
                # 启动应用
                subprocess.run(
                    ['adb', '-s', device_serial, 'shell', 'am', 'start', '-n', activity],
                    capture_output=True,
                    timeout=10
                )
                
                print(f"  ✅ 应用已启动\n")
                return True
            else:
                # 如果无法获取Activity,使用monkey启动
                subprocess.run(
                    ['adb', '-s', device_serial, 'shell', 'monkey', '-p', package_name, '-c', 'android.intent.category.LAUNCHER', '1'],
                    capture_output=True,
                    timeout=10
                )
                
                print(f"  ✅ 应用已启动\n")
                return True
                
        except Exception as e:
            print(f"  ⚠️  启动应用可能失败: {str(e)}\n")
            return False
    
    def capture_logcat(self, device_serial: str, timeout: int = 30) -> str:
        """
        抓取logcat日志
        
        Args:
            device_serial: 设备序列号
            timeout: 超时时间(秒)
        
        Returns:
            logcat日志内容
        """
        print(f"\n📋 抓取logcat日志(超时{timeout}秒)...")
        print("  正在等待SDK初始化...\n")
        
        try:
            # 先清空logcat
            subprocess.run(
                ['adb', '-s', device_serial, 'logcat', '-c'],
                capture_output=True,
                timeout=5
            )
            
            # 抓取logcat
            result = subprocess.run(
                ['adb', '-s', device_serial, 'logcat', '-d'],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                print("  ✅ 日志抓取完成\n")
                return result.stdout
            else:
                print("  ❌ 日志抓取失败\n")
                return ""
                
        except subprocess.TimeoutExpired:
            print(f"  ⚠️  日志抓取超时({timeout}秒)\n")
            # 返回已抓取的部分
            return ""
        except Exception as e:
            print(f"  ❌ 日志抓取失败: {str(e)}\n")
            return ""
    
    def verify_sdk_log(self, logcat_output: str, keyword: str = "本次启动数据: 发送成功!") -> Tuple[bool, str]:
        """
        验证SDK日志
        
        Args:
            logcat_output: logcat日志内容
            keyword: 成功关键词
        
        Returns:
            (是否成功, 详细信息)
        """
        print("\n🔍 验证SDK日志...")
        print(f"  搜索关键词: {keyword}\n")
        
        if not logcat_output:
            print("  ❌ 日志内容为空\n")
            return False, "日志内容为空"
        
        # 搜索关键词
        if keyword in logcat_output:
            print("  ✅ 找到成功关键词!")
            print("  ✅ SDK集成验证成功\n")
            return True, "SDK集成验证成功"
        
        # 尝试搜索其他相关日志
        umeng_logs = [line for line in logcat_output.split('\n') if 'umeng' in line.lower() or 'UMConfigure' in line]
        
        if umeng_logs:
            print("  ⚠️  未找到成功关键词,但发现友盟相关日志:")
            for log in umeng_logs[:5]:  # 最多显示5条
                print(f"    {log}")
            print()
            return False, "未找到成功关键词"
        else:
            print("  ❌ 未找到友盟SDK相关日志")
            print("  💡 可能原因:")
            print("    1. SDK初始化代码未执行")
            print("    2. appkey或channel配置错误")
            print("    3. 网络连接问题")
            print("    4. 应用未正常启动")
            print()
            return False, "未找到SDK日志"


def main():
    """主函数 - 用于测试"""
    manager = DeviceManager()
    devices = manager.detect_devices()
    
    if not devices:
        choice = manager.handle_no_device()
        if choice == 'emulator':
            manager.provide_emulator_guide()
        elif choice == 'skip':
            print("跳过设备测试")
        else:
            print("退出")
            sys.exit(0)
    else:
        device = manager.get_available_device()
        print(f"\n✅ 选择设备: {device['name']} ({device['serial']})")


if __name__ == '__main__':
    main()
