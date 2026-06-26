# -*- coding: utf-8 -*-
"""
自动归纳分类脚本 v1.0.0
从用户收藏标题中自动发现自然分类体系

用法：
    python auto_discover.py                    # 从 favorites_all.csv 采样，输出 user_categories.json
    python auto_discover.py --sample 1000      # 指定采样数量
    python auto_discover.py --input xxx.csv    # 指定输入文件
    python auto_discover.py --output xxx.json  # 指定输出文件
    python auto_discover.py --min-categories 5 --max-categories 20  # 类别数量范围

输出格式（user_categories.json）：
{
  "categories": [
    {"name": "生物医药", "description": "药物研发、临床试验...", "keywords": ["创新药", "ADC", ...]},
    ...
  ],
  "meta": {"sample_size": 500, "total_articles": 32333, "created_at": "2026-04-27"}
}
"""

import os
import sys
import csv
import json
import random
import argparse
import urllib.request
import urllib.error
from datetime import datetime
from typing import List, Dict, Any, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "exported_favorites")

# ===== 安全模式 =====
SAFE_MODE = os.environ.get("SAFE_MODE", "").lower() in ("1", "true", "yes")
if SAFE_MODE:
    print("[SAFE_MODE] 网络功能已禁用，自动归纳不可用")
    sys.exit(1)

# ===== 配置 =====
LLM_API_KEY = os.environ.get("LLM_API_KEY", "")
LLM_API_URL = os.environ.get("LLM_API_URL", "https://openrouter.ai/api/v1/chat/completions")
LLM_MODEL = os.environ.get("LLM_MODEL", "deepseek/deepseek-chat")


def parse_args():
    parser = argparse.ArgumentParser(description="自动归纳分类体系")
    parser.add_argument("--sample", type=int, default=500, help="采样数量（默认 500）")
    parser.add_argument("--input", type=str, default=None, help="输入 CSV 路径")
    parser.add_argument("--output", type=str, default=None, help="输出 JSON 路径")
    parser.add_argument("--min-categories", type=int, default=8, help="最小类别数（默认 8）")
    parser.add_argument("--max-categories", type=int, default=15, help="最大类别数（默认 15）")
    return parser.parse_args()


def load_articles(input_path: str) -> List[Dict[str, str]]:
    """加载收藏数据"""
    articles = []
    with open(input_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            articles.append({
                "title": row.get("title", "").strip(),
                "source": row.get("source_account", row.get("source", "")).strip(),
            })
    return articles


def sample_articles(articles: List[Dict[str, str]], n: int) -> List[Dict[str, str]]:
    """随机采样"""
    if len(articles) <= n:
        return articles
    return random.sample(articles, n)


def build_discover_prompt(
    articles: List[Dict[str, str]],
    min_cat: int,
    max_cat: int
) -> str:
    """构建归纳 prompt"""
    # 格式化标题列表
    titles_text = "\n".join([
        f"{i+1}. {a['title']}" + (f"（来源：{a['source']}）" if a['source'] else "")
        for i, a in enumerate(articles)
    ])

    return f"""你是一个专业的内容分类专家。以下是用户微信收藏的文章标题样本（{len(articles)} 条）。

请分析这些标题，归纳出 {min_cat}-{max_cat} 个自然分类。要求：
1. 每个分类名称用 2-4 个中文字符
2. 每个分类给出简短描述（10-20 字）
3. 每个分类列出 10-20 个代表性关键词/短语

标题列表：
{titles_text}

请以 JSON 格式输出：
{{
  "categories": [
    {{"name": "分类名", "description": "简短描述", "keywords": ["关键词1", "关键词2", ...]}},
    ...
  ],
  "reasoning": "归纳思路说明"
}}

只输出 JSON，不要有其他内容。"""


def call_llm(prompt: str) -> Optional[Dict[str, Any]]:
    """调用 LLM API"""
    if not LLM_API_KEY:
        print("[ERROR] LLM_API_KEY 环境变量未设置")
        return None

    payload = {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 2000,
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            LLM_API_URL,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {LLM_API_KEY}",
                "HTTP-Referer": "https://github.com/qclaw/wechat-favorites",
                "X-Title": "QClaw Favorites Category Discovery"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            if resp.status != 200:
                print(f"[ERROR] API 返回 {resp.status}")
                return None
            result = json.loads(resp.read().decode("utf-8"))
            content = result["choices"][0]["message"]["content"]
            return parse_llm_response(content)
    except Exception as e:
        print(f"[ERROR] LLM 调用失败: {e}")
        return None


def parse_llm_response(text: str) -> Optional[Dict[str, Any]]:
    """解析 LLM 返回"""
    try:
        text = text.strip()
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            text = text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            text = text[start:end].strip()

        result = json.loads(text)

        # 验证格式
        if "categories" not in result:
            return None

        for cat in result["categories"]:
            if "name" not in cat or "keywords" not in cat:
                return None
            # 确保 keywords 是列表
            if isinstance(cat["keywords"], str):
                cat["keywords"] = [k.strip() for k in cat["keywords"].split("、") if k.strip()]
            cat["keywords"] = list(cat["keywords"])[:20]  # 最多 20 个关键词

        return result
    except Exception as e:
        print(f"[ERROR] 解析失败: {e}")
        return None


def main():
    args = parse_args()

    print("=" * 60)
    print("  自动归纳分类体系 v1.0.0")
    print("=" * 60)

    input_path = args.input or os.path.join(OUTPUT_DIR, "favorites_all.csv")
    output_path = args.output or os.path.join(OUTPUT_DIR, "user_categories.json")

    if not os.path.exists(input_path):
        print(f"[ERROR] 输入文件不存在: {input_path}")
        sys.exit(1)

    # 加载数据
    print(f"\n[1/4] 加载收藏数据...")
    articles = load_articles(input_path)
    print(f"      共 {len(articles)} 条")

    # 采样
    print(f"\n[2/4] 随机采样 {args.sample} 条...")
    sample = sample_articles(articles, args.sample)
    print(f"      实际采样 {len(sample)} 条")

    # 调用 LLM 归纳
    print(f"\n[3/4] 调用 LLM 归纳分类（{args.min_categories}-{args.max_categories} 个类别）...")
    prompt = build_discover_prompt(sample, args.min_categories, args.max_categories)
    result = call_llm(prompt)

    if not result:
        print("[ERROR] 归纳失败")
        sys.exit(1)

    categories = result.get("categories", [])
    print(f"      归纳出 {len(categories)} 个分类")

    # 构建输出
    output = {
        "categories": categories,
        "meta": {
            "source": "auto_discover",
            "sample_size": len(sample),
            "total_articles": len(articles),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    }

    # 保存
    print(f"\n[4/4] 保存到 {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # 打印结果
    print(f"\n{'=' * 60}")
    print("归纳结果：")
    print("=" * 60)
    for i, cat in enumerate(categories, 1):
        print(f"\n{i}. {cat['name']}")
        print(f"   描述：{cat.get('description', '-')}")
        keywords = cat.get("keywords", [])
        if keywords:
            print(f"   关键词（{len(keywords)} 个）：{', '.join(keywords[:10])}" + ("..." if len(keywords) > 10 else ""))

    print(f"\n已保存: {output_path}")

    if "reasoning" in result:
        print(f"\n归纳思路：{result['reasoning']}")


if __name__ == "__main__":
    main()
