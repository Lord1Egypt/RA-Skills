#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能管理器核心脚本
功能：注册技能、检查更新、管理配置、更新记录、自动提取技能元数据
"""

import argparse
import json
import os
import re
import zipfile
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests
import yaml
from bs4 import BeautifulSoup
from packaging import version


class SkillRegistry:
    """技能注册管理器"""
    
    # 使用脚本所在目录作为基准路径
    SCRIPT_DIR = Path(__file__).parent
    REGISTRY_FILE = str(SCRIPT_DIR.parent / "skills_registry.json")
    # 配置文件路径：/home/gem/workspace/agent/workspace/MEMORY.md
    # 路径计算：scripts -> skills-update-manager -> skills -> agent -> workspace
    MEMORY_FILE = str(SCRIPT_DIR.parent.parent.parent / "workspace" / "MEMORY.md")
    
    def __init__(self):
        """初始化注册表"""
        self.registry = self._load_registry()
        # 首次加载时自动初始化 MEMORY.md 配置
        self._init_memory_config()
    
    def _load_registry(self) -> Dict:
        """加载注册表"""
        if os.path.exists(self.REGISTRY_FILE):
            try:
                with open(self.REGISTRY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {"skills": [], "next_id": 1}
        return {"skills": [], "next_id": 1}
    
    def _init_memory_config(self):
        """首次加载时自动初始化 MEMORY.md 配置（只追加，不创建文件）"""
        if not os.path.exists(self.MEMORY_FILE):
            # MEMORY.md 不存在，跳过初始化（不创建文件）
            return
        
        try:
            with open(self.MEMORY_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已包含技能管理器配置
            if "技能管理器配置" in content:
                # 配置已存在，跳过
                return
            
            # 配置不存在，追加配置
            self._append_memory_config(content)
            
        except Exception as e:
            print(f"初始化 MEMORY.md 配置失败：{e}")
    
    def _append_memory_config(self, existing_content: str):
        """追加配置到现有 MEMORY.md"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        config_content = f"""
---

## 🧩 技能管理器配置

**注册文件**: `skills/skills-update-manager/skills_registry.json`

### 更新设置
- **启用更新检查**: 否
- **上次检查时间**: {current_time}
- **已注册技能**: {len(self.registry.get("skills", []))} 个

### 使用说明
1. 每次安装技能前优先加载 skills-update-manager
2. 本地技能（source=local）无法自动更新，update_url 为 null
3. 如需启用更新检查，需将技能来源设置为 github 或 clawhub 并提供有效更新地址

### 管理命令
```bash
# 查看已注册技能
python skills/skills-update-manager/scripts/skill_registry.py --action list

# 检查更新（本地技能将跳过）
python skills/skills-update-manager/scripts/skill_registry.py --action check_updates

# 注册新技能
python skills/skills-update-manager/scripts/skill_registry.py --action register --name <技能名> --source local

# 更新配置
python skills/skills-update-manager/scripts/skill_registry.py --action update_config --enable-updates true
```
"""
        
        try:
            with open(self.MEMORY_FILE, 'w', encoding='utf-8') as f:
                f.write(existing_content + config_content)
        except Exception as e:
            print(f"追加 MEMORY.md 配置失败：{e}")
    
    def _save_registry(self):
        """保存注册表"""
        with open(self.REGISTRY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.registry, f, indent=2, ensure_ascii=False)
    
    def extract_skill_metadata(self, skill_path: str) -> Dict:
        """
        从技能文件或目录中提取元数据
        
        Args:
            skill_path: .skill 文件路径或技能目录路径
        
        Returns:
            提取的元数据
        """
        try:
            skill_md_content = None
            
            # 判断是文件还是目录
            if os.path.isfile(skill_path) and skill_path.endswith('.skill'):
                # 解压 .skill 文件
                with zipfile.ZipFile(skill_path, 'r') as zip_ref:
                    # 查找 SKILL.md 文件
                    for file_name in zip_ref.namelist():
                        if file_name.endswith('SKILL.md'):
                            skill_md_content = zip_ref.read(file_name).decode('utf-8')
                            break
                            
            elif os.path.isdir(skill_path):
                # 直接读取目录中的 SKILL.md
                skill_md_path = os.path.join(skill_path, 'SKILL.md')
                if os.path.exists(skill_md_path):
                    with open(skill_md_path, 'r', encoding='utf-8') as f:
                        skill_md_content = f.read()
            
            if not skill_md_content:
                return {
                    "success": False,
                    "message": "未找到 SKILL.md 文件"
                }
            
            # 解析 YAML 前言区
            metadata = self._parse_skill_md(skill_md_content)
            
            return {
                "success": True,
                "metadata": metadata
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"提取元数据失败: {str(e)}"
            }
    
    def _parse_skill_md(self, content: str) -> Dict:
        """
        解析 SKILL.md 文件内容
        
        Args:
            content: SKILL.md 文件内容
        
        Returns:
            提取的元数据
        """
        metadata = {
            "name": None,
            "version": "1.0.0",
            "source": None,
            "update_url": None
        }
        
        # 提取 YAML 前言区
        yaml_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        
        if yaml_match:
            yaml_content = yaml_match.group(1)
            try:
                yaml_data = yaml.safe_load(yaml_content)
                
                if yaml_data:
                    # 提取 name
                    if 'name' in yaml_data:
                        metadata['name'] = yaml_data['name']
                    
                    # 提取 version（如果有）
                    if 'version' in yaml_data:
                        metadata['version'] = yaml_data['version']
                        
            except yaml.YAMLError:
                pass
        
        return metadata
    
    def register_skill(self, name: str, version: str = "1.0.0", 
                      source: str = "github", update_url: str = None) -> Dict:
        """
        注册新技能
        
        Args:
            name: 技能名称（必需）
            version: 版本号（可选，默认 "1.0.0"）
            source: 来源类型（可选，默认 "github"）
            update_url: 更新地址（可选）
        
        Returns:
            注册结果
        """
        # 检查技能是否已存在
        for skill in self.registry["skills"]:
            if skill["name"] == name:
                return {
                    "success": False,
                    "message": f"技能 '{name}' 已存在，请使用 update_record 更新版本"
                }
        
        # 根据来源处理更新地址和更新能力
        source_lower = source.lower()
        if source_lower == "local":
            # 本地技能无法自动更新
            can_update = False
            update_url = None
        elif not update_url:
            # 其他来源如果没有提供更新地址，生成默认 GitHub 地址
            update_url = f"https://github.com/user/{name}"
            can_update = True
        else:
            can_update = True
        
        # 创建新技能记录
        skill_record = {
            "id": self.registry["next_id"],
            "name": name,
            "version": version,
            "source": source_lower,
            "update_url": update_url,
            "can_update": can_update,
            "update_status": "未检查" if can_update else "不适用",
            "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.registry["skills"].append(skill_record)
        self.registry["next_id"] += 1
        self._save_registry()
        
        return {
            "success": True,
            "message": f"技能 '{name}' 注册成功",
            "skill": skill_record
        }
    
    def list_skills(self) -> Dict:
        """列出所有已注册技能"""
        return {
            "success": True,
            "count": len(self.registry["skills"]),
            "skills": self.registry["skills"]
        }
    
    def update_record(self, name: str, new_version: str) -> Dict:
        """
        更新技能记录的版本号
        
        Args:
            name: 技能名称
            new_version: 新版本号
        
        Returns:
            更新结果
        """
        for skill in self.registry["skills"]:
            if skill["name"] == name:
                old_version = skill["version"]
                skill["version"] = new_version
                skill["update_status"] = "已更新"
                skill["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save_registry()
                
                return {
                    "success": True,
                    "message": f"技能 '{name}' 版本已更新：{old_version} -> {new_version}",
                    "skill": skill
                }
        
        return {
            "success": False,
            "message": f"未找到技能 '{name}'"
        }
    
    def check_updates(self) -> Dict:
        """
        检查所有技能的更新
        
        Returns:
            更新检查结果
        """
        # 检查是否启用更新
        config = self._load_memory_config()
        if not config.get("enable_updates", False):
            return {
                "success": True,
                "message": "更新检查已禁用",
                "has_updates": False,
                "updates": []
            }
        
        updates = []
        
        for skill in self.registry["skills"]:
            if not skill["can_update"]:
                continue
            
            try:
                latest_version = self._get_latest_version(skill["source"], skill["update_url"])
                
                if latest_version:
                    # 版本比较
                    if self._compare_versions(skill["version"], latest_version):
                        updates.append({
                            "name": skill["name"],
                            "current_version": skill["version"],
                            "latest_version": latest_version,
                            "source": skill["source"],
                            "update_url": skill["update_url"]
                        })
                        skill["update_status"] = f"有更新 (v{latest_version})"
                    else:
                        skill["update_status"] = "已是最新版本"
                else:
                    skill["update_status"] = "版本检查失败"
                    
            except Exception as e:
                skill["update_status"] = f"检查出错: {str(e)}"
        
        # 更新最后检查时间
        self._update_check_time()
        self._save_registry()
        
        return {
            "success": True,
            "message": f"检查完成，发现 {len(updates)} 个技能有更新",
            "has_updates": len(updates) > 0,
            "updates": updates
        }
    
    def _get_latest_version(self, source: str, url: str) -> Optional[str]:
        """
        获取最新版本号
        
        Args:
            source: 来源类型
            url: 更新地址
        
        Returns:
            最新版本号，失败返回None
        """
        if source == "github":
            return self._get_github_version(url)
        elif source == "clawhub":
            return self._get_clawhub_version(url)
        else:
            return None
    
    def _get_github_version(self, repo_url: str) -> Optional[str]:
        """
        从GitHub获取最新版本号
        
        Args:
            repo_url: GitHub仓库URL（如：https://github.com/owner/repo）
        
        Returns:
            最新版本号
        """
        try:
            # 提取 owner/repo
            match = re.search(r'github\.com/([^/]+)/([^/]+)', repo_url)
            if not match:
                return None
            
            owner, repo = match.groups()
            api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
            
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # 优先使用 tag_name，其次使用 name
                version_str = data.get("tag_name") or data.get("name")
                if version_str:
                    # 清理版本号（去除 v 前缀）
                    return version_str.lstrip('v')
            
            return None
            
        except Exception as e:
            print(f"GitHub版本获取失败: {e}")
            return None
    
    def _get_clawhub_version(self, skill_url: str) -> Optional[str]:
        """
        从ClawHub获取最新版本号
        
        Args:
            skill_url: ClawHub技能页面URL
        
        Returns:
            最新版本号
        """
        try:
            response = requests.get(skill_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找包含 "Current version" 的文本
                # 尝试多种可能的HTML结构
                text = soup.get_text()
                match = re.search(r'Current\s+version[:\s]+([v]?[\d.]+)', text, re.IGNORECASE)
                
                if match:
                    version_str = match.group(1)
                    return version_str.lstrip('v')
                
                return None
            
            return None
            
        except Exception as e:
            print(f"ClawHub版本获取失败: {e}")
            return None
    
    def _compare_versions(self, current: str, latest: str) -> bool:
        """
        比较版本号
        
        Args:
            current: 当前版本
            latest: 最新版本
        
        Returns:
            True表示有更新（latest > current）
        """
        try:
            # 清理版本号
            current_clean = current.lstrip('v')
            latest_clean = latest.lstrip('v')
            
            # 使用 packaging 进行版本比较
            return version.parse(latest_clean) > version.parse(current_clean)
            
        except Exception:
            # 如果版本比较失败，使用字符串比较
            return latest_clean != current_clean
    
    def _load_memory_config(self) -> Dict:
        """加载MEMORY.md配置"""
        if not os.path.exists(self.MEMORY_FILE):
            return {"enable_updates": False}
        
        try:
            with open(self.MEMORY_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析配置
            enable_updates = "是" in content or "true" in content.lower()
            
            return {
                "enable_updates": enable_updates
            }
            
        except Exception:
            return {"enable_updates": False}
    
    def _update_check_time(self):
        """更新最后检查时间"""
        if os.path.exists(self.MEMORY_FILE):
            try:
                with open(self.MEMORY_FILE, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 更新时间
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                content = re.sub(
                    r'上次检查时间[:\s]+[\d\-: ]+',
                    f'上次检查时间：{current_time}',
                    content
                )
                
                with open(self.MEMORY_FILE, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception:
                pass
    
    def update_config(self, enable_updates: bool) -> Dict:
        """
        更新 MEMORY.md 配置（只追加，不覆盖）
        
        Args:
            enable_updates: 是否启用更新检查
        
        Returns:
            更新结果
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        enable_text = "是" if enable_updates else "否"
        
        # 检查文件是否存在
        if not os.path.exists(self.MEMORY_FILE):
            return {
                "success": False,
                "message": f"MEMORY.md 文件不存在：{self.MEMORY_FILE}",
                "hint": "请先创建 MEMORY.md 文件或使用其他方式初始化"
            }
        
        try:
            with open(self.MEMORY_FILE, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            # 检查是否已包含技能管理器配置
            if "技能管理器配置" in file_content:
                # 配置已存在，更新现有配置
                return self._update_existing_config(file_content, enable_updates, current_time)
            else:
                # 配置不存在，追加配置
                return self._append_new_config(file_content, enable_updates, current_time)
            
        except Exception as e:
            return {
                "success": False,
                "message": f"配置更新失败：{str(e)}"
            }
    
    def _update_existing_config(self, content: str, enable_updates: bool, current_time: str) -> Dict:
        """更新现有的技能管理器配置"""
        enable_text = "是" if enable_updates else "否"
        
        # 替换启用更新检查
        content = re.sub(
            r'- 启用更新检查：[是否]',
            f'- 启用更新检查：{enable_text}',
            content
        )
        
        # 替换上次检查时间
        content = re.sub(
            r'- 上次检查时间：[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}',
            f'- 上次检查时间：{current_time}',
            content
        )
        
        with open(self.MEMORY_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "success": True,
            "message": f"配置已更新，更新检查：{enable_text}",
            "config_path": self.MEMORY_FILE
        }
    
    def _append_new_config(self, content: str, enable_updates: bool, current_time: str) -> Dict:
        """追加新的技能管理器配置"""
        enable_text = "是" if enable_updates else "否"
        
        config_content = """
---

# 技能管理器配置

## 更新设置
- 启用更新检查：""" + enable_text + """
- 上次检查时间：""" + current_time + """

## 使用说明
1. 每次安装技能前优先加载 skills-update-manager
2. 更新开启时，启动技能前需加载本管理器检查更新
3. 更新关闭时，跳过更新检查
"""
        
        with open(self.MEMORY_FILE, 'a', encoding='utf-8') as f:
            f.write(config_content)
        
        return {
            "success": True,
            "message": f"配置已追加，更新检查：{enable_text}",
            "config_path": self.MEMORY_FILE
        }




def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="技能管理器")
    parser.add_argument("--action", required=True, 
                       choices=["register", "list", "check_updates", "update_config", 
                               "update_record", "extract"],
                       help="操作类型")
    
    # 注册技能参数
    parser.add_argument("--name", help="技能名称")
    parser.add_argument("--version", default="1.0.0", help="版本号（默认：1.0.0）")
    parser.add_argument("--source", default="github", help="来源类型（默认：github）")
    parser.add_argument("--update-url", help="更新地址")
    
    # 提取元数据参数
    parser.add_argument("--skill-path", help="技能文件或目录路径")
    
    # 更新配置参数
    parser.add_argument("--enable-updates", type=lambda x: x.lower() == 'true',
                       help="是否启用更新检查（true/false）")
    
    args = parser.parse_args()
    
    registry = SkillRegistry()
    
    if args.action == "extract":
        if not args.skill_path:
            print(json.dumps({
                "success": False,
                "message": "需要提供 --skill-path 参数"
            }, ensure_ascii=False, indent=2))
            return
        
        result = registry.extract_skill_metadata(args.skill_path)
        
    elif args.action == "register":
        if not args.name:
            print(json.dumps({
                "success": False,
                "message": "注册技能需要提供技能名称 (--name)"
            }, ensure_ascii=False, indent=2))
            return
        
        result = registry.register_skill(
            args.name, args.version, args.source, args.update_url
        )
        
    elif args.action == "list":
        result = registry.list_skills()
        
    elif args.action == "check_updates":
        result = registry.check_updates()
        
    elif args.action == "update_config":
        if args.enable_updates is None:
            print(json.dumps({
                "success": False,
                "message": "需要提供 --enable-updates 参数（true/false）"
            }, ensure_ascii=False, indent=2))
            return
        
        result = registry.update_config(args.enable_updates)
        
    elif args.action == "update_record":
        if not all([args.name, args.version]):
            print(json.dumps({
                "success": False,
                "message": "更新记录需要提供：--name, --version"
            }, ensure_ascii=False, indent=2))
            return
        
        result = registry.update_record(args.name, args.version)
    
    else:
        result = {"success": False, "message": "未知操作"}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
