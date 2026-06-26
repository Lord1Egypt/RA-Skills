#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
支持环境变量和配置文件
"""

import json
import os
from pathlib import Path
from typing import Any, Optional


class Config:
    """配置管理类"""
    
    def __init__(self, config_path: Optional[str] = None, interactive: bool = True):
        """
        初始化配置
        
        Args:
            config_path: 配置文件路径，如果为 None 则自动查找
            interactive: 是否启用交互式配置（首次使用时询问用户）
        """
        self.config_path = config_path
        self._config_data = {}
        self.interactive = interactive
        
        # 如果指定了配置文件路径，直接使用
        if config_path:
            if os.path.exists(config_path):
                self._load_config_file(config_path)
            return
        
        # 自动查找配置文件（按优先级）
        config_paths = self._get_config_paths()
        for path in config_paths:
            if path and os.path.exists(path):
                self._load_config_file(path)
                self.config_path = path
                break
        
        # 检查必需配置，如果缺失且启用交互模式，则进入配置流程
        if interactive and self._needs_configuration():
            self._interactive_setup()
    
    def _get_config_paths(self) -> list:
        """
        获取配置文件查找路径列表（按优先级排序）
        
        Returns:
            list: 配置文件路径列表
        """
        paths = []
        home_dir = os.path.expanduser('~')
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # 1. 环境变量指定的路径（最高优先级）
        env_path = os.getenv('SKILL_IMAGE_GEN_CONFIG')
        if env_path:
            paths.append(env_path)
        
        # 2. 技能安装目录下的配置（优先，方便开发调试）
        paths.append(os.path.join(home_dir, '.openclaw', 'skills', 'skill-image-gen', 'config.json'))
        
        # 3. 独立技能配置目录（不受技能卸载影响，备选）
        paths.append(os.path.join(home_dir, '.openclaw', 'skills', 'config', 'skill-image-gen', 'config.json'))
        
        # 4. 当前工作目录下的配置
        cwd = os.getcwd()
        paths.append(os.path.join(cwd, 'skills', 'skill-image-gen', 'config.json'))
        paths.append(os.path.join(cwd, '.skill-image-gen', 'config.json'))
        
        # 5. 旧版全局配置（向后兼容）
        paths.append(os.path.join(home_dir, '.openclaw', 'skill', 'skill-image-gen', 'config.json'))
        paths.append(os.path.join(home_dir, '.openclaw', 'skill-image-gen', 'config.json'))
        
        # 6. 技能所在目录
        paths.append(os.path.join(script_dir, 'config.json'))
        
        return paths
    
    def _load_config_file(self, config_path: str):
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config_data = json.load(f)
        except Exception as e:
            print(f"警告: 加载配置文件失败: {e}")
            self._config_data = {}
    
    def _needs_configuration(self) -> bool:
        """
        检查是否需要配置
        
        Returns:
            bool: 是否需要配置
        """
        # 检查必需的配置项是否存在
        api_key = self.get('gitee.api_key')
        
        # 如果 API Key 不存在或为空或为占位符，则需要配置
        if not api_key or api_key == 'YOUR_GITEE_AI_API_KEY_HERE' or api_key == 'your_gitee_api_key':
            return True
        
        return False
    
    def _interactive_setup(self):
        """
        交互式配置流程（通过控制台询问用户）
        
        注意：这个方法主要用于命令行工具
        对于 AI Agent 使用，应该通过对话获取参数，而不是控制台输入
        """
        print("\n" + "="*60)
        print("  Free Image Gen - 首次使用配置")
        print("="*60)
        print("\n检测到这是首次使用，需要配置 Gitee AI API Key")
        print("\n获取 API Key 的方法：")
        print("1. 访问 https://ai.gitee.com/")
        print("2. 注册/登录账号")
        print("3. 进入控制台获取 API Key")
        print("\n" + "-"*60)
        
        try:
            # 获取 API Key
            api_key = input("\n请输入你的 Gitee AI API Key: ").strip()
            
            if not api_key:
                print("\n错误: API Key 不能为空！")
                return False
            
            # 简单验证 API Key 格式（Gitee AI 的 API Key 通常较长）
            if len(api_key) < 20:
                print("\n警告: API Key 格式可能不正确，请检查")
                confirm = input("是否继续保存？(y/n): ").strip().lower()
                if confirm != 'y':
                    return False
            
            # 更新配置
            self._config_data = {
                'gitee': {
                    'api_key': api_key,
                    'model': 'Kolors',
                    'base_url': 'https://ai.gitee.com/v1'
                },
                'cos': {
                    'enabled': False,
                    'secret_id': '',
                    'secret_key': '',
                    'region': 'ap-guangzhou',
                    'bucket': ''
                },
                'output': {
                    'path': './output',
                    'format': 'png'
                }
            }
            
            # 询问是否配置 COS（可选）
            print("\n是否配置腾讯云 COS（用于图片云存储）？")
            use_cos = input("配置 COS？(y/n，默认 n): ").strip().lower()
            
            if use_cos == 'y':
                self._config_data['cos']['enabled'] = True
                self._config_data['cos']['secret_id'] = input("请输入 COS Secret ID: ").strip()
                self._config_data['cos']['secret_key'] = input("请输入 COS Secret Key: ").strip()
                self._config_data['cos']['bucket'] = input("请输入 COS Bucket 名称: ").strip()
            
            # 保存配置文件
            save_path = self._save_config()
            
            if save_path:
                print("\n" + "="*60)
                print("  ✅ 配置成功！")
                print("="*60)
                print(f"\n配置文件已保存到: {save_path}")
                print("\n现在你可以开始生成图片了！")
                print("\n示例命令:")
                print('  python scripts/main.py --prompt "一只可爱的小狗"')
                print("\n" + "="*60)
                return True
            else:
                print("\n❌ 配置保存失败")
                return False
                
        except KeyboardInterrupt:
            print("\n\n配置已取消")
            return False
        except Exception as e:
            print(f"\n配置过程出错: {e}")
            return False
    
    def _save_config(self) -> Optional[str]:
        """
        保存配置文件
        
        Returns:
            str: 配置文件保存路径，失败返回 None
        """
        try:
            # 确定保存路径（使用独立的技能配置目录，不受技能卸载影响）
            home_dir = os.path.expanduser('~')
            save_dir = os.path.join(home_dir, '.openclaw', 'skills', 'config', 'skill-image-gen')
            save_path = os.path.join(save_dir, 'config.json')
            
            # 创建目录
            os.makedirs(save_dir, exist_ok=True)
            
            # 保存配置
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(self._config_data, f, indent=2, ensure_ascii=False)
            
            self.config_path = save_path
            return save_path
            
        except Exception as e:
            print(f"保存配置失败: {e}")
            return None
    
    def update_config(self, key: str, value: Any, save: bool = True) -> bool:
        """
        更新配置项
        
        Args:
            key: 配置键（支持点号分隔，如 'gitee.api_key'）
            value: 配置值
            save: 是否立即保存到文件
        
        Returns:
            bool: 是否更新成功
        """
        try:
            # 解析键路径
            keys = key.split('.')
            
            # 更新配置数据
            current = self._config_data
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]
            
            current[keys[-1]] = value
            
            # 保存到文件
            if save and self.config_path:
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(self._config_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"更新配置失败: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        优先级: 环境变量 > 配置文件 > 默认值
        
        Args:
            key: 配置键，支持点号分隔的嵌套键 (如 'gitee.api_key')
            default: 默认值
        
        Returns:
            配置值
        """
        # 转换为环境变量格式
        env_key = key.upper().replace('.', '_')
        
        # 优先从环境变量获取
        env_value = os.environ.get(env_key)
        if env_value is not None:
            return env_value
        
        # 从配置文件获取
        keys = key.split('.')
        value = self._config_data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value if value is not None else default
    
    def get_cos_config(self) -> Optional[dict]:
        """获取 COS 配置"""
        if not self.get('cos.enabled', False):
            return None
        
        return {
            'secret_id': self.get('cos.secret_id'),
            'secret_key': self.get('cos.secret_key'),
            'region': self.get('cos.region', 'ap-guangzhou'),
            'bucket': self.get('cos.bucket')
        }
    
    def get_gitee_config(self) -> dict:
        """获取 Gitee 配置"""
        return {
            'api_key': self.get('gitee.api_key'),
            'model': self.get('gitee.model', 'Kolors'),
            'base_url': self.get('gitee.base_url', 'https://ai.gitee.com/v1')
        }


# 默认配置实例
_default_config = None


def get_config(config_path: Optional[str] = None) -> Config:
    """获取配置实例"""
    global _default_config
    if _default_config is None:
        _default_config = Config(config_path)
    return _default_config
