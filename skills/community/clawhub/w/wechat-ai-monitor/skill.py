#!/usr/bin/env python3

# 微信公众号监控脚本（Python 版本，带 AI/科技筛选）
# 支持解析 RSS XML，提取过去24小时的文章

import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
import os
import re

# 配置文件路径
CONFIG_FILE = os.path.expanduser("~/.config/wechat-monitor/accounts.json")
OUTPUT_DIR = os.path.expanduser("~/.config/wechat-monitor/reports")

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 获取当前时间（带时区）
tz = timezone(timedelta(hours=8))  # 北京时间 UTC+8
now = datetime.now(tz)
hours_24_ago = now - timedelta(hours=24)

# AI/科技相关关键词
AI_KEYWORDS = [
    # AI 核心词汇
    'AI', '人工智能', '大模型', 'LLM', 'ChatGPT', 'GPT', 'Kimi', 'Claude',
    'DeepSeek', '文心一言', '通义千问', '智谱', '月之暗面', '豆包',
    'OpenAI', 'Anthropic', '模型', '训练', '推理', '微调', 'RAG',
    '智能体', 'Agent', 'Copilot', '助手', 'AIoT',

    # 机器学习/深度学习
    '机器学习', '深度学习', '神经网络', 'Transformer', 'Diffusion', '扩散模型',
    '强化学习', '监督学习', '无监督学习',

    # 智能硬件
    '智能硬件', 'AIoT', '物联网', 'IoT', '机器人', 'Robot', '人形机器人',
    '芯片', 'GPU', 'CPU', 'NPU', 'TPU', '算力', '服务器',
    '自动驾驶', '智能汽车', '智能驾驶', '激光雷达', 'LiDAR',
    '智能手表', '智能眼镜', 'AR', 'VR', 'XR', '脑机接口',
    '无人机', 'UAV', '智能音箱', '智能耳机', '智能穿戴',

    # 科技领域（适度放宽）
    '科技', '技术', '创新', '研发', 'R&D', '创业', '初创',
    '算法', '代码', '编程', '开发', '开源', 'Open Source',
    '数字化', '数字化转型', '云计算', 'Cloud', '大数据', 'Big Data',
    '区块链', 'Web3', '加密', '加密货币', 'Crypto',
    '5G', '6G', '卫星', '太空', 'Space', '航天',
    '量子', '量子计算', 'Quantum',

    # 企业/产品（AI 相关）
    '英伟达', 'NVIDIA', '黄仁勋', '华为', '小米', '百度', '阿里巴巴',
    '腾讯', '字节跳动', '抖音', 'TikTok', '苹果', 'Apple',
    'Google', '微软', 'Microsoft', 'Meta', 'Facebook',
]

# 函数：去除 HTML 标签
def strip_html(text):
    if not text:
        return ""
    # 去除 CDATA 标签
    text = re.sub(r'<!\[CDATA\[', '', text)
    text = re.sub(r'\]\]>', '', text)
    # 去除 HTML 标签
    text = re.sub(r'<[^>]+>', ' ', text)
    # 去除多余空格
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# 函数：检查文章是否与 AI/科技相关
def is_ai_related(title, summary):
    """检查标题和摘要是否包含 AI/科技相关关键词"""
    text_to_check = (title + " " + summary).lower()

    for keyword in AI_KEYWORDS:
        if keyword.lower() in text_to_check:
            return True

    return False

# 函数：解析 RSS 并提取过去24小时的文章
def parse_rss(rss_url, source_name):
    try:
        # 下载 RSS
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(rss_url, headers=headers, timeout=15)
        response.raise_for_status()

        # 解析 XML
        root = ET.fromstring(response.text)
        articles = []
        filtered_articles = []

        # 查找所有 item 元素
        for item in root.findall('.//item'):
            # 提取标题
            title_elem = item.find('title')
            title = strip_html(title_elem.text) if title_elem is not None else "无标题"

            # 提取链接
            link_elem = item.find('link')
            link = strip_html(link_elem.text) if link_elem is not None else "无链接"

            # 提取发布时间
            pubdate_elem = item.find('pubDate')
            pubdate = pubdate_elem.text if pubdate_elem is not None else ""
            article_time = None

            if pubdate:
                try:
                    article_time = datetime.strptime(pubdate, "%Y-%m-%d %H:%M:%S %z")
                except:
                    try:
                        article_time = datetime.strptime(pubdate, "%Y-%m-%d %H:%M:%S")
                    except:
                        article_time = None

            # 提取摘要
            description_elem = item.find('description')
            summary = strip_html(description_elem.text) if description_elem is not None else ""

            # 限制摘要长度
            if len(summary) > 500:
                summary = summary[:500] + "..."

            # 只保留过去24小时的文章
            if article_time and article_time >= hours_24_ago:
                articles.append({
                    'title': title,
                    'pubdate': pubdate,
                    'link': link,
                    'summary': summary
                })

        # 筛选 AI/科技相关文章
        for article in articles:
            if is_ai_related(article['title'], article['summary']):
                filtered_articles.append(article)

        return filtered_articles

    except Exception as e:
        print(f"*无法获取 {source_name} 的文章: {str(e)}")
        return []

# 主逻辑
def main():
    # 读取配置文件
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # 生成报告
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M')
    report_content = f"# {date_str} {time_str} 监控报告（AI/科技相关）\n\n"

    # 添加筛选说明
    report_content += "> 筛选条件：只显示与 AI、智能硬件、科技领域相关的文章\n\n"

    # 处理每个账号
    for account in config['accounts']:
        if not account.get('enabled', False):
            continue

        name = account['name']
        rss_url = account.get('rss_url', '')

        report_content += f"## {name}\n\n"

        if rss_url == "待填写":
            report_content += "*该账号的 RSS URL 未配置*\n\n"
            continue

        # 解析 RSS
        print(f"正在获取 {name} 的文章...")
        articles = parse_rss(rss_url, name)

        if not articles:
            report_content += "*过去24小时没有新文章*\n\n"
        else:
            for article in articles:
                report_content += f"### {article['title']}\n"
                report_content += f"**发布时间**: {article['pubdate']}\n"
                report_content += f"**链接**: {article['link']}\n"
                report_content += f"**摘要**: {article['summary']}\n\n"

    # 添加页脚
    report_content += "\n---\n*本报告由 Molty 自动生成* 🐍\n"

    # 保存报告
    output_file = os.path.join(OUTPUT_DIR, f"{date_str}-{time_str.replace(':', '-')}.md")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"报告已生成: {output_file}")
    print("\n报告内容：\n")
    print(report_content)

if __name__ == '__main__':
    main()
