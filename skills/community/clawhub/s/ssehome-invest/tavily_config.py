"""
Tavily Search API Configuration
投资研究报告 - 新闻搜索配置

获取 API Key: https://app.tavily.com/
免费版：每天 1000 次搜索额度
"""

# 请将您的 Tavily API Key 填入下方
TAVILY_API_KEY = "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"  # TODO: 替换为真实的 API Key

def get_tavily_api_key():
    """获取 Tavily API Key"""
    if not TAVILY_API_KEY:
        raise ValueError(
            "⚠️ Tavily API Key 未配置！\n"
            "请在 tavily_config.py 文件中设置 TAVILY_API_KEY\n"
            "获取地址：https://app.tavily.com/"
        )
    return TAVILY_API_KEY

if __name__ == '__main__':
    pass
