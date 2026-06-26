"""配置加载器 - 从 config.txt 读取配置"""
import os

def _parse_value(value):
    """解析配置值，转换为适当的类型"""
    value = value.strip()
    # 布尔值
    if value.lower() == 'true':
        return True
    if value.lower() == 'false':
        return False
    # 整数
    try:
        return int(value)
    except ValueError:
        pass
    # 浮点数
    try:
        return float(value)
    except ValueError:
        pass
    # 字符串
    return value

def _load_config_txt(txt_path):
    """从 txt 文件加载配置"""
    config = {}
    if os.path.exists(txt_path):
        with open(txt_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = _parse_value(value)
    return config

def _build_config():
    """构建完整的 CONFIG 字典"""
    txt_path = os.path.join(os.path.dirname(__file__), 'config.txt')
    raw_config = _load_config_txt(txt_path)
    
    config = {
        "VERSION": raw_config.get("VERSION", "V3.0"),
        "SOURCE_LANG": raw_config.get("SOURCE_LANG", "auto"),
        "TARGET_LANG": raw_config.get("TARGET_LANG", "zh-CN"),
        "TARGETS_FILE": raw_config.get("TARGETS_FILE", "targets.txt"),
        "OUTPUT_PATH_CONFIG": raw_config.get("OUTPUT_PATH_CONFIG", "output_path.txt"),
        "PDF_TO_DOCX_TMP": raw_config.get("PDF_TO_DOCX_TMP", "tmp"),
        "TRANSLATE_ENGINE": raw_config.get("TRANSLATE_ENGINE", "ollama"),
        "CURRENT_CLOUD_MODEL": raw_config.get("CURRENT_CLOUD_MODEL", "DeepSeek (V3/R1)"),
        "CLOUD_MODELS": {
            "DeepSeek (V3/R1)": {
                "base_url": raw_config.get("CLOUD_MODEL_DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
                "model": raw_config.get("CLOUD_MODEL_DEEPSEEK_MODEL", "deepseek-chat"),
                "env_key": raw_config.get("CLOUD_MODEL_DEEPSEEK_ENV_KEY", "DEEPSEEK_API_KEY")
            },
            "GPT-4o": {
                "base_url": raw_config.get("CLOUD_MODEL_GPT4O_BASE_URL", "https://api.openai.com/v1"),
                "model": raw_config.get("CLOUD_MODEL_GPT4O_MODEL", "gpt-4o"),
                "env_key": raw_config.get("CLOUD_MODEL_GPT4O_ENV_KEY", "OPENAI_API_KEY")
            },
            "Claude 3.5 Sonnet": {
                "base_url": raw_config.get("CLOUD_MODEL_CLAUDE_BASE_URL", "https://api.anthropic.com/v1"),
                "model": raw_config.get("CLOUD_MODEL_CLAUDE_MODEL", "claude-3-5-sonnet-20240620"),
                "env_key": raw_config.get("CLOUD_MODEL_CLAUDE_ENV_KEY", "ANTHROPIC_API_KEY")
            },
            "SiliconFlow (Qwen2.5)": {
                "base_url": raw_config.get("CLOUD_MODEL_SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1"),
                "model": raw_config.get("CLOUD_MODEL_SILICONFLOW_MODEL", "deepseek-ai/DeepSeek-V3"),
                "env_key": raw_config.get("CLOUD_MODEL_SILICONFLOW_ENV_KEY", "SILICONFLOW_API_KEY")
            },
            "自定义 (OpenAI 兼容)": {
                "base_url": raw_config.get("CLOUD_MODEL_CUSTOM_BASE_URL", ""),
                "model": raw_config.get("CLOUD_MODEL_CUSTOM_MODEL", ""),
                "env_key": raw_config.get("CLOUD_MODEL_CUSTOM_ENV_KEY", "CUSTOM_API_KEY")
            }
        },
        "DEEPSEEK_API_KEY": os.getenv("DEEPSEEK_API_KEY", ""),
        "DEEPSEEK_BASE_URL": "https://api.deepseek.com",
        "DEEPSEEK_MODEL": "deepseek-chat",
        "OLLAMA_MODEL": raw_config.get("OLLAMA_MODEL", "qwen3:1.7b"),
        "SAVE_IN_SOURCE_DIR": raw_config.get("SAVE_IN_SOURCE_DIR", True),
        "VERBOSE_OUTPUT": raw_config.get("VERBOSE_OUTPUT", False),
        "AUTO_FORMAT_LAYOUT": raw_config.get("AUTO_FORMAT_LAYOUT", True),
        "BATCH_CONFIG": {
            "cloud": {
                "max_len": raw_config.get("BATCH_CLOUD_MAX_LEN", 15000),
                "max_count": raw_config.get("BATCH_CLOUD_MAX_COUNT", 200),
                "concurrent": raw_config.get("BATCH_CLOUD_CONCURRENT", 2),
                "max_tokens": raw_config.get("BATCH_CLOUD_MAX_TOKENS", 16384),
                "adaptive": raw_config.get("BATCH_CLOUD_ADAPTIVE", False)
            },
            "ollama": {
                "max_len": raw_config.get("BATCH_OLLAMA_MAX_LEN", 1000),
                "max_count": raw_config.get("BATCH_OLLAMA_MAX_COUNT", 1),
                "concurrent": raw_config.get("BATCH_OLLAMA_CONCURRENT", 1),
                "max_tokens": raw_config.get("BATCH_OLLAMA_MAX_TOKENS", 1000)
            },
            "python": {
                "max_len": raw_config.get("BATCH_PYTHON_MAX_LEN", 1),
                "max_count": raw_config.get("BATCH_PYTHON_MAX_COUNT", 1),
                "concurrent": raw_config.get("BATCH_PYTHON_CONCURRENT", 1),
                "max_tokens": raw_config.get("BATCH_PYTHON_MAX_TOKENS", 100)
            }
        },
        "BATCH_OPTIMIZATION": {
            "enabled": raw_config.get("BATCH_OPTIMIZATION_ENABLED", True),
            "auto_adjust": raw_config.get("BATCH_OPTIMIZATION_AUTO_ADJUST", True),
            "small_file_threshold": raw_config.get("BATCH_OPTIMIZATION_SMALL_FILE_THRESHOLD", 50),
            "large_file_threshold": raw_config.get("BATCH_OPTIMIZATION_LARGE_FILE_THRESHOLD", 500),
            "progress_interval": raw_config.get("BATCH_OPTIMIZATION_PROGRESS_INTERVAL", 10)
        }
    }
    return config

def _get_output_dir(config):
    """从配置文件读取输出目录"""
    output_path_config = config.get("OUTPUT_PATH_CONFIG", "output_path.txt")
    if os.path.exists(output_path_config):
        with open(output_path_config, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    return line
    return "output"

# 加载配置
CONFIG = _build_config()
CONFIG["OUTPUT_DIR"] = _get_output_dir(CONFIG)

# 确保目录存在
if not os.path.exists(CONFIG["OUTPUT_DIR"]):
    os.makedirs(CONFIG["OUTPUT_DIR"])

if not os.path.exists(CONFIG["PDF_TO_DOCX_TMP"]):
    os.makedirs(CONFIG["PDF_TO_DOCX_TMP"])
