#!/usr/bin/env python3
"""
HIIC日报 - tech-news-digest 数据桥接脚本
用于从 tech-news-digest 技能获取数据并转换为 HIIC日报格式
"""

import json
import argparse
import sys
import subprocess
from pathlib import Path

# tech-news-digest 的路径
TECH_DIGEST_DIR = Path("/root/.openclaw/workspace/skills/tech-news-digest")

# 产业到主题的映射
INDUSTRY_TO_TOPICS = {
    "人工智能": ["llm", "ai-agent"],
    "智能网联汽车": ["ai-agent", "frontier-tech"],
    "机器人": ["ai-agent"],
    "智能机器人": ["ai-agent"],
    "量子信息": ["frontier-tech"],
    "新能源": ["frontier-tech"],
    "生物医药": ["frontier-tech"],
    "高端医疗器械": ["frontier-tech"],
    "大健康": ["frontier-tech"],
    "生物制造": ["frontier-tech"],
    "脑科学与脑机工程": ["frontier-tech", "ai-agent"],
    "细胞与基因": ["frontier-tech"],
    "半导体与集成电路": ["frontier-tech"],
    "网络与通信": ["frontier-tech"],
    "超高清视频显示": ["frontier-tech"],
    "智能终端": ["ai-agent", "frontier-tech"],
    "智能传感器": ["ai-agent", "frontier-tech"],
    "软件与信息服务": ["ai-agent"],
    "数字创意": ["frontier-tech"],
    "高端装备与仪器": ["frontier-tech"],
    "低空经济与空天": ["frontier-tech"],
    "现代时尚": [],
    "安全节能环保": ["frontier-tech"],
    "海洋产业": [],
    "深地深海": [],
}

def main():
    parser = argparse.ArgumentParser(description="从 tech-news-digest 获取数据")
    parser.add_argument("--industry", required=True, help="产业名称")
    parser.add_argument("--hours", type=int, default=24, help="时间窗口（小时）")
    parser.add_argument("--max-items", type=int, default=10, help="最大返回条数")
    parser.add_argument("--output", help="输出文件路径")
    parser.add_argument("--verbose", action="store_true", help="详细输出")
    
    args = parser.parse_args()
    
    # 获取主题
    topics = INDUSTRY_TO_TOPICS.get(args.industry, [])
    
    if not topics:
        if args.verbose:
            print(f"⚠️  产业 '{args.industry}' 没有对应的技术主题映射", file=sys.stderr)
        # 返回空结果
        result = {"articles": [], "source": "tech-news-digest", "total": 0}
        print(json.dumps(result, ensure_ascii=False))
        return
    
    if args.verbose:
        print(f"📊 产业 '{args.industry}' 映射到主题: {topics}", file=sys.stderr)
    
    try:
        # 使用 subprocess 调用 tech-news-digest 的脚本
        output_file = "/tmp/td-hiic-bridge.json"
        
        cmd = [
            "python3",
            str(TECH_DIGEST_DIR / "scripts" / "run-pipeline.py"),
            "--defaults", str(TECH_DIGEST_DIR / "config" / "defaults"),
            "--hours", str(args.hours),
            "--freshness", "pd",
            "--output", output_file,
        ]
        
        if args.verbose:
            print(f"🔧 执行命令: {' '.join(cmd)}", file=sys.stderr)
        
        result_subprocess = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result_subprocess.returncode != 0:
            if args.verbose:
                print(f"❌ tech-news-digest 执行失败: {result_subprocess.stderr}", file=sys.stderr)
            result = {"articles": [], "source": "tech-news-digest", "total": 0, "error": result_subprocess.stderr}
            print(json.dumps(result, ensure_ascii=False))
            return
        
        # 读取结果
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 筛选相关主题的文章
        articles = []
        for topic in topics:
            if topic in data.get("topics", {}):
                topic_articles = data["topics"][topic]["articles"]
                for article in topic_articles:
                    articles.append({
                        "title": article["title"],
                        "url": article["link"],
                        "source": article.get("source_name", "tech-news-digest"),
                        "published_date": article.get("date", ""),
                        "summary": "",  # tech-news-digest 默认没有摘要，需要后续提取
                        "quality_score": article.get("quality_score", 5),
                        "source_type": article.get("source_type", "unknown"),
                        "topic": topic
                    })
        
        # 去重（基于URL）
        seen_urls = set()
        unique_articles = []
        for article in articles:
            if article["url"] not in seen_urls:
                unique_articles.append(article)
                seen_urls.add(article["url"])
        
        # 按质量评分排序
        unique_articles.sort(key=lambda x: x["quality_score"], reverse=True)
        
        # 限制数量
        unique_articles = unique_articles[:args.max_items]
        
        # 返回结果
        result = {
            "articles": unique_articles,
            "source": "tech-news-digest",
            "total": len(unique_articles),
            "topics": topics
        }
        
        if args.verbose:
            print(f"✅ 获取到 {len(unique_articles)} 条相关资讯", file=sys.stderr)
        
        print(json.dumps(result, ensure_ascii=False))
        
        # 保存到文件（如果指定）
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        
    except subprocess.TimeoutExpired:
        if args.verbose:
            print(f"❌ tech-news-digest 执行超时", file=sys.stderr)
        result = {"articles": [], "source": "tech-news-digest", "total": 0, "error": "Timeout"}
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        if args.verbose:
            print(f"❌ 获取失败: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
        
        # 返回空结果
        result = {"articles": [], "source": "tech-news-digest", "total": 0, "error": str(e)}
        print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
