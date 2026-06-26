# openclaw_skill.py
# OpenClaw Skill核心逻辑，支持3个触发词，调用API获取科技热点新闻

import requests

# 定义触发词列表
TRIGGER_WORDS = ["X-TechCon科技热点", "科技区角热点", "科技新闻热点"]

# API调用地址
API_URL = "https://www.x-techcon.com/api/hot_news"

def skill_main(user_query):
    """
    OpenClaw Skill主函数
    接收用户输入，判断是否包含触发词，调用API获取新闻并格式化输出
    
    参数:
        user_query: str - 用户输入的字符串
    
    返回:
        str - 格式化的新闻信息或提示信息
    """
    # 检查用户输入是否包含触发词
    trigger_found = False
    for trigger in TRIGGER_WORDS:
        if trigger in user_query:
            trigger_found = True
            break
    
    # 如果不包含触发词，返回提示信息
    if not trigger_found:
        return "暂不支持，请说'X-TechCon科技热点''科技区角热点'或'科技新闻热点'获取最新科技新闻"
    
    # 包含触发词，调用API获取新闻
    try:
        # 设置请求头和参数
        headers = {'User-Agent': 'curl/7.61.1'}
        # 发送GET请求调用API，设置超时
        response = requests.get(API_URL, headers=headers, timeout=10)
        # 解析响应数据
        data = response.json()
        
        # 检查API返回是否成功
        if data.get("code") == 200:
            # 获取新闻列表
            news_list = data.get("data", [])
            # 格式化输出新闻信息
            result = "科技热点新闻：\n\n"
            for i, news in enumerate(news_list, 1):
                # 提取新闻信息
                title = news.get("title", "")
                summary = news.get("summary", "")
                url = news.get("url", "")
                # 格式化每条新闻
                result += f"{i}. 标题：{title}\n"
                result += f"   摘要：{summary}\n"
                result += f"   链接：{url}\n\n"
            # 添加结尾提示
            result += "更多内容请访问 https://www.x-techcon.com"
            return result
        else:
            # API返回失败
            return "获取新闻失败，请稍后重试"
    except Exception as e:
        # 异常处理
        return "获取新闻失败，请稍后重试"


