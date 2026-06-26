"""
配置管理模块
"""
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# 基础路径
WORKSPACE_DIR = Path.home() / ".openclaw" / "workspace"
SKILL_DATA_DIR = WORKSPACE_DIR / "smart-email-data"
MAIL_ARCHIVES_DIR = SKILL_DATA_DIR / "mail-archives"
TMP_DIR = SKILL_DATA_DIR / "tmp"
OUTBOX_DIR = SKILL_DATA_DIR / "outbox"
LOGS_DIR = SKILL_DATA_DIR / "logs"
DATA_DIR = SKILL_DATA_DIR / "data"

# 测试模式路径（/tmp/smart-email-data/）
TEST_DATA_DIR = Path("/tmp/smart-email-data")
TEST_MAIL_ARCHIVES_DIR = TEST_DATA_DIR / "mail-archives"
TEST_OUTBOX_DIR = TEST_DATA_DIR / "outbox"
TEST_LOGS_DIR = TEST_DATA_DIR / "logs"
TEST_DATA_SUBDIR = TEST_DATA_DIR / "data"

# 配置文件路径
CONFIG_FILE = DATA_DIR / "config.json"
DB_FILE = DATA_DIR / "mail_tracker.db"

# Outbox 路径
OUTBOX_PENDING_DIR = OUTBOX_DIR / "pending"
OUTBOX_SENT_DIR = OUTBOX_DIR / "sent"

# 默认配置
DEFAULT_CONFIG = {
    "check_interval_minutes": 30,
    "digest_times": ["11:00", "17:00"],
    "timezone": "Asia/Shanghai",
    "paths": {
        "skill_data": str(SKILL_DATA_DIR),
        "mail_archives": str(MAIL_ARCHIVES_DIR),
        "tmp": str(TMP_DIR),
        "outbox": str(OUTBOX_DIR),
        "outbox_pending": str(OUTBOX_PENDING_DIR),
        "outbox_sent": str(OUTBOX_SENT_DIR),
        "data": str(DATA_DIR),
        "logs": str(LOGS_DIR)
    },
    "ai": {
        "model": "gpt-4o-mini",
        # OpenAI 配置
        "openai_api_key_env": "SMART_EMAIL_OPENAI_API_KEY",
        "openai_base_url_env": "SMART_EMAIL_OPENAI_API_URL",
        "openai_model_env": "SMART_EMAIL_OPENAI_MODEL",
        # Anthropic 配置
        "anthropic_api_key_env": "SMART_EMAIL_ANTHROPIC_API_KEY",
        "anthropic_base_url_env": "SMART_EMAIL_ANTHROPIC_API_URL",
        "anthropic_model_env": "SMART_EMAIL_ANTHROPIC_MODEL",
        # 通用配置
        "max_concurrent": 5,
        "analyze_limit": 20,
        "multimodal_analysis": False,
        "multimodal_env": "SMART_EMAIL_MULTIMODAL_ANALYSIS",
        "retry_count": 3,
        "retry_count_env": "SMART_EMAIL_LLM_RETRY_COUNT",
        "retry_base_delay": 1.0,
        "retry_base_delay_env": "SMART_EMAIL_LLM_RETRY_BASE_DELAY",
        "llm_provider_env": "SMART_EMAIL_LLM_PROVIDER",
        "subagent_concurrency_env": "SMART_EMAIL_SUBAGENT_CONCURRENCY",
        "subagent_timeout_env": "SMART_EMAIL_SUBAGENT_TIMEOUT",
        "subagent_timeout_default": 120
    },
    "download": {
        "limit": 50,
        "limit_env": "SMART_EMAIL_DOWNLOAD_LIMIT"
    },
    "cron": {
        "check_interval_minutes": 30,
        "check_interval_env": "SMART_EMAIL_CHECK_INTERVAL",
        "digest_times": ["11:00", "17:00"],
        "digest_times_env": "SMART_EMAIL_DIGEST_TIMES"
    },
    "urgent_headers": ["Priority: high", "X-Priority: 1", "Importance: high"],
    "db_path": str(DB_FILE),
    "test_mode": False
}

# 邮箱配置模板
EMAIL_PROVIDERS = {
    "qq": {
        "server": "imap.qq.com",
        "port": 993,
        "use_ssl": True,
        "email_env": "SMART_EMAIL_QQ_EMAIL",
        "password_env": "SMART_EMAIL_QQ_AUTH_CODE"
    },
    "126": {
        "server": "imap.126.com",
        "port": 993,
        "use_ssl": True,
        "email_env": "SMART_EMAIL_126_EMAIL",
        "password_env": "SMART_EMAIL_126_AUTH_CODE"
    },
    "163": {
        "server": "imap.163.com",
        "port": 993,
        "use_ssl": True,
        "email_env": "SMART_EMAIL_163_EMAIL",
        "password_env": "SMART_EMAIL_163_AUTH_CODE"
    },
    "outlook": {
        "server": "outlook.office365.com",
        "port": 993,
        "use_ssl": True,
        "email_env": "SMART_EMAIL_OUTLOOK_EMAIL",
        "password_env": "SMART_EMAIL_OUTLOOK_APP_PASSWORD"
    }
}


class Config:
    """配置管理类"""
    
    def __init__(self):
        self._config = None
        self._load_env()
        self._load_config()
    
    def _load_env(self):
        """加载环境变量"""
        # 尝试从多个位置加载 .env
        env_paths = [
            Path.home() / ".openclaw" / ".env",
            Path.cwd() / ".env",
            WORKSPACE_DIR / ".env"
        ]
        for env_path in env_paths:
            if env_path.exists():
                load_dotenv(env_path, override=True)
                break
    
    def _load_config(self):
        """加载配置文件"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        else:
            self._config = DEFAULT_CONFIG.copy()
            self._save_config()
    
    def _save_config(self):
        """保存配置文件"""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, indent=2, ensure_ascii=False)
    
    def get(self, key, default=None):
        """获取配置项"""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key, value):
        """设置配置项"""
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self._save_config()
    
    def get_env(self, key, default=None):
        """获取环境变量"""
        return os.getenv(key, default)
    
    def get_ai_config(self):
        """获取 AI 配置"""
        # OpenAI 配置
        openai_api_key_env = self.get("ai.openai_api_key_env", "SMART_EMAIL_OPENAI_API_KEY")
        openai_api_key = self.get_env(openai_api_key_env)
        
        openai_base_url_env = self.get("ai.openai_base_url_env", "SMART_EMAIL_OPENAI_API_URL")
        openai_base_url = self.get_env(openai_base_url_env)
        
        openai_model_env = self.get("ai.openai_model_env", "SMART_EMAIL_OPENAI_MODEL")
        openai_model = self.get_env(openai_model_env)
        
        # 读取并发限制，默认为 5
        max_concurrent_str = self.get_env("SMART_EMAIL_MAX_CONCURRENT")
        try:
            max_concurrent = int(max_concurrent_str) if max_concurrent_str else self.get("ai.max_concurrent", 5)
        except ValueError:
            max_concurrent = 5
        
        # 读取 AI 分析限制，默认为 20
        analyze_limit_str = self.get_env("SMART_EMAIL_ANALYZE_LIMIT")
        try:
            analyze_limit = int(analyze_limit_str) if analyze_limit_str else self.get("ai.analyze_limit", 20)
        except ValueError:
            analyze_limit = 20
        
        # 读取多模态分析开关，默认为 False
        multimodal_env = self.get("ai.multimodal_env", "SMART_EMAIL_MULTIMODAL_ANALYSIS")
        multimodal_str = self.get_env(multimodal_env)
        if multimodal_str is None:
            multimodal_analysis = self.get("ai.multimodal_analysis", False)
        else:
            multimodal_analysis = multimodal_str.lower() in ('true', '1', 'yes', 'on')
        
        # 读取 LLM 重试配置
        retry_count_str = self.get_env(self.get("ai.retry_count_env", "SMART_EMAIL_LLM_RETRY_COUNT"))
        try:
            retry_count = int(retry_count_str) if retry_count_str else self.get("ai.retry_count", 3)
        except ValueError:
            retry_count = 3
        
        retry_base_delay_str = self.get_env(self.get("ai.retry_base_delay_env", "SMART_EMAIL_LLM_RETRY_BASE_DELAY"))
        try:
            retry_base_delay = float(retry_base_delay_str) if retry_base_delay_str else self.get("ai.retry_base_delay", 1.0)
        except ValueError:
            retry_base_delay = 1.0
        
        return {
            "model": openai_model,
            "api_key": openai_api_key,
            "base_url": openai_base_url,
            "max_concurrent": max_concurrent,
            "analyze_limit": analyze_limit,
            "multimodal_analysis": multimodal_analysis,
            "retry_count": retry_count,
            "retry_base_delay": retry_base_delay
        }
    
    def get_download_limit(self) -> int:
        """获取下载限制"""
        limit_str = self.get_env("SMART_EMAIL_DOWNLOAD_LIMIT")
        try:
            return int(limit_str) if limit_str else self.get("download.limit", 50)
        except ValueError:
            return 50
    
    def get_cron_config(self) -> dict:
        """获取 cron 配置"""
        # 检查间隔（分钟）
        interval_str = self.get_env("SMART_EMAIL_CHECK_INTERVAL")
        try:
            check_interval = int(interval_str) if interval_str else self.get("cron.check_interval_minutes", 30)
        except ValueError:
            check_interval = 30
        
        # 汇总时间（逗号分隔）
        times_str = self.get_env("SMART_EMAIL_DIGEST_TIMES")
        if times_str:
            digest_times = [t.strip() for t in times_str.split(",")]
        else:
            digest_times = self.get("cron.digest_times", ["11:00", "17:00"])
        
        return {
            "check_interval_minutes": check_interval,
            "digest_times": digest_times
        }
    
    def get_email_accounts(self):
        """获取配置的邮箱账号列表"""
        accounts = []
        for provider, config in EMAIL_PROVIDERS.items():
            email = self.get_env(config["email_env"])
            password = self.get_env(config["password_env"])
            if email and password:
                accounts.append({
                    "provider": provider,
                    "email": email,
                    "password": password,
                    "server": config["server"],
                    "port": config["port"],
                    "use_ssl": config["use_ssl"]
                })
        return accounts
    
    def get_db_path(self):
        """获取数据库路径"""
        return self.get("db_path", str(DB_FILE))
    
    def get_storage_path(self, test_mode=False):
        """获取邮件存储路径"""
        if test_mode:
            return TEST_MAIL_ARCHIVES_DIR
        return Path(self.get("paths.mail_archives", str(MAIL_ARCHIVES_DIR)))
    
    def get_test_db_path(self):
        """获取测试模式数据库路径"""
        return TEST_DATA_SUBDIR / "mail_tracker.db"
    
    def get_test_logs_path(self):
        """获取测试模式日志路径"""
        return TEST_LOGS_DIR
    
    def get_outbox_path(self, test_mode=False):
        """获取 Outbox 路径"""
        if test_mode:
            return SKILL_DATA_DIR / "tmp" / "outbox"
        return Path(self.get("paths.outbox", str(OUTBOX_DIR)))
    
    def get_logs_path(self):
        """获取日志路径"""
        return Path(self.get("paths.logs", str(LOGS_DIR)))
    
    def get_skill_data_path(self):
        """获取 Skill 数据根目录"""
        return Path(self.get("paths.skill_data", str(SKILL_DATA_DIR)))
    
    def is_test_mode(self):
        """是否测试模式"""
        return self.get("test_mode", False)
    
    def get_delivery_config(self):
        """获取发送渠道配置"""
        channel = self.get_env("SMART_EMAIL_DELIVERY_CHANNEL", "")
        target = self.get_env("SMART_EMAIL_DELIVERY_TARGET", "")
        return {
            "channel": channel,
            "target": target,
            "enabled": bool(channel and target)
        }


# 全局配置实例
config = Config()
