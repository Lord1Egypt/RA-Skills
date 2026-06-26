#!/usr/bin/env python3
"""
OpenClaw Skill 示例 - 小红书爬虫 + 飞书推送

使用场景:
    用户在飞书群输入: "新燕宝"
    OpenClaw 调用此 Skill，返回小红书笔记到飞书群
"""

import os
import sys
from pathlib import Path

# Skill 根目录（当前文件所在目录）
SKILL_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILL_DIR))

from xhs_crawler import crawl_notes
from feishu_app_bot import FeishuAppBot

# 配置群聊 ID
FEISHU_CHAT_ID = "oc_29fbba0871ab7371a4c1a1ebe0350dac"


async def handle_feishu_message(text: str, chat_id: str = None) -> dict:
    """
    处理飞书消息（供 OpenClaw 直接调用）
    
    自动识别 run-xhs 指令，支持:
        - run-xhs：新燕宝2025
        - run-xhs: 新燕宝2025
        - run-xhs 新燕宝2025
    
    Args:
        text: 飞书收到的完整消息文本
        chat_id: 飞书群聊 ID
        
    Returns:
        dict: 执行结果
    """
    # 解析指令
    is_command, keyword = parse_command(text)
    
    if is_command:
        # 匹配到 run-xhs 指令，执行搜索
        return await xhs_search_skill(keyword, chat_id)
    else:
        # 未匹配到指令，返回提示
        return {
            "success": False,
            "message": "未识别到指令，请使用格式: run-xhs：关键词",
            "data": None
        }


async def xhs_search_skill(keyword: str, chat_id: str = None) -> dict:
    """
    OpenClaw Skill 主函数
    
    Args:
        keyword: 用户输入的关键词，如 "新燕宝"
        chat_id: 飞书群聊 ID，为 None 则使用默认配置
        
    Returns:
        dict: 执行结果
        {
            "success": True/False,
            "message": "执行结果描述",
            "data": {笔记数据}
        }
    """
    target_chat = chat_id or FEISHU_CHAT_ID
    
    if target_chat == "oc_xxxxxxxxxxxxxxxx":
        return {
            "success": False,
            "message": "未配置飞书群聊 ID，请在代码中设置 FEISHU_CHAT_ID",
            "data": None
        }
    
    # 创建飞书应用机器人
    bot = FeishuAppBot()
    
    # 发送开始搜索提示
    bot.send_text_to_chat(target_chat, f"🔍 正在搜索小红书关键词: 「{keyword}」，请稍候...")
    
    try:
        # 检查 Cookie 有效性（传入 chat_id 以启用自动二维码登录）
        from cookie_manager import CookieManager
        
        manager = CookieManager()
        cookie = await manager.ensure_valid_cookie(target_chat)
        
        if not cookie:
            return {
                "success": False,
                "message": "Cookie 无效且自动登录失败",
                "data": None
            }
        
        # 执行爬虫（使用浏览器搜索，避免API被拦截）
        from xhs_search_with_browser import search_with_browser
        
        results = await search_with_browser(keyword, max_notes=5)
        
        if not results:
            bot.send_text_to_chat(target_chat, f"❌ 未找到关键词「{keyword}」的相关笔记")
            return {
                "success": True,
                "message": f"未找到关键词「{keyword}」的相关笔记",
                "data": []
            }
        
        # 发送汇总结果到飞书
        bot.send_notes_summary(target_chat, keyword, results)
        
        return {
            "success": True,
            "message": f"成功获取 {len(results)} 条笔记",
            "data": results
        }
        
    except Exception as e:
        error_msg = f"搜索失败: {str(e)}"
        bot.send_text_to_chat(target_chat, f"❌ {error_msg}")
        return {
            "success": False,
            "message": error_msg,
            "data": None
        }


def parse_command(text: str) -> tuple:
    """
    解析飞书指令
    
    支持格式:
        run-xhs：关键词
        run-xhs: 关键词
        run-xhs 关键词
        
    Args:
        text: 用户输入的完整文本
        
    Returns:
        tuple: (是否匹配, 关键词)
    """
    import re
    # 匹配 run-xhs 后跟中文冒号、英文冒号或空格，然后捕获关键词
    pattern = r'run-xhs[：:\s]+(.+)'
    match = re.search(pattern, text, re.IGNORECASE)
    
    if match:
        keyword = match.group(1).strip()
        return True, keyword
    return False, None


def main():
    """
    命令行测试入口
    
    用法:
        python example_openclaw_skill.py "新燕宝"
        python example_openclaw_skill.py "run-xhs：新燕宝2025"
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="小红书爬虫飞书 Skill")
    parser.add_argument("text", help="搜索关键词或完整指令（如: run-xhs：新燕宝2025）")
    parser.add_argument("--chat-id", help="飞书群聊 ID（可选，默认使用代码中的配置）")
    
    args = parser.parse_args()
    
    # 检查群聊 ID 配置
    if not args.chat_id and FEISHU_CHAT_ID == "oc_xxxxxxxxxxxxxxxx":
        print("❌ 错误: 未配置飞书群聊 ID")
        print()
        print("请通过以下方式之一配置:")
        print("1. 修改代码中的 FEISHU_CHAT_ID 变量")
        print("2. 使用命令行参数: --chat-id 'oc_xxxxxxxxxxxxxxxx'")
        print()
        print("群聊 ID 获取方式:")
        print("  1. 先把应用机器人添加到飞书群")
        print("  2. 运行: python feishu_app_bot.py")
        print("  3. 查看输出的群列表，复制对应的 chat_id")
        sys.exit(1)
    
    # 解析指令
    is_command, keyword = parse_command(args.text)
    
    if is_command:
        # 匹配到 run-xhs 指令
        print(f"🎯 检测到指令: run-xhs")
        print(f"🔍 提取关键词: {keyword}")
    else:
        # 未匹配到指令，直接将输入作为关键词
        keyword = args.text.strip()
        print(f"🔍 搜索关键词: {keyword}")
    
    # 执行 Skill
    print(f"🚀 开始执行搜索...")
    import asyncio
    result = asyncio.run(xhs_search_skill(keyword, args.chat_id))
    
    # 输出结果
    print()
    print("=" * 50)
    if result["success"]:
        print(f"✅ {result['message']}")
        if result["data"]:
            print(f"📊 获取到 {len(result['data'])} 条笔记")
    else:
        print(f"❌ {result['message']}")


if __name__ == "__main__":
    main()
