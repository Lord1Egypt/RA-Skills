#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SDK集成模块
自动完成友盟统计SDK的所有集成步骤
"""

import os
import re
import shutil
from datetime import datetime
from typing import Tuple, List


class SDKIntegrator:
    """友盟统计SDK集成器"""
    
    def __init__(self, project_path: str, app_module: str, config: dict):
        self.project_path = os.path.abspath(project_path)
        self.app_module = app_module
        self.config = config  # {'appkey': str, 'channel': str, 'using_placeholder': bool}
        self.backup_dir = None
        self.modified_files = []
    
    def integrate(self) -> Tuple[bool, str]:
        """
        执行SDK集成
        
        Returns:
            (是否成功, 详细信息)
        """
        print("\n📦 开始集成友盟统计SDK...\n")
        
        # 创建备份目录(备份整个工程)
        self._create_backup_dir()
        
        try:
            # 1. 添加Maven仓库
            if not self._add_maven_repository():
                return False, "Maven仓库配置失败"
            
            # 2. 添加SDK依赖
            if not self._add_sdk_dependencies():
                return False, "SDK依赖添加失败"
            
            # 3. 添加权限
            if not self._add_permissions():
                return False, "权限配置失败"
            
            # 4. 添加混淆规则
            if not self._add_proguard_rules():
                return False, "混淆配置失败"
            
            # 5. 处理Application类
            if not self._handle_application_class():
                return False, "Application类处理失败"
            
            print("✅ SDK集成完成\n")
            return True, "SDK集成完成"
            
        except Exception as e:
            print(f"\n❌ SDK集成失败: {str(e)}\n")
            return False, f"SDK集成失败: {str(e)}"
    
    def _create_backup_dir(self):
        """创建备份目录(备份整个工程)"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_dir = os.path.join(
            os.path.dirname(self.project_path),
            f'{os.path.basename(self.project_path)}_backup_{timestamp}'
        )
        
        print(f"📁 开始备份整个工程目录...")
        print(f"   源目录: {self.project_path}")
        print(f"   备份到: {self.backup_dir}\n")
        
        # 使用shutil.copytree备份整个工程
        try:
            shutil.copytree(self.project_path, self.backup_dir)
            print(f"✅ 工程备份完成\n")
        except Exception as e:
            print(f"❌ 备份失败: {str(e)}\n")
            raise
    
    def _backup_file(self, file_path: str):
        """备份文件"""
        if not os.path.exists(file_path):
            return
        
        # 保持相对路径结构
        rel_path = os.path.relpath(file_path, self.project_path)
        backup_path = os.path.join(self.backup_dir, rel_path)
        
        # 创建目录
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        # 复制文件
        shutil.copy2(file_path, backup_path)
        self.modified_files.append(file_path)
        print(f"  💾 备份: {rel_path}")
    
    def _add_maven_repository(self) -> bool:
        """步骤1: 添加Maven仓库配置"""
        print("步骤 1/5: 配置Maven仓库")
        
        # 根据文件类型选择正确的语法
        maven_repo_kts = "maven { setUrl(\"https://repo1.maven.org/maven2/\") }"
        maven_repo_groovy = "maven { url 'https://repo1.maven.org/maven2/' }"
        
        # 检查项目级build.gradle.kts
        build_gradle = os.path.join(self.project_path, 'build.gradle.kts')
        build_gradle_groovy = os.path.join(self.project_path, 'build.gradle')
        
        if os.path.exists(build_gradle):
            if not self._inject_maven_to_file(build_gradle, maven_repo_kts):
                return False
        elif os.path.exists(build_gradle_groovy):
            if not self._inject_maven_to_file(build_gradle_groovy, maven_repo_groovy):
                return False
        else:
            print("  ❌ 未找到项目级build.gradle文件\n")
            return False
        
        print("  ✅ Maven仓库配置完成\n")
        return True
    
    def _inject_maven_to_file(self, file_path: str, maven_repo: str) -> bool:
        """向 build.gradle文件注入Maven仓库配置"""
        self._backup_file(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已存在
        if 'repo1.maven.org' in content:
            print("  ⚠️  Maven仓库已存在,跳过")
            return True
        
        # 新版Android项目可能使用settings.gradle.kts管理repositories
        # 检查是否有settings.gradle.kts
        settings_gradle = os.path.join(os.path.dirname(file_path), 'settings.gradle.kts')
        settings_gradle_groovy = os.path.join(os.path.dirname(file_path), 'settings.gradle')
        
        # 优先在settings.gradle中配置
        if os.path.exists(settings_gradle):
            return self._inject_maven_to_settings(settings_gradle, maven_repo)
        elif os.path.exists(settings_gradle_groovy):
            return self._inject_maven_to_settings(settings_gradle_groovy, maven_repo)
        
        # 如果没有settings.gradle,尝试在build.gradle中添加
        lines = content.split('\n')
        new_lines = []
        in_repositories = False
        repositories_level = 0
        injected = False
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            
            # 检测进入repositories块
            if 'repositories' in line and '{' in line:
                in_repositories = True
                repositories_level = line.count('{') - line.count('}')
                continue
            
            if in_repositories:
                repositories_level += line.count('{') - line.count('}')
                
                # 在repositories块内,遇到第一个}时注入
                if repositories_level <= 0:
                    # 检查前一行是否有缩进
                    indent = '        '  # 默认8个空格
                    
                    # 注入Maven仓库配置
                    new_lines.insert(-1, f'{indent}{maven_repo}')
                    injected = True
                    in_repositories = False
        
        if not injected:
            # 如果没有找到repositories块,在文件末尾添加
            # 这是针对使用Version Catalogs的新项目
            print("  ⚠️  使用Version Catalogs格式,将在settings.gradle中配置")
            print("  💡 如果settings.gradle不存在,需要手动配置Maven仓库")
            
            # 创建或修改settings.gradle.kts
            if not os.path.exists(settings_gradle):
                settings_gradle = os.path.join(os.path.dirname(file_path), 'settings.gradle')
            
            if os.path.exists(settings_gradle):
                return self._inject_maven_to_settings(settings_gradle, maven_repo)
            else:
                # 创建settings.gradle.kts
                settings_content = """pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
        maven { url 'https://repo1.maven.org/maven2/' }
    }
}

rootProject.name = "android_demo_project"
include(":app")
"""
                with open(settings_gradle, 'w', encoding='utf-8') as f:
                    f.write(settings_content)
                print(f"  ✅ 已创建settings.gradle.kts并配置Maven仓库")
                return True
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print("  ✅ 已在项目级build.gradle中添加Maven仓库")
        return True
    
    def _inject_maven_to_settings(self, settings_file: str, maven_repo: str) -> bool:
        """settings.gradle注入Maven仓库配置"""
        # 检查是否需要备份(如果settings文件不在原来的修改列表中)
        if settings_file not in self.modified_files:
            self._backup_file(settings_file)
            
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查是否已存在
        if 'repo1.maven.org' in content:
            print("  ⚠️  Maven仓库已存在于settings.gradle,跳过")
            return True
            
        # 根据文件类型选择正确的语法
        is_kotlin_dsl = settings_file.endswith('.kts')
        if is_kotlin_dsl:
            maven_repo = "maven { setUrl(\"https://repo1.maven.org/maven2/\") }"
        else:
            maven_repo = "maven { url 'https://repo1.maven.org/maven2/' }"
        
        # 查找dependencyResolutionManagement.repositories块
        lines = content.split('\n')
        new_lines = []
        in_dependency_repos = False
        repo_level = 0
        injected = False
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            
            # 检测进入dependencyResolutionManagement的repositories块
            if 'dependencyResolutionManagement' in line:
                in_dependency_repos = True
                continue
            
            if in_dependency_repos and 'repositories' in line and '{' in line:
                repo_level = line.count('{') - line.count('}')
                continue
            
            if in_dependency_repos and repo_level > 0:
                repo_level += line.count('{') - line.count('}')
                
                # 在repositories块结束前注入
                if repo_level <= 0:
                    indent = '        '
                    new_lines.insert(-1, f'{indent}{maven_repo}')
                    injected = True
                    in_dependency_repos = False
        
        if not injected:
            # 如果没有找到,在文件末尾添加
            print("  ⚠️  未找到dependencyResolutionManagement块,手动添加")
            new_lines.append('')
            new_lines.append('dependencyResolutionManagement {')
            new_lines.append('    repositoriesMode.set(RepositoriesMode.PREFER_SETTINGS)')
            new_lines.append('    repositories {')
            new_lines.append('        google()')
            new_lines.append('        mavenCentral()')
            new_lines.append(f'        {maven_repo}')
            new_lines.append('    }')
            new_lines.append('}')
            injected = True
        
        # 写回文件
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print("  ✅ 已在settings.gradle中添加Maven仓库")
        return True
    
    def _add_sdk_dependencies(self) -> bool:
        """步骤2: 添加SDK依赖"""
        print("步骤 2/5: 添加SDK依赖")
        
        # 检查是否使用Version Catalogs
        version_catalog = os.path.join(self.project_path, 'gradle', 'libs.versions.toml')
        
        if os.path.exists(version_catalog):
            print("  检测到Version Catalogs,使用libs.versions.toml管理依赖")
            return self._add_dependencies_via_version_catalog(version_catalog)
        else:
            print("  未检测到Version Catalogs,使用build.gradle直接声明")
            app_build_gradle = os.path.join(self.project_path, self.app_module, 'build.gradle.kts')
            app_build_gradle_groovy = os.path.join(self.project_path, self.app_module, 'build.gradle')
            
            if os.path.exists(app_build_gradle):
                # Kotlin DSL使用括号语法
                return self._inject_dependencies(app_build_gradle, use_parentheses=True)
            elif os.path.exists(app_build_gradle_groovy):
                # Groovy使用空格语法
                return self._inject_dependencies(app_build_gradle_groovy, use_parentheses=False)
            else:
                print(f"  ❌ 未找到{self.app_module}/build.gradle文件\n")
                return False
    
    def _add_dependencies_via_version_catalog(self, version_catalog: str) -> bool:
        """
        通过Version Catalogs添加SDK依赖
        
        Args:
            version_catalog: libs.versions.toml文件路径
        
        Returns:
            是否成功
        """
        self._backup_file(version_catalog)
        
        with open(version_catalog, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已存在
        if 'umeng-common' in content or 'umeng-asms' in content:
            print("  ⚠️  友盟SDK依赖已存在于Version Catalogs,跳过")
            return True
        
        # 添加版本定义到[versions]部分
        versions_to_add = [
            'umeng-common = "+"',
            'umeng-asms = "+"'
        ]
        
        # 添加库定义到[libraries]部分
        libraries_to_add = [
            'umeng-common = { module = "com.umeng.umsdk:common", version.ref = "umeng-common" }',
            'umeng-asms = { module = "com.umeng.umsdk:asms", version.ref = "umeng-asms" }'
        ]
        
        lines = content.split('\n')
        new_lines = []
        in_versions = False
        in_libraries = False
        injected_versions = False
        injected_libraries = False
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            stripped = line.strip()
            
            # 检测[versions]部分
            if stripped == '[versions]':
                in_versions = True
                in_libraries = False
                continue
            
            # 检测[libraries]部分
            if stripped == '[libraries]':
                in_libraries = True
                in_versions = False
                continue
            
            # 检测其他部分开始
            if stripped.startswith('[') and stripped.endswith(']'):
                # 如果在[versions]部分末尾,注入版本定义
                if in_versions and not injected_versions:
                    # 在前一行插入
                    new_lines.pop()  # 移除刚添加的部分标题
                    for version in versions_to_add:
                        new_lines.append(version)
                        print(f"  ✅ 添加版本: {version}")
                    new_lines.append('')  # 空行
                    new_lines.append(line)  # 重新添加部分标题
                    injected_versions = True
                    in_versions = False
                in_libraries = False
                continue
            
            # 在[versions]部分末尾注入
            if in_versions and not injected_versions:
                # 检查下一行是否是新的部分或文件末尾
                if i + 1 >= len(lines) or lines[i + 1].strip().startswith('['):
                    for version in versions_to_add:
                        new_lines.append(version)
                        print(f"  ✅ 添加版本: {version}")
                    injected_versions = True
            
            # 在[libraries]部分末尾注入
            if in_libraries and not injected_libraries:
                # 检查下一行是否是新的部分或文件末尾
                if i + 1 >= len(lines) or lines[i + 1].strip().startswith('['):
                    for library in libraries_to_add:
                        new_lines.append(library)
                        print(f"  ✅ 添加库: {library}")
                    injected_libraries = True
        
        # 如果没有找到[versions]或[libraries]部分,手动添加
        if not injected_versions:
            print("  ⚠️  未找到[versions]部分,手动添加")
            new_lines.append('')
            new_lines.append('[versions]')
            for version in versions_to_add:
                new_lines.append(version)
            injected_versions = True
        
        if not injected_libraries:
            print("  ⚠️  未找到[libraries]部分,手动添加")
            new_lines.append('')
            new_lines.append('[libraries]')
            for library in libraries_to_add:
                new_lines.append(library)
            injected_libraries = True
        
        # 写回文件
        with open(version_catalog, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        # 现在需要在build.gradle.kts中添加对Version Catalogs的引用
        print("\n  📝 在build.gradle.kts中添加依赖引用...")
        return self._add_version_catalog_references_to_build_gradle()
    
    def _add_version_catalog_references_to_build_gradle(self) -> bool:
        """在build.gradle.kts中添加Version Catalogs依赖引用"""
        app_build_gradle = os.path.join(self.project_path, self.app_module, 'build.gradle.kts')
        
        if not os.path.exists(app_build_gradle):
            print(f"  ❌ 未找到{self.app_module}/build.gradle.kts")
            return False
        
        self._backup_file(app_build_gradle)
        
        with open(app_build_gradle, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已存在
        if 'libs.umeng.common' in content:
            print("  ⚠️  Version Catalogs引用已存在,跳过")
            return True
        
        # 在dependencies块中添加引用
        references_to_add = [
            'implementation(libs.umeng.common)',
            'implementation(libs.umeng.asms)'
        ]
        
        lines = content.split('\n')
        new_lines = []
        in_dependencies = False
        dependencies_level = 0
        
        for line in lines:
            new_lines.append(line)
            
            # 检测进入dependencies块
            if 'dependencies' in line and '{' in line:
                in_dependencies = True
                dependencies_level = line.count('{') - line.count('}')
                continue
            
            if in_dependencies:
                dependencies_level += line.count('{') - line.count('}')
                
                # 在dependencies块结束前注入
                if dependencies_level <= 0:
                    indent = '    '  # 4个空格
                    for ref in references_to_add:
                        new_lines.insert(-1, f'{indent}{ref}')
                        print(f"  ✅ 添加引用: {ref}")
                    in_dependencies = False
        
        # 写回文件
        with open(app_build_gradle, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print()
        return True
    
    def _inject_dependencies(self, file_path: str, use_parentheses: bool = False) -> bool:
        """app/build.gradle注入SDK依赖"""
        self._backup_file(file_path)
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查是否已存在
        if 'com.umeng.umsdk:common' in content:
            print("  ⚠️  SDK依赖已存在,跳过")
            return True
            
        # 根据文件类型选择正确的语法
        if use_parentheses:
            # Kotlin DSL: implementation("...")
            dependencies_to_add = [
                'implementation("com.umeng.umsdk:common:+")',
                'implementation("com.umeng.umsdk:asms:+")'
            ]
        else:
            # Groovy: implementation '...'
            dependencies_to_add = [
                "implementation 'com.umeng.umsdk:common:+'",
                "implementation 'com.umeng.umsdk:asms+'"
            ]
        
        lines = content.split('\n')
        new_lines = []
        in_dependencies = False
        dependencies_level = 0
        
        for line in lines:
            new_lines.append(line)
            
            # 检测进入dependencies块
            if 'dependencies' in line and '{' in line:
                in_dependencies = True
                dependencies_level = line.count('{') - line.count('}')
                continue
            
            if in_dependencies:
                dependencies_level += line.count('{') - line.count('}')
                
                # 在dependencies块结束前注入
                if dependencies_level <= 0:
                    indent = '    '  # 4个空格
                    
                    # 注入依赖
                    for dep in dependencies_to_add:
                        new_lines.insert(-1, f'{indent}{dep}')
                        print(f"  ✅ 添加依赖: {dep}")
                    
                    in_dependencies = False
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print()
        return True
    
    def _add_permissions(self) -> bool:
        """步骤3: 添加权限配置"""
        print("步骤 3/5: 配置权限")
        
        manifest_path = os.path.join(
            self.project_path,
            self.app_module,
            'src',
            'main',
            'AndroidManifest.xml'
        )
        
        if not os.path.exists(manifest_path):
            print(f"  ❌ 未找到AndroidManifest.xml\n")
            return False
        
        self._backup_file(manifest_path)
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已存在
        if 'android.permission.INTERNET' in content:
            print("  ⚠️  权限已存在,跳过")
            return True
        
        # 添加权限
        permissions = [
            '<uses-permission android:name="android.permission.INTERNET" />',
            '<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />'
        ]
        
        # 在<manifest>标签后,第一个<application>标签前插入
        lines = content.split('\n')
        new_lines = []
        inserted = False
        
        for i, line in enumerate(lines):
            # 在<application>标签前插入
            if '<application' in line and not inserted:
                # 添加空行和权限
                new_lines.append('')
                for perm in permissions:
                    new_lines.append(f'    {perm}')
                    print(f"  ✅ 添加权限: {perm}")
                new_lines.append('')
                inserted = True
            
            new_lines.append(line)
        
        if not inserted:
            print("  ❌ 未找到<application>标签\n")
            return False
        
        # 写回文件
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print()
        return True
    
    def _add_proguard_rules(self) -> bool:
        """步骤4: 添加混淆规则"""
        print("步骤 4/5: 配置混淆规则")
        
        proguard_path = os.path.join(
            self.project_path,
            self.app_module,
            'proguard-rules.pro'
        )
        
        # 如果文件不存在,创建它
        if not os.path.exists(proguard_path):
            with open(proguard_path, 'w', encoding='utf-8') as f:
                f.write('# Add project specific ProGuard rules here.\n')
            print("  📝 创建proguard-rules.pro")
        
        self._backup_file(proguard_path)
        
        with open(proguard_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已存在
        if 'com.umeng.**' in content:
            print("  ⚠️  混淆规则已存在,跳过")
            return True
        
        # 添加混淆规则
        proguard_rules = """
# ========== 友盟统计SDK混淆规则 ==========
-keep class com.umeng.** {*;}
-keep class org.repackage.** {*;}
-keep class com.uyumao.** { *; }
-keepclassmembers class * {
   public <init> (org.json.JSONObject);
}
"""
        
        with open(proguard_path, 'a', encoding='utf-8') as f:
            f.write(proguard_rules)
        
        print("  ✅ 已添加友盟统计SDK混淆规则\n")
        return True
    
    def _handle_application_class(self) -> bool:
        """步骤5: 处理Application类"""
        print("步骤 5/5: 配置Application类")
        
        # 检测项目语言
        language = self._detect_project_language()
        print(f"  检测到项目语言: {language}\n")
        
        # 查找现有Application类
        app_class_name = self._find_application_class()
        
        if app_class_name:
            print(f"  找到现有Application类: {app_class_name}")
            return self._modify_application_class(app_class_name, language)
        else:
            print("  未找到Application类,将创建新的")
            return self._create_application_class(language)
    
    def _detect_project_language(self) -> str:
        """检测项目主要语言(Kotlin/Java)"""
        src_main = os.path.join(self.project_path, self.app_module, 'src', 'main')
        
        kotlin_dir = os.path.join(src_main, 'kotlin')
        java_dir = os.path.join(src_main, 'java')
        
        # 检查是否有Kotlin文件
        if os.path.exists(kotlin_dir):
            for root, dirs, files in os.walk(kotlin_dir):
                if any(f.endswith('.kt') for f in files):
                    return 'Kotlin'
        
        # 检查是否有Java文件
        if os.path.exists(java_dir):
            for root, dirs, files in os.walk(java_dir):
                if any(f.endswith('.java') for f in files):
                    return 'Java'
        
        # 默认返回Kotlin
        return 'Kotlin'
    
    def _find_application_class(self) -> str:
        """查找AndroidManifest.xml中注册的Application类"""
        manifest_path = os.path.join(
            self.project_path,
            self.app_module,
            'src',
            'main',
            'AndroidManifest.xml'
        )
        
        if not os.path.exists(manifest_path):
            return None
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找<application>标签中的android:name属性
        # 使用更精确的正则,只匹配<application标签内的android:name
        match = re.search(r'<application[^>]*\sandroid:name="([^"]+)"', content)
        if match:
            name = match.group(1)
            # 排除MultiDexApplication
            if name != 'android.support.multidex.MultiDexApplication':
                # 如果是相对路径(以.开头),去掉点号
                if name.startswith('.'):
                    name = name[1:]
                return name
        
        return None
    
    def _modify_application_class(self, app_class_name: str, language: str) -> bool:
        """修改现有Application类,在onCreate尾部追加SDK初始化代码"""
        # 查找Application类文件
        app_file_path = self._find_class_file(app_class_name, language)
            
        if not app_file_path:
            print(f"  ❌ 未找到Application类文件: {app_class_name}\n")
            return False
            
        self._backup_file(app_file_path)
            
        with open(app_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查是否已经存在UMConfigure初始化代码
        if 'UMConfigure.init' in content or 'UMConfigure.preInit' in content:
            print("  ⚠️  友盟SDK初始化代码已存在,跳过")
            return True
            
        # 生成SDK初始化代码
        init_code = self._generate_sdk_init_code(language)
            
        # 查找onCreate方法
        if language == 'Kotlin':
            # Kotlin: 在super.onCreate()后追加
            if 'super.onCreate()' in content:
                new_content = content.replace(
                    'super.onCreate()',
                    f'super.onCreate()\n{init_code}',
                    1  # 只替换第一次出现
                )
            else:
                print("  ❌ 未找到super.onCreate()\n")
                return False
        else:
            # Java: 在super.onCreate()后追加
            if 'super.onCreate();' in content:
                new_content = content.replace(
                    'super.onCreate();',
                    f'super.onCreate();\n{init_code}',
                    1  # 只替换第一次出现
                )
            else:
                print("  ❌ 未找到super.onCreate()\n")
                return False
            
        # 写回文件
        with open(app_file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"  ✅ 已在{app_class_name}.onCreate()中追加SDK初始化代码\n")
        return True
    
    def _create_application_class(self, language: str) -> bool:
        """创建新的Application类"""
        # 生成类名
        app_class_name = 'UmengApplication'
        
        # 从AndroidManifest.xml获取包名
        package_name = self._find_package_name()
        print(f"  包名: {package_name}")
        
        # 确定文件路径
        src_main = os.path.join(self.project_path, self.app_module, 'src', 'main')
        
        # 在java或kotlin目录下创建
        base_dir = None
        kotlin_dir = os.path.join(src_main, 'kotlin')
        java_dir = os.path.join(src_main, 'java')
        
        if os.path.exists(kotlin_dir):
            base_dir = kotlin_dir
        elif os.path.exists(java_dir):
            base_dir = java_dir
        else:
            # 如果都不存在,使用java目录
            base_dir = java_dir
            os.makedirs(base_dir, exist_ok=True)
        
        # 将包名转换为路径
        package_path = package_name.replace('.', '/')
        file_dir = os.path.join(base_dir, package_path)
        os.makedirs(file_dir, exist_ok=True)
        
        # 生成文件路径
        if language == 'Kotlin':
            file_path = os.path.join(file_dir, f'{app_class_name}.kt')
        else:
            file_path = os.path.join(file_dir, f'{app_class_name}.java')
        
        # 生成类代码
        if language == 'Kotlin':
            class_code = self._generate_kotlin_application_class(package_name)
        else:
            class_code = self._generate_java_application_class(package_name)
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(class_code)
        
        print(f"  ✅ 已创建Application类: {os.path.relpath(file_path, self.project_path)}")
        
        # 在AndroidManifest.xml中注册
        if not self._register_application_class(app_class_name):
            return False
        
        print()
        return True
    
    def _find_package_name(self) -> str:
        """查找包名"""
        # 优先从build.gradle.kts获取namespace或applicationId
        build_gradle = os.path.join(self.project_path, self.app_module, 'build.gradle.kts')
        if os.path.exists(build_gradle):
            with open(build_gradle, 'r', encoding='utf-8') as f:
                gradle_content = f.read()
            
            # 优先查找namespace
            match = re.search(r'namespace\s*=\s*"([^"]+)"', gradle_content)
            if match:
                return match.group(1)
            
            # 查找applicationId
            match = re.search(r'applicationId\s*=\s*"([^"]+)"', gradle_content)
            if match:
                return match.group(1)
        
        # Groovy版本的build.gradle
        build_gradle_groovy = os.path.join(self.project_path, self.app_module, 'build.gradle')
        if os.path.exists(build_gradle_groovy):
            with open(build_gradle_groovy, 'r', encoding='utf-8') as f:
                gradle_content = f.read()
            
            match = re.search(r"applicationId\s+'([^']+)'", gradle_content)
            if match:
                return match.group(1)
            
            match = re.search(r'applicationId\s+"([^"]+)"', gradle_content)
            if match:
                return match.group(1)
        
        # 从AndroidManifest.xml获取
        manifest_path = os.path.join(
            self.project_path,
            self.app_module,
            'src',
            'main',
            'AndroidManifest.xml'
        )
        
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            match = re.search(r'package="([^"]+)"', content)
            if match:
                return match.group(1)
        
        return 'com.example.app'
    
    def _generate_sdk_init_code(self, language: str) -> str:
        """生成SDK初始化代码"""
        appkey = self.config['appkey']
        channel = self.config['channel']
        
        if language == 'Kotlin':
            return f"""
        // 友盟统计SDK初始化
        UMConfigure.setLogEnabled(true)
        UMConfigure.preInit(this, "{appkey}", "{channel}")
        
        Thread {{
            UMConfigure.init(
                this,
                "{appkey}",
                "{channel}",
                UMConfigure.DEVICE_TYPE_PHONE,
                null
            )
        }}.start()"""
        else:
            return f"""
        // 友盟统计SDK初始化
        UMConfigure.setLogEnabled(true);
        UMConfigure.preInit(this, "{appkey}", "{channel}");
        
        new Thread(new Runnable() {{
            @Override
            public void run() {{
                UMConfigure.init(
                    this,
                    "{appkey}",
                    "{channel}",
                    UMConfigure.DEVICE_TYPE_PHONE,
                    null
                );
            }}
        }}).start();"""
    
    def _generate_kotlin_application_class(self, package_name: str) -> str:
        """生成Kotlin Application类"""
        appkey = self.config['appkey']
        channel = self.config['channel']
        
        return f"""package {package_name}

import android.app.Application
import com.umeng.commonsdk.UMConfigure

class UmengApplication : Application() {{
    override fun onCreate() {{
        super.onCreate()
        
        // 友盟统计SDK初始化
        UMConfigure.setLogEnabled(true)
        UMConfigure.preInit(this, "{appkey}", "{channel}")
        
        Thread {{
            UMConfigure.init(
                this,
                "{appkey}",
                "{channel}",
                UMConfigure.DEVICE_TYPE_PHONE,
                null
            )
        }}.start()
    }}
}}
"""
    
    def _generate_java_application_class(self, package_name: str) -> str:
        """生成Java Application类"""
        appkey = self.config['appkey']
        channel = self.config['channel']
        
        return f"""package {package_name};

import android.app.Application;
import com.umeng.commonsdk.UMConfigure;

public class UmengApplication extends Application {{
    @Override
    public void onCreate() {{
        super.onCreate();
        
        // 友盟统计SDK初始化
        UMConfigure.setLogEnabled(true);
        UMConfigure.preInit(this, "{appkey}", "{channel}");
        
        new Thread(new Runnable() {{
            @Override
            public void run() {{
                UMConfigure.init(
                    this,
                    "{appkey}",
                    "{channel}",
                    UMConfigure.DEVICE_TYPE_PHONE,
                    null
                );
            }}
        }}).start();
    }}
}}
"""
    
    def _register_application_class(self, app_class_name: str) -> bool:
        """在AndroidManifest.xml中注册Application类"""
        manifest_path = os.path.join(
            self.project_path,
            self.app_module,
            'src',
            'main',
            'AndroidManifest.xml'
        )
        
        if not os.path.exists(manifest_path):
            print(f"  ❌ AndroidManifest.xml不存在")
            return False
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已注册
        if re.search(r'<application[^>]*\sandroid:name=', content):
            print(f"  ⚠️  Application已注册,跳过")
            return True
        
        # 在<application标签中添加android:name属性
        # 匹配 <application 或 <application\n
        new_content = re.sub(
            r'(<application\s)',
            f'\\1\n        android:name=".{app_class_name}"',
            content,
            count=1
        )
        
        if new_content == content:
            print(f"  ❌ 无法找到<application标签")
            return False
        
        # 写回文件
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  ✅ 已在AndroidManifest.xml中注册.{app_class_name}")
        return True
    
    def _find_class_file(self, class_name: str, language: str) -> str:
        """查找类文件路径"""
        src_main = os.path.join(self.project_path, self.app_module, 'src', 'main')
        
        # 在java和kotlin目录中查找
        search_dirs = []
        java_dir = os.path.join(src_main, 'java')
        kotlin_dir = os.path.join(src_main, 'kotlin')
        
        if os.path.exists(java_dir):
            search_dirs.append(java_dir)
        if os.path.exists(kotlin_dir):
            search_dirs.append(kotlin_dir)
        
        for base_dir in search_dirs:
            for root, dirs, files in os.walk(base_dir):
                for file in files:
                    if language == 'Kotlin' and file == f'{class_name}.kt':
                        return os.path.join(root, file)
                    elif language == 'Java' and file == f'{class_name}.java':
                        return os.path.join(root, file)
        
        return None


def main():
    """主函数 - 用于测试"""
    import sys
    
    if len(sys.argv) < 4:
        print("用法: python sdk_integrator.py <project_path> <app_module> <appkey> <channel>")
        sys.exit(1)
    
    project_path = sys.argv[1]
    app_module = sys.argv[2]
    appkey = sys.argv[3]
    channel = sys.argv[4] if len(sys.argv) > 4 else 'default_channel'
    
    config = {
        'appkey': appkey,
        'channel': channel,
        'using_placeholder': appkey == 'YOUR_UMENG_APPKEY'
    }
    
    integrator = SDKIntegrator(project_path, app_module, config)
    success, message = integrator.integrate()
    
    if success:
        print("✅ SDK集成成功")
        sys.exit(0)
    else:
        print(f"❌ SDK集成失败: {message}")
        sys.exit(1)


if __name__ == '__main__':
    main()
