"""
飞书日报推送模块
用法：python send_feishu.py [json_file]
"""

import json
import sys
import os
import requests
from pathlib import Path

# 配置
FEISHU_WEBHOOK = os.getenv("FEISHU_WEBHOOK_URL", "")
DEFAULT_REPORT = Path("data/daily/today.json")


def build_markdown_report(report: dict) -> str:
    """构建 Markdown 格式日报"""
    date = report.get("date", "今日")
    title = report.get("title", f"📅 科技日报 | {date}")
    sections = report.get("sections", {})
    
    md = f"""
{title}

---

## 🚀 今日重磅
"""
    
    # 重磅新闻
    for item in sections.get("重磅", []):
        md += f"- **{item.get('title', '未命名')}** 🔥🔥🔥\n"
        md += f"  - {item.get('summary', '')}\n"
        md += f"  - [链接]({item.get('url', '')})\n\n"
    
    if not sections.get("重磅"):
        md += "*暂无重磅新闻*\n\n"
    
    # 技术前沿
    md += "## 💡 技术前沿\n\n"
    for item in sections.get("技术前沿", []):
        md += f"- {item.get('title', '')}\n"
        md += f"  - [链接]({item.get('url', '')})\n\n"
    
    # 行业动态
    md += "## 🏢 行业动态\n\n"
    for item in sections.get("行业动态", []):
        md += f"- {item.get('title', '')}\n"
        md += f"  - [链接]({item.get('url', '')})\n\n"
    
    # AI 应用
    md += "## 🤖 AI 应用\n\n"
    for item in sections.get("AI 应用", []):
        md += f"- {item.get('title', '')}\n"
        md += f"  - [链接]({item.get('url', '')})\n\n"
    
    md += """
---
*本日报由 OpenClaw 自动聚合生成*
"""
    
    return md


def send_feishu_message(report_file: str = None):
    """发送日报到飞书"""
    
    # 读取报告
    file_path = report_file or os.getenv("REPORT_FILE", str(DEFAULT_REPORT))
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            report = json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] 报告文件不存在: {file_path}")
        return False
    except json.JSONDecodeError:
        print(f"[ERROR] 报告文件格式错误: {file_path}")
        return False
    
    # 构建消息
    md_content = build_markdown_report(report)
    
    # 消息体
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"📰 科技日报 | {report.get('date', '今日')}"
                }
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": md_content
                },
                {
                    "tag": "note",
                    "elements": [
                        {
                            "tag": "plain_text",
                            "content": f"共 {report.get('total', 0)} 条资讯 • OpenClaw 自动聚合"
                        }
                    ]
                }
            ]
        }
    }
    
    # 发送
    if not FEISHU_WEBHOOK:
        print("[WARN] FEISHU_WEBHOOK_URL 未配置，消息未发送")
        print("\n" + "=" * 50)
        print(md_content)
        print("=" * 50)
        return False
    
    try:
        resp = requests.post(
            FEISHU_WEBHOOK,
            json=payload,
            timeout=10
        )
        resp.raise_for_status()
        print(f"✅ 日报已发送到飞书 ({resp.status_code})")
        return True
    except Exception as e:
        print(f"[ERROR] 发送失败: {e}")
        return False


if __name__ == "__main__":
    report_file = sys.argv[1] if len(sys.argv) > 1 else None
    success = send_feishu_message(report_file)
    sys.exit(0 if success else 1)