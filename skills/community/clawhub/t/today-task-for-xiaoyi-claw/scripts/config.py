#!/usr/bin/env python3
"""
配置管理模块 - 简化版
专为小艺claw skill适配，移除所有OpenClaw全局配置依赖
"""

import os
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class Config:
    """配置管理类 - 仅从本地config.json文件读取"""
    
    def __init__(self, config_path: str = None):
        """初始化配置，仅从本地config.json文件读取"""
        self.config = self._load_local_config(config_path)
        
        # 设置默认值
        self._set_defaults()
        
        logger.debug(f"配置初始化完成")
    
    def _load_local_config(self, config_path: str = None) -> Dict[str, Any]:
        """从本地config.json文件加载配置"""
        config = {}
        
        # 确定配置文件路径
        if config_path and os.path.exists(config_path):
            config_file = config_path
        else:
            # 使用技能目录的config.json
            script_dir = os.path.dirname(os.path.abspath(__file__))
            skill_dir = os.path.dirname(script_dir)
            config_file = os.path.join(skill_dir, 'config.json')
        
        # 加载配置文件
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logger.info(f"从本地配置文件加载配置: {config_file}")
            except json.JSONDecodeError as e:
                logger.error(f"配置文件JSON格式错误: {str(e)}")
                raise ValueError(f"配置文件格式错误: {str(e)}")
            except Exception as e:
                logger.error(f"加载配置文件失败: {str(e)}")
                # 使用空配置，后续会设置默认值
        else:
            logger.info(f"本地配置文件不存在: {config_file}，使用默认配置")
        
        return config
    
    def _set_defaults(self):
        """设置默认配置值"""
        defaults = {
            'timeout': 30,
            'max_content_length': 5000,
            'auto_generate_id': True,
            'default_result': '任务已完成',
            'log_level': 'INFO',
            'save_records': True,
            'records_dir': 'push_records',
            'max_records': 100
        }
        
        # 确保所有默认值都存在
        for key, default_value in defaults.items():
            if key not in self.config:
                self.config[key] = default_value
                logger.debug(f"设置默认值 {key}: {default_value}")
    
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
        """设置配置值（仅内存中）"""
        self.config[key] = value
        logger.debug(f"设置配置 {key}: {value}")
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self.config.copy()
    
    def __str__(self) -> str:
        """字符串表示"""
        return json.dumps(self.config, ensure_ascii=False, indent=2)

# 创建配置说明
def show_config_instructions():
    """显示配置说明"""
    instructions = """
    ============================================================
    今日任务推送器配置说明 - 小艺claw适配版
    ============================================================
    
    [配置说明]：
    本技能无需配置即可使用，所有配置都有合理的默认值
    
    [可选配置] 从本地config.json文件读取：
    
    在技能目录的config.json文件中设置（可选）：
    {
      "timeout": 30,                    // 超时时间（秒）
      "max_content_length": 5000,       // 最大内容长度
      "auto_generate_id": true,         // 是否自动生成任务ID
      "default_result": "任务已完成",   // 默认任务结果
      "log_level": "INFO",              // 日志级别
      "save_records": true,             // 是否保存推送记录
      "records_dir": "push_records",    // 记录目录
      "max_records": 100                // 最大记录数
    }
    
    [重要说明]：
    1. 推送URL已硬编码，无需配置
    2. 云端会自动获取授权码，无需配置
    3. 所有配置都有默认值，不配置也能正常工作
    
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