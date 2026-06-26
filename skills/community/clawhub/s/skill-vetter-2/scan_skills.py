#!/usr/bin/env python3
"""
技能安全审计脚本 v3 — 完善版
扫描 /workspace/skills/ 目录，输出 Markdown + JSON 双报告，支持白名单过滤
"""
import os, json, re
from datetime import datetime
from pathlib import Path

SKILLS_DIR = "/workspace/skills"
REPORT_FILE = "/workspace/技能安全审计报告.md"
EXCLUDE_SELF = os.path.abspath(__file__)
EXCLUDE_PATTERNS = ["技能安全审计报告", "__pycache__", ".git", "node_modules"]

# 分级关键词 + 修复建议
SUSPICIOUS = {
    "严重": [
        ("eval(",         "eval() 可执行任意代码，建议用 json.loads / ast.literal_eval 替代"),
        ("exec(",         "exec() 可执行任意代码，禁止在生产环境使用"),
        ("os.system",    "os.system() 可执行 shell 命令，建议用 subprocess.run([...], shell=False)"),
        ("os.popen",      "os.popen() 存在命令注入风险，建议用 subprocess.PIPE"),
        ("subprocess.call","subprocess.call 已废弃，建议用 subprocess.run"),
        ("subprocess.Popen","subprocess.Popen 需确认输入可控，建议加 shlex.quote"),
        ("__import__",    "__import__ 动态导入有安全风险，建议显式 import"),
        ("importlib",     "importlib 可动态执行代码，确认用途后使用"),
        ("pty.spawn",     "pty.spawn 创建伪终端，避免在服务器环境使用"),
    ],
    "高危": [
        ("requests.get(",   "requests.get 发起网络请求，确认目标地址可信"),
        ("requests.post(",  "requests.post 提交数据，确认目标地址可信且使用 HTTPS"),
        ("urllib.request",  "urllib.request 发起网络请求，确认目标地址可信"),
        ("urllib2",         "urllib2 为 Python2 遗留库，建议用 urllib.request"),
        ("http.client",     "http.client 底层 HTTP 库，注意异常处理"),
        ("socket.create_connection","socket 网络连接，确认用途后使用"),
        ("curl ",           "curl 命令行工具，确认参数来源可信"),
        ("wget ",           "wget 下载文件，确认 URL 可信，避免自动执行"),
        ("httpx",           "httpx 异步 HTTP 库，确认目标地址可信"),
        ("aiohttp",         "aiohttp 异步 HTTP，确认用途"),
    ],
    "中危": [
        ("chmod ",    "chmod 修改权限，生产环境谨慎操作"),
        ("chown ",    "chown 修改所有者，需 root 权限"),
        ("sudo ",     "sudo 提权命令，确认必要性"),
        ("chattr ",   "chattr 修改文件属性，需 root 权限"),
        (".bashrc",   ".bashrc 涉及 Shell 配置，确认来源可信"),
        ("/etc/passwd","读取系统账户文件，确认用途"),
        ("/etc/shadow","读取密码哈希文件，禁止在外部传输"),
        (".ssh/",     "涉及 SSH 密钥目录，确认用途后使用"),
    ],
    "低危": [
        ("base64.",   "base64 编解码，确认用途"),
        ("gzip.",     "gzip 压缩，确认用途"),
        ("zlib.",     "zlib 压缩，确认用途"),
        ("codecs.open","codecs.open 指定编码，确认用途"),
    ],
}

# 已知安全工具白名单（扫描时自动跳过或降低扣分）
SAFE_PATTERNS = [
    "skill-vetter", "skill_scanner", "dangerous-patterns",
    "ibkr", "keepalive", "whisper", "tts_generator",
    "video-workflow", "fetch_transcript", "rss_parser",
]

EXT_WEIGHT = {".py": 1.0, ".js": 0.9, ".sh": 0.8,
              ".json": 0.6, ".yaml": 0.6, ".yml": 0.6, ".md": 0.2}
DEDUCTION = {"严重": 25, "高危": 20, "中危": 15, "低危": 5}
MAX_SCORE = 100


def is_whitelisted(path: str, kw: str) -> bool:
    """检查文件是否为已知安全工具（白名单）"""
    name = os.path.basename(path).lower()
    for pat in SAFE_PATTERNS:
        if pat in name:
            return True
    return False


def scan_file(path: str) -> dict:
    _, ext = os.path.splitext(path)
    ext = ext.lower()
    weight = EXT_WEIGHT.get(ext, 0.8)
    rel = os.path.relpath(path, SKILLS_DIR)

    result = {
        "文件": rel, "类型": ext or "unknown",
        "大小_字节": os.path.getsize(path),
        "风险评分": MAX_SCORE, "风险等级": "🟢 低风险",
        "风险点": [], "建议": "✅ 允许安装",
        "详情": [], "修复建议": [],
    }

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        content = "".join(lines)
    except Exception as e:
        result["风险点"].append(f"文件读取失败: {e}")
        result["风险评分"] = 0
        result["风险等级"] = "⛔ 无法扫描"
        result["建议"] = "❌ 禁止安装"
        return result

    # 检测每个级别
    for level, keywords in SUSPICIOUS.items():
        for kw, fix_tip in keywords:
            if kw not in content:
                continue
            # 如果在白名单工具中，扣分减半
            deduction = DEDUCTION[level] * (0.5 if is_whitelisted(path, kw) else 1.0)
            for i, line in enumerate(lines):
                if kw in line:
                    result["详情"].append({
                        "级别": level, "关键词": kw,
                        "行号": i + 1,
                        "上下文": line.strip()[:150],
                        "修复建议": fix_tip,
                        "白名单": is_whitelisted(path, kw),
                    })
                    break

    # 计算扣分（每个关键词只扣一次）
    seen_kw = set()
    for d in result["详情"]:
        if d["关键词"] not in seen_kw:
            seen_kw.add(d["关键词"])
            result["风险评分"] -= DEDUCTION[d["级别"]] * weight
            if d["修复建议"] and d["修复建议"] not in result["修复建议"]:
                result["修复建议"].append(d["修复建议"])

    # 统计各级别命中数
    level_counts = {}
    for d in result["详情"]:
        lvl = d["级别"]
        level_counts[lvl] = level_counts.get(lvl, 0) + 1

    for lvl, cnt in level_counts.items():
        icon = {"严重": "💥", "高危": "🔴", "中危": "🟡", "低危": "🟠"}.get(lvl, "⚪")
        wl = " [已知安全工具]" if any(d["白名单"] for d in result["详情"]) else ""
        result["风险点"].append(f"{icon} [{lvl}] 命中 {cnt} 处{wl}")

    if not result["风险点"]:
        result["风险点"].append("✅ 未发现可疑代码")

    score = max(0, int(result["风险评分"]))
    if score <= 20:
        result.update(风险等级="⛔ 严重风险", 建议="❌ 禁止安装")
    elif score <= 40:
        result.update(风险等级="🔴 高风险", 建议="❌ 禁止安装，查看源码")
    elif score <= 60:
        result.update(风险等级="🟠 较高风险", 建议="⚠️ 沙箱测试，限制权限")
    elif score <= 80:
        result.update(风险等级="🟡 中风险", 建议="⚠️ 谨慎安装，运行时监控")
    else:
        result.update(风险等级="🟢 低风险", 建议="✅ 允许安装")

    result["风险评分"] = score
    return result


def gen_markdown(results: list) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    counts = {"⛔ 严重风险": 0, "🔴 高风险": 0, "🟠 较高风险": 0,
              "🟡 中风险": 0, "🟢 低风险": 0}
    for r in results:
        counts[r["风险等级"]] = counts.get(r["风险等级"], 0) + 1

    if counts["⛔ 严重风险"] > 0 or counts["🔴 高风险"] > 0:
        overall = "🔴 存在高风险技能，建议立即处理"
    elif counts["🟠 较高风险"] > 0:
        overall = "🟠 存在风险技能，请人工审核"
    elif counts["🟡 中风险"] > 0:
        overall = "🟡 整体可控，建议运行时监控"
    else:
        overall = "🟢 全部通过，可正常安装使用"

    # 只显示有风险的分组
    risk_files = [r for r in results if r["风险等级"] not in ("🟢 低风险",)]
    safe_files = [r for r in results if r["风险等级"] == "🟢 低风险"]

    lines = [
        "# 技能安全审计报告\n",
        f"**扫描时间**: {now}",
        f"**扫描目录**: `{SKILLS_DIR}`",
        f"**总体建议**: {overall}\n",
        "## 📊 总览\n",
        f"| 等级 | 数量 |",
        f"|------|------|",
    ]
    for lvl, cnt in counts.items():
        if cnt > 0:
            lines.append(f"| {lvl} | {cnt} |")
    lines += [
        f"",
        f"**合计**: {len(results)} 个文件（🟢 安全 {len(safe_files)} | 需关注 {len(risk_files)}）",
        "",
        "---",
        "",
        "## 🚨 需处理（按风险排序）\n",
    ]

    # 按风险从高到低排序
    risk_files.sort(key=lambda r: r["风险评分"])
    for r in risk_files:
        bar = "█" * max(0, r["风险评分"] // 10) + "░" * max(0, (100 - r["风险评分"]) // 10)
        lines += [
            f"### {r['文件']}",
            f"",
            f"- **类型**: `{r['类型']}` | **大小**: {r['大小_字节']:,} B",
            f"- **评分**: `{r['风险评分']}/100` {r['风险等级']} `[{bar}]`",
            f"- **建议**: {r['建议']}",
            f"",
        ]
        if r["详情"]:
            lines.append("**风险点**:")
            for d in r["详情"][:8]:
                wl = "✅ 白名单" if d["白名单"] else "⚠️"
                lines.append(f"- {wl} 行{d['行号']} `[{d['级别']}]` `{d['关键词']}`")
                if d.get("修复建议"):
                    lines.append(f"  → {d['修复建议']}")
            lines.append("")

    if safe_files:
        lines += ["---\n", "## ✅ 安全文件（示例）\n"]
        for r in safe_files[:10]:
            lines.append(f"- `{r['文件']}` — {r['风险评分']}/100 🟢")
        if len(safe_files) > 10:
            lines.append(f"- ... 还有 {len(safe_files)-10} 个安全文件")

    return "\n".join(lines)


def main():
    results = []
    for root, dirs, files in os.walk(SKILLS_DIR):
        dirs[:] = [d for d in dirs if not d.startswith(".")
                    and d != "__pycache__" and not d.endswith(".git")]
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in EXT_WEIGHT:
                continue
            path = os.path.join(root, file)
            if os.path.abspath(path) == EXCLUDE_SELF:
                continue
            if any(pat in path for pat in EXCLUDE_PATTERNS):
                continue
            results.append(scan_file(path))

    md = gen_markdown(results)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(md)

    json_report = REPORT_FILE.replace(".md", ".json")
    with open(json_report, "w", encoding="utf-8") as f:
        json.dump({
            "scan_time": datetime.now().isoformat(),
            "skills_dir": SKILLS_DIR,
            "total_files": len(results),
            "summary": {
                "safe": len([r for r in results if r["风险等级"] == "🟢 低风险"]),
                "attention": len([r for r in results if r["风险等级"] != "🟢 低风险"]),
            },
            "results": results,
        }, f, ensure_ascii=False, indent=2)

    print(f"✅ 安全审计完成 | {len(results)} 个文件 | 🟢 安全 {len([r for r in results if r['风险等级']=='🟢 低风险'])} | 🚨 需关注 {len([r for r in results if r['风险等级']!='🟢 低风险'])}")
    print(f"📄 报告: {REPORT_FILE}")


if __name__ == "__main__":
    main()
