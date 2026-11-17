#!/usr/bin/env python3
"""
SkillHub.cn 数据抓取脚本 v3.0
7 排行榜 + 11 分类搜索 + 记忆关键词搜索
目标覆盖：1000+ 条候选
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# 动态查找 skillhub CLI 路径（兼容不同安装位置）
SKILLHUB_BIN = shutil.which("skillhub") or os.environ.get("SKILLHUB_BIN", "skillhub")

RANKING_TYPES = ["hot", "newest", "trending", "featured", "recommended", "paid", "all"]

CATEGORY_SLUGS = {
    "knowledge-management": "知识管理",
    "office-efficiency": "办公效率",
    "content-creation": "内容创作",
    "data-analysis": "数据分析",
    "ai-agent": "AI Agent",
    "design-media": "设计多媒体",
    "professional": "行业专业",
    "dev-programming": "开发编程",
    "life-service": "生活服务",
    "it-ops-security": "IT运维安全",
    "business-ops": "商业运营",
}

MEMORY_SEARCH_KEYWORDS = ["飞书", "Python", "定时任务", "审计", "财务", "GitHub"]


def run_cli(args, timeout=30):
    """执行 skillhub CLI 命令"""
    cmd = [SKILLHUB_BIN] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return "", 1


def parse_json_output(output):
    """从 CLI 输出中提取 JSON"""
    if not output:
        return None
    # 直接尝试解析
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        pass
    # 找 JSON 起始
    for marker in ['{"skills"', '{"category"', '{"slug"', '{"query"', '[{']:
        idx = output.find(marker)
        if idx >= 0:
            try:
                return json.loads(output[idx:])
            except json.JSONDecodeError:
                # 尝试找到最后一个 } 的位置
                depth = 0
                end = idx
                for i in range(idx, len(output)):
                    if output[i] == '{' or output[i] == '[':
                        depth += 1
                    elif output[i] == '}' or output[i] == ']':
                        depth -= 1
                        if depth == 0:
                            end = i + 1
                            break
                try:
                    return json.loads(output[idx:end])
                except:
                    pass
    return None


def fetch_rankings():
    """抓取 7 大排行榜"""
    print("[1/3] 抓取排行榜...")
    all_skills = {}

    for rt in RANKING_TYPES:
        print(f"  {rt:15s}", end="", flush=True)
        output, rc = run_cli(["skill", "rankings", "--type", rt], timeout=45)
        data = parse_json_output(output)

        if data and isinstance(data, dict) and "skills" in data:
            skills = data["skills"]
        elif data and isinstance(data, list):
            skills = data
        else:
            print(f" FAIL")
            continue

        for s in skills:
            slug = s.get("slug", "")
            if slug and slug not in all_skills:
                all_skills[slug] = s
                all_skills[slug]["_rankings"] = [rt]
            elif slug and rt not in all_skills[slug].get("_rankings", []):
                all_skills[slug].setdefault("_rankings", []).append(rt)

        print(f" OK ({len(skills)})")
        time.sleep(0.3)

    return list(all_skills.values())


def fetch_category_search():
    """按 11 个分类搜索补充长尾"""
    print("\n[2/3] 按分类搜索...")
    all_skills = {}
    for cat_slug, cat_zh in CATEGORY_SLUGS.items():
        print(f"  {cat_zh:10s}", end="", flush=True)
        output, rc = run_cli(["search", cat_zh, "--json", "--search-limit", "20"], timeout=15)
        data = parse_json_output(output)

        if data and isinstance(data, dict) and "results" in data:
            results = data["results"]
        elif data and isinstance(data, list):
            results = data
        else:
            print(f" FAIL")
            continue

        for s in results:
            slug = s.get("slug", "")
            if slug and slug not in all_skills:
                all_skills[slug] = s
                all_skills[slug]["_source"] = "category_search"
                all_skills[slug]["_search_category"] = cat_slug

        print(f" OK ({len(results)})")
        time.sleep(0.3)

    return list(all_skills.values())


def fetch_keyword_search(keywords=None):
    """按记忆关键词精准搜索"""
    kws = keywords or MEMORY_SEARCH_KEYWORDS
    print(f"\n[3/3] 关键词搜索（{len(kws)} 个）...")
    all_skills = {}

    for kw in kws:
        print(f"  {kw:10s}", end="", flush=True)
        output, rc = run_cli(["search", kw, "--json", "--search-limit", "20"], timeout=15)
        data = parse_json_output(output)

        if data and isinstance(data, dict) and "results" in data:
            results = data["results"]
        elif data and isinstance(data, list):
            results = data
        else:
            print(f" FAIL")
            continue

        for s in results:
            slug = s.get("slug", "")
            if slug and slug not in all_skills:
                all_skills[slug] = s
                all_skills[slug]["_source"] = "keyword_search"
                all_skills[slug]["_search_keyword"] = kw

        print(f" OK ({len(results)})")
        time.sleep(0.3)

    return list(all_skills.values())


def normalize_skill(skill):
    """标准化技能数据"""
    labels = skill.get("labels", {})
    if isinstance(labels, str):
        try:
            labels = json.loads(labels)
        except:
            labels = {}

    return {
        "slug": skill.get("slug", ""),
        "name": skill.get("name", ""),
        "ownerName": skill.get("ownerName", ""),
        "version": skill.get("version", ""),
        "source": skill.get("source", ""),
        "category": skill.get("category", ""),
        "category_zh": CATEGORY_SLUGS.get(skill.get("category", ""), skill.get("category", "")),
        "subCategories": skill.get("subCategories", []),
        "description": skill.get("description", ""),
        "description_zh": skill.get("description_zh", ""),
        "downloads": skill.get("downloads", 0),
        "installs": skill.get("installs", 0),
        "stars": skill.get("stars", 0),
        "score": skill.get("score", 0),
        "requires_api_key": labels.get("requires_api_key", "false") == "true" if isinstance(labels, dict) else False,
        "verified": skill.get("verified", False),
        "claimable": skill.get("claimable", False),
        "created_at": skill.get("created_at", 0),
        "updated_at": skill.get("updated_at", 0),
        "homepage": skill.get("homepage", ""),
        "_rankings": skill.get("_rankings", []),
        "_source": skill.get("_source", "rankings"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/snapshots", help="输出目录")
    parser.add_argument("--date", default=None)
    args = parser.parse_args()

    date_str = args.date or datetime.now().strftime("%Y-%m-%d")

    # 1. 排行榜
    ranking_skills = fetch_rankings()

    # 2. 分类搜索
    category_skills = fetch_category_search()

    # 3. 关键词搜索
    keyword_skills = fetch_keyword_search()

    # 合并去重
    all_skills = {}
    for s in ranking_skills:
        slug = s.get("slug", "")
        if slug and slug not in all_skills:
            all_skills[slug] = normalize_skill(s)

    for s in category_skills:
        slug = s.get("slug", "")
        if slug and slug not in all_skills:
            all_skills[slug] = normalize_skill(s)
            all_skills[slug]["_source"] = "category_search"
        elif slug and slug in all_skills:
            # 补充分类搜索来源
            if "category_search" not in all_skills[slug].get("_source", ""):
                all_skills[slug]["_source"] = all_skills[slug].get("_source", "") + "+category_search"

    for s in keyword_skills:
        slug = s.get("slug", "")
        if slug and slug not in all_skills:
            all_skills[slug] = normalize_skill(s)
            all_skills[slug]["_source"] = "keyword_search"
        elif slug and slug in all_skills:
            all_skills[slug]["_source"] = all_skills[slug].get("_source", "") + "+keyword_search"

    skills = list(all_skills.values())
    print(f"\n合并去重后: {len(skills)} 个独立技能")

    # 保存
    output_path = Path(args.output) / f"{date_str}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    snapshot = {
        "snapshot_date": date_str,
        "fetched_at": datetime.now().isoformat(),
        "platform": "skillhub.cn",
        "total_count": len(skills),
        "source_breakdown": {
            "rankings_only": sum(1 for s in skills if "+" not in s.get("_source", "") and s.get("_source") == "rankings"),
            "with_category_search": sum(1 for s in skills if "category_search" in s.get("_source", "")),
            "with_keyword_search": sum(1 for s in skills if "keyword_search" in s.get("_source", "")),
        },
        "skills": skills
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    print(f"已保存: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
