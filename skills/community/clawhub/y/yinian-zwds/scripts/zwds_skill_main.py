"""
zwds_skill_main.py — 一念紫微斗数 OpenClaw Skill 入口 v2
Telegram Bot命令路由：/zwds /reading /yearly /monthly /star /help /about

Author: 崽儿虾 🦞
"""

import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tg_bot_handler import (
    parse_birth_input,
    handle_zwds_command,
    handle_reading_command,
    handle_yearly_command,
    handle_monthly_command,
    handle_star_command,
    handle_help,
    handle_about,
    handle_reading_english,
    handle_matching_command,
    handle_daily_command,
    handle_name_command,
)
from formats import format_chart_for_telegram
from ai_reader import create_chart_and_reading, read_astrolabe
from ai_engine import ai_reading, full_reading_with_yearly


class YinianZWDS:
    """一念紫微斗数 Skill 主入口 v2"""
    
    def __init__(self):
        self.last_chart = None  # 缓存最后一次排盘结果
    
    def process_message(self, text: str) -> str:
        """处理用户消息主入口（OpenClaw框架自动调用）"""
        if not text or not text.strip():
            return ""
        
        text = text.strip()
        
        # 命令路由
        if text.startswith("/reading"):
            return handle_reading_command(text)
        
        if text.startswith("/read_en"):
            return handle_reading_english(text)
        
        if text.startswith("/yearly"):
            return handle_yearly_command(text)
        
        if text.startswith("/monthly"):
            return handle_monthly_command(text)
        
        if text.startswith("/daily"):
            return handle_daily_command(text)
        
        if text.startswith("/match"):
            return handle_matching_command(text)
        
        if text.startswith("/star"):
            rest = text.split(maxsplit=1)[1] if len(text.split()) > 1 else ""
            return handle_star_command(rest)
        
        if text.startswith("/name"):
            rest = text[5:].strip()
            return handle_name_command(rest)
        
        if text.startswith("/help") or text.startswith("/zwds_help"):
            return handle_help()
        
        if text.startswith("/about") or text.startswith("/zwds_about"):
            return handle_about()
        
        if text.startswith("/read"):
            return read_astrolabe(self.last_chart) if self.last_chart else "❌ 请先排盘（/zwds），再使用 /read 解盘"
        
        # /zwds 命令（含 --deep 标志）
        if text.startswith("/zwds") or text.startswith("/zwds_lunar") or re.match(r'^\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}\s+[男女]', text):
            result_text = handle_zwds_command(text)
            # 缓存chart
            if not any(s in result_text[:50] for s in ["❌"]):
                self.last_chart = {"has_chart": True}
            return result_text
        
        return ""
    
    def reset(self):
        """重置会话状态"""
        self.last_chart = None


# ====== 全局实例（供OpenClaw加载）======
yinian_zwds = YinianZWDS()


def handle_user_input(text: str) -> str:
    """OpenClaw调用的入口函数"""
    return yinian_zwds.process_message(text)


if __name__ == "__main__":
    handler = YinianZWDS()
    tests = [
        "/zwds 2000-8-16 6 男",
        "/help",
        "/star 紫微",
        "/about",
    ]
    for t in tests:
        print(f"\n{'='*50}")
        print(f">>> {t}")
        result = handler.process_message(t)
        print(result[:500] if len(str(result)) > 500 else result)
