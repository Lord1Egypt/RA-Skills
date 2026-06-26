#!/usr/bin/env python3
"""
RSS Reader + AI Summary
订阅 RSS，检测新文章，AI 生成摘要，推送到飞书
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import feedparser
except ImportError:
    print("❌ 缺少依赖：feedparser")
    print("请运行：pip install feedparser")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("❌ 缺少依赖：requests")
    print("请运行：pip install requests")
    sys.exit(1)

# 配置
DATA_DIR = Path(__file__).parent / "data"
SUBSCRIPTIONS_FILE = DATA_DIR / "subscriptions.json"
ARTICLES_FILE = DATA_DIR / "articles.json"

# 从环境变量获取配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")  # 默认智谱
FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL", "")

# 默认订阅源（首次使用自动添加）
DEFAULT_SUBSCRIPTIONS = {
    # 中文源
    "https://www.ruanyifeng.com/blog/atom.xml": {
        "name": "阮一峰博客",
        "category": "技术"
    },
    "https://www.v2ex.com/index.xml": {
        "name": "V2EX",
        "category": "社区"
    },
    "https://sspai.com/feed": {
        "name": "少数派",
        "category": "科技"
    },
    "https://36kr.com/feed": {
        "name": "36氪",
        "category": "商业"
    },
    "https://www.huxiu.com/rss/0.xml": {
        "name": "虎嗅",
        "category": "商业"
    },
    "https://www.infoq.cn/feed": {
        "name": "InfoQ 中文",
        "category": "技术"
    },
    "https://www.ithome.com/rss/": {
        "name": "IT之家",
        "category": "科技"
    },
    "https://www.oschina.net/news/rss": {
        "name": "开源中国",
        "category": "技术"
    },
    # 国外源 - AI
    "https://www.anthropic.com/news/rss": {
        "name": "Anthropic Blog",
        "category": "AI"
    },
    "https://openai.com/blog/rss.xml": {
        "name": "OpenAI Blog",
        "category": "AI"
    },
    "https://deepmind.google/discover/blog/rss/": {
        "name": "Google DeepMind",
        "category": "AI"
    },
    "https://blog.google/technology/ai/rss/": {
        "name": "Google AI Blog",
        "category": "AI"
    },
    # 国外源 - 科技媒体
    "https://techcrunch.com/feed/": {
        "name": "TechCrunch",
        "category": "Tech"
    },
    "https://www.theverge.com/rss/index.xml": {
        "name": "The Verge",
        "category": "Tech"
    },
    "https://www.wired.com/feed/rss": {
        "name": "Wired",
        "category": "Tech"
    },
    "https://arstechnica.com/feed/": {
        "name": "Ars Technica",
        "category": "Tech"
    },
    # 国外源 - 开发者
    "https://github.blog/feed/": {
        "name": "GitHub Blog",
        "category": "Dev"
    },
    "https://hnrss.org/frontpage": {
        "name": "Hacker News",
        "category": "Dev"
    },
    "https://www.producthunt.com/feed": {
        "name": "Product Hunt",
        "category": "Product"
    },
    # 国外源 - 商业
    "https://hbr.org/feed": {
        "name": "Harvard Business Review",
        "category": "Business"
    },
    "https://www.economist.com/rss": {
        "name": "The Economist",
        "category": "Business"
    }
}

# 确保数据目录存在
DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_json(file_path: Path, default=None):
    """加载 JSON 文件"""
    if not file_path.exists():
        return default if default is not None else {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ 加载 {file_path} 失败：{e}")
        return default if default is not None else {}


def save_json(file_path: Path, data):
    """保存 JSON 文件"""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ 保存 {file_path} 失败：{e}")


def init_default_subscriptions():
    """初始化默认订阅源（首次使用时自动添加）"""
    subscriptions = load_json(SUBSCRIPTIONS_FILE, {})
    
    if subscriptions:  # 如果已有订阅，跳过
        return
    
    print("🎁 首次使用，正在添加默认订阅源...")
    
    for url, info in DEFAULT_SUBSCRIPTIONS.items():
        try:
            feed = feedparser.parse(url)
            if not feed.bozo or feed.entries:
                subscriptions[url] = {
                    "name": info["name"],
                    "url": url,
                    "category": info.get("category", "未分类"),
                    "added_at": datetime.now().isoformat(),
                    "last_check": None,
                    "article_count": len(feed.entries) if hasattr(feed, 'entries') else 0,
                    "is_default": True
                }
                print(f"  ✅ {info['name']}")
        except Exception as e:
            print(f"  ⚠️ 跳过 {info['name']}: {e}")
    
    save_json(SUBSCRIPTIONS_FILE, subscriptions)
    print(f"\n✅ 已添加 {len(subscriptions)} 个默认订阅源")


def add_subscription(url: str, name: str = None):
    """添加订阅"""
    subscriptions = load_json(SUBSCRIPTIONS_FILE, {})
    
    if url in subscriptions:
        return f"⚠️ 已存在订阅：{subscriptions[url]['name']}"
    
    # 解析 RSS 获取名称
    try:
        feed = feedparser.parse(url)
        if feed.bozo and not feed.entries:
            return f"❌ 无效的 RSS 地址：{url}"
        
        feed_name = name or feed.feed.get("title", url)
    except Exception as e:
        return f"❌ 解析 RSS 失败：{e}"
    
    subscriptions[url] = {
        "name": feed_name,
        "url": url,
        "added_at": datetime.now().isoformat(),
        "last_check": None,
        "article_count": len(feed.entries) if hasattr(feed, 'entries') else 0
    }
    
    save_json(SUBSCRIPTIONS_FILE, subscriptions)
    
    # 初始化已读文章
    articles = load_json(ARTICLES_FILE, {})
    if hasattr(feed, 'entries'):
        for entry in feed.entries[:10]:  # 只记录最新的10篇
            article_id = entry.get("id", entry.get("link", ""))
            if article_id:
                articles[article_id] = {
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "read": True,
                    "read_at": datetime.now().isoformat()
                }
        save_json(ARTICLES_FILE, articles)
    
    return f"✅ 已订阅：{feed_name}\n📄 当前文章数：{len(feed.entries) if hasattr(feed, 'entries') else 0}"


def remove_subscription(url: str):
    """取消订阅"""
    subscriptions = load_json(SUBSCRIPTIONS_FILE, {})
    
    if url not in subscriptions:
        return f"❌ 未找到订阅：{url}"
    
    name = subscriptions[url]["name"]
    del subscriptions[url]
    save_json(SUBSCRIPTIONS_FILE, subscriptions)
    return f"✅ 已取消订阅：{name}"


def list_subscriptions():
    """列出所有订阅"""
    subscriptions = load_json(SUBSCRIPTIONS_FILE, {})
    
    if not subscriptions:
        return "📭 暂无订阅\n\n使用「订阅 <RSS地址>」添加订阅"
    
    lines = [f"📰 订阅列表（共 {len(subscriptions)} 个）：", ""]
    for i, (url, info) in enumerate(subscriptions.items(), 1):
        last_check = info.get("last_check")
        last_check_str = ""
        if last_check:
            try:
                dt = datetime.fromisoformat(last_check)
                last_check_str = f"\n   最后检查：{dt.strftime('%Y-%m-%d %H:%M')}"
            except:
                pass
        
        lines.append(
            f"{i}. **{info['name']}**\n"
            f"   {url}"
            f"{last_check_str}"
        )
    
    lines.append("")
    lines.append("💡 使用「立即刷新」检查新文章")
    
    return "\n".join(lines)


def fetch_new_articles(url: str):
    """获取新文章"""
    subscriptions = load_json(SUBSCRIPTIONS_FILE, {})
    articles = load_json(ARTICLES_FILE, {})
    
    try:
        feed = feedparser.parse(url)
        if feed.bozo and not feed.entries:
            print(f"  ⚠️ 解析失败：{url}")
            return []
    except Exception as e:
        print(f"  ❌ 获取失败：{e}")
        return []
    
    new_articles = []
    
    for entry in feed.entries:
        article_id = entry.get("id", entry.get("link", ""))
        
        if not article_id:
            continue
        
        # 跳过已读的文章
        if article_id in articles:
            continue
        
        article = {
            "id": article_id,
            "title": entry.get("title", "无标题"),
            "link": entry.get("link", ""),
            "summary": entry.get("summary", entry.get("description", "")),
            "published": entry.get("published", entry.get("updated", "")),
            "fetched_at": datetime.now().isoformat(),
            "subscription_url": url
        }
        
        new_articles.append(article)
    
    # 更新最后检查时间
    if url in subscriptions:
        subscriptions[url]["last_check"] = datetime.now().isoformat()
        subscriptions[url]["article_count"] = len(feed.entries)
        save_json(SUBSCRIPTIONS_FILE, subscriptions)
    
    return new_articles


def generate_summary(articles: list) -> dict:
    """
    使用 AI 生成摘要
    支持单条和多条文章批量总结
    返回：{article_id: summary}
    """
    if not OPENAI_API_KEY:
        return {a['id']: "（未配置 API Key）" for a in articles}
    
    if not articles:
        return {}
    
    # 单篇文章
    if len(articles) == 1:
        article = articles[0]
        return {article['id']: generate_single_summary(article)}
    
    # 多篇文章批量总结
    return generate_batch_summary(articles)


def generate_single_summary(article: dict) -> str:
    """单篇文章生成摘要"""
    import re
    
    title = article.get('title', '')
    content = article.get('summary', '')
    content_clean = re.sub(r'<[^>]+>', '', content)[:1500]
    
    try:
        response = requests.post(
            f"{OPENAI_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "glm-5",
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个专业的文章摘要助手。请用简洁的中文总结文章要点，控制在100字以内。"
                    },
                    {
                        "role": "user",
                        "content": f"请总结这篇文章：\n\n标题：{title}\n\n内容：{content_clean}"
                    }
                ],
                "max_tokens": 200,
                "temperature": 0.3
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        else:
            print(f"    ⚠️ API 调用失败：{response.status_code}")
            print(f"    响应：{response.text[:200]}")
            return f"（摘要失败：HTTP {response.status_code}）"
    
    except Exception as e:
        print(f"    ⚠️ 摘要生成出错：{e}")
        return f"（摘要出错）"


def generate_batch_summary(articles: list) -> dict:
    """多篇文章批量生成摘要"""
    import re
    
    # 构建批量摘要的 prompt
    articles_text = []
    for i, article in enumerate(articles[:5], 1):  # 最多5篇
        title = article.get('title', '')
        content = article.get('summary', '')
        content_clean = re.sub(r'<[^>]+>', '', content)[:500]
        articles_text.append(f"{i}. {title}\n   {content_clean}")
    
    prompt = "请为以下文章分别生成摘要，每篇摘要控制在50字以内，用序号区分：\n\n"
    prompt += "\n\n".join(articles_text)
    prompt += "\n\n请按以下格式输出：\n1. [摘要内容]\n2. [摘要内容]\n..."
    
    try:
        response = requests.post(
            f"{OPENAI_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "glm-5",
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个专业的文章摘要助手。请为多篇文章分别生成简洁的中文摘要。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 1000,
                "temperature": 0.3
            },
            timeout=60
        )
        
        if response.status_code != 200:
            print(f"    ⚠️ 批量摘要失败：{response.status_code}")
            print(f"    响应：{response.text[:200]}")
            return {a['id']: f"（摘要失败：HTTP {response.status_code}）" for a in articles}
        
        result = response.json()
        content = result["choices"][0]["message"]["content"].strip()
        
        # 解析批量摘要结果
        summaries = {}
        lines = content.split('\n')
        current_idx = 0
        
        for line in lines:
            # 匹配 "1. xxx" 或 "1、xxx" 格式
            import re
            match = re.match(r'^(\d+)[.、]\s*(.+)', line.strip())
            if match:
                idx = int(match.group(1)) - 1
                summary = match.group(2).strip()
                if 0 <= idx < len(articles):
                    summaries[articles[idx]['id']] = summary
                    current_idx = idx
        
        # 为未匹配到的文章设置默认值
        for article in articles:
            if article['id'] not in summaries:
                summaries[article['id']] = "（摘要解析失败）"
        
        return summaries
    
    except Exception as e:
        print(f"    ⚠️ 批量摘要出错：{e}")
        return {a['id']: "（摘要出错）" for a in articles}


def send_to_feishu(title: str, summary: str, link: str, source_name: str = ""):
    """推送到飞书"""
    if not FEISHU_WEBHOOK_URL:
        print("  ⚠️ 未配置飞书 Webhook，跳过推送")
        return False
    
    # 构建消息卡片
    message = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": f"📰 {title}"},
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": f"**来源：**{source_name}"}
                },
                {
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": summary}
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {"tag": "plain_text", "content": "查看原文 ↗"},
                            "url": link,
                            "type": "primary"
                        }
                    ]
                }
            ]
        }
    }
    
    try:
        response = requests.post(
            FEISHU_WEBHOOK_URL, 
            json=message, 
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                print("  ✅ 已推送到飞书")
                return True
            else:
                print(f"  ❌ 推送失败：{result.get('msg', '未知错误')}")
        else:
            print(f"  ❌ 推送失败：HTTP {response.status_code}")
    except Exception as e:
        print(f"  ❌ 推送出错：{e}")
    
    return False


def refresh_all():
    """刷新所有订阅（不单独推送，等汇总后一起推送）"""
    subscriptions = load_json(SUBSCRIPTIONS_FILE, {})
    articles = load_json(ARTICLES_FILE, {})
    
    if not subscriptions:
        return "📭 暂无订阅\n\n使用「订阅 <RSS地址>」添加订阅"
    
    print(f"🔄 开始刷新 {len(subscriptions)} 个订阅...")
    print()
    
    total_new = 0
    
    for url, info in subscriptions.items():
        print(f"📡 检查：{info['name']}")
        
        new_articles = fetch_new_articles(url)
        
        if not new_articles:
            print("  📭 暂无新文章")
            continue
        
        print(f"  📄 发现 {len(new_articles)} 篇新文章")
        
        # 记录文章（不生成摘要，不单独推送）
        for article in new_articles:
            articles[article['id']] = {
                "title": article['title'],
                "link": article['link'],
                "source": info['name'],
                "read": True,
                "read_at": datetime.now().isoformat()
            }
            total_new += 1
        
        print()
    
    save_json(ARTICLES_FILE, articles)
    
    if total_new > 0:
        return f"✅ 刷新完成，发现 {total_new} 篇新文章"
    else:
        return "📭 刷新完成，暂无新文章"


def generate_daily_report():
    """生成每日汇总分析报告"""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("⚠️  未配置 OPENAI_API_KEY，跳过汇总分析")
        print("💡 请在 Gateway 配置中添加：")
        print("   export OPENAI_API_KEY=\"你的智谱API Key\"")
        print("   export OPENAI_BASE_URL=\"https://open.bigmodel.cn/api/paas/v4\"")
        return None
    
    # 收集所有新文章
    articles = load_json(ARTICLES_FILE, {})
    new_articles = [a for a in articles.values() if a.get("read")]
    
    if not new_articles:
        print("📭 暂无新文章，跳过汇总分析")
        return None
    
    print(f"\n📊 正在生成汇总分析报告（共 {len(new_articles)} 篇文章）...")
    
    # 构建文章列表（只用标题和来源）
    articles_text = "\n\n".join([
        f"【{i+1}】{a['title']}\n来源：{a.get('source', '未知')}"
        for i, a in enumerate(new_articles[:30])  # 最多 30 篇
    ])
    
    # 调用智谱 API 生成分析报告
    try:
        base_url = os.getenv("OPENAI_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
        api_url = base_url if base_url.endswith("/chat/completions") else f"{base_url}/chat/completions"
        
        response = requests.post(
            api_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "glm-4-flash",
                "messages": [
                    {
                        "role": "system",
                        "content": """你是一个科技资讯分析助手。请根据用户提供的文章列表，生成一份简洁的分析报告。

报告格式：
# 📊 每日资讯汇总

## 🔥 热门话题
（列出 3-5 个最热门的话题，每个话题用一句话说明）

## 💡 关键趋势
（分析这些文章反映的技术/行业趋势，2-3 条）

## 📌 推荐阅读
（推荐 3-5 篇最值得阅读的文章，只写文章标题）

## 🎯 一句话总结
（用一句话总结今天的主要资讯）

要求：
- 简洁明了，避免冗余
- 突出重点，抓住趋势
- 不需要推荐理由"""
                    },
                    {
                        "role": "user",
                        "content": f"以下是今天收集的 {len(new_articles)} 篇科技资讯文章：\n\n{articles_text}"
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 800
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            report = result["choices"][0]["message"]["content"]
            
            # 添加原文链接列表
            links_section = "\n\n---\n\n## 📚 原文链接\n\n"
            for i, a in enumerate(new_articles[:20], 1):  # 最多 20 个链接
                links_section += f"{i}. [{a['title'][:40]}]({a['link']})\n"
            
            full_report = report + links_section
            print("✅ 汇总分析报告生成成功")
            return full_report
        else:
            print(f"⚠️  生成报告失败：{response.status_code}")
            print(f"   响应：{response.text}")
            return None
    except Exception as e:
        print(f"⚠️  生成报告出错：{e}")
        return None


def push_report_to_feishu(report):
    """推送汇总报告到飞书"""
    webhook_url = os.getenv("FEISHU_WEBHOOK_URL")
    
    if not webhook_url or not report:
        return
    
    print("\n📤 正在推送汇总报告到飞书...")
    
    # 今天的日期
    today = datetime.now().strftime("%Y-%m-%d")
    
    payload = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"📊 每日资讯汇总（{today}）"
                },
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": report
                },
                {
                    "tag": "note",
                    "elements": [
                        {
                            "tag": "plain_text",
                            "content": f"由 RSS Reader Skill 自动生成 | {datetime.now().strftime('%H:%M')}"
                        }
                    ]
                }
            ]
        }
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get("StatusCode") == 0:
                print("✅ 汇总报告已推送到飞书")
            else:
                print(f"⚠️  推送失败：{result}")
        else:
            print(f"⚠️  推送失败：{response.status_code}")
    except Exception as e:
        print(f"⚠️  推送出错：{e}")


def main():
    """主函数"""
    # 首次使用时初始化默认订阅
    if not SUBSCRIPTIONS_FILE.exists() or len(load_json(SUBSCRIPTIONS_FILE, {})) == 0:
        init_default_subscriptions()
    
    if len(sys.argv) < 2:
        print("RSS Reader + AI Summary")
        print()
        print("用法：python rss_reader.py <命令> [参数]")
        print()
        print("命令：")
        print("  订阅 <url> [名称]     添加 RSS 订阅")
        print("  取消订阅 <url>        取消订阅")
        print("  订阅列表              查看所有订阅")
        print("  立即刷新              检查新文章")
        print("  汇总                  生成 AI 汇总报告")
        print()
        print("环境变量：")
        print("  OPENAI_API_KEY       AI 摘要用（必需）")
        print("  OPENAI_BASE_URL      API 地址（默认：智谱）")
        print("  FEISHU_WEBHOOK_URL   飞书推送用（可选）")
        return
    
    command = sys.argv[1]
    
    if command == "订阅":
        if len(sys.argv) < 3:
            print("❌ 请提供 RSS 地址")
            print("用法：python rss_reader.py 订阅 <url> [名称]")
            return
        url = sys.argv[2]
        name = sys.argv[3] if len(sys.argv) >= 4 else None
        print(add_subscription(url, name))
    
    elif command == "取消订阅":
        if len(sys.argv) < 3:
            print("❌ 请提供 RSS 地址")
            return
        print(remove_subscription(sys.argv[2]))
    
    elif command in ["订阅列表", "列表", "list"]:
        print(list_subscriptions())
    
    elif command in ["立即刷新", "刷新", "refresh"]:
        print(refresh_all())
        
        # 刷新后自动生成汇总报告
        print("\n" + "="*60)
        report = generate_daily_report()
        if report:
            print(report)
            print("="*60)
            push_report_to_feishu(report)
    
    elif command in ["汇总", "报告", "report"]:
        # 手动生成汇总报告
        report = generate_daily_report()
        if report:
            print("\n" + "="*60)
            print(report)
            print("="*60)
            push_report_to_feishu(report)
    
    elif command == "help":
        print("RSS Reader + AI Summary")
        print()
        print("命令：")
        print("  订阅 <url> [名称]     添加 RSS 订阅")
        print("  取消订阅 <url>        取消订阅")
        print("  订阅列表              查看所有订阅")
        print("  立即刷新              检查新文章")
        print("  汇总                  生成 AI 汇总报告")
    
    else:
        print(f"❌ 未知命令：{command}")
        print("可用命令：订阅、取消订阅、订阅列表、立即刷新")


if __name__ == "__main__":
    main()
