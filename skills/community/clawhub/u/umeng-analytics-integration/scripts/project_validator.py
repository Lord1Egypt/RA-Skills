#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目验证模块
验证Android项目完整性并尝试编译
"""

import os
import sys
import subprocess
import platform
from typing import Tuple, List


class ProjectValidator:
    """Android项目验证器"""
    
    def __init__(self, project_path: str, app_module: str = 'app'):
        self.project_path = os.path.abspath(project_path)
        self.app_module = app_module
    
    def validate(self) -> Tuple[bool, str]:
        """
        验证项目完整性
        
        Returns:
            (是否通过, 详细信息)
        """
        print("\n📂 验证项目完整性...\n")
        
        # 1. 检查项目根目录
        if not os.path.exists(self.project_path):
            return False, f"项目路径不存在: {self.project_path}"
        
        print(f"项目路径: {self.project_path}\n")
        
        # 2. 检查必需文件
        if not self._check_required_files():
            return False, "项目缺少必需文件"
        
        # 3. 检查Gradle Wrapper
        if not self._check_gradle_wrapper():
            return False, "Gradle Wrapper检查失败"
        
        # 4. 编译验证
        if not self._check_build():
            return False, "项目编译失败"
        
        print("✅ 项目验证通过\n")
        return True, "项目验证通过"
    
    def _check_required_files(self) -> bool:
        """检查必需文件是否存在"""
        print("检查项目结构...")
        
        required_files = [
            'build.gradle.kts',
            'settings.gradle.kts',
            'gradle.properties',
            f'{self.app_module}/build.gradle.kts',
            f'{self.app_module}/src/main/AndroidManifest.xml'
        ]
        
        # 也支持Groovy格式
        groovy_alternatives = {
            'build.gradle.kts': 'build.gradle',
            'settings.gradle.kts': 'settings.gradle',
            f'{self.app_module}/build.gradle.kts': f'{self.app_module}/build.gradle'
        }
        
        missing_files = []
        for file in required_files:
            file_path = os.path.join(self.project_path, file)
            if not os.path.exists(file_path):
                # 检查是否有Groovy格式的替代文件
                if file in groovy_alternatives:
                    alt_file = groovy_alternatives[file]
                    alt_path = os.path.join(self.project_path, alt_file)
                    if not os.path.exists(alt_path):
                        missing_files.append(file)
                else:
                    missing_files.append(file)
        
        if missing_files:
            print(f"  ❌ 缺少必需文件:")
            for file in missing_files:
                print(f"     - {file}")
            print()
            return False
        
        print("  ✅ 项目结构完整\n")
        return True
    
    def _check_gradle_wrapper(self) -> bool:
        """检查Gradle Wrapper"""
        print("检查 Gradle Wrapper...")
        
        gradlew = os.path.join(self.project_path, 'gradlew')
        gradlew_bat = os.path.join(self.project_path, 'gradlew.bat')
        wrapper_dir = os.path.join(self.project_path, 'gradle', 'wrapper')
        wrapper_jar = os.path.join(wrapper_dir, 'gradle-wrapper.jar')
        wrapper_props = os.path.join(wrapper_dir, 'gradle-wrapper.properties')
        
        # 检查Unix脚本
        if os.path.exists(gradlew):
            if not os.access(gradlew, os.X_OK):
                print("  ❌ gradlew没有执行权限")
                print("  💡 运行: chmod +x gradlew\n")
                return False
            print("  ✅ gradlew存在且有执行权限")
        else:
            print("  ⚠️  未找到gradlew(Unix)")
        
        # 检查Windows脚本
        if os.path.exists(gradlew_bat):
            print("  ✅ gradlew.bat存在")
        else:
            print("  ⚠️  未找到gradlew.bat(Windows)")
        
        # 检查wrapper jar
        if not os.path.exists(wrapper_jar):
            print(f"  ❌ 缺少gradle-wrapper.jar")
            print(f"  💡 请确保{wrapper_dir}目录包含gradle-wrapper.jar\n")
            return False
        print("  ✅ gradle-wrapper.jar存在")
        
        # 检查wrapper properties
        if not os.path.exists(wrapper_props):
            print(f"  ❌ 缺少gradle-wrapper.properties")
            print(f"  💡 请确保{wrapper_dir}目录包含gradle-wrapper.properties\n")
            return False
        print("  ✅ gradle-wrapper.properties存在\n")
        
        return True
    
    def _check_build(self) -> bool:
        """尝试编译项目"""
        print("尝试编译项目...")
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
            
            # 执行编译
            result = subprocess.run(
                [gradlew, 'assembleDebug', '--no-daemon'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=600  # 10分钟超时
            )
            
            if result.returncode == 0:
                print("  ✅ 编译成功\n")
                return True
            else:
                print("  ❌ 编译失败\n")
                self._print_build_error(result)
                return False
                
        except subprocess.TimeoutExpired:
            print("  ❌ 编译超时(超过10分钟)")
            print("  💡 请手动检查项目是否有编译问题\n")
            return False
        except Exception as e:
            print(f"  ❌ 编译过程出错: {str(e)}\n")
            return False
    
    def _configure_java_home(self, java_home: str):
        """
        配置org.gradle.java.home到gradle.properties文件
        
        Args:
            java_home: Java安装路径
        """
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
    
    def _print_build_error(self, result: subprocess.CompletedProcess):
        """打印编译错误信息"""
        print("=" * 60)
        print("编译错误详情")
        print("=" * 60)
        
        # 输出stderr
        if result.stderr:
            # 只显示错误相关部分
            lines = result.stderr.split('\n')
            error_lines = []
            capture = False
            
            for line in lines:
                if 'error' in line.lower() or 'failed' in line.lower() or 'exception' in line.lower():
                    capture = True
                if capture:
                    error_lines.append(line)
            
            if error_lines:
                print('\n'.join(error_lines[:50]))  # 最多显示50行
            else:
                # 如果没有找到错误关键词,显示最后30行
                print('\n'.join(lines[-30:]))
        
        # 输出stdout中的有用信息
        if result.stdout:
            lines = result.stdout.split('\n')
            for line in lines:
                if 'BUILD FAILED' in line or 'error' in line.lower():
                    print(line)
        
        print("=" * 60)
        print()
        print("可能原因:")
        print("  1. 依赖下载失败(网络问题)")
        print("  2. SDK版本不兼容")
        print("  3. 代码语法错误")
        print("  4. 资源文件错误")
        print()
        print("建议:")
        print("  1. 检查网络连接")
        print("  2. 在Android Studio中打开项目查看错误")
        print("  3. 修复所有编译错误后再运行SDK集成")
        print()


def main():
    """主函数 - 用于测试"""
    if len(sys.argv) < 2:
        print("用法: python project_validator.py <project_path> [app_module]")
        sys.exit(1)
    
    project_path = sys.argv[1]
    app_module = sys.argv[2] if len(sys.argv) > 2 else 'app'
    
    validator = ProjectValidator(project_path, app_module)
    success, message = validator.validate()
    
    if success:
        print("✅ 项目验证通过")
        sys.exit(0)
    else:
        print(f"❌ 项目验证失败: {message}")
        sys.exit(1)


if __name__ == '__main__':
    main()
