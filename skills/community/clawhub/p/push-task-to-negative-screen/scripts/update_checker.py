#!/usr/bin/env python3
"""
技能更新检查器
使用clawhub inspect命令获取真实版本信息
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

class SkillUpdateChecker:
    """技能更新检查器"""
    
    def __init__(self, skill_dir=None):
        if skill_dir is None:
            skill_dir = Path(__file__).parent.parent
        
        self.skill_dir = Path(skill_dir)
        self.version_file = self.skill_dir / "version.json"
        self.config_file = self.skill_dir / "update_config.json"
        
        # 加载配置
        self.config = self._load_config()
        self.local_version = self._load_local_version()
        
        # 更新状态
        self.update_available = False
        self.remote_version = None
        self.update_info = {}
    
    def _load_config(self):
        """加载配置"""
        default_config = {
            "enabled": True,
            "check_on_startup": True,
            "check_interval_hours": 24,
            "show_notification": True,
            "last_check_time": None
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return default_config
        return default_config
    
    def _load_local_version(self):
        """从version.json加载本地版本"""
        if self.version_file.exists():
            try:
                with open(self.version_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("current_version", "0.0.0")
            except:
                return "0.0.0"
        return "0.0.0"
    
    def should_check_update(self):
        """判断是否应该检查更新"""
        if not self.config["enabled"]:
            return False
        
        last_check = self.config["last_check_time"]
        if last_check is None:
            return True
        
        try:
            last_time = datetime.fromisoformat(last_check)
            interval = timedelta(hours=self.config["check_interval_hours"])
            return datetime.now() - last_time > interval
        except:
            return True
    
    def check_for_updates(self, force=False):
        """检查更新"""
        if not force and not self.should_check_update():
            return None  # 返回None表示不需要检查
        
        print(f"[检查] 检查技能更新...")
        print(f"[信息] 本地版本: {self.local_version}")
        
        # 更新检查时间
        self.config["last_check_time"] = datetime.now().isoformat()
        self._save_config()
        
        # 获取远程版本
        remote_info = self._get_clawhub_version()
        
        if remote_info is None:
            print("[信息] 无法从ClawHub获取版本信息")
            return None  # 返回None表示检查异常
        
        remote_version = remote_info.get("version")
        print(f"[信息] 远程版本: {remote_version}")
        
        if self._compare_versions(remote_version, self.local_version) > 0:
            self.update_available = True
            self.remote_version = remote_version
            self.update_info = remote_info
            return True  # 有更新可用
        else:
            # 不输出"已是最新版本"的信息
            return False  # 已是最新版本
    
    def _get_clawhub_version(self):
        """从ClawHub获取版本信息"""
        import threading
        
        def run_command():
            """在子线程中运行命令"""
            nonlocal result
            try:
                result[0] = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='ignore'
                )
            except Exception as e:
                result[0] = e
        
        try:
            print("[信息] 从ClawHub检查更新...")
            
            # 使用clawhub inspect命令
            cmd = ["powershell", "-Command", "clawhub inspect today-task --json"]
            
            # 使用线程和超时机制
            result = [None]
            thread = threading.Thread(target=run_command)
            thread.daemon = True
            thread.start()
            thread.join(timeout=10)  # 10秒超时
            
            if thread.is_alive():
                print("[信息] ClawHub检查超时")
                return None
            
            if isinstance(result[0], Exception):
                print(f"[信息] ClawHub检查异常: {result[0]}")
                return None
            
            process_result = result[0]
            if process_result is None:
                print("[信息] 未获取到ClawHub响应")
                return None
            
            if process_result.returncode != 0:
                # 检查是否是速率限制
                stderr = process_result.stderr or ""
                if "Rate limit exceeded" in stderr:
                    print("[信息] ClawHub速率限制")
                else:
                    print(f"[信息] ClawHub命令失败")
                return None
            
            output = process_result.stdout
            
            # 解析JSON
            start = output.find('{')
            end = output.rfind('}') + 1
            
            if start < 0 or end <= start:
                print("[信息] 未找到ClawHub数据")
                return None
            
            json_str = output[start:end]
            
            try:
                data = json.loads(json_str)
                
                # 提取版本信息
                version = None
                changelog = ""
                
                # 从skill.tags.latest获取
                if "skill" in data and "tags" in data["skill"]:
                    version = data["skill"]["tags"].get("latest")
                
                # 从latestVersion获取
                if not version and "latestVersion" in data:
                    version = data["latestVersion"].get("version")
                    changelog = data["latestVersion"].get("changelog", "")
                
                if version:
                    print(f"[信息] ClawHub版本: {version}")
                    return {
                        "version": version,
                        "changelog": changelog,
                        "source": "clawhub"
                    }
                else:
                    print("[信息] 未找到版本信息")
                    return None
                    
            except json.JSONDecodeError:
                print("[信息] ClawHub数据解析失败")
                return None
                
        except Exception as e:
            print(f"[信息] ClawHub检查异常: {e}")
            return None
    
    def _compare_versions(self, v1, v2):
        """比较版本号"""
        def parse_version(v):
            parts = v.split('.')
            result = []
            for part in parts[:3]:
                try:
                    result.append(int(part))
                except:
                    result.append(0)
            while len(result) < 3:
                result.append(0)
            return result
        
        v1_parts = parse_version(v1)
        v2_parts = parse_version(v2)
        
        return (v1_parts > v2_parts) - (v1_parts < v2_parts)
    
    def show_update_notification(self):
        """显示更新通知"""
        if not self.update_available or not self.config["show_notification"]:
            return False
        
        # 只有在有更新时才显示通知
        source = self.update_info.get("source", "unknown")
        
        print(f"\n[更新检查] 技能更新检查完成")
        print(f"当前版本: {self.local_version}")
        print(f"最新版本: {self.remote_version}")
        
        changelog = self.update_info.get("changelog", "")
        if changelog:
            print("更新内容:")
            if isinstance(changelog, list):
                for item in changelog[:3]:  # 只显示前3条
                    print(f"  • {item}")
            else:
                lines = changelog.strip().split('\n')
                for line in lines[:3]:  # 只显示前3行
                    if line.strip():
                        print(f"  • {line.strip()}")
        
        print(f"[更新命令] clawhub update today-task")
        
        return True
    
    def _save_config(self):
        """保存配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except:
            pass

def check_update():
    """检查更新"""
    checker = SkillUpdateChecker()
    
    # 首先检查是否应该检查更新
    if not checker.should_check_update():
        return None  # 返回None表示不需要检查，也不提示用户
    
    # 执行更新检查
    update_available = checker.check_for_updates(force=False)
    
    if update_available:
        checker.show_update_notification()
        return True  # 有更新可用
    elif update_available is False:
        # 检查了但版本是最新的，不提示用户
        return False  # 已是最新版本，不提示
    else:
        # update_available为None表示检查异常
        print("[信息] 更新检查异常，请稍后重试")
        return None  # 检查异常

if __name__ == "__main__":
    check_update()