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
        """混合加载配置：auth_code和hiboard_url从OpenClaw全局配置读取，其他从本地文件读取"""
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
            
            # 首先从OpenClaw全局配置读取auth_code和hiboard_url
            openclaw_auth_code = self._get_from_openclaw_global('authCode')
            openclaw_push_url = self._get_from_openclaw_global('pushServiceUrl')
            
            # 优先使用OpenClaw全局配置中的值
            if openclaw_auth_code and openclaw_auth_code != 'NOT_SET_IN_OPENCLAW':
                config['auth_code'] = openclaw_auth_code
                logger.info("使用OpenClaw全局配置中的auth_code")
            else:
                # 如果OpenClaw全局配置中没有，检查本地文件
                if 'auth_code' in config:
                    logger.warning("auth_code从本地文件读取（建议使用OpenClaw全局配置）")
                else:
                    config['auth_code'] = 'NOT_SET'
                    logger.warning("auth_code未设置")
                
            if openclaw_push_url and openclaw_push_url != 'NOT_SET_IN_OPENCLAW':
                config['hiboard_url'] = openclaw_push_url
                logger.info("使用OpenClaw全局配置中的hiboard_url")
            else:
                # 如果OpenClaw全局配置中没有，检查本地文件中的pushServiceUrl
                local_push_url = config.get('pushServiceUrl')
                if local_push_url:
                    config['hiboard_url'] = local_push_url
                    logger.info("使用本地config.json中的pushServiceUrl配置")
                else:
                    config['hiboard_url'] = 'NOT_SET'
                    logger.warning("hiboard_url未设置")
            
            # 从本地文件读取的配置中移除auth_code和hiboard_url，避免混淆
            config.pop('auth_code', None)
            config.pop('hiboard_url', None)
            # 重新添加从OpenClaw全局配置读取的值
            config['auth_code'] = openclaw_auth_code if openclaw_auth_code != 'NOT_SET_IN_OPENCLAW' else 'NOT_SET'
            config['hiboard_url'] = openclaw_push_url if openclaw_push_url != 'NOT_SET_IN_OPENCLAW' else config.get('pushServiceUrl', 'NOT_SET')
            
        except json.JSONDecodeError as e:
            logger.error(f"配置文件JSON格式错误: {str(e)}")
            raise ValueError(f"配置文件格式错误: {str(e)}")
        except Exception as e:
            logger.error(f"加载配置文件失败: {str(e)}")
            # 使用默认配置，但必需字段会验证失败
            config = {
                'auth_code': 'NOT_SET',
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
        required_fields = ['auth_code', 'hiboard_url']
        missing_fields = []
        
        for field in required_fields:
            value = self.config.get(field)
            if not value or value == 'NOT_SET' or value == 'NOT_SET_IN_OPENCLAW_CONFIG':
                missing_fields.append(field)
        
        if missing_fields:
            error_msg = f"配置中缺少必需字段: {', '.join(missing_fields)}\n"
            error_msg += "请使用以下方式设置配置:\n"
            error_msg += "1. auth_code (授权码): 使用OpenClaw全局配置命令设置\n"
            error_msg += "   命令: openclaw config set skills.entries.today-task.config.authCode YOUR_AUTH_CODE\n"
            error_msg += "2. hiboards_url (推送URL): 使用OpenClaw全局配置命令设置\n"
            error_msg += "   命令: openclaw config set skills.entries.today-task.config.pushServiceUrl YOUR_PUSH_URL\n"
            error_msg += "\n其他配置项请在技能目录的config.json文件中设置。"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # 验证授权码格式
        auth_code = self.config.get('auth_code', '')
        if not isinstance(auth_code, str) or len(auth_code) < 10:
            logger.warning(f"授权码格式可能不正确: {auth_code[:4]}***")
        
        # 验证URL格式
        hiboards_url = self.config.get('hiboard_url', '')
        if not hiboards_url.startswith('http'):
            logger.warning(f"推送URL格式可能不正确: {hiboards_url}")
        
        logger.info("必需配置验证通过")
    
    @property
    def auth_code(self) -> str:
        """获取授权码（必需）"""
        return self.config['auth_code']
    
    @property
    def hiboards_url(self) -> str:
        """获取Hiboards URL（必需）"""
        return self.config['hiboard_url']
    
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
        # 隐藏敏感信息
        if 'auth_code' in safe_config and safe_config['auth_code']:
            safe_config['auth_code'] = safe_config['auth_code'][:4] + '***'
        
        return json.dumps(safe_config, ensure_ascii=False, indent=2)

# 创建配置说明
def show_config_instructions():
    """显示配置说明"""
    instructions = """
    ============================================================
    今日任务推送器配置说明（混合配置系统）
    ============================================================
    
    本技能使用混合配置系统：
    
    [必需配置] 从OpenClaw全局配置读取：
    
    1. 设置授权码:
       openclaw config set skills.entries.today-task.config.authCode YOUR_AUTH_CODE
    
    2. 设置推送URL:
       openclaw config set skills.entries.today-task.config.pushServiceUrl YOUR_PUSH_URL
    
    3. 查看技能配置:
       openclaw config get skills.entries.today-task
    
    4. 删除配置:
       openclaw config unset skills.entries.today-task.config.authCode
       openclaw config unset skills.entries.today-task.config.pushServiceUrl
    
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
    
    [获取授权码步骤]：
    1. 从手机桌面右滑进入负一屏
    2. 点击左上角头像
    3. 进入"我的"页面，点击右上角设置图标
    4. 选择"动态管理"
    5. 点击"关联账号"
    6. 找到"Claw智能体"并点击获取授权码
    
    [推送URL示例]：
    https://hiboard-claw-drcn.ai.dbankcloud.cn/distribution/message/cloud/claw/msg/upload
    
    ============================================================
    """
    print(instructions)

# 测试代码
if __name__ == "__main__":
    print("测试OpenClaw配置管理...")
    
    try:
        # 测试配置加载
        config = Config()
        print("配置加载成功:")
        print(config)
        
        # 测试必需字段
        print(f"\n授权码: {config.auth_code[:4]}***")
        print(f"推送URL: {config.hiboards_url}")
        
        # 显示配置说明
        show_config_instructions()
        
    except ValueError as e:
        print(f"配置错误: {str(e)}")
        show_config_instructions()