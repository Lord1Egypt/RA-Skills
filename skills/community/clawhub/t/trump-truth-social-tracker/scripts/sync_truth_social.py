#!/usr/bin/env python3
"""
同步特朗普 Truth Social 帖子到本地 SQLite 数据库

功能：
1. 从 CNN 归档 JSON 获取数据
2. Upsert 到 SQLite（id 作为主键）
3. 只保存有内容的帖子
4. 增量同步模式：只同步新增帖子
5. 金融市场影响检测：检测可能影响市场的帖子并输出预警
6. 将预警信息写入 memory 文件

使用：
    python3 sync_truth_social.py                     # 全量同步
    python3 sync_truth_social.py --incremental 10    # 增量同步，最多10条新帖子
    python3 sync_truth_social.py --incremental 10 --alert --write-memory  # 增量同步+预警+写入memory

默认：
    db-path: ~/.openclaw/workspace/temp/trump_truth_social.sqlite
    json-url: https://ix.cnn.io/data/truth-social/truth_archive.json
"""

import argparse
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


DEFAULT_DB_PATH = Path.home() / ".openclaw" / "workspace" / "temp" / "trump_truth_social.sqlite"
DEFAULT_JSON_URL = "https://ix.cnn.io/data/truth-social/truth_archive.json"


# 金融市场影响关键词（英文为主，因为 Trump 帖子多为英文）
MARKET_IMPACT_KEYWORDS = {
    # 关税相关
    "tariff": "关税",
    "tariffs": "关税",
    "加征关税": "关税",
    
    # 谈判相关
    "negotiation": "谈判",
    "negotiate": "谈判",
    "negotiating": "谈判",
    "deal": "协议/谈判",
    "agreement": "协议",
    "trade deal": "贸易协议",
    "谈判": "谈判",
    "谈判破裂": "谈判破裂",
    "talks": "谈判",
    
    # 军事相关
    "military": "军事",
    "strike": "打击",
    "attack": "攻击",
    "blockade": "封锁",
    "war": "战争",
    "WAR": "战争",
    "obliterated": "摧毁",
    "blown up": "炸毁",
    "destroyed": "摧毁",
    "nuclear": "核武器",
    "NUCLEAR": "核武器",
    "missile": "导弹",
    "bomb": "炸弹",
    "invasion": "入侵",
    "制裁": "制裁",
    "sanctions": "制裁",
    
    # 美联储相关
    "Fed": "美联储",
    "Federal Reserve": "美联储",
    "interest rate": "利率",
    "rates": "利率",
    "cut rates": "降息",
    "raise rates": "加息",
    "美联储": "美联储",
    "利率": "利率",
    "降息": "降息",
    
    # 国家/地区（可能触发市场波动）
    "China": "中国",
    "Iran": "伊朗",
    "Russia": "俄罗斯",
    "Russia's": "俄罗斯",
    "Mexican": "墨西哥",
    "Mexico": "墨西哥",
    "Canada": "加拿大",
    "Canada's": "加拿大",
    "European Union": "欧盟",
    "EU": "欧盟",
    "Japan": "日本",
    "Japan's": "日本",
    "South Korea": "韩国",
    "Taiwan": "台湾",
    "Venezuela": "委内瑞拉",
    
    # 行动指令
    "must": "必须",
    "should": "应该",
    "immediately": "立即",
    "Effective immediately": "立即生效",
    "deadline": "最后期限",
    
    # 能源/大宗商品
    "oil": "石油",
    "Oil": "石油",
    "OPEC": "OPEC",
    "gas": "天然气",
    "energy": "能源",
    "Hormuz": "霍尔木兹海峡",
    "Strait of Hormuz": "霍尔木兹海峡",
}


def create_table(conn: sqlite3.Connection) -> None:
    """创建数据表"""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS truth_posts (
            id TEXT PRIMARY KEY,
            created_at TEXT,
            content TEXT NOT NULL,
            url TEXT,
            replies_count INTEGER DEFAULT 0,
            reblogs_count INTEGER DEFAULT 0,
            favourites_count INTEGER DEFAULT 0,
            media TEXT,
            fetched_at TEXT
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON truth_posts(created_at)")
    conn.commit()


def fetch_json(url: str) -> list:
    """获取 JSON 数据"""
    print(f"正在获取: {url}")
    try:
        with urlopen(url, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
            print(f"获取到 {len(data)} 条记录")
            return data
    except (URLError, HTTPError) as e:
        print(f"错误: 无法获取数据 - {e}")
        sys.exit(1)


def get_latest_post_time(conn: sqlite3.Connection) -> str:
    """获取数据库中最新帖子的时间"""
    row = conn.execute(
        "SELECT created_at FROM truth_posts ORDER BY created_at DESC LIMIT 1"
    ).fetchone()
    return row[0] if row else None


def analyze_market_impact(content: str) -> list:
    """分析帖子内容是否可能影响金融市场"""
    alerts = []
    content_lower = content.lower()
    
    for keyword, category in MARKET_IMPACT_KEYWORDS.items():
        # 不区分大小写搜索
        if keyword.lower() in content_lower:
            # 获取上下文（关键词前后50字符）
            idx = content_lower.find(keyword.lower())
            start = max(0, idx - 50)
            end = min(len(content), idx + len(keyword) + 50)
            context = content[start:end]
            
            alerts.append({
                "keyword": keyword,
                "category": category,
                "context": context.strip()
            })
    
    return alerts


def upsert_posts(conn: sqlite3.Connection, posts: list, incremental: bool = False, max_new: int = 10) -> tuple[int, int, list]:
    """
    Upsert 帖子数据
    返回: (插入数, 跳过数, 新增帖子列表)
    """
    fetched_at = datetime.utcnow().isoformat() + "Z"
    
    inserted = 0
    skipped = 0
    new_posts = []
    
    # 增量模式下，获取最新帖子时间
    latest_post_time = None
    if incremental:
        latest_post_time = get_latest_post_time(conn)
    
    for post in posts:
        content = post.get("content", "")
        post_id = post.get("id")
        post_time = post.get("created_at")
        
        # 只保存有内容的帖子
        if not content or content.strip() == "":
            skipped += 1
            continue
        
        # 增量模式：只同步比数据库中最新帖子更晚的帖子
        if incremental and latest_post_time:
            if post_time and post_time <= latest_post_time:
                continue
        
        # 增量模式：限制新增数量
        if incremental and len(new_posts) >= max_new:
            break
        
        media = json.dumps(post.get("media", [])) if post.get("media") else None
        
        conn.execute("""
            INSERT OR REPLACE INTO truth_posts 
            (id, created_at, content, url, replies_count, reblogs_count, favourites_count, media, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            post.get("id"),
            post.get("created_at"),
            content,
            post.get("url"),
            post.get("replies_count", 0),
            post.get("reblogs_count", 0),
            post.get("favourites_count", 0),
            media,
            fetched_at
        ))
        inserted += 1
        new_posts.append(post)
    
    conn.commit()
    return inserted, skipped, new_posts


def get_stats(conn: sqlite3.Connection) -> dict:
    """获取数据库统计信息"""
    stats = {}
    
    stats["total_posts"] = conn.execute("SELECT COUNT(*) FROM truth_posts").fetchone()[0]
    
    # 最新帖子
    row = conn.execute("SELECT created_at, content FROM truth_posts ORDER BY created_at DESC LIMIT 1").fetchone()
    if row:
        stats["latest_post_time"] = row[0]
        stats["latest_post_preview"] = row[1][:100] if len(row[1]) > 100 else row[1]
    
    # 最早帖子
    row = conn.execute("SELECT created_at FROM truth_posts ORDER BY created_at ASC LIMIT 1").fetchone()
    if row:
        stats["earliest_post_time"] = row[0]
    
    # 互动统计
    stats["total_replies"] = conn.execute("SELECT SUM(replies_count) FROM truth_posts").fetchone()[0] or 0
    stats["total_reblogs"] = conn.execute("SELECT SUM(reblogs_count) FROM truth_posts").fetchone()[0] or 0
    stats["total_favourites"] = conn.execute("SELECT SUM(favourites_count) FROM truth_posts").fetchone()[0] or 0
    
    return stats


def format_alert_message(post: dict, alerts: list) -> str:
    """格式化预警消息"""
    created_at = post.get("created_at", "")
    content = post.get("content", "")
    url = post.get("url", "")
    
    # 解析时间
    try:
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        time_str = dt.strftime("%Y-%m-%d %H:%M UTC")
    except:
        time_str = created_at
    
    # 关键词摘要
    keywords = [a["category"] for a in alerts]
    keyword_str = ", ".join(set(keywords))
    
    # 内容截取
    content_preview = content[:300] if len(content) > 300 else content
    
    msg = f"""🚨 **金融市场预警 - Trump Truth Social**

**时间**: {time_str}
**触发关键词**: {keyword_str}

**帖子内容**:
{content_preview}

**原文链接**: {url}
"""
    return msg


def write_alert_to_report(alerts: list) -> None:
    """将预警信息追加到报告文件"""
    report_dir = Path.home() / ".openclaw" / "workspace" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_file = report_dir / "trump_truth_social_alerts.md"
    
    # 如果文件不存在，创建并写入标题
    if not report_file.exists():
        header = "# Trump Truth Social 金融市场预警报告\n\n\n"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(header)
    
    # 格式化预警内容
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"## 预警 [{timestamp}]",
        ""
    ]
    
    for alert in alerts:
        lines.append(alert["message"])
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # 追加到文件
    with open(report_file, "a", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"预警已写入: {report_file}")


def main():
    parser = argparse.ArgumentParser(description="同步 Trump Truth Social 帖子")
    parser.add_argument("--db-path", default=str(DEFAULT_DB_PATH), help="SQLite 数据库路径")
    parser.add_argument("--json-url", default=DEFAULT_JSON_URL, help="JSON 数据 URL")
    parser.add_argument("--incremental", type=int, default=0, help="增量同步模式，指定最多新增帖子数")
    parser.add_argument("--alert", action="store_true", help="检测金融市场影响并输出预警")
    parser.add_argument("--output-json", action="store_true", help="以 JSON 格式输出结果（便于程序解析）")
    parser.add_argument("--write-report", action="store_true", help="将预警信息写入报告文件")
    args = parser.parse_args()
    
    db_path = Path(args.db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not args.output_json:
        print(f"数据库路径: {db_path}")
    
    # 连接数据库
    conn = sqlite3.connect(db_path)
    create_table(conn)
    
    # 获取数据
    posts = fetch_json(args.json_url)
    
    # Upsert
    incremental_mode = args.incremental > 0
    inserted, skipped, new_posts = upsert_posts(conn, posts, incremental=incremental_mode, max_new=args.incremental)
    
    # 分析新帖子的市场影响
    market_alerts = []
    if args.alert and new_posts:
        for post in new_posts:
            content = post.get("content", "")
            alerts = analyze_market_impact(content)
            if alerts:
                market_alerts.append({
                    "post": post,
                    "alerts": alerts,
                    "message": format_alert_message(post, alerts)
                })
    
    # 写入报告文件
    if args.write_report and market_alerts:
        write_alert_to_report(market_alerts)
    
    # 输出结果
    if args.output_json:
        result = {
            "success": True,
            "incremental": incremental_mode,
            "inserted": inserted,
            "skipped": skipped,
            "new_posts_count": len(new_posts),
            "market_alerts_count": len(market_alerts),
            "market_alerts": market_alerts if market_alerts else None,
            "report_written": args.write_report and len(market_alerts) > 0
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"插入/更新: {inserted} 条, 跳过（无内容）: {skipped} 条")
        if incremental_mode:
            print(f"新增帖子: {len(new_posts)} 条")
        
        # 统计
        stats = get_stats(conn)
        print("\n=== 数据库统计 ===")
        print(f"总帖子数: {stats['total_posts']}")
        print(f"时间范围: {stats.get('earliest_post_time', 'N/A')} ~ {stats.get('latest_post_time', 'N/A')}")
        print(f"总互动: 回复 {stats['total_replies']}, 转发 {stats['total_reblogs']}, 点赞 {stats['total_favourites']}")
        
        # 预警输出
        if market_alerts:
            print("\n" + "=" * 50)
            print("🚨 金融市场影响预警")
            print("=" * 50)
            for alert in market_alerts:
                print(alert["message"])
                print("-" * 30)
    
    conn.close()
    
    if not args.output_json:
        print("\n同步完成!")
    
    # 返回预警数量（供脚本调用）
    return len(market_alerts)


if __name__ == "__main__":
    main()