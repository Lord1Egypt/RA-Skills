#!/usr/bin/env python3
"""
小红书AI日报发布示例
Example: AI Daily News Publisher for Xiaohongshu
"""

import sys
from pathlib import Path
import subprocess
from datetime import datetime


def fetch_ai_news():
    """抓取AI新闻（示例）"""
    # 这里是示例新闻内容，实际使用时可以接入真实的新闻API
    news_items = [
        {
            "title": "MIT发布新AI模型CausVid，可秒级生成高质量视频",
            "summary": "MIT CSAIL与Adobe Research联合发布混合架构AI模型，实现视频内容的快速生成。"
        },
        {
            "title": "OpenAI发布GPT-5预览版，性能提升显著",
            "summary": "新版本在推理能力和多模态理解方面有重大突破。"
        },
        {
            "title": "谷歌Bard更新，支持实时网络搜索",
            "summary": "用户现在可以获取最新的实时信息和数据。"
        },
        {
            "title": "微软Copilot集成Office全家桶",
            "summary": "AI助手将在Word、Excel、PowerPoint中提供智能协助。"
        }
    ]
    
    return news_items


def format_content_for_xiaohongshu(news_items, date_str):
    """格式化内容为小红书格式"""
    
    title = f"{date_str}AI热点速递🔥"
    
    content_lines = ["【今日AI要闻】", ""]
    
    for i, item in enumerate(news_items[:7], 1):  # 最多7条新闻
        emoji = f"{i}️⃣"
        content_lines.append(f"{emoji} {item['title'][:50]}")  # 限制标题长度
        content_lines.append(f"{item['summary'][:80]}")  # 限制摘要长度
        content_lines.append("")
    
    # 添加话题标签
    content_lines.extend([
        "——",
        "国内外AI资讯聚合，每日更新",
        "",
        "#AI #人工智能 #科技前沿 #热点速递"
    ])
    
    content = "\n".join(content_lines)
    
    # 确保内容不超过1000字
    if len(content) > 1000:
        content = content[:997] + "..."
    
    return title, content


def generate_cover(title, date_str):
    """生成封面图片"""
    cover_script = Path(__file__).parent.parent / "scripts" / "cover_generator.py"
    output_path = "/tmp/openclaw/uploads/ai_daily_cover.jpg"
    
    cmd = f"python3 {cover_script} --title '{title}' --date '{date_str}' --output '{output_path}'"
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ 封面生成成功: {output_path}")
        return output_path
    else:
        print(f"❌ 封面生成失败: {result.stderr}")
        return None


def publish_to_xiaohongshu(title, content, cover_path):
    """发布到小红书"""
    publish_script = Path(__file__).parent.parent / "scripts" / "publish.py"
    
    cmd = f"python3 {publish_script} --title '{title}' --content '{content}' --image '{cover_path}'"
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 小红书发布成功!")
        return True
    else:
        print(f"❌ 小红书发布失败: {result.stderr}")
        return False


def main():
    """主函数"""
    print("🚀 开始AI日报自动发布流程...")
    
    # 获取当前日期
    today = datetime.now()
    date_str = today.strftime("%m月%d日")
    
    # 1. 抓取AI新闻
    print("📰 抓取AI新闻...")
    news_items = fetch_ai_news()
    print(f"获取到 {len(news_items)} 条新闻")
    
    # 2. 格式化内容
    print("📝 格式化内容...")
    title, content = format_content_for_xiaohongshu(news_items, date_str)
    
    print(f"标题: {title} ({len(title)}字)")
    print(f"内容长度: {len(content)}字")
    
    # 检查长度限制
    if len(title) > 20:
        print("⚠️  标题超长，需要缩短")
        title = title[:20]
    
    # 3. 生成封面
    print("🎨 生成封面...")
    cover_path = generate_cover("AI热点速递", today.strftime("%Y.%m.%d"))
    
    if not cover_path:
        print("❌ 封面生成失败，终止发布")
        sys.exit(1)
    
    # 4. 发布到小红书
    print("📱 发布到小红书...")
    success = publish_to_xiaohongshu(title, content, cover_path)
    
    if success:
        print("🎉 AI日报发布完成!")
        print(f"📊 标题: {title}")
        print(f"📊 内容: {len(content)}字")
        print(f"📊 封面: {cover_path}")
    else:
        print("❌ AI日报发布失败")
        sys.exit(1)


if __name__ == '__main__':
    main()