#!/usr/bin/env python3
"""
配置管理模块 - 从OpenClaw配置系统读取

"""

import os
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class Config:
    """配置管理类 - 从OpenClaw配置系统读取"""
    
    def __init__(self, config_path: str = None):
        """初始化配置，从OpenClaw配置系统读取"""
        # config_path参数保留但不使用，用于兼容性
        self.config = self._load_from_openclaw_config()
        
        # 验证必需配置
        self._validate_required_config()
        
        logger.debug(f"配置初始化完成: {self}")
    
    def _load_from_openclaw_config(self) -> Dict[str, Any]:
        """混合加载配置：hiboard_url从OpenClaw全局配置读取，其他从本地文件读取"""
        config = {}
        
        try:
            # 首先从技能目录的config.json文件读取基础配置
            script_dir = os.path.dirname(os.path.abspath(__file__))
            skill_dir = os.path.dirname(script_dir)
            config_file = os.path.join(skill_dir, 'config.json')
            
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logger.info(f"从本地配置文件加载基础配置: {config_file}")
            else:
                logger.warning(f"本地配置文件不存在: {config_file}")
                # 使用默认配置
                config = {
                    'timeout': 30,
                    'max_content_length': 5000,
                    'auto_generate_id': True,
                    'default_result': '任务已完成',
                    'log_level': 'INFO',
                    'save_records': True,
                    'records_dir': 'push_records',
                    'max_records': 100
                }
            
            # 注意：推送URL已硬编码在hiboards_client.py中，不再支持配置
            # 移除所有推送URL配置逻辑
            logger.info("推送URL已硬编码，不再支持配置")
            
        except json.JSONDecodeError as e:
            logger.error(f"配置文件JSON格式错误: {str(e)}")
            raise ValueError(f"配置文件格式错误: {str(e)}")
        except Exception as e:
            logger.error(f"加载配置文件失败: {str(e)}")
            # 使用默认配置，但必需字段会验证失败
            config = {
                'hiboard_url': 'NOT_SET',
                'timeout': 30,
                'max_content_length': 5000,
                'auto_generate_id': True,
                'default_result': '任务已完成',
                'log_level': 'INFO',
                'save_records': True,
                'records_dir': 'push_records',
                'max_records': 100
            }
        
        return config
    
    def _get_from_openclaw_global(self, key: str) -> str:
        """从OpenClaw全局配置获取值"""
        try:
            # 读取OpenClaw全局配置文件
            openclaw_config_path = os.path.join(os.path.expanduser("~"), ".openclaw", "openclaw.json")
            
            if os.path.exists(openclaw_config_path):
                with open(openclaw_config_path, 'r', encoding='utf-8') as f:
                    openclaw_config = json.load(f)
                
                # 获取技能配置
                skill_config = openclaw_config.get('skills', {}).get('entries', {}).get('today-task', {})
                
                # 获取config中的值
                config_value = skill_config.get('config', {}).get(key)
                
                if config_value:
                    logger.debug(f"从OpenClaw全局配置读取 {key}: {config_value[:4]}***" if key == 'authCode' else f"从OpenClaw全局配置读取 {key}: {config_value}")
                    return config_value
                else:
                    logger.debug(f"OpenClaw全局配置中未找到 {key}")
                    return 'NOT_SET_IN_OPENCLAW'
            else:
                logger.warning(f"OpenClaw配置文件不存在: {openclaw_config_path}")
                return 'NOT_SET_IN_OPENCLAW'
                
        except Exception as e:
            logger.error(f"读取OpenClaw全局配置失败: {str(e)}")
            return 'NOT_SET_IN_OPENCLAW'
    
    def _validate_required_config(self):
        """验证必需配置"""
        # 注意：推送URL已硬编码，不再需要验证
        # 云端会自动获取授权码，不再需要验证授权码
        logger.info("配置验证通过（推送URL已硬编码）")
    
    @property
    def hiboards_url(self) -> str:
        """获取Hiboards URL（已硬编码，返回空字符串）"""
        # 注意：推送URL已硬编码在hiboards_client.py中
        return ""
    
    @property
    def timeout(self) -> int:
        """获取超时时间"""
        return self.config.get('timeout', 30)
    
    @property
    def max_content_length(self) -> int:
        """获取最大内容长度"""
        return self.config.get('max_content_length', 5000)
    
    @property
    def auto_generate_id(self) -> bool:
        """是否自动生成ID"""
        return self.config.get('auto_generate_id', True)
    
    @property
    def default_result(self) -> str:
        """获取默认结果"""
        return self.config.get('default_result', '任务已完成')
    
    @property
    def log_level(self) -> str:
        """获取日志级别"""
        return self.config.get('log_level', 'INFO')
    
    @property
    def save_records(self) -> bool:
        """是否保存记录"""
        return self.config.get('save_records', True)
    
    @property
    def records_dir(self) -> str:
        """获取记录目录"""
        return self.config.get('records_dir', 'push_records')
    
    @property
    def max_records(self) -> int:
        """获取最大记录数"""
        return self.config.get('max_records', 100)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置配置值（仅内存中，不会持久化到OpenClaw配置）"""
        self.config[key] = value
        logger.debug(f"设置配置 {key}: {value}")
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self.config.copy()
    
    def __str__(self) -> str:
        """字符串表示"""
        safe_config = self.config.copy()
        # 注意：auth_code已移除，云端会自动获取授权码
        # 注意：推送URL已硬编码，不再显示在配置中
        
        return json.dumps(safe_config, ensure_ascii=False, indent=2)

# 创建配置说明
def show_config_instructions():
    """显示配置说明"""
    instructions = """
    ============================================================
    今日任务推送器配置说明
    ============================================================
    
    [配置说明]：
    本技能无需配置即可使用
    
    [可选配置] 从本地config.json文件读取：
    
    在技能目录的config.json文件中设置：
    {
      "timeout": 30,
      "max_content_length": 5000,
      "auto_generate_id": true,
      "default_result": "任务已完成",
      "log_level": "INFO",
      "save_records": true,
      "records_dir": "push_records",
      "max_records": 100
    }
    
    ============================================================
    """
    print(instructions)

# 测试代码
if __name__ == "__main__":
    print("测试配置管理...")
    
    try:
        # 测试配置加载
        config = Config()
        print("配置加载成功:")
        print(config)
        
        # 显示配置说明
        show_config_instructions()
        
    except ValueError as e:
        print(f"配置错误: {str(e)}")
        show_config_instructions()