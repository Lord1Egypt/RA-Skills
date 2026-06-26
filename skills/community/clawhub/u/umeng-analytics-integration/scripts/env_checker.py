#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境检测模块
检测开发环境是否满足友盟统计SDK集成要求
"""

import os
import sys
import shutil
import platform
import subprocess
from typing import Dict, Tuple


class EnvChecker:
    """开发环境检测器"""
    
    def __init__(self):
        self.results = {}
    
    def check_all(self) -> Dict[str, dict]:
        """执行所有环境检查"""
        print("\n🔍 检查开发环境...\n")
        
        # 检查Java环境
        self._check_java()
        
        # 检查Android SDK
        self._check_android_sdk()
        
        # 检查adb
        self._check_adb()
        
        return self.results
    
    def _check_java(self):
        """检查Java环境"""
        print("检查 Java 环境...")
        
        # 先尝试检测macOS上的所有Java版本
        if platform.system() == 'Darwin':
            java_17_path = self._find_java_on_macos(17)
            if java_17_path:
                self.results['java'] = {
                    'status': 'ok',
                    'message': f'Java 17环境正常 ({java_17_path})',
                    'guide': None
                }
                print(f"  ✅ Java 17: {java_17_path}\n")
                return
        
        # 检查默认java命令
        java_path = shutil.which('java')
        if not java_path:
            self.results['java'] = {
                'status': 'critical',
                'message': '未找到Java环境',
                'guide': self._get_java_install_guide()
            }
            print("  ❌ 未找到Java环境\n")
            return
        
        # 获取Java版本
        try:
            result = subprocess.run(
                ['java', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            version_str = result.stderr.split('\n')[0]
            
            # 检查版本是否 >= 17
            if '"17' in version_str or '"18' in version_str or '"19' in version_str or '"20' in version_str or '"21' in version_str:
                self.results['java'] = {
                    'status': 'ok',
                    'message': f'Java环境正常 ({version_str})',
                    'guide': None
                }
                print(f"  ✅ {version_str}\n")
            else:
                self.results['java'] = {
                    'status': 'warning',
                    'message': f'默认Java版本较低 (推荐JDK 17+, 当前: {version_str})',
                    'guide': '建议配置JAVA_HOME指向JDK 17+: export JAVA_HOME=$(/usr/libexec/java_home -v 17)'
                }
                print(f"  ⚠️  {version_str}\n")
        except Exception as e:
            self.results['java'] = {
                'status': 'critical',
                'message': f'检查Java版本失败: {str(e)}',
                'guide': '请手动检查Java环境配置'
            }
            print(f"  ❌ 检查Java版本失败\n")
    
    def _find_java_on_macos(self, version: int) -> str:
        """在macOS上查找指定版本的Java"""
        try:
            result = subprocess.run(
                ['/usr/libexec/java_home', '-v', str(version)],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return None
    
    def _check_android_sdk(self):
        """检查Android SDK"""
        print("检查 Android SDK...")
        
        android_home = os.environ.get('ANDROID_HOME') or os.environ.get('ANDROID_SDK_ROOT')
        
        if not android_home:
            self.results['android_sdk'] = {
                'status': 'critical',
                'message': '未配置ANDROID_HOME或ANDROID_SDK_ROOT环境变量',
                'guide': self._get_android_sdk_guide()
            }
            print("  ❌ 未配置Android SDK环境变量\n")
            return
        
        if not os.path.exists(android_home):
            self.results['android_sdk'] = {
                'status': 'critical',
                'message': f'ANDROID_HOME路径不存在: {android_home}',
                'guide': '请检查ANDROID_HOME环境变量配置'
            }
            print(f"  ❌ Android SDK路径不存在\n")
            return
        
        # 检查关键目录
        required_dirs = ['platforms', 'build-tools', 'platform-tools']
        missing_dirs = [d for d in required_dirs if not os.path.exists(os.path.join(android_home, d))]
        
        if missing_dirs:
            self.results['android_sdk'] = {
                'status': 'warning',
                'message': f'Android SDK缺少以下组件: {", ".join(missing_dirs)}',
                'guide': f'请在Android Studio SDK Manager中安装缺失的组件\nSDK路径: {android_home}'
            }
            print(f"  ⚠️  缺少组件: {', '.join(missing_dirs)}\n")
        else:
            self.results['android_sdk'] = {
                'status': 'ok',
                'message': f'Android SDK配置正常 ({android_home})',
                'guide': None
            }
            print(f"  ✅ Android SDK配置正常\n")
    
    def _check_adb(self):
        """检查adb工具"""
        print("检查 adb 工具...")
        
        adb_path = shutil.which('adb')
        if not adb_path:
            self.results['adb'] = {
                'status': 'warning',
                'message': '未找到adb工具(仅SDK验证时需要)',
                'guide': self._get_adb_install_guide()
            }
            print("  ⚠️  未找到adb工具(仅SDK验证时需要)\n")
            return
        
        try:
            result = subprocess.run(
                ['adb', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            version_line = result.stdout.split('\n')[0]
            self.results['adb'] = {
                'status': 'ok',
                'message': f'adb工具正常 ({version_line})',
                'guide': None
            }
            print(f"  ✅ {version_line}\n")
        except Exception as e:
            self.results['adb'] = {
                'status': 'warning',
                'message': f'检查adb版本失败: {str(e)}',
                'guide': None
            }
            print(f"  ⚠️  检查adb版本失败\n")
    
    def report(self) -> bool:
        """生成检测报告,返回是否通过"""
        print("=" * 60)
        print("环境检测报告")
        print("=" * 60)
        
        has_critical = False
        has_warning = False
        
        for tool, result in self.results.items():
            status = result['status']
            message = result['message']
            
            if status == 'ok':
                print(f"✅ {tool}: {message}")
            elif status == 'warning':
                print(f"⚠️  {tool}: {message}")
                has_warning = True
            elif status == 'critical':
                print(f"❌ {tool}: {message}")
                has_critical = True
            
            if result.get('guide'):
                print(f"   💡 {result['guide']}")
        
        print("=" * 60)
        
        if has_critical:
            print("\n❌ 环境检查失败: 存在必需工具缺失")
            print("请安装上述标记为❌的工具后再运行SDK集成。\n")
            return False
        
        if has_warning:
            print("\n⚠️  环境检查通过,但有建议安装的工具")
            print("标记为⚠️的工具不是必需的,但可能影响部分功能。\n")
        else:
            print("\n✅ 环境检查通过\n")
        
        return True
    
    def _get_java_install_guide(self) -> str:
        """获取Java安装指引"""
        system = platform.system()
        if system == 'Darwin':
            return 'macOS: brew install openjdk@17'
        elif system == 'Linux':
            return 'Linux: sudo apt install openjdk-17-jdk'
        else:
            return 'Windows: 下载 https://adoptium.net/'
    
    def _get_android_sdk_guide(self) -> str:
        """获取Android SDK安装指引"""
        return '下载Android Studio: https://developer.android.com/studio\n安装后会在~/.bash_profile或~/.zshrc中自动配置环境变量'
    
    def _get_adb_install_guide(self) -> str:
        """获取adb安装指引"""
        system = platform.system()
        if system == 'Darwin':
            return 'macOS: brew install android-platform-tools'
        elif system == 'Linux':
            return 'Linux: sudo apt install android-tools-adb'
        else:
            return 'Windows: 安装Android SDK Platform-Tools'


def main():
    """主函数"""
    checker = EnvChecker()
    checker.check_all()
    success = checker.report()
    
    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()
