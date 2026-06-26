from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import pytz

from utils.logger import get_logger
from config import Settings

class BlogPoster:
    """Hugo Blog Poster"""
    
    def __init__(self, config: Settings):
        self.config = config
        self.logger = get_logger(__name__)
    
    def create_post(self, market_summary: str, ai_analysis: Optional[str], date: str) -> Path:
        """
        Create a Hugo blog post with market summary and AI analysis
        
        Args:
            market_summary: market summary Markdown
            ai_analysis: AI analysis Markdown
            date: date
            
        Returns:
            post path
        """
        # use local timezone
        now = datetime.now().astimezone()
        safe_now = now - timedelta(minutes=10)

        date_filename = safe_now.strftime("%Y-%m-%d")
        formatted_date = safe_now.strftime("%Y-%m-%dT%H:%M:%S%z")

        # RFC3339 format requires a colon in the timezone offset, e.g. +08:00 instead of +0800
        if len(formatted_date) > 5 and formatted_date[-5:-4] not in '+-':
            formatted_date = formatted_date[:-2] + ':' + formatted_date[-2:]

        # print(f"time: {formatted_date}")
        
        filename = self.config.content_dir / f"stock-analysis-{date_filename}.md"
        display_title = f"A股全市场复盘：{date_filename} 深度解析及AI洞察"
        
        content = f"""---
title: "{display_title}"
date: {formatted_date}
tags: ["每日复盘", "重点个股", "行业板块", "市场分析"]
categories: ["每日更新"]
showToc: true
draft: false
---

## 📈 A股市场概览

{market_summary}

"""

        if ai_analysis:
            content += f"""
## 🤖 AI 深度分析与洞察

{ai_analysis}

"""

        content += """
---
*注：
1. 数据来源：AKShare。
2. 本文由AI辅助生成，旨在提供市场洞察和数据分析，非投资建议。
3. 声明：投资有风险，入市需谨慎。本文内容仅供参考，不构成任何投资建议或推荐。请根据自身情况做出独立判断。*
"""
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        
        self.logger.info(f"Hugo post created: {filename}")
        return filename