#!/usr/bin/env python3
"""
GitHub Stars Analyzer — fetch_stars.py
用途：抓取指定 GitHub 用户所有 starred 仓库，按大类分组，生成标准化中文 Markdown 报告。

用法：
    python3 fetch_stars.py <用户名或主页URL> [--token <PAT>] [--output <文件路径>]

示例：
    python3 fetch_stars.py blckrabbit
    python3 fetch_stars.py https://github.com/blckrabbit?tab=stars
    python3 fetch_stars.py blckrabbit --token ghp_xxx --output report.md

依赖：
    pip install requests
"""

import sys
import re
import time
import argparse
from datetime import datetime

try:
    import requests
except ImportError:
    print("❌ 缺少依赖，请先运行：pip install requests")
    sys.exit(1)

# ─────────────────────────────────────────────
# 大类分类规则（按优先级排序，首次匹配即止）
# ─────────────────────────────────────────────
CATEGORIES = [
    ("🤖 人工智能与机器学习", [
        "ai", "ml", "machine-learning", "deep-learning", "llm", "nlp",
        "neural-network", "gpt", "pytorch", "tensorflow", "transformers",
        "diffusion", "stable-diffusion", "langchain", "openai", "chatgpt",
        "computer-vision", "reinforcement-learning", "rag",
    ]),
    ("🛠️ 开发工具与效率", [
        "cli", "tool", "productivity", "devtools", "vscode", "vim", "neovim",
        "ide", "automation", "workflow", "terminal", "shell", "zsh", "bash",
        "git", "github", "plugin", "extension",
    ]),
    ("🌐 前端与界面", [
        "frontend", "react", "vue", "angular", "svelte", "css", "html",
        "ui", "design", "javascript", "typescript", "nextjs", "nuxt",
        "tailwind", "animation", "web", "browser",
    ]),
    ("⚙️ 后端与框架", [
        "backend", "api", "rest", "graphql", "microservice", "server",
        "django", "flask", "fastapi", "express", "go", "rust", "java",
        "spring", "grpc", "websocket",
    ]),
    ("📦 基础设施与运维", [
        "devops", "docker", "kubernetes", "k8s", "ci-cd", "cloud", "aws",
        "gcp", "azure", "infra", "terraform", "ansible", "nginx", "linux",
        "monitoring", "logging", "observability",
    ]),
    ("🗄️ 数据库与数据", [
        "database", "sql", "nosql", "redis", "postgres", "postgresql",
        "mongodb", "mysql", "data", "analytics", "etl", "pipeline",
        "spark", "kafka", "elasticsearch", "vector-database",
    ]),
    ("🔒 安全与隐私", [
        "security", "hacking", "pentest", "ctf", "crypto", "privacy",
        "auth", "oauth", "vulnerability", "exploit", "reverse-engineering",
        "malware", "forensics",
    ]),
    ("📚 学习资源与文档", [
        "awesome", "tutorial", "learning", "course", "book", "guide",
        "roadmap", "cheatsheet", "interview", "algorithm", "leetcode",
        "education", "documentation", "notes",
    ]),
    ("🎮 游戏与创意", [
        "game", "gamedev", "graphics", "animation", "art", "creative",
        "shader", "opengl", "unity", "godot", "pixel-art", "generative",
    ]),
]

LANG_CATEGORIES = {
    "Python": "🐍 Python 生态",
}


def parse_username(raw: str) -> str:
    """从 URL 或字符串中提取 GitHub 用户名"""
    raw = raw.strip().rstrip("/")
    m = re.search(r"github\.com/([A-Za-z0-9_.-]+)", raw)
    if m:
        return m.group(1)
    if raw.startswith("@"):
        return raw[1:]
    return raw


def classify(repo: dict) -> str:
    """根据 topics 和语言对仓库分大类"""
    topics = [t.lower() for t in (repo.get("topics") or [])]
    lang = repo.get("language") or ""
    name_desc = (
        (repo.get("name") or "") + " " + (repo.get("description") or "")
    ).lower()

    for category, keywords in CATEGORIES:
        for kw in keywords:
            if kw in topics or kw in name_desc:
                return category

    if lang in LANG_CATEGORIES:
        return LANG_CATEGORIES[lang]

    return "📌 其他"


def fetch_starred(username: str, token: str = None) -> list:
    """调用 GitHub API 分页抓取所有 starred 仓库"""
    headers = {"Accept": "application/vnd.github.star+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    repos = []
    page = 1

    while True:
        url = f"https://api.github.com/users/{username}/starred"
        params = {"per_page": 100, "page": page}
        print(f"  📄 第 {page} 页...", end=" ", flush=True)

        try:
            resp = requests.get(url, headers=headers, params=params, timeout=20)
        except requests.exceptions.ConnectionError:
            print("\n❌ 网络连接失败：无法访问 api.github.com")
            print("   提示：请在本地终端运行此脚本，确保网络可访问 GitHub（可开启 VPN）")
            sys.exit(1)

        if resp.status_code == 404:
            print(f"\n❌ 用户 '{username}' 不存在，请检查用户名")
            sys.exit(1)

        if resp.status_code == 403:
            reset_ts = resp.headers.get("X-RateLimit-Reset", "")
            wait = max(0, int(reset_ts) - int(time.time())) if reset_ts else 60
            print(f"\n⚠️  GitHub API 请求超限，请等待 {wait} 秒后重试")
            print("   提示：使用 --token 参数传入 GitHub PAT 可将限额提升至 5000次/小时")
            print("   生成 Token：GitHub → Settings → Developer settings → Personal access tokens → 无需勾选任何权限")
            sys.exit(1)

        resp.raise_for_status()
        data = resp.json()

        if not data:
            print("完成")
            break

        for item in data:
            repo = item.get("repo") or item
            repos.append({
                "name":        repo.get("full_name", ""),
                "url":         repo.get("html_url", ""),
                "description": (repo.get("description") or "").strip() or "暂无描述",
                "language":    repo.get("language") or "-",
                "stars":       repo.get("stargazers_count", 0),
                "forks":       repo.get("forks_count", 0),
                "topics":      repo.get("topics") or [],
                "license":     (repo.get("license") or {}).get("spdx_id") or "-",
                "archived":    repo.get("archived", False),
                "starred_at":  (item.get("starred_at") or repo.get("updated_at") or "")[:10],
                "category":    classify(repo),
            })

        print(f"获得 {len(data)} 个（累计 {len(repos)} 个）")

        if len(data) < 100:
            break
        page += 1
        time.sleep(0.3)

    return repos


def render_report(username: str, repos: list) -> str:
    """按模板渲染标准化中文 Markdown 报告"""
    today = datetime.now().strftime("%Y-%m-%d")
    total = len(repos)
    langs = sorted({r["language"] for r in repos if r["language"] != "-"})
    total_stars = sum(r["stars"] for r in repos)
    total_forks = sum(r["forks"] for r in repos)
    archived_count = sum(1 for r in repos if r["archived"])

    # ── 语言统计 ──
    lang_counts: dict[str, int] = {}
    for r in repos:
        if r["language"] != "-":
            lang_counts[r["language"]] = lang_counts.get(r["language"], 0) + 1
    top_langs = sorted(lang_counts.items(), key=lambda x: -x[1])

    # ── 大类统计 ──
    all_categories = [c[0] for c in CATEGORIES] + list(LANG_CATEGORIES.values()) + ["📌 其他"]
    # 保持顺序去重
    seen = set()
    ordered_cats = []
    for c in all_categories:
        if c not in seen:
            seen.add(c)
            ordered_cats.append(c)

    cat_groups: dict[str, list] = {c: [] for c in ordered_cats}
    for r in repos:
        cat_groups.setdefault(r["category"], []).append(r)
    # 只保留有数据的大类
    active_cats = [(c, cat_groups[c]) for c in ordered_cats if cat_groups.get(c)]

    lines = []

    # ════════════════════════════════════════
    # 标题 & 摘要
    # ════════════════════════════════════════
    lines += [
        f"# {username} 的 GitHub Stars 收藏报告",
        "",
        f"> **生成时间**：{today}　｜　**Stars 总数**：{total} 个　｜　"
        f"**涉及语言**：{len(langs)} 种　｜　**项目大类**：{len(active_cats)} 类　｜　"
        f"**累计获赞**：{total_stars:,}",
        "",
        "---",
        "",
    ]

    # ════════════════════════════════════════
    # 一、总览统计
    # ════════════════════════════════════════
    lines += [
        "## 一、总览统计",
        "",
        "| 统计项 | 数值 |",
        "| --- | ---: |",
        f"| Stars 总数 | {total} 个 |",
        f"| 涉及编程语言 | {len(langs)} 种 |",
        f"| 项目大类数 | {len(active_cats)} 类 |",
        f"| 已归档项目 | {archived_count} 个 |",
        f"| 累计获赞（Stars 之和） | {total_stars:,} |",
        f"| 累计 Fork 数之和 | {total_forks:,} |",
        "",
        "---",
        "",
    ]

    # ════════════════════════════════════════
    # 二、语言分布
    # ════════════════════════════════════════
    lines += [
        "## 二、语言分布",
        "",
        "| 排名 | 语言 | 仓库数 | 占比 |",
        "| ---: | --- | ---: | ---: |",
    ]
    for i, (lang, cnt) in enumerate(top_langs, 1):
        pct = cnt / total * 100
        lines.append(f"| {i} | {lang} | {cnt} | {pct:.1f}% |")
    lines += ["", "---", ""]

    # ════════════════════════════════════════
    # 三、大类分布
    # ════════════════════════════════════════
    lines += [
        "## 三、大类分布",
        "",
        "| 大类 | 仓库数 | 占比 |",
        "| --- | ---: | ---: |",
    ]
    for cat, group in active_cats:
        pct = len(group) / total * 100
        lines.append(f"| {cat} | {len(group)} | {pct:.1f}% |")
    lines += ["", "---", ""]

    # ════════════════════════════════════════
    # 四、完整收藏列表
    # ════════════════════════════════════════
    lines += [
        "## 四、完整收藏列表",
        "",
        "| # | 项目名称 | 描述 | 语言 | ⭐ Stars | 🍴 Forks | 大类 | 收藏时间 |",
        "| ---: | --- | --- | --- | ---: | ---: | --- | --- |",
    ]
    for i, r in enumerate(repos, 1):
        name_cell = f"[{r['name']}]({r['url']})"
        desc = r["description"].replace("|", "\\|")[:60]
        archived_mark = " 🗃️" if r["archived"] else ""
        lines.append(
            f"| {i} | {name_cell}{archived_mark} | {desc} | {r['language']} "
            f"| {r['stars']:,} | {r['forks']:,} | {r['category']} | {r['starred_at']} |"
        )
    lines += ["", "---", ""]

    # ════════════════════════════════════════
    # 五、分类详情
    # ════════════════════════════════════════
    lines += ["## 五、分类详情", ""]

    for cat, group in active_cats:
        lines += [
            f"### {cat}（{len(group)} 个）",
            "",
            "| # | 项目 | 描述 | 语言 | Stars |",
            "| ---: | --- | --- | --- | ---: |",
        ]
        for j, r in enumerate(sorted(group, key=lambda x: -x["stars"]), 1):
            name_cell = f"[{r['name']}]({r['url']})"
            desc = r["description"].replace("|", "\\|")[:55]
            lines.append(f"| {j} | {name_cell} | {desc} | {r['language']} | {r['stars']:,} |")
        lines += ["", "---", ""]

    lines += [
        f"*由 GitHub Stars Analyzer 自动生成 · {today}*",
        "",
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="GitHub Stars Analyzer — 生成标准化中文收藏报告",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("username", help="GitHub 用户名或主页 URL")
    parser.add_argument("--token", default=None, help="GitHub Personal Access Token（可选）")
    parser.add_argument("--output", default=None, help="输出文件路径（默认：<用户名>_github_stars.md）")
    args = parser.parse_args()

    username = parse_username(args.username)
    output = args.output or f"{username}_github_stars.md"

    print(f"🚀 开始抓取 {username} 的 GitHub Stars...\n")
    repos = fetch_starred(username, token=args.token)

    print(f"\n✅ 共抓取 {len(repos)} 个仓库，正在生成报告...")
    report = render_report(username, repos)

    with open(output, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"📄 报告已保存：{output}")
    print(f"\n📊 摘要：{len(repos)} 个项目 | {sum(r['stars'] for r in repos):,} 累计 Stars")


if __name__ == "__main__":
    main()
