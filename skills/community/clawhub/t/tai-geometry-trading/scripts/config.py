#!/usr/bin/env python3
"""
太几何交易 - 配置文件
请填写自己的API Token
"""

# ============================================
# 数据源配置 (二选一)
# ============================================

# 方式1: Tushare配置 (需要token)
TUSHARE_TOKEN = ""  # 你的tushare token，注册地址: https://tushare.pro

# 方式2: AkShare (免费，无需token，默认使用)
# 无需配置，直接使用腾讯/东方财富接口

# 数据源选择: "tushare" 或 "akshare" (默认akshare)
DATA_SOURCE = "akshare"


# ============================================
# 大模型配置 (完整版需要)
# ============================================

# 大模型提供商选择: "openai" / "anthropic" / "minimax" / "deepseek" / "qwen" / "自定义"
LLM_PROVIDER = "minimax"

# 以下填写你已有的API Key (选择你使用的提供商填入对应位置)
OPENAI_API_KEY = ""       # OpenAI API Key (ChatGPT)
ANTHROPIC_API_KEY = ""   # Anthropic API Key (Claude)
MINIMAX_API_KEY = ""
MINIMAX_BASE_URL = "https://api.minimax.chat/v1"      # MiniMax API Key
DEEPSEEK_API_KEY = ""     # DeepSeek API Key
QWEN_API_KEY = ""         # 阿里Qwen API Key

# 自定义API配置 (如使用其他大模型)
CUSTOM_API_KEY = ""
CUSTOM_BASE_URL = ""       # 如: https://api.openai.com/v1
CUSTOM_MODEL = ""         # 如: gpt-4o


# ============================================
# 提示信息
# ============================================

def check_config():
    """检查配置状态"""
    issues = []
    
    if DATA_SOURCE == "tushare" and not TUSHARE_TOKEN:
        issues.append("⚠️ 数据源: TUSHARE_TOKEN 未填写")
    
    # 检查大模型配置
    llm_enabled = False
    provider_name = ""
    
    if LLM_PROVIDER == "openai" and OPENAI_API_KEY:
        llm_enabled = True
        provider_name = "OpenAI"
    elif LLM_PROVIDER == "anthropic" and ANTHROPIC_API_KEY:
        llm_enabled = True
        provider_name = "Anthropic"
    elif LLM_PROVIDER == "minimax" and MINIMAX_API_KEY:
        llm_enabled = True
        provider_name = "MiniMax"
    elif LLM_PROVIDER == "deepseek" and DEEPSEEK_API_KEY:
        llm_enabled = True
        provider_name = "DeepSeek"
    elif LLM_PROVIDER == "qwen" and QWEN_API_KEY:
        llm_enabled = True
        provider_name = "阿里Qwen"
    elif LLM_PROVIDER == "自定义" and CUSTOM_API_KEY and CUSTOM_BASE_URL:
        llm_enabled = True
        provider_name = "自定义"
    
    if not llm_enabled:
        issues.append(f"⚠️ 大模型({LLM_PROVIDER}): API Key 未填写")
        issues.append("  → 完整版(带AI分析)将不可用")
        issues.append("  → 可使用核心版(无需API)，运行 analyze_stock_core.py")
        issues.append(f"\n  当前支持: openai, anthropic, minimax, deepseek, qwen, 自定义")
    else:
        issues.append(f"✅ 大模型({provider_name}): 已配置")
    
    if not issues or (len(issues) == 1 and "TUSHARE" in issues[0]):
        print("✅ 配置检查通过")
        return True
    else:
        print("\n📋 配置状态:")
        for issue in issues:
            print(issue)
        print("\n获取API Key:")
        print("  - Tushare: https://tushare.pro")
        print("  - OpenAI: https://platform.openai.com")
        print("  - Anthropic: https://www.anthropic.com")
        print("  - MiniMax: https://www.minimax.io")
        print("  - DeepSeek: https://platform.deepseek.com")
        print("  - 阿里Qwen: https://dashscope.console.aliyun.com")
        return False


def get_data_source():
    """获取数据源"""
    if DATA_SOURCE == "tushare" and TUSHARE_TOKEN:
        return "tushare"
    return "akshare"


def get_llm_config():
    """获取大模型配置"""
    provider = LLM_PROVIDER.lower()
    
    if provider == "openai" and OPENAI_API_KEY:
        return {
            "provider": "openai",
            "api_key": OPENAI_API_KEY,
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-4o"
        }
    elif provider == "anthropic" and ANTHROPIC_API_KEY:
        return {
            "provider": "anthropic",
            "api_key": ANTHROPIC_API_KEY,
            "base_url": "https://api.anthropic.com",
            "model": "claude-sonnet-4-20250514"
        }
    elif provider == "minimax" and MINIMAX_API_KEY:
        return {
            "provider": "minimax",
            "api_key": MINIMAX_API_KEY,
            "base_url": MINIMAX_BASE_URL if 'MINIMAX_BASE_URL' in globals() else "https://api.minimaxi.com/anthropic",
            "model": "MiniMax-M2.5"
        }
    elif provider == "deepseek" and DEEPSEEK_API_KEY:
        return {
            "provider": "deepseek",
            "api_key": DEEPSEEK_API_KEY,
            "base_url": "https://api.deepseek.com/v1",
            "model": "deepseek-chat"
        }
    elif provider == "qwen" and QWEN_API_KEY:
        return {
            "provider": "qwen",
            "api_key": QWEN_API_KEY,
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "model": "qwen-turbo"
        }
    elif provider == "自定义" and CUSTOM_API_KEY and CUSTOM_BASE_URL:
        return {
            "provider": "custom",
            "api_key": CUSTOM_API_KEY,
            "base_url": CUSTOM_BASE_URL,
            "model": CUSTOM_MODEL or "gpt-4o"
        }
    
    return None


def get_llm_enabled():
    """是否启用大模型辅助因子"""
    return get_llm_config() is not None


if __name__ == '__main__':
    check_config()