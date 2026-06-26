#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SDK验证模块
通过logcat日志验证友盟统计SDK是否成功上报数据
"""

import os
import sys
import subprocess
import glob
import platform
from typing import Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from device_manager import DeviceManager


class SDKVerifier:
    """友盟统计SDK验证器"""
    
    def __init__(self, project_path: str, app_module: str = 'app'):
        self.project_path = os.path.abspath(project_path)
        self.app_module = app_module
        self.device_manager = DeviceManager()
    
    def verify(self) -> Tuple[bool, str]:
        """
        执行SDK验证
        
        Returns:
            (是否成功, 详细信息)
        """
        print("\n📱 开始验证SDK集成...\n")
        
        # 1. 检测设备
        devices = self.device_manager.detect_devices()
        
        if not devices:
            choice = self.device_manager.handle_no_device()
            
            if choice == 'emulator':
                self.device_manager.provide_emulator_guide()
                return False, "用户选择配置模拟器"
            elif choice == 'skip':
                print("⚠️  跳过设备测试")
                print("请在有设备时手动验证SDK是否成功上报数据\n")
                return True, "跳过验证"
            else:
                return False, "用户选择退出"
        
        # 2. 获取可用设备
        device = self.device_manager.get_available_device()
        if not device:
            print("❌ 无可用设备\n")
            return False, "无可用设备"
        
        print(f"✅ 使用设备: {device['name']} ({device['serial']})\n")
        
        # 3. 编译项目
        if not self._build_project():
            return False, "项目编译失败"
        
        # 4. 查找APK
        apk_path = self._find_apk()
        if not apk_path:
            return False, "未找到APK文件"
        
        # 5. 获取包名
        package_name = self._get_package_name()
        if not package_name:
            return False, "无法获取应用包名"
        
        # 6. 安装APK
        if not self.device_manager.install_apk(device['serial'], apk_path):
            return False, "APK安装失败"
        
        # 7. 启动应用
        if not self.device_manager.launch_app(device['serial'], package_name):
            print("⚠️  应用启动可能失败,继续尝试验证\n")
        
        # 8. 抓取logcat
        logcat_output = self.device_manager.capture_logcat(device['serial'], timeout=30)
        
        # 9. 验证SDK日志
        success, message = self.device_manager.verify_sdk_log(
            logcat_output,
            keyword="本次启动数据: 发送成功!"
        )
        
        if success:
            print("🎉 SDK集成验证成功!")
            print("   友盟统计SDK已成功上报数据\n")
            return True, "SDK集成验证成功"
        else:
            print("⚠️  SDK集成验证未通过")
            print(f"   原因: {message}")
            print("\n💡 建议:")
            print("   1. 检查appkey和channel是否正确")
            print("   2. 检查网络连接")
            print("   3. 查看完整logcat日志排查问题")
            print("   4. 确认SDK初始化代码已执行\n")
            return False, message
    
    def _build_project(self) -> bool:
        """编译项目"""
        print("🔨 编译项目...")
        print("  执行: ./gradlew assembleDebug\n")
        
        try:
            gradlew = os.path.join(self.project_path, 'gradlew')
            
            # 在macOS上查找Java 17并配置到gradle.properties
            if platform.system() == 'Darwin':
                try:
                    result = subprocess.run(
                        ['/usr/libexec/java_home', '-v', '17'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        java_17_home = result.stdout.strip()
                        print(f"  检测到 Java 17: {java_17_home}")
                        
                        # 配置到gradle.properties
                        self._configure_java_home(java_17_home)
                except Exception as e:
                    print(f"  ⚠️  配置JAVA_HOME失败: {str(e)}")
            
            result = subprocess.run(
                [gradlew, 'assembleDebug', '--no-daemon'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode == 0:
                print("  ✅ 编译成功\n")
                return True
            else:
                print("  ❌ 编译失败\n")
                return False
                
        except Exception as e:
            print(f"  ❌ 编译失败: {str(e)}\n")
            return False
    
    def _configure_java_home(self, java_home: str):
        """配置org.gradle.java.home到gradle.properties文件"""
        gradle_properties = os.path.join(self.project_path, 'gradle.properties')
        
        # 读取现有内容
        existing_content = {}
        if os.path.exists(gradle_properties):
            with open(gradle_properties, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        existing_content[key.strip()] = value.strip()
        
        # 检查是否已配置
        if 'org.gradle.java.home' in existing_content:
            current_java_home = existing_content['org.gradle.java.home']
            if current_java_home == java_home:
                print(f"  ✅ org.gradle.java.home已配置")
                return
            else:
                print(f"  ⚠️  更新org.gradle.java.home")
        else:
            print(f"  📝 配置org.gradle.java.home")
        
        # 更新或添加配置
        existing_content['org.gradle.java.home'] = java_home
        
        # 写回文件
        with open(gradle_properties, 'w', encoding='utf-8') as f:
            for key, value in existing_content.items():
                f.write(f"{key}={value}\n")
        
        print(f"  ✅ 已配置: org.gradle.java.home={java_home}\n")
    
    def _find_apk(self) -> str:
        """查找APK文件"""
        print("🔍 查找APK文件...")
        
        # APK输出路径
        apk_dir = os.path.join(
            self.project_path,
            self.app_module,
            'build',
            'outputs',
            'apk',
            'debug'
        )
        
        if not os.path.exists(apk_dir):
            print(f"  ❌ APK目录不存在: {apk_dir}\n")
            return None
        
        # 查找所有apk文件
        apk_files = glob.glob(os.path.join(apk_dir, '*.apk'))
        
        if not apk_files:
            print(f"  ❌ 未找到APK文件\n")
            return None
        
        # 优先选择debug apk
        for apk in apk_files:
            if 'debug' in apk.lower():
                print(f"  ✅ 找到APK: {os.path.basename(apk)}\n")
                return apk
        
        # 返回第一个找到的APK
        apk_path = apk_files[0]
        print(f"  ✅ 找到APK: {os.path.basename(apk_path)}\n")
        return apk_path
    
    def _get_package_name(self) -> str:
        """获取应用包名"""
        print("🔍 获取应用包名...")
        
        manifest_path = os.path.join(
            self.project_path,
            self.app_module,
            'src',
            'main',
            'AndroidManifest.xml'
        )
        
        if not os.path.exists(manifest_path):
            print(f"  ❌ AndroidManifest.xml不存在\n")
            return None
        
        try:
            import re
            
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取package属性
            match = re.search(r'package="([^"]+)"', content)
            if match:
                package_name = match.group(1)
                print(f"  ✅ 包名: {package_name}\n")
                return package_name
            
            print("  ❌ 未找到package属性\n")
            return None
            
        except Exception as e:
            print(f"  ❌ 获取包名失败: {str(e)}\n")
            return None
    
    def verify_manually(self, device_serial: str = None) -> Tuple[bool, str]:
        """
        手动验证模式(用户手动安装和启动应用)
        
        Args:
            device_serial: 指定设备序列号, None则自动选择
        
        Returns:
            (是否成功, 详细信息)
        """
        print("\n📱 手动验证模式")
        print("=" * 60)
        print("\n请手动完成以下步骤:")
        print("  1. 编译项目: ./gradlew assembleDebug")
        print("  2. 安装APK到设备")
        print("  3. 启动应用")
        print("  4. 等待10-30秒")
        print()
        
        input("完成后按Enter继续验证...")
        
        # 检测设备
        if device_serial:
            devices = self.device_manager.detect_devices()
            device = next((d for d in devices if d['serial'] == device_serial), None)
        else:
            devices = self.device_manager.detect_devices()
            device = self.device_manager.get_available_device()
        
        if not device:
            return False, "未检测到设备"
        
        # 抓取logcat
        logcat_output = self.device_manager.capture_logcat(device['serial'], timeout=30)
        
        # 验证SDK日志
        return self.device_manager.verify_sdk_log(
            logcat_output,
            keyword="本次启动数据: 发送成功!"
        )


def main():
    """主函数 - 用于测试"""
    if len(sys.argv) < 2:
        print("用法: python sdk_verifier.py <project_path> [app_module]")
        sys.exit(1)
    
    project_path = sys.argv[1]
    app_module = sys.argv[2] if len(sys.argv) > 2 else 'app'
    
    verifier = SDKVerifier(project_path, app_module)
    success, message = verifier.verify()
    
    if success:
        print("✅ SDK验证通过")
        sys.exit(0)
    else:
        print(f"❌ SDK验证失败: {message}")
        sys.exit(1)


if __name__ == '__main__':
    main()
